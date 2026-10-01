#### 要点

**状態密度**（和を積分に直す道具。どのアンサンブルでも使う）
$$\sum_{\text{状態}} \to \int D(\epsilon)\,d\epsilon, \qquad D(\epsilon)d\epsilon = g\frac{V}{(2\pi\hbar)^3}4\pi p^2dp$$
（$g$ はスピン縮退度。電子なら2、光子なら偏極2）

| 分散関係 | $D(\epsilon)$ |
| --- | --- |
| 非相対論 $\epsilon = p^2/2m$ | $D(\epsilon) = \dfrac{gV}{4\pi^2}\left(\dfrac{2m}{\hbar^2}\right)^{3/2}\sqrt{\epsilon}$ |
| 相対論（超）$\epsilon = cp$ | $D(\epsilon) = \dfrac{gV}{2\pi^2\hbar^3c^3}\epsilon^2$ |
| 光子 $\epsilon = \hbar\omega$、$g = 2$ | $D(\omega) = \dfrac{V\omega^2}{\pi^2c^3}$ |

**フェルミ気体 $T = 0$**（$g = 2$、非相対論）
$$N = \int_0^{\epsilon_F}D\,d\epsilon \;\Rightarrow\; \epsilon_F = \frac{\hbar^2}{2m}(3\pi^2n)^{2/3}, \qquad U_0 = \frac{3}{5}N\epsilon_F, \qquad p_0 = \frac{2}{5}n\epsilon_F$$

**光子気体**：$\mu = 0$（粒子数が保存しない）。$U = aVT^4$、$F = -U/3$、$p = U/3V$、$S = 4U/3T$、$C_V = 4aVT^3$、断熱で $VT^3 = $ 一定。


#### 問4-1 ★ 立方体中の粒子と状態密度（立教2014春・2015春 大問4）


一辺 $L$ の立方体に閉じ込められた質量 $m$ の自由粒子。壁で波動関数がゼロ。

(1) エネルギー固有値が $E = E_0(n_x^2 + n_y^2 + n_z^2)$、$E_0 = \dfrac{\pi^2\hbar^2}{2mL^2}$、$n_i$ は正整数、と離散化されることを示せ。
(2) $E$ 以下の状態数 $N(E)$ を、$(n_x, n_y, n_z)$ 空間の球の $1/8$ の体積として求めよ。
(3) 状態密度 $D(E) = dN/dE$ を求めよ。
(4) スピン1/2のフェルミ粒子 $N$ 個をこの箱に入れたときの $T = 0$ でのフェルミエネルギー $\epsilon_F$ と全エネルギー $U_0$ を求めよ。

**解答**

(1) $\psi = \sin(n_x\pi x/L)\sin(n_y\pi y/L)\sin(n_z\pi z/L)$ が境界条件を満たし、$-\dfrac{\hbar^2}{2m}\nabla^2\psi = E\psi$ に代入して $E = \dfrac{\hbar^2\pi^2}{2mL^2}(n_x^2+n_y^2+n_z^2)$。

(2) $n_x^2+n_y^2+n_z^2 \le E/E_0 = R^2$ の正の八分球：$N(E) = \dfrac{1}{8}\cdot\dfrac{4\pi}{3}R^3 = \dfrac{\pi}{6}\left(\dfrac{E}{E_0}\right)^{3/2}$。

(3) $D(E) = \dfrac{\pi}{4}E_0^{-3/2}E^{1/2} = \dfrac{V}{4\pi^2}\left(\dfrac{2m}{\hbar^2}\right)^{3/2}\sqrt{E}$（$V = L^3$）。スピン2をかければ要点の式。

(4) $N = 2\int_0^{\epsilon_F}D\,dE = 2\cdot\dfrac{\pi}{6}\left(\dfrac{\epsilon_F}{E_0}\right)^{3/2}$ より $\epsilon_F = E_0\left(\dfrac{3N}{\pi}\right)^{2/3} = \dfrac{\hbar^2}{2m}(3\pi^2n)^{2/3}$。
$U_0 = 2\int_0^{\epsilon_F}E\,D\,dE = \dfrac{3}{5}N\epsilon_F$（$\int E\cdot E^{1/2} = \frac{2}{5}E^{5/2}$ と $\int E^{1/2} = \frac{2}{3}E^{3/2}$ の比）。


#### 問4-2 ★ 相対論的フェルミ気体（立教2022夏・2020夏 大問4）


1粒子エネルギー $\epsilon(p) = \sqrt{c^2p^2 + m^2c^4}$。スピン縮退なし。

(1) 状態密度 $D(\epsilon)$ を求めよ。
(2) 超相対論極限 $\epsilon \gg mc^2$ での $D(\epsilon)$ と、$T = 0$ でのフェルミエネルギー $\epsilon_F$。
(3) $\ln\Xi$ を $p$ の積分で表せ。

**解答**

(1) $D(\epsilon)d\epsilon = \dfrac{V}{(2\pi\hbar)^3}4\pi p^2dp$。$\epsilon d\epsilon = c^2p\,dp$ より $dp = \dfrac{\epsilon\,d\epsilon}{c^2p}$、$p = \dfrac{\sqrt{\epsilon^2 - m^2c^4}}{c}$：
$$D(\epsilon) = \frac{V}{2\pi^2\hbar^3c^3}\epsilon\sqrt{\epsilon^2 - m^2c^4}$$

(2) $\epsilon \gg mc^2$ で $D \simeq \dfrac{V\epsilon^2}{2\pi^2\hbar^3c^3}$。$N = \dfrac{V\epsilon_F^3}{6\pi^2\hbar^3c^3}$ より $\epsilon_F = \hbar c(6\pi^2n)^{1/3}$。

(3) $\ln\Xi = \sum_{\boldsymbol p}\ln[1 + e^{-\beta(\epsilon(p) - \mu)}] = \dfrac{V}{2\pi^2\hbar^3}\int_0^\infty p^2\ln\left[1 + e^{-\beta(\sqrt{c^2p^2+m^2c^4} - \mu)}\right]dp$。
