"""[2026-07-28] 他天体 (矮小銀河 5 天体 + M31) の ROI 幾何を 1 箇所に定義する。

`compute_exposure_map_targets.py` (露出マップ) と `apply_v20_method_targets.py`
(フィット本体) の両方が同じグリッド・同じ立体角を使う必要があるため、
定義をここに集約する (2 箇所に書くと片方だけ直す事故が起きる)。

天球上の ROI は **接平面 (gnomonic) 投影**で切る。天の川の解析のように (l, b) の
矩形で切ると、Coma Berenices (b=+83.6°) や Sculptor (b=-83.2°) のような高銀緯天体で
矩形が極端に歪む (b=84° では Δl=10° が天球上の 1.0° にしかならない)。
接平面なら中心からの角距離が素直に扱える。

立体角: 接平面座標 (xi, eta) [rad] の面素 dxi*deta は、天球上では
    dOmega = dxi * deta / (1 + xi^2 + eta^2)^(3/2)
に対応する (gnomonic 投影のヤコビアン)。半径 10° で 1/(1+r^2)^1.5 は 0.954 なので、
無視すると端で 4.6% ずれる。必ずこの係数を掛ける。
"""
from __future__ import annotations

import pathlib as _pathlib
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

@dataclass(frozen=True)
class Target:
    """解析対象 1 天体。ハローの角度スケール theta_s と距離だけで幾何が決まる。"""
    key: str
    display: str
    ra: float            # [deg, ICRS]
    dec: float           # [deg, ICRS]
    d_kpc: float         # 距離 [kpc]
    theta_s_deg: float   # NFW scale radius の角度 [deg]
    category: str        # "dwarf" | "galaxy" | "control"
    source: str          # 値の出典

    @property
    def rs_kpc(self) -> float:
        return self.d_kpc * float(np.tan(np.radians(self.theta_s_deg)))

    @property
    def trunc_kpc(self) -> float:
        """切断半径 = 10 rs。NFW の典型的な濃度 c = 10 (r_vir = c rs) に対応する。

        全天体に同一の規則を適用する。矮小銀河では 10 rs の中央値が 1.1 kpc となり、
        dSph の潮汐半径 (1-3 kpc) と整合する。rho^2 は外側で r^-6 と急減するので
        J マップの形はこの選択にほとんど依存しない (`--trunc-scan` で確認できる)。
        """
        return 10.0 * self.rs_kpc


LVDB_CSV = _pathlib.Path(__file__).resolve().parent.parent / "ref/lvdb_dwarf_mw.csv"

# LVDB に無い天体は個別に定義する。rs は「公表された R_vir と濃度 c から rs = R_vir / c」で出す。
_EXTRA_GALAXIES: list[Target] = [
    Target("m31", "M31", 10.6847, 41.2690, 785.0,
           float(np.degrees(np.arctan(15.4 / 785.0))), "galaxy",
           "R_200 ≈ 200 kpc (Tamm+2012, A&A 546 A4) と c = 13 → rs = 15.4 kpc"),
    Target("m33", "M33", 23.4621, 30.6600, 840.0,
           float(np.degrees(np.arctan(17.1 / 840.0))), "galaxy",
           "M_200 = 3e11 Msun (Corbelli+2014) → R_200 = 137 kpc、c = 8 → rs = 17.1 kpc"),
]


def load_dwarfs() -> list[Target]:
    """LVDB (Pace 2025) の天の川矮小銀河から、確認済みの銀河を読む。

    採用条件: `confirmed_real == 1` かつ `confirmed_galaxy == 1` かつ
    位置・距離・半光度半径が揃っていること (2026-07-31 時点で 54 天体)。

    **ハローの角度スケールは theta_s = theta_half (半光度半径の角度) と置く。**
    これは仮定である。矮小銀河の NFW scale radius は運動学から一意に決まらないため、
    観測量として確実な半光度半径を代用する。この選択の影響は小さい:
    54 天体中 43 天体は theta_half < PSF (0.198° @ 20 GeV) で、テンプレートの形は
    PSF が支配する。影響が出るのは残り 11 天体 (Sagittarius 5.70° / LMC 3.22° /
    Antlia 2 1.74° / SMC 0.99° 等) だけで、これらは `--theta-scale` で感度を測れる。
    """
    import pandas as pd

    d = pd.read_csv(LVDB_CSV)
    g = d[(d["confirmed_real"] == 1) & (d["confirmed_galaxy"] == 1)]
    g = g.dropna(subset=["ra", "dec", "distance", "rhalf"])
    out: list[Target] = []
    for _, r in g.iterrows():
        name = str(r["name"]) if isinstance(r.get("name"), str) else str(r["key"])
        out.append(Target(str(r["key"]), name, float(r["ra"]), float(r["dec"]),
                          float(r["distance"]), float(r["rhalf"]) / 60.0, "dwarf",
                          "LVDB (Pace 2025, OJAp 8 142; arXiv:2411.07424)"))
    return out


def make_control_fields(n: int, seed: int = 20260731, min_sep_deg: float = 20.0,
                        min_abs_b: float = 20.0, roi_half_deg: float = 10.0,
                        avoid: list[Target] | None = None) -> list[Target]:
    """統計検証用の**対照フィールド** (既知の標的が無い空の領域) を作る。

    同じ手法を「何も無い場所」に当てたときに有意度がどう散らばるかを実データで測るための
    もの。合成データの較正 (`audit_target_fit_calibration.py`) が理論どおりでも、
    実データには拡散モデルの誤差や点源の消し残りがあるので、**実データでの帰無分布**は
    別に測る必要がある。

    条件:
      - |b| >= min_abs_b (銀河面を避ける。拡散モデルが最も苦しい領域を除く)
      - 互いに min_sep_deg 以上離す (ROI が重ならないようにして独立性を保つ)
      - 既知の標的からも min_sep_deg 以上離す
    ハローテンプレートは典型的な矮小銀河相当 (theta_s = 0.1°, D = 100 kpc) を使う。
    """
    rng = np.random.default_rng(seed)
    placed: list[tuple[float, float]] = []
    if avoid:
        for t in avoid:
            placed.append(radec_to_galactic(t.ra, t.dec))
    out: list[Target] = []
    tries = 0
    while len(out) < n and tries < 200000:
        tries += 1
        l = float(rng.uniform(-180.0, 180.0))
        b = float(np.degrees(np.arcsin(rng.uniform(-1.0, 1.0))))   # 立体角一様
        if abs(b) < min_abs_b:
            continue
        if placed:
            pl = np.array([p[0] for p in placed])
            pb = np.array([p[1] for p in placed])
            if float(angsep_deg(l, b, pl, pb).min()) < min_sep_deg:
                continue
        placed.append((l, b))
        ra, dec = galactic_to_radec(l, b)
        out.append(Target(f"control_{len(out):03d}", f"対照 {len(out):03d}", ra, dec,
                          100.0, 0.1, "control", "無作為に選んだ空の領域 (統計検証用)"))
    return out


def load_targets(dwarfs: bool = True, galaxies: bool = True, n_control: int = 0,
                 control_seed: int = 20260731) -> list[Target]:
    """解析対象の一覧を組み立てる。"""
    out: list[Target] = []
    if dwarfs:
        out += load_dwarfs()
    if galaxies:
        out += _EXTRA_GALAXIES
    if n_control > 0:
        out += make_control_fields(n_control, seed=control_seed, avoid=list(out))
    return out

ROI_HALF_DEG_FIT = 10.0   # フィットに使う ROI 半幅 [deg]
ROI_HALF_DEG_EXP = 12.0   # 露出マップを作る範囲 [deg]。補間の端の余裕を持たせる
EXP_STEP_DEG = 1.0        # 露出マップの刻み [deg] (天の川と同じ。0.125° へは双線形補間)


def radec_to_galactic(ra_deg: float, dec_deg: float) -> tuple[float, float]:
    """赤道座標 (ICRS) → 銀河座標。l は (-180, 180] に折り返す。"""
    from astropy.coordinates import SkyCoord
    import astropy.units as u

    c = SkyCoord(ra=ra_deg * u.deg, dec=dec_deg * u.deg, frame="icrs").galactic
    l = float(c.l.deg)
    return (l if l <= 180.0 else l - 360.0), float(c.b.deg)


def galactic_to_radec(l_deg: float, b_deg: float) -> tuple[float, float]:
    """銀河座標 → 赤道座標 (ICRS)。対照フィールドを (l, b) で作って登録するのに使う。"""
    from astropy.coordinates import SkyCoord
    import astropy.units as u

    c = SkyCoord(l=l_deg * u.deg, b=b_deg * u.deg, frame="galactic").icrs
    return float(c.ra.deg), float(c.dec.deg)


def target_lb(name: str) -> tuple[float, float]:
    """天体名 → 銀河座標 (l, b) [deg]。"""
    for t in load_targets():
        if t.key == name:
            return radec_to_galactic(t.ra, t.dec)
    raise KeyError(f"未知の天体: {name}")


def gnomonic_inverse(l0_deg: float, b0_deg: float,
                     xi: NDArray[np.float64], eta: NDArray[np.float64]
                     ) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """接平面座標 (xi[東], eta[北]) [rad] → 銀河座標 (l, b) [deg]。

    中心 (l0, b0) の gnomonic 投影の逆変換。標準式 (Calabretta & Greisen 2002 §5.1.3)。
    """
    l0, b0 = np.radians(l0_deg), np.radians(b0_deg)
    rho = np.sqrt(xi ** 2 + eta ** 2)
    c = np.arctan(rho)
    sin_c, cos_c = np.sin(c), np.cos(c)
    # rho = 0 (中心画素) では 0/0 になるので、そこだけ中心の値を入れる
    safe_rho = np.where(rho == 0.0, 1.0, rho)
    sin_b = cos_c * np.sin(b0) + eta * sin_c * np.cos(b0) / safe_rho
    b = np.arcsin(np.clip(np.where(rho == 0.0, np.sin(b0), sin_b), -1.0, 1.0))
    l = l0 + np.arctan2(xi * sin_c,
                        safe_rho * np.cos(b0) * cos_c - eta * np.sin(b0) * sin_c)
    l = np.where(rho == 0.0, l0, l)
    l_deg = np.degrees(l)
    l_deg = (l_deg + 180.0) % 360.0 - 180.0   # (-180, 180] に折り返す
    return l_deg, np.degrees(b)


def gnomonic_forward(l0_deg: float, b0_deg: float,
                     l_deg: NDArray[np.float64], b_deg: NDArray[np.float64]
                     ) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.bool_]]:
    """銀河座標 (l, b) [deg] → 接平面座標 (xi[東], eta[北]) [deg]。

    戻り値の 3 番目は「接平面に投影できるか」の真偽値 (cos c > 0、すなわち中心から
    90° 未満の半球にあるか)。裏側の天体は投影すると偽の像を結ぶので必ず除外する。
    """
    l0, b0 = np.radians(l0_deg), np.radians(b0_deg)
    l, b = np.radians(l_deg), np.radians(b_deg)
    dl = l - l0
    cos_c = np.sin(b0) * np.sin(b) + np.cos(b0) * np.cos(b) * np.cos(dl)
    ok = cos_c > 1e-6
    safe = np.where(ok, cos_c, 1.0)
    xi = np.cos(b) * np.sin(dl) / safe
    eta = (np.cos(b0) * np.sin(b) - np.sin(b0) * np.cos(b) * np.cos(dl)) / safe
    return np.degrees(xi), np.degrees(eta), ok


def make_grid(l0_deg: float, b0_deg: float, half_deg: float, step_deg: float
              ) -> tuple[NDArray[np.float64], NDArray[np.float64],
                         NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """接平面グリッドを作る。

    戻り値 (すべて shape (n, n), n = 2*half/step):
      xi_c, eta_c : 画素中心の接平面座標 [deg]
      l_grid, b_grid : 画素中心の銀河座標 [deg]
      domega : 画素の立体角 [sr] (gnomonic ヤコビアン込み)
    """
    edges = np.arange(-half_deg, half_deg + step_deg, step_deg)
    centers = (edges[:-1] + edges[1:]) / 2.0
    xi_c, eta_c = np.meshgrid(centers, centers, indexing="ij")
    xi_r, eta_r = np.radians(xi_c), np.radians(eta_c)
    l_grid, b_grid = gnomonic_inverse(l0_deg, b0_deg, xi_r, eta_r)
    dstep = np.radians(step_deg)
    domega = dstep ** 2 / (1.0 + xi_r ** 2 + eta_r ** 2) ** 1.5
    return xi_c, eta_c, l_grid, b_grid, domega


def angsep_deg(l0: float, b0: float,
               l: NDArray[np.float64], b: NDArray[np.float64]) -> NDArray[np.float64]:
    """(l0, b0) と配列 (l, b) の角距離 [deg] (haversine、l の折り返しに対応)。"""
    l0r, b0r = np.radians(l0), np.radians(b0)
    lr, br = np.radians(l), np.radians(b)
    dl = lr - l0r
    x = np.sin((br - b0r) / 2.0) ** 2 + np.cos(b0r) * np.cos(br) * np.sin(dl / 2.0) ** 2
    return np.degrees(2.0 * np.arcsin(np.sqrt(np.clip(x, 0.0, 1.0))))
