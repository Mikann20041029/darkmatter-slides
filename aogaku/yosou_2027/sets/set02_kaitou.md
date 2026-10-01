# 解答・解説 — 予想問題 第 2 回

各大問 100 点。

## 1

**(1)（15 点）** 行基本変形により

$$
A \to \begin{pmatrix} 1 & 2 & 0 & 1 \\ 0 & -1 & 1 & -2 \\ 0 & -1 & 1 & -2 \end{pmatrix} \to \begin{pmatrix} 1 & 2 & 0 & 1 \\ 0 & -1 & 1 & -2 \\ 0 & 0 & 0 & 0 \end{pmatrix}
$$

よって $\operatorname{rank} A = 2$。

**(2)（20 点）** 主成分は第 1・第 2 列。$\operatorname{Im} f$ はこの 2 列が張る空間で

$$
\text{基底}\ \left\{ (1,2,1)^\top,\ (2,3,1)^\top \right\}, \qquad \dim\operatorname{Im} f = 2
$$

**(3)（30 点）** 階段形から $x_1 + 2x_2 + x_4 = 0$、$-x_2 + x_3 - 2x_4 = 0$。$x_3 = s$、$x_4 = t$ を自由変数として

$$
x_2 = s - 2t, \qquad x_1 = -2x_2 - x_4 = -2s + 3t
$$

$$
\text{基底}\ \left\{ (-2,1,1,0)^\top,\ (3,-2,0,1)^\top \right\}, \qquad \dim\operatorname{Ker} f = 2
$$

**(4)（10 点）** $2 + 2 = 4 = \dim\mathbb{R}^4$。成立。

**(5)（25 点）** 拡大係数行列を同じ変形にかけると最終行が $0 = 0$ となり、解は存在する。$x_3 = x_4 = 0$ とすると $x_2 = 0$、$x_1 = 1$。よって

$$
\boldsymbol x = (1,0,0,0)^\top + s(-2,1,1,0)^\top + t(3,-2,0,1)^\top \quad (s,t\in\mathbb{R})
$$

（検算: $A(1,0,0,0)^\top = (1,2,1)^\top = \boldsymbol b$）

---

## 3

**(1)（30 点）**

$$
f_x = 3x^2 - 3ay = 0,\qquad f_y = 3y^2 - 3ax = 0
$$

より $y = x^2/a$、$x = y^2/a$。前者を後者に代入して $x = x^4/a^3$、すなわち $x(x^3 - a^3) = 0$。

$$
\therefore\ (x,y) = (0,0),\ (a,a)
$$

**(2)（50 点）** $f_{xx} = 6x$、$f_{yy} = 6y$、$f_{xy} = -3a$。

- $(0,0)$: $H = 0 - 9a^2 = -9a^2 < 0$ → **鞍点**
- $(a,a)$: $H = 36a^2 - 9a^2 = 27a^2 > 0$、$f_{xx} = 6a > 0$ → **極小**

$$
f(a,a) = a^3 + a^3 - 3a\cdot a\cdot a = -a^3
$$

**(3)（20 点）** $a<0$ でも停留点は $(0,0)$ と $(a,a)$ のままで、$(0,0)$ は鞍点。$(a,a)$ では $f_{xx} = 6a < 0$、$H = 27a^2 > 0$ なので **極大**となり、極大値は $f(a,a) = -a^3 = |a|^3 > 0$。

なお $a = 0$ のときは $f = x^3+y^3$ で停留点は $(0,0)$ のみ、$H = 0$ で判定不能。実際 $y=0$ 上で $f = x^3$ は原点で符号を変えるので極値ではない。

---

## 4

**(1)（30 点）** $x = \tan\phi$ と置換すると $dx = \sec^2\phi\,d\phi$、$1+x^2 = \sec^2\phi$。

$$
\int_0^{\pi/2}\frac{\sec^2\phi}{\sec^4\phi}d\phi = \int_0^{\pi/2}\cos^2\phi\,d\phi = \boxed{\frac{\pi}{4}}
$$

**(2)（30 点）** 極座標。$D$ は $1\le r\le 2$、$0\le\theta\le\pi$（上半分の円環）。被積分関数は $1/r$、面積要素は $r\,dr\,d\theta$ なので

$$
\int_0^{\pi}\!\!d\theta\int_1^2 \frac{1}{r}\,r\,dr = \pi\,[r]_1^2 = \boxed{\pi}
$$

**(3)（40 点）** $e^{-x^2}$ は初等的な原始関数を持たないので **積分順序を交換する**。

領域は $\{0\le y\le 1,\ y\le x\le 1\}$、すなわち $\{0\le x\le 1,\ 0\le y\le x\}$。

$$
\int_0^1\!\!dx\int_0^x e^{-x^2}dy = \int_0^1 x e^{-x^2}dx = \left[-\frac{e^{-x^2}}{2}\right]_0^1 = \boxed{\frac{1-e^{-1}}{2}} \simeq 0.3161
$$

---

## 7 ｜ 力学：剛体（配点 100）

**問 1（20 点）**

**円柱**: 半径 $r$、厚さ $dr$、長さ $L$ の円筒殻の質量は $dm = \rho\,2\pi r L\,dr$。

$$
I = \int_0^a r^2\,\rho\,2\pi rL\,dr = 2\pi\rho L\frac{a^4}{4} = \frac{(\rho\pi a^2 L)a^2}{2} = \frac{Ma^2}{2}
$$

**球**: 対称性から $\displaystyle\int (x^2+y^2)dV = \frac23\int (x^2+y^2+z^2)dV = \frac23\int r^2 dV$。

$$
I = \frac23\rho\int_0^a r^2\cdot 4\pi r^2 dr = \frac23\rho\frac{4\pi a^5}{5} = \frac23\cdot\frac{3M}{4\pi a^3}\cdot\frac{4\pi a^5}{5} = \frac{2}{5}Ma^2
$$

**問 2（25 点）** $k \equiv I/(Ma^2)$ とおく。斜面に沿って $s$ だけ下ったとき、$v = a\omega$ より

$$
Mgs\sin\theta = \frac12 Mv^2 + \frac12 I\omega^2 = \frac12 M(1+k)v^2
$$

$$
v^2 = \frac{2gs\sin\theta}{1+k} \ \Longrightarrow\ a_{\rm cm} = \frac{1}{2}\frac{d(v^2)}{ds} = \boxed{\frac{g\sin\theta}{1+k}}
$$

円柱 $k = 1/2$: $a_{\rm cm} = \dfrac23 g\sin\theta$　／　球 $k = 2/5$: $a_{\rm cm} = \dfrac57 g\sin\theta$

**問 3（25 点）** 斜面方向の並進の運動方程式 $Mg\sin\theta - f = Ma_{\rm cm}$ より

$$
f = Mg\sin\theta\left(1 - \frac{1}{1+k}\right) = \frac{k}{1+k}Mg\sin\theta
$$

円柱 $f = \frac13 Mg\sin\theta$、球 $f = \frac27 Mg\sin\theta$。すべらない条件 $f \le \mu Mg\cos\theta$ より

$$
\mu \ge \frac{k}{1+k}\tan\theta \quad\Longrightarrow\quad \text{円柱: } \mu \ge \frac{\tan\theta}{3},\qquad \text{球: } \mu \ge \frac{2\tan\theta}{7}
$$

**問 4（20 点）** 平行軸の定理より接触点まわりの慣性モーメントは $I_{\rm c} = I + Ma^2 = Ma^2(1+k)$。接触点まわりの重力のモーメントは $Mga\sin\theta$（垂直抗力と摩擦力は接触点を通るのでモーメントを持たない）。角加速度 $\alpha = a_{\rm cm}/a$ を用いて

$$
Mga\sin\theta = Ma^2(1+k)\frac{a_{\rm cm}}{a} \ \Longrightarrow\ a_{\rm cm} = \frac{g\sin\theta}{1+k}
$$

問 2 と一致する。

**問 5（10 点）** $k$ が小さいほど $a_{\rm cm}$ が大きい。$k_{\rm 球} = 2/5 < k_{\rm 円柱} = 1/2$ なので **球が先に到達する**。$a_{\rm cm}$ は $k$ のみで決まり、$M$ にも $a$ にも依存しない。回転にエネルギーを取られる割合が形状だけで決まるためである。

---

## 8 ｜ 電磁気学（配点 100）

### 問 1（35 点）

**(1)** 極板間に自由電荷はないので $D$ は界面で連続。極板にガウスの法則を適用して

$$
D = \frac{Q}{S}\ (\text{両層共通}), \qquad E_1 = \frac{Q}{\varepsilon_1 S},\quad E_2 = \frac{Q}{\varepsilon_2 S}
$$

**(2)**

$$
V = E_1 d_1 + E_2 d_2 = \frac{Q}{S}\left(\frac{d_1}{\varepsilon_1} + \frac{d_2}{\varepsilon_2}\right)
\ \Longrightarrow\ \boxed{C = \frac{S}{\dfrac{d_1}{\varepsilon_1} + \dfrac{d_2}{\varepsilon_2}}}
$$

（コンデンサーの直列接続と等価）

**(3)** $P_i = D - \varepsilon_0 E_i = \dfrac{Q}{S}\left(1 - \dfrac{\varepsilon_0}{\varepsilon_i}\right)$。境界面（法線を層 1 → 層 2 にとる）では

$$
\sigma_b = P_1 - P_2 = \frac{\varepsilon_0 Q}{S}\left(\frac{1}{\varepsilon_2} - \frac{1}{\varepsilon_1}\right)
$$

$\varepsilon_1 = \varepsilon_2$ ならゼロ。誘電率が同じなら界面は存在しないのと同じなので当然である。

### 問 2（35 点）

**(1)** 中心軸と同心の半径 $r$ の円を貫く電流は $NI$。

$$
B\cdot 2\pi r = \mu_0 NI \ \Longrightarrow\ B(r) = \frac{\mu_0 NI}{2\pi r}
$$

外部では、トロイドの内側を通る円は電流を囲まず（$I_{\rm enc}=0$）、外側を通る円は行きと帰りの電流を同数囲むので $I_{\rm enc} = 0$。いずれも $B = 0$。

**(2)** $R \gg \sqrt S$ より断面内で $B \simeq B(R)$ とみなせる。1 巻きあたりの磁束 $\Phi_1 = B(R)S$、鎖交磁束は $N\Phi_1$。

$$
L = \frac{N\Phi_1}{I} = \boxed{\frac{\mu_0 N^2 S}{2\pi R}}
$$

**(3)** 体積は $2\pi R\cdot S$、エネルギー密度は $B(R)^2/2\mu_0$。

$$
W = \frac{1}{2\mu_0}\left(\frac{\mu_0 NI}{2\pi R}\right)^2 2\pi RS = \frac{\mu_0 N^2I^2S}{4\pi R} = \frac12 L I^2 \quad\checkmark
$$

### 問 3（30 点）

**(1)** $L\dfrac{dI}{dt} + RI = V_0$、$I(0)=0$ より

$$
I(t) = \frac{V_0}{R}\left(1 - e^{-t/\tau}\right), \qquad \tau = \frac{L}{R}
$$

**(2)** $L\dot I + RI = 0$、$I(0) = I_0 = V_0/R$ より $I(t) = I_0 e^{-t/\tau}$。

**(3)**

$$
W = \int_0^\infty I^2R\,dt = I_0^2R\int_0^\infty e^{-2t/\tau}dt = I_0^2 R\frac{\tau}{2} = \frac12 LI_0^2 \quad\checkmark
$$

---

## 9 ｜ 量子力学：有限深さ井戸（配点 100）

**問 1（10 点）** $V(-x) = V(x)$ よりパリティ演算子 $\hat P$ は $\hat H$ と交換する。したがって同時固有状態がとれる。さらに 1 次元の束縛状態は縮退しないので、各固有状態は必ず偶または奇のパリティを持つ。

**問 2（20 点）** 偶関数解は

$$
\psi(x) = \begin{cases} A\cos kx & (|x|<a) \\ Be^{-\kappa|x|} & (|x|>a)\end{cases}
$$

$x=a$ で $\psi$ と $\psi'$ が連続:

$$
A\cos ka = Be^{-\kappa a}, \qquad -Ak\sin ka = -\kappa Be^{-\kappa a}
$$

辺々割って

$$
k\tan(ka) = \kappa
$$

**問 3（15 点）** 奇関数解 $\psi = A\sin kx$（$|x|<a$）、$\psi = Be^{-\kappa x}$（$x>a$）。

$$
A\sin ka = Be^{-\kappa a},\qquad Ak\cos ka = -\kappa Be^{-\kappa a}
\ \Longrightarrow\ -k\cot(ka) = \kappa
$$

**問 4（25 点）**

$$
k^2 + \kappa^2 = \frac{2m(E+V_0)}{\hbar^2} + \frac{-2mE}{\hbar^2} = \frac{2mV_0}{\hbar^2}
$$

両辺に $a^2$ を掛けて $(ka)^2 + (\kappa a)^2 = R^2$。

$(ka, \kappa a)$ 平面で、半径 $R$ の円と、偶解の曲線 $\kappa a = ka\tan(ka)$（$ka = 0, \pi, 2\pi,\dots$ から立ち上がる枝）および奇解の曲線 $\kappa a = -ka\cot(ka)$（$ka = \pi/2, 3\pi/2,\dots$ から立ち上がる枝）との交点が束縛状態に対応する。枝の立ち上がりは $ka = n\pi/2$（$n = 0,1,2,\dots$）にあるので

$$
\boxed{\ \text{束縛状態の個数} = 1 + \left\lfloor \frac{2R}{\pi} \right\rfloor\ }
$$

**問 5（20 点）** 偶解の最初の枝は原点 $ka = 0$ から立ち上がるので、$R$ がどれほど小さくても半径 $R$ の円と必ず 1 回交わる。したがって 1 次元では **どんなに浅い井戸にも必ず束縛状態が 1 つ以上ある**。

3 次元の球対称井戸では、動径方程式を $u(r) = rR(r)$ と書き換えると $u(0) = 0$ という境界条件がつき、これは 1 次元の **奇関数解**と同じ条件になる。奇解の最初の枝は $ka = \pi/2$ から立ち上がるので、束縛状態が存在するには $R > \pi/2$、すなわち

$$
V_0 a^2 > \frac{\pi^2\hbar^2}{8m}
$$

が必要である。3 次元では井戸が浅すぎると束縛状態が存在しない。

**問 6（10 点）** $V_0\to\infty$ すなわち $R\to\infty$ では $\kappa a \to \infty$ となり、偶解は $\tan(ka)\to\infty$ すなわち $ka \to (2n-1)\pi/2$、奇解は $\cot(ka)\to -\infty$ すなわち $ka\to n\pi$。合わせて $ka = n\pi/2$（$n = 1,2,3,\dots$）。

$$
E + V_0 = \frac{\hbar^2k^2}{2m} = \frac{\hbar^2\pi^2 n^2}{8ma^2} = \frac{\hbar^2\pi^2n^2}{2mL^2}\quad (L = 2a)
$$

幅 $L=2a$ の無限に深い井戸の準位に一致する。

---

## 10 ｜ 統計力学：2 準位系（配点 100）

**問 1（10 点）** $z = 1 + e^{-\beta\Delta}$。粒子が独立で（格子点に固定され）区別できる場合 $Z_N = z^N$。

**問 2（15 点）**

$$
p_1 = \frac{e^{-\beta\Delta}}{1+e^{-\beta\Delta}} = \frac{1}{e^{\beta\Delta}+1}
$$

$T\to 0$ で $p_1\to 0$、$T\to\infty$ で $p_1\to 1/2$（2 準位が等確率）。

**問 3（10 点）** $U = N\Delta p_1 = \dfrac{N\Delta}{e^{\beta\Delta}+1}$

**問 4（20 点）** $x = \beta\Delta = \Delta/k_BT$ とすると $dx/dT = -x/T$。

$$
C = \frac{dU}{dT} = N\Delta\frac{e^x}{(e^x+1)^2}\cdot\frac{x}{T} = \boxed{Nk_B\frac{x^2e^x}{(e^x+1)^2}}
$$

**問 5（20 点）**

- **高温** $x\ll1$: $e^x\simeq1$ より $C \simeq \dfrac{Nk_Bx^2}{4} = \dfrac{Nk_B}{4}\left(\dfrac{\Delta}{k_BT}\right)^2 \propto T^{-2}$。$T\to\infty$ で $C\to0$（両準位が飽和して温度を上げても吸熱しない）。
- **低温** $x\gg1$: $C \simeq Nk_Bx^2e^{-x} = Nk_B\left(\dfrac{\Delta}{k_BT}\right)^2e^{-\Delta/k_BT}$。指数関数的にゼロへ（ギャップがあるため）。

両極限でゼロなので有限温度に極大が存在する。$\ln C = 2\ln x + x - 2\ln(e^x+1)$ を $x$ で微分してゼロと置くと

$$
\frac{2}{x} + 1 - \frac{2e^x}{e^x+1} = 0 \ \Longleftrightarrow\ \boxed{\ \frac{2}{x} = \tanh\frac{x}{2}\ }
$$

$x \simeq 2.3994$ より $\dfrac{k_BT_{\rm peak}}{\Delta} = \dfrac{1}{x} \simeq 0.417$。このとき $C_{\max} \simeq 0.4392\,Nk_B$。

**問 6（15 点）** $F = -k_BT\ln Z_N = -Nk_BT\ln(1+e^{-x})$、$S = -\partial F/\partial T$ より

$$
S = Nk_B\left[\ln\left(1+e^{-x}\right) + \frac{x}{e^x+1}\right]
$$

$T\to0$（$x\to\infty$）で $S\to0$（熱力学第三法則）。$T\to\infty$（$x\to0$）で $S\to Nk_B\ln 2$。

後者は、高温では各粒子が 2 状態を等確率でとるので全状態数が $W = 2^N$ となり、$S = k_B\ln W = Nk_B\ln2$ に一致する。

**問 7（10 点）** 実験では全比熱が $C = \gamma T + \beta T^3 + C_{\rm Schottky}$ と書ける。

1. まず十分低温（$T \ll T_{\rm peak}$）のデータを $C/T$ 対 $T^2$ でプロットし、切片から電子比熱係数 $\gamma$、傾きから格子項 $\beta$ を決める。
2. 全温度域のデータからこの $\gamma T + \beta T^3$ を差し引き、残りを Schottky の関数形でフィットして $\Delta$ と関与する粒子数 $N$ を決める。
3. さらに確実な同定として、**磁場を印加する**。ゼーマン分裂に由来するギャップなら $\Delta \propto B$ となり、ピーク位置が磁場に比例して移動する。格子・電子項は動かないので分離できる。

---

## 11 ｜ 物性物理：ホール効果（配点 100）

**問 1（20 点）** キャリアの速度を $\boldsymbol v = (v_x,0,0)$、磁束密度を $\boldsymbol B = (0,0,B)$ とすると

$$
\boldsymbol v\times\boldsymbol B = (0,\,-v_xB,\,0)
$$

定常状態では $y$ 方向の正味の力がゼロなので $q(E_y - v_xB) = 0$、すなわち

$$
\boxed{E_y = v_xB}
$$

（電荷 $q$ の符号によらずこの関係が成り立つ点に注意）

**問 2（25 点）** $j_x = nqv_x$ より $v_x = j_x/(nq)$。

$$
E_y = \frac{j_xB}{nq}, \qquad R_H = \frac{E_y}{j_xB} = \boxed{\frac{1}{nq}}
$$

ホール電圧は幅 $w$ にわたる電位差で、$j_x = I/(wt)$ より

$$
V_H = E_y w = \frac{j_xBw}{nq} = \boxed{\frac{IB}{nqt}}
$$

厚さ $t$ が薄いほど大きな信号が得られる。

**問 3（20 点）** $R_H$ の符号はキャリアの電荷 $q$ の符号そのものである。

- 金属ナトリウム: 伝導キャリアは電子（$q = -e$）なので $R_H < 0$。実測値から $n \simeq 2.5\times10^{28}\ \mathrm{m^{-3}}$ が得られ、原子 1 個あたり価電子 1 個という描像とよく一致する。
- $p$ 型シリコン: キャリアは正孔（$q = +e$）なので $R_H > 0$。ホール測定は半導体の型（$n$ 型か $p$ 型か）を判定する標準的手段である。

**問 4（15 点）** ドルーデ模型で $\sigma = nq\mu$（$\mu$ は移動度）。$|R_H| = 1/(n|q|)$ と掛け合わせると $n$ が消えて

$$
\mu = |R_H|\,\sigma
$$

すなわち **ホール測定と伝導度測定を組み合わせると、キャリア密度と移動度を別々に決められる**（これを Hall mobility という）。

**問 5（20 点）** $n = p$ を代入すると

$$
R_H = \frac{n(\mu_p^2 - \mu_n^2)}{en^2(\mu_p+\mu_n)^2} = \frac{\mu_p^2-\mu_n^2}{en(\mu_p+\mu_n)^2}
$$

$\mu_n > \mu_p$ なので分子は負、すなわち $R_H < 0$。

物理的意味: 電子と正孔は電荷の符号が逆なので、電場によるドリフトの向きも磁場によるローレンツ力の向きも互いに逆向きになる。その結果、ホール電圧への寄与は互いに打ち消し合う。打ち消しは完全ではなく、**移動度の大きいキャリアが勝つ**。真性半導体では通常 $\mu_n > \mu_p$ なので、電子と正孔が同数でもホール係数は電子的な符号（負）を示す。

---

## 12 ｜ 原子核・素粒子：コンプトン散乱（配点 100）

**問 1（25 点）** 入射光子の 4 元運動量を $(h\nu/c,\,h\nu/c,\,0)$、静止電子を $(m_ec,\,0,\,0)$、散乱光子を $(h\nu'/c,\ h\nu'\cos\theta/c,\ h\nu'\sin\theta/c)$、反跳電子を $p_e^\mu$ とする。

4 元運動量保存 $p_\gamma + p_e = p_\gamma' + p_e'$ を $p_e' = p_\gamma + p_e - p_\gamma'$ と書き、両辺の 2 乗（不変量）をとる。$p_\gamma^2 = p_\gamma'^2 = 0$、$p_e^2 = p_e'^2 = m_e^2c^2$ より

$$
m_e^2c^2 = m_e^2c^2 + 2p_e\cdot p_\gamma - 2p_e\cdot p_\gamma' - 2p_\gamma\cdot p_\gamma'
$$

$$
p_e\cdot p_\gamma = m_e h\nu, \quad p_e\cdot p_\gamma' = m_e h\nu', \quad p_\gamma\cdot p_\gamma' = \frac{h^2\nu\nu'}{c^2}(1-\cos\theta)
$$

$$
\therefore\ m_ec^2\left(\frac{1}{h\nu'} - \frac{1}{h\nu}\right) = 1-\cos\theta
\ \Longleftrightarrow\ \lambda'-\lambda = \frac{h}{m_ec}(1-\cos\theta)
$$

コンプトン波長は

$$
\lambda_C = \frac{h}{m_ec} = \frac{hc}{m_ec^2} = \frac{1240\ \mathrm{eV\cdot nm}}{0.511\times10^6\ \mathrm{eV}} = 2.43\times10^{-3}\ \mathrm{nm} = \boxed{2.43\ \mathrm{pm}}
$$

**問 2（15 点）** $\lambda = c/\nu$ を代入して整理すると

$$
\boxed{h\nu' = \frac{h\nu}{1 + \alpha(1-\cos\theta)}}, \qquad \alpha = \frac{h\nu}{m_ec^2}
$$

**問 3（20 点）**

$$
T = h\nu - h\nu' = h\nu\,\frac{\alpha(1-\cos\theta)}{1+\alpha(1-\cos\theta)}
$$

$1-\cos\theta$ の単調増加関数なので、$T$ は $\theta = 180^\circ$（真後ろへの散乱）で最大。

$$
\boxed{T_{\max} = h\nu\,\frac{2\alpha}{1+2\alpha}}
$$

これが検出器スペクトルの **コンプトン端**である。

**問 4（20 点）** $h\nu = 662$ keV、$\alpha = 662/511 = 1.2955$。

$$
T_{\max} = 662\times\frac{2\times1.2955}{1+2\times1.2955} = 662\times\frac{2.5910}{3.5910} = \boxed{478\ \mathrm{keV}}
$$

$$
h\nu'(180^\circ) = \frac{662}{1+2\times1.2955} = \frac{662}{3.5910} = \boxed{184\ \mathrm{keV}}
$$

検算: $478 + 184 = 662$ keV でエネルギー保存が成り立つ。

**問 5（10 点）** スペクトルは低エネルギー側から

1. **後方散乱ピーク**（184 keV）: 検出器の外側（遮蔽体、線源容器、検出器を支える構造物）でほぼ $180^\circ$ に散乱された光子が検出器に入射し、全吸収されて作る小さなピーク。$\theta \simeq 180^\circ$ 付近で $h\nu'$ が $\theta$ にほとんど依存しない（$dh\nu'/d\theta \to 0$）ため、幅の狭いピークになる。
2. **コンプトン連続部**: 検出器内で 1 回コンプトン散乱した後に散乱光子が逃げた事象。0 から 478 keV まで連続。
3. **コンプトン端**（478 keV）: 上記連続部の上端で、急な段差として見える。
4. **全吸収ピーク（光電ピーク）**（662 keV）: 光電効果、または多重散乱の末に全エネルギーが検出器内に落ちた事象。

**問 6（10 点）** **コンプトン散乱が支配的**である。

- 光電効果の断面積は $\sigma_{\rm pe}\propto Z^{4\sim5}/E_\gamma^{3}$ と光子エネルギーに対して急激に減少し、$Z\simeq50$ の NaI では 662 keV での寄与は数 % 程度にとどまる（数十 keV 以下では逆に支配的）。
- 電子対生成のしきい値は $2m_ec^2 = 1.022$ MeV なので、662 keV では **起こらない**。
- コンプトン散乱の断面積は電子数、すなわち $Z$ に比例するだけで、この領域では緩やかにしか減少しない。

なお、光電効果の寄与が小さくても全吸収ピークは十分観測される。多重コンプトン散乱の後に光電吸収されれば、全エネルギーが検出器内に落ちるためである。結晶が大きいほどこの寄与（ピーク・トータル比）が増える。
