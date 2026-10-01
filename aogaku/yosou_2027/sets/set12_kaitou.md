# 第 12 回 解答 — 統計力学（光子気体・黒体輻射）

## 10 ｜ 統計力学

### 問 1. 状態密度

周期境界条件より、許される波数は $\boldsymbol k = \dfrac{2\pi}{L}(n_x, n_y, n_z)$、$n_i \in \mathbb Z$。
$\boldsymbol k$ 空間で 1 つのモードが占める体積は $(2\pi/L)^3 = (2\pi)^3/V$。

半径 $k$ と $k+dk$ の球殻の体積は $4\pi k^2 dk$ なので、モード数は偏光 2 を掛けて

$$
dN = 2 \cdot \frac{V}{(2\pi)^3}\,4\pi k^2\,dk = \frac{V k^2}{\pi^2}\,dk .
$$

$k = \omega/c$、$dk = d\omega/c$ を代入して

$$
\boxed{\;D(\omega) = \frac{V\omega^2}{\pi^2 c^3}\;}
$$

**検算**: $[D(\omega)] = \mathrm{m^3 \cdot s^{-2} / (m^3 s^{-3})} = \mathrm{s}$。
$D(\omega)d\omega$ が無次元（個数）になるので正しい。

### 問 2. $\mu = 0$ の理由

**光子の数は保存しないから。** 空洞の壁が光子を自由に吸収・放出するため、$N$ は熱平衡で
自分自身が決まる変数である。したがって平衡条件は $F$ を $N$ について最小化すること、すなわち

$$
\left(\frac{\partial F}{\partial N}\right)_{T,V} = \mu = 0 .
$$

（粒子数が保存する理想ボース気体では $\mu$ は $N$ を固定する未定乗数として残るが、
光子にはその拘束がない。）

### 問 3. 平均光子数

$\mu = 0$ のボース分布、または 1 モードを調和振動子とみて直接:

$$
z = \sum_{n=0}^{\infty} e^{-\beta n\hbar\omega} = \frac{1}{1 - e^{-\beta\hbar\omega}},\qquad
\langle n\rangle = -\frac{1}{\hbar\omega}\frac{\partial \ln z}{\partial \beta}
= \frac{e^{-\beta\hbar\omega}}{1-e^{-\beta\hbar\omega}}
$$

$$
\boxed{\;\langle n(\omega)\rangle = \frac{1}{e^{\beta\hbar\omega}-1}\;}
$$

**検算**: $T\to 0$（$\beta\to\infty$）で $\langle n\rangle \to 0$、$T\to\infty$ で
$\langle n\rangle \to k_BT/\hbar\omega \to \infty$。どちらも妥当。

### 問 4. プランクの放射則

単位体積・単位角振動数あたりのエネルギー密度は $u = \dfrac{1}{V}\hbar\omega\,D(\omega)\langle n\rangle$ より

$$
\boxed{\;u(\omega,T) = \frac{\hbar\,\omega^3}{\pi^2c^3}\,\frac{1}{e^{\beta\hbar\omega}-1}\;}
$$

**低振動数側** $\hbar\omega \ll k_BT$: $e^{\beta\hbar\omega}-1 \simeq \beta\hbar\omega$ より

$$
u \to \frac{\omega^2}{\pi^2c^3}\,k_BT \qquad(\text{レイリー–ジーンズの法則})
$$

これは $\dfrac{1}{V}D(\omega)\times k_BT$ に等しい。**1 モードあたり $k_BT$**、すなわち
調和振動子 1 個（運動 + ポテンシャルで $\frac12 k_BT \times 2$）のエネルギー等分配則そのもの。
$\hbar$ が消えることが古典極限であることの証拠。

**高振動数側** $\hbar\omega \gg k_BT$:

$$
u \to \frac{\hbar\omega^3}{\pi^2c^3}\,e^{-\beta\hbar\omega} \qquad(\text{ウィーンの法則})
$$

指数関数的に落ちる。**レイリー–ジーンズをそのまま全 $\omega$ で積分すると発散する
（紫外破綻）のを、この因子が救っている。**

### 問 5. シュテファン–ボルツマンの法則

$$
\frac{U}{V} = \int_0^\infty u(\omega,T)\,d\omega
= \frac{\hbar}{\pi^2c^3}\int_0^\infty \frac{\omega^3}{e^{\beta\hbar\omega}-1}\,d\omega
$$

$x = \beta\hbar\omega$ と置くと $\omega^3 d\omega = \dfrac{x^3dx}{(\beta\hbar)^4}$ なので

$$
\frac{U}{V} = \frac{\hbar}{\pi^2c^3}\left(\frac{k_BT}{\hbar}\right)^4\int_0^\infty\frac{x^3}{e^x-1}dx
= \frac{\hbar}{\pi^2c^3}\cdot\frac{(k_BT)^4}{\hbar^4}\cdot\frac{\pi^4}{15}
$$

$$
\boxed{\;U = \frac{\pi^2 (k_BT)^4}{15\,\hbar^3c^3}\,V \;\propto\; T^4\;}
$$

**この $T^4$ がどこから来るか**（口頭試問で聞かれたらこう答える）:
状態密度が $\omega^2$、1 モードのエネルギーが $\hbar\omega$、
そして温度が決める振動数スケールが $\omega \sim k_BT/\hbar$。よって
$U/V \sim \hbar\omega\cdot\omega^2\cdot\omega \sim \hbar\omega^4 \propto T^4$。
**次数は「$\varepsilon \propto k$（質量ゼロ）」と「3 次元」だけで決まる。**

### 問 6. 自由エネルギー・圧力・比熱

$\mu = 0$ なので大分配関数と分配関数が一致し、

$$
\ln Z = -\int_0^\infty D(\omega)\ln\!\left(1 - e^{-\beta\hbar\omega}\right)d\omega,\qquad
F = -k_BT\ln Z = k_BT\int_0^\infty D(\omega)\ln\!\left(1-e^{-\beta\hbar\omega}\right)d\omega
$$

$D(\omega) \propto \omega^2$ なので部分積分すると（$\left[\frac{\omega^3}{3}\ln(1-e^{-\beta\hbar\omega})\right]_0^\infty = 0$）

$$
F = -\frac{V}{3}\cdot\frac{\hbar}{\pi^2c^3}\int_0^\infty\frac{\omega^3}{e^{\beta\hbar\omega}-1}d\omega
= -\frac{U}{3}
$$

$F$ は $V$ に比例する（$U/V$ が $V$ に依らない）ので

$$
P = -\left(\frac{\partial F}{\partial V}\right)_T = -\frac{F}{V} = \boxed{\;\frac{U}{3V}\;}
$$

**検算**: 非相対論的な理想気体は $PV = \frac23 U$、超相対論的（$\varepsilon \propto p$）は $PV = \frac13 U$。
光子は後者。係数 $1/3$ は「3 次元」から来ている（$d$ 次元なら $PV = U/d$）。

比熱は

$$
C_V = \left(\frac{\partial U}{\partial T}\right)_V = \frac{4U}{T}
= \frac{4\pi^2k_B^4}{15\hbar^3c^3}\,V\,T^3 \;\propto\; \boxed{T^3}
$$

**注意**: これはデバイ比熱の $T^3$ と**同じ形だが理由が違う**。
デバイは「音響フォノンの $\omega = vk$ ＋ 低温でカットオフに届かない」。
光子は「$\omega = ck$ ＋ そもそも上限がない」。**$\varepsilon \propto k$ の線形分散が共通の原因。**

### 問 7. 2 次元・$d$ 次元

**2 次元**: モードが占める面積は $(2\pi)^2/A$、半径 $k$ の円環は $2\pi k\,dk$。偏光 2 を掛けて

$$
dN = 2\cdot\frac{A}{(2\pi)^2}\,2\pi k\,dk = \frac{Ak}{\pi}dk
\;\Longrightarrow\;
D(\omega) = \frac{A\,\omega}{\pi c^2}
$$

$$
U = \int_0^\infty \hbar\omega\,D(\omega)\langle n\rangle\,d\omega
= \frac{A\hbar}{\pi c^2}\left(\frac{k_BT}{\hbar}\right)^3\int_0^\infty\frac{x^2}{e^x-1}dx
\;\propto\; \boxed{T^3}
$$

（$\int_0^\infty \frac{x^2}{e^x-1}dx = 2\zeta(3) \simeq 2.404$）

**$d$ 次元**: $D(\omega)\propto \omega^{d-1}$ なので

$$
U \propto \int_0^\infty \frac{\omega^{d}}{e^{\beta\hbar\omega}-1}d\omega \propto T^{d+1}
\qquad\Longrightarrow\qquad \boxed{U \propto T^{d+1}},\quad C_V \propto T^{d}
$$

$d=3$ で $T^4$、$d=2$ で $T^3$。**問 5 の答えと整合している。**

---

### この問題で必ずやる検算（弱点 B 対策）

| 場所 | 検算 |
| --- | --- |
| 問 1 | $D(\omega)d\omega$ が無次元（個数）か |
| 問 3 | $T\to0$ で $\langle n\rangle\to0$、$T\to\infty$ で発散するか |
| 問 4 | 低振動数極限で $\hbar$ が消えるか（消えなければ古典極限になっていない） |
| 問 5 | $U$ の次元がエネルギーか。$T^4$ の指数が問 7 の $d+1$ と一致するか |
| 問 6 | $C_V = 4U/T$ を $U\propto T^4$ から独立に確かめる |
| 問 7 | $d=3$ を代入して問 5 に戻るか |
