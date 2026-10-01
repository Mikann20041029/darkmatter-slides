# 解答・解説 — 基礎科学コース「専門科目」

各大問 100 点。

---

## 7 ｜ 力学：中心力（配点 100）

**問 1（20 点）**

$$
L = \frac{m}{2}\left(\dot r^2 + r^2\dot\theta^2\right) + \frac{k}{r}
$$

（$\boldsymbol F = -\nabla U$、$U(r) = -k/r$）

$$
r:\ \frac{d}{dt}\!\left(m\dot r\right) = mr\dot\theta^2 - \frac{k}{r^2}, \qquad
\theta:\ \frac{d}{dt}\!\left(mr^2\dot\theta\right) = 0
$$

$\theta$ は循環座標なので角運動量 $\ell = mr^2\dot\theta$ が保存する。

**問 2（20 点）** $\dot\theta = \ell/(mr^2)$ を $r$ の式に代入して

$$
m\ddot r = \frac{\ell^2}{mr^3} - \frac{k}{r^2} = -\frac{d}{dr}\underbrace{\left[\frac{\ell^2}{2mr^2} - \frac{k}{r}\right]}_{U_{\rm eff}(r)}
$$

$U_{\rm eff}$ は $r\to 0$ で $+\infty$（遠心力障壁）、$r\to\infty$ で $0^-$、途中に 1 つの極小をもつ。円軌道は極小点:

$$
\frac{dU_{\rm eff}}{dr} = -\frac{\ell^2}{mr^3} + \frac{k}{r^2} = 0 \ \Longrightarrow\ \boxed{r_0 = \frac{\ell^2}{mk}}
$$

**問 3（20 点）** $r = r_0 + \delta$ として線形化すると $m\ddot\delta = -U_{\rm eff}''(r_0)\,\delta$。

$$
U_{\rm eff}'' = \frac{3\ell^2}{mr^4} - \frac{2k}{r^3}
\ \xrightarrow{\ r=r_0,\ \ell^2 = mkr_0\ }\
\frac{3k}{r_0^3} - \frac{2k}{r_0^3} = \frac{k}{r_0^3}
$$

$$
\boxed{\ \omega_r = \sqrt{\frac{k}{m r_0^3}}\ }
$$

**問 4（20 点）**

$$
\omega_\theta = \dot\theta = \frac{\ell}{mr_0^2},\qquad
\omega_\theta^2 = \frac{\ell^2}{m^2 r_0^4} = \frac{mkr_0}{m^2r_0^4} = \frac{k}{mr_0^3} = \omega_r^2
$$

$\omega_r = \omega_\theta$。すなわち**質点が中心の周りを 1 周する間に動径方向がちょうど 1 回振動する**ので、軌道は 1 周期で元に戻り閉じる。これは逆 2 乗力（および調和振動子ポテンシャル）に固有の性質で、ベルトランの定理として知られる。

**問 5（20 点）** $\dot r = 0$ のとき $E = U_{\rm eff}(r)$。

$$
E = \frac{\ell^2}{2mr^2} - \frac{k}{r}\ \Longrightarrow\ Er^2 + kr - \frac{\ell^2}{2m} = 0
$$

$$
r_\pm = \frac{k \mp \sqrt{k^2 + \frac{2E\ell^2}{m}}}{2|E|}\qquad (E = -|E| < 0)
$$

解と係数の関係から $r_+ + r_- = -k/E = k/|E|$、よって

$$
a = \frac{r_+ + r_-}{2} = \frac{k}{2|E|}
$$

長半径はエネルギーのみで決まり、$\ell$ に依存しない（$\ell$ は離心率だけを決める）。

> **補充**: 剛体（慣性モーメント・平行軸の定理・斜面を転がる剛体）が過去 5 年間 1 度も出ていないため、大問 7 の第 2 候補である。教科書の該当章を必ず 1 周すること。

---

## 8 ｜ 電磁気学（配点 100）

### 問 1（40 点）

**(1)** 半径 $r$ の球面にガウスの法則（$D$ について）を適用する。誘電体があっても $D$ は自由電荷のみで決まる。

$$
D(r) = \begin{cases} 0 & (r<a) \\ \dfrac{Q}{4\pi r^2} & (r>a)\end{cases}
\qquad
E(r) = \begin{cases} 0 & (r<a) \\[4pt] \dfrac{Q}{4\pi\varepsilon r^2} & (a<r<b) \\[6pt] \dfrac{Q}{4\pi\varepsilon_0 r^2} & (r>b)\end{cases}
$$

**(2)** $V(r) = \int_r^\infty E\,dr'$。

$$
V(r) = \begin{cases}
\dfrac{Q}{4\pi\varepsilon_0 r} & (r \ge b) \\[8pt]
\dfrac{Q}{4\pi\varepsilon_0 b} + \dfrac{Q}{4\pi\varepsilon}\left(\dfrac1r - \dfrac1b\right) & (a \le r \le b) \\[8pt]
\dfrac{Q}{4\pi\varepsilon_0 b} + \dfrac{Q}{4\pi\varepsilon}\left(\dfrac1a - \dfrac1b\right) & (r \le a)
\end{cases}
$$

（導体内は等電位なので $r\le a$ では一定）

**(3)** $\boldsymbol P = \boldsymbol D - \varepsilon_0\boldsymbol E = \left(1 - \dfrac{\varepsilon_0}{\varepsilon}\right)\boldsymbol D$ より

$$
P(r) = \frac{\varepsilon - \varepsilon_0}{\varepsilon}\cdot\frac{Q}{4\pi r^2}\qquad (a<r<b,\ \text{向きは}\ \hat{\boldsymbol r})
$$

分極面電荷は $\sigma_b = \boldsymbol P\cdot\hat{\boldsymbol n}$（$\hat{\boldsymbol n}$ は誘電体から外向き）:

$$
\sigma_b(a) = -\frac{(\varepsilon-\varepsilon_0)Q}{4\pi\varepsilon a^2}, \qquad
\sigma_b(b) = +\frac{(\varepsilon-\varepsilon_0)Q}{4\pi\varepsilon b^2}
$$

総和は $-\dfrac{(\varepsilon-\varepsilon_0)Q}{\varepsilon} + \dfrac{(\varepsilon-\varepsilon_0)Q}{\varepsilon} = 0$。
体積分極電荷は $\rho_b = -\nabla\cdot\boldsymbol P = 0$（$\boldsymbol P \propto \hat{\boldsymbol r}/r^2$ は $r\ne 0$ で発散なし）なので、束縛電荷は 2 つの面にのみ現れ、総和ゼロ。**（電荷保存として当然）**

### 問 2（30 点）

**(1)** 半径 $r$ の円周にアンペールの法則 $\oint \boldsymbol B\cdot d\boldsymbol l = \mu_0 I_{\rm enc}$ を適用。向きは右ねじの向き（周回方向）。

$$
B(r) = \begin{cases} \dfrac{\mu_0 j r}{2} & (r < a) \\[6pt] \dfrac{\mu_0 j a^2}{2r} = \dfrac{\mu_0 I}{2\pi r} & (r > a)\end{cases}
$$

**(2)** 内部のエネルギー密度は $u = B^2/(2\mu_0) = \mu_0 j^2 r^2/8$。単位長さあたり

$$
\frac{W}{\ell} = \int_0^a \frac{\mu_0 j^2 r^2}{8}\,2\pi r\,dr = \frac{\pi\mu_0 j^2}{4}\cdot\frac{a^4}{4} = \frac{\pi\mu_0 j^2 a^4}{16}
$$

$I = j\pi a^2$ を代入すると

$$
\boxed{\ \frac{W}{\ell} = \frac{\mu_0 I^2}{16\pi}\ }
$$

これは $a$ を含まない。$\frac12 L_{\rm int} I^2$ と比較すると、単位長さあたりの**内部インダクタンス** $L_{\rm int} = \mu_0/(8\pi)$ が導体の太さによらない、という有名な結果である。

### 問 3（30 点）

**(1)** キルヒホッフの電圧則。$I = \dot Q$ として

$$
L\ddot Q + R\dot Q + \frac{Q}{C} = 0
$$

**(2)** $\gamma = \dfrac{R}{2L}$、$\omega_0 = \dfrac{1}{\sqrt{LC}}$ とおくと $\ddot Q + 2\gamma\dot Q + \omega_0^2 Q = 0$。

減衰振動（不足減衰）の条件は $\gamma < \omega_0$、すなわち

$$
\boxed{\ R < 2\sqrt{\frac{L}{C}}\ }
$$

$\omega_d = \sqrt{\omega_0^2 - \gamma^2}$ とすると、初期条件 $Q(0)=Q_0,\ \dot Q(0)=0$ の下で

$$
Q(t) = Q_0 e^{-\gamma t}\left(\cos\omega_d t + \frac{\gamma}{\omega_d}\sin\omega_d t\right)
$$

**(3)**

$$
Q_{\text{値}} = \frac{\omega_0 L}{R} = \frac{1}{R}\sqrt{\frac{L}{C}}
$$

$Q$ 値は「1 周期あたりに失われるエネルギーの割合の逆数（$\times 2\pi$）」であり、大きいほど減衰が遅く、共振曲線が鋭い（帯域幅 $\Delta\omega/\omega_0 = 1/Q$）。

---

## 9 ｜ 量子力学：トンネル効果（配点 100）

**問 1（15 点）**

$$
-\frac{\hbar^2}{2m}\psi'' = E\psi\ (x<0,\ x>a), \qquad -\frac{\hbar^2}{2m}\psi'' + V_0\psi = E\psi\ (0<x<a)
$$

$$
\psi(x) = \begin{cases}
e^{ikx} + r\,e^{-ikx} & (x<0) \\
C e^{\kappa x} + D e^{-\kappa x} & (0<x<a) \\
t\,e^{ikx} & (x>a)
\end{cases}
$$

障壁内は $E<V_0$ なので指数関数的な解（振動しない）になる。

**問 2（15 点）** $\psi$ と $\psi'$ が $x=0, a$ で連続。理由: ポテンシャルが有限のジャンプしか持たないとき、シュレディンガー方程式から $\psi''$ が有限 → $\psi'$ は連続、$\psi$ は連続。（$\psi'$ の不連続が許されるのは $\delta$ 関数ポテンシャルの場合のみ）

**問 3（30 点）** 4 つの接続条件から $t$ を解くと

$$
t = \frac{4ik\kappa\, e^{-ika}}{(\kappa + ik)^2 e^{-\kappa a} - (\kappa - ik)^2 e^{\kappa a}}
$$

分母の絶対値の 2 乗を整理すると

$$
|t|^{-2} = 1 + \frac{(k^2+\kappa^2)^2}{4k^2\kappa^2}\sinh^2(\kappa a)
$$

ここで

$$
k^2 + \kappa^2 = \frac{2mV_0}{\hbar^2}, \qquad k^2\kappa^2 = \frac{4m^2 E(V_0-E)}{\hbar^4}
\ \Longrightarrow\ \frac{(k^2+\kappa^2)^2}{4k^2\kappa^2} = \frac{V_0^2}{4E(V_0-E)}
$$

入射波と透過波で $k$ が同じなので $T = |t|^2$。よって与式が示された。

**問 4（20 点）** $\kappa a \gg 1$ で $\sinh(\kappa a)\simeq \frac12 e^{\kappa a}$、$\sinh^2 \simeq \frac14 e^{2\kappa a}$。分母の 1 は無視できて

$$
T \simeq \left[\frac{V_0^2 e^{2\kappa a}}{16E(V_0-E)}\right]^{-1} = \frac{16E(V_0-E)}{V_0^2}\,e^{-2\kappa a}
$$

**問 5（10 点）** $E>V_0$ では $\kappa \to i k'$、$k' = \sqrt{2m(E-V_0)}/\hbar$ となり $\sinh(\kappa a)\to i\sin(k'a)$。したがって $\sin(k'a) = 0$、すなわち

$$
k' a = n\pi \quad (n = 1,2,\dots) \qquad \Longleftrightarrow \quad a = n\frac{\lambda'}{2}
$$

のとき $T=1$。**共鳴透過**（ラムザウアー–タウンゼント効果）と呼ばれる。障壁の両端での反射波が干渉で打ち消し合うため。

**問 6（10 点）** 例: $\alpha$ 崩壊。$\alpha$ 粒子はクーロン障壁を透過して核から出る。$T\propto e^{-2\kappa a}$ で $\kappa = \sqrt{2m(V_0-E)}/\hbar$ なので、崩壊エネルギー $E$ がわずかに増えると $\kappa$ が減り、**指数関数の肩**が変わる。その結果、$E$ が数 MeV 変わるだけで半減期が $10^{20}$ 桁以上変化する（Geiger–Nuttall 則）。透過率が指数関数的であることが、この極端な感度の起源である。

---

## 10 ｜ 統計力学：黒体輻射（配点 100）

**問 1（15 点）** 等比級数の和より

$$
Z_1 = \sum_{n=0}^{\infty} e^{-\beta\hbar\omega(n+1/2)} = \frac{e^{-\beta\hbar\omega/2}}{1 - e^{-\beta\hbar\omega}} = \frac{1}{2\sinh(\beta\hbar\omega/2)}
$$

$$
\langle n\rangle = \frac{\sum n e^{-\beta\hbar\omega n}}{\sum e^{-\beta\hbar\omega n}} = \frac{1}{e^{\beta\hbar\omega}-1}
$$

**問 2（15 点）** 零点を除いた平均エネルギーは

$$
\langle\varepsilon\rangle = \hbar\omega\,\langle n\rangle = \frac{\hbar\omega}{e^{\beta\hbar\omega}-1}
$$

$\langle n\rangle$ はボース–アインシュタイン分布 $\left[e^{\beta(\varepsilon-\mu)}-1\right]^{-1}$ で $\varepsilon = \hbar\omega$, $\mu = 0$ としたものに一致する。すなわち「モードの励起量子数」＝「そのモードにいる光子の数」と読み替えられる。

$\mu = 0$ の理由: 光子数 $N$ は保存量ではなく、壁による吸収・放出で自由に変化する。平衡では自由エネルギーが $N$ に関して最小になるので $\mu = \left(\partial F/\partial N\right)_{T,V} = 0$。

**問 3（15 点）** 一辺 $L$ の立方体に周期境界条件を課すと $\boldsymbol k = \frac{2\pi}{L}(n_x,n_y,n_z)$。$k$ 空間の単位体積あたりのモード数は $(L/2\pi)^3 = V/(2\pi)^3$。半径 $k$ の球殻の体積 $4\pi k^2 dk$ をかけ、さらに横波 2 つの偏光自由度で 2 倍:

$$
D(k)dk = 2\cdot\frac{V}{(2\pi)^3}4\pi k^2 dk = \frac{Vk^2}{\pi^2}dk
$$

$\omega = ck$ を代入して $D(\omega)d\omega = \dfrac{V\omega^2}{\pi^2c^3}d\omega$。

**問 4（25 点）**

$$
U = \int_0^\infty D(\omega)\langle\varepsilon(\omega)\rangle d\omega = \frac{V\hbar}{\pi^2c^3}\int_0^\infty \frac{\omega^3}{e^{\beta\hbar\omega}-1}d\omega
$$

$x = \beta\hbar\omega$ と置換すると $\omega^3 d\omega = (k_BT/\hbar)^4 x^3 dx$。

$$
U = \frac{V\hbar}{\pi^2c^3}\left(\frac{k_BT}{\hbar}\right)^4\cdot\frac{\pi^4}{15}
= \boxed{\ \frac{\pi^2 V (k_BT)^4}{15\,\hbar^3c^3}\ }\ \propto VT^4
$$

（これがシュテファン–ボルツマンの法則。放射強度 $I = \frac{c}{4}\frac{U}{V} = \sigma T^4$）

**問 5（15 点）**

$$
u(\omega) = \frac{U}{V}\text{の}\omega\text{分布} = \frac{\hbar\omega^3}{\pi^2c^3\left(e^{\beta\hbar\omega}-1\right)}
$$

- $\hbar\omega\ll k_BT$: $e^{\beta\hbar\omega}-1 \simeq \beta\hbar\omega$ より $u \simeq \dfrac{\omega^2 k_BT}{\pi^2c^3}$ → **レイリー–ジーンズの法則**。これは 1 モードあたり $k_BT$（古典的等分配則）に相当し、$\omega$ について積分すると発散する（**紫外破綻**）。エネルギーが量子化されている（$\hbar\omega$ の飛び）ことがこの発散を止める。
- $\hbar\omega\gg k_BT$: $u \simeq \dfrac{\hbar\omega^3}{\pi^2c^3}e^{-\hbar\omega/k_BT}$ → **ウィーンの放射法則**。

**問 6（15 点）** $x=\beta\hbar\omega$ とすると $u \propto \dfrac{x^3}{e^x-1}$。$x$ で微分してゼロと置くと

$$
3x^2(e^x-1) - x^3e^x = 0 \ \Longrightarrow\ 3\left(1 - e^{-x}\right) = x
$$

これは $T$ を含まないので、解 $x^* \simeq 2.82$ は定数。したがって

$$
\omega_{\max} = \frac{x^* k_BT}{\hbar} \propto T
$$

（**ウィーンの変位則**。波長で表すと $\lambda_{\max}T = $ 一定だが、$x^*$ の値は $4.965$ になり異なることに注意）

---

## 11 ｜ 物性：結晶構造と X 線回折（配点 100）

### 1-a（20 点）

単位格子あたりの原子数: 頂点 $8\times\frac18 = 1$、面心 $6\times\frac12 = 3$、計 **4 個**。

最近接原子は面の対角線上にあるので、最近接距離は $\dfrac{\sqrt2}{2}a = 2r$、すなわち $r = \dfrac{\sqrt2}{4}a$。

$$
\text{充填率} = \frac{4\cdot\frac43\pi r^3}{a^3} = \frac{16\pi}{3}\cdot\frac{1}{16\sqrt2} = \frac{\pi}{3\sqrt2} = \boxed{0.740}
$$

### 1-b（20 点）

$(hkl)$ 面のうち原点に最も近いものは $\dfrac{hx}{a} + \dfrac{ky}{a} + \dfrac{lz}{a} = 1$、すなわち $hx + ky + lz = a$。原点からこの平面までの距離は

$$
d = \frac{|a|}{\sqrt{h^2+k^2+l^2}} = \frac{a}{\sqrt{h^2+k^2+l^2}}
$$

隣り合う面は右辺が $a, 2a, \dots$ と等間隔に並ぶので、これが面間隔である。
（逆格子で言えば $d = 2\pi/|\boldsymbol G_{hkl}|$、$\boldsymbol G_{hkl} = \frac{2\pi}{a}(h,k,l)$）

### 1-c（30 点）

ブラッグの条件: $\ 2d_{hkl}\sin\theta = n\lambda$

$2\theta$ が最小 ⟺ $\sin\theta$ が最小 ⟺ $d$ が最大 ⟺ $\sqrt{h^2+k^2+l^2}$ が最小。
消滅則（$h,k,l$ が全部偶数または全部奇数）を満たす最小は $(111)$ で $\sqrt3$。次は $(200)$ で $2$。

$$
d_{111} = \frac{0.405}{\sqrt3} = 0.2338\ \mathrm{nm}
$$

$$
\sin\theta = \frac{\lambda}{2d_{111}} = \frac{0.154}{2\times 0.2338} = 0.3293 \ \Longrightarrow\ \theta = 19.2^\circ
$$

$$
\boxed{(hkl) = (111),\qquad 2\theta = 38.5^\circ}
$$

（参考: $a = 0.405$ nm の fcc 金属はアルミニウム。Cu K$\alpha$ 線での Al の最強線が $2\theta = 38.5^\circ$ に出るのは実測どおり）

検算として $(200)$: $d = 0.2025$ nm、$\sin\theta = 0.380$、$2\theta = 44.7^\circ$ でたしかに大きい。

### 2-a（30 点、選択）

伝導帯の状態密度は帯の底 $E_c$ から測って $D_c(E) \propto (E-E_c)^{1/2}$。真性半導体では $E_c - \mu \gg k_BT$ なのでフェルミ分布はボルツマン分布で近似できる: $f(E)\simeq e^{-(E-\mu)/k_BT}$。

$$
n = \int_{E_c}^{\infty} D_c(E)f(E)dE \propto e^{-(E_c-\mu)/k_BT}\int_0^\infty \epsilon^{1/2}e^{-\epsilon/k_BT}d\epsilon \propto (k_BT)^{3/2}e^{-(E_c-\mu)/k_BT}
$$

積分が $T^{3/2}$ を与える。真性半導体では電子と正孔の数が等しいことから化学ポテンシャルはギャップのほぼ中央 $\mu \simeq (E_c+E_v)/2$ にあり、$E_c - \mu \simeq E_g/2$。よって

$$
n \propto T^{3/2}\exp\!\left(-\frac{E_g}{2k_BT}\right)
$$

### 2-b（30 点、選択）

マイスナー効果: 超伝導体は $T<T_c$ で内部の磁束密度を $B=0$ に保つ（完全反磁性）。表面に遮蔽電流が流れ、ロンドン侵入長 $\lambda_L$ 程度の薄い層を除いて磁場を排除する。

完全導体との違い: 完全導体（$\rho=0$）に対しては $\boldsymbol E = 0$ とマクスウェル方程式から $\partial\boldsymbol B/\partial t = 0$ しか言えない。したがって「磁場をかけたまま冷却」した場合、完全導体は磁束を**閉じ込めたまま**になる。一方、超伝導体は磁場中で冷却しても $T_c$ を下回った瞬間に磁束を**能動的に追い出す**（$B=0$）。すなわちマイスナー効果は履歴に依存しない熱力学的な状態であり、完全導電性からは導けない独立した性質である。

---

## 12 ｜ 原子核・素粒子・相対論（配点 100）

### I. 光子と物質の相互作用

**問 1（15 点）** 光子が完全に吸収されたと仮定する。運動量保存より終状態の電子の運動量は $p' = E_\gamma/c$。エネルギー保存より

$$
E_\gamma + m_ec^2 = \sqrt{(p'c)^2 + m_e^2c^4} = \sqrt{E_\gamma^2 + m_e^2c^4}
$$

両辺を 2 乗すると

$$
E_\gamma^2 + 2E_\gamma m_ec^2 + m_e^2c^4 = E_\gamma^2 + m_e^2c^4 \ \Longrightarrow\ 2E_\gamma m_ec^2 = 0
$$

$E_\gamma > 0$ に矛盾。よって自由電子は光子を完全吸収できない。

実際の光電効果では電子が原子に束縛されており、**原子核（原子全体）が反跳運動量を分担する**ため、エネルギーと運動量を同時に保存できる。これが光電効果の断面積が原子番号 $Z$ に強く依存する（$\propto Z^4$〜$Z^5$）理由でもある。

**問 2（15 点）** 4 元運動量の 2 乗（不変質量の 2 乗）$s = (\sum p^\mu)^2$ はローレンツ不変で、反応の前後で保存する。

- 始状態（光子 1 個）: $s_i = 0$（光子は質量ゼロ）
- 終状態（$e^+e^-$）: 重心系で考えると $s_f = (E_1+E_2)^2/c^2 \ge (2m_ec)^2 > 0$

$s_i \ne s_f$ なので不可能。（別の言い方: 光子の静止系は存在しないが、$e^+e^-$ 対には必ず重心静止系が存在する）

**問 3（20 点）** 反応 $\gamma + N \to N + e^+ + e^-$。実験室系（$N$ が静止）で

$$
s = \left(E_\gamma + Mc^2\right)^2 - \left(E_\gamma\right)^2 = 2E_\gamma Mc^2 + M^2c^4
$$

しきい値は終状態の 3 粒子が重心系ですべて静止する場合で $\sqrt{s} = (M + 2m_e)c^2$。

$$
2E_\gamma Mc^2 + M^2c^4 = M^2c^4 + 4Mm_ec^4 + 4m_e^2c^4
$$

$$
\boxed{\ E_\gamma^{\rm th} = 2m_ec^2\left(1 + \frac{m_e}{M}\right)\ }
$$

$M \gg m_e$ の極限で

$$
E_\gamma^{\rm th} \to 2m_ec^2 = 2\times 0.511 = \boxed{1.022\ \mathrm{MeV}}
$$

（電子を相手にする対生成 $\gamma + e^- \to e^-e^+e^-$ では $M = m_e$ となり $E_\gamma^{\rm th} = 4m_ec^2 = 2.044$ MeV）

### II. 相対論的ビーミング

**問 4（20 点）** 光子の 4 元運動量を $K'$ 系で $p'^\mu = \dfrac{E'}{c}(1, \cos\theta', \sin\theta', 0)$ とする。$K$ 系へのローレンツ変換（$x$ 方向に速度 $+v$ のブースト）は

$$
\frac{E}{c} = \gamma\left(\frac{E'}{c} + \beta p'_x\right) = \gamma\frac{E'}{c}\left(1 + \beta\cos\theta'\right)
$$
$$
p_x = \gamma\left(p'_x + \beta\frac{E'}{c}\right) = \gamma\frac{E'}{c}\left(\cos\theta' + \beta\right), \qquad p_y = p'_y = \frac{E'}{c}\sin\theta'
$$

$$
\therefore\ \cos\theta = \frac{p_x c}{E} = \frac{\cos\theta' + \beta}{1 + \beta\cos\theta'}
$$

**問 5（15 点）** 上式の逆変換 $\cos\theta' = \dfrac{\cos\theta - \beta}{1 - \beta\cos\theta}$ を $E = \gamma E'(1+\beta\cos\theta')$ に代入する。

$$
1 + \beta\cos\theta' = \frac{(1-\beta\cos\theta) + \beta\cos\theta - \beta^2}{1-\beta\cos\theta} = \frac{1-\beta^2}{1-\beta\cos\theta} = \frac{1}{\gamma^2(1-\beta\cos\theta)}
$$

$$
\therefore\ E = \frac{\gamma E'}{\gamma^2(1-\beta\cos\theta)} = \frac{E'}{\gamma(1-\beta\cos\theta)} = \delta E'
$$

**問 6（10 点）** $\theta' = 90^\circ$（$\cos\theta'=0$）を問 4 に代入すると $\cos\theta = \beta$。すなわち $K'$ 系の前方半球に出た光子は、$K$ 系では

$$
0 \le \theta < \arccos\beta
$$

の円錐内に集まる。$\gamma\gg1$ では $\beta = \sqrt{1-\gamma^{-2}}\simeq 1 - \dfrac{1}{2\gamma^2}$ で $\theta$ は小さく、

$$
\sin\theta = \sqrt{1-\beta^2} = \frac{1}{\gamma} \ \Longrightarrow\ \theta \simeq \frac{1}{\gamma}
$$

**問 7（5 点）** 静止系で全立体角 $4\pi$ に等方放射された光のうち半分が、観測者系では立体角 $\sim\pi\theta^2 = \pi/\gamma^2$ の狭い円錐に押し込まれる。加えて各光子のエネルギーが $\delta$ 倍、到来率も $\delta$ 倍になるため、観測される単位立体角あたりの光度は $\delta^4$ に比例して増大する。

したがって、観測されたフラックスから「等方放射」を仮定して総エネルギーを見積もると、真の放射エネルギーを大幅に過大評価する。GRB で見かけの等方エネルギーが $10^{54}$ erg に達するのに、ジェットの開き角（$\theta_j$）補正を行うと $10^{51}$ erg 程度に収まるのはこのためである。
