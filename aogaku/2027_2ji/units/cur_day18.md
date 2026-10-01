（要点は S6 の板書を参照）


#### 問4-3 ★ フェルミ気体の感受率と揺らぎ（都立2026冬 物理学II[2]）


スピン1/2の3次元自由フェルミ気体。グランドカノニカル。$\chi \equiv \left(\dfrac{\partial\langle N\rangle}{\partial\mu}\right)_{T,V}$。

(1) 状態密度 $D(\epsilon)$ を求めよ。
(2) $T = 0$ での $\chi$ を $D(\mu)$ で表せ。
(3) 有限温度での $\chi$ を $\langle N\rangle$ と $\langle N^2\rangle$ で表せ。

**解答**

(1) 要点の式（$g = 2$）：$D(\epsilon) = \dfrac{V}{2\pi^2}\left(\dfrac{2m}{\hbar^2}\right)^{3/2}\sqrt\epsilon$。

(2) $T = 0$ で $\langle N\rangle = \int_0^\mu D(\epsilon)d\epsilon$。よって $\chi = D(\mu)$。

(3) $\langle N\rangle = \dfrac{1}{\beta}\dfrac{\partial\ln\Xi}{\partial\mu}$。もう一度微分：
$$\chi = \frac{1}{\beta}\frac{\partial^2\ln\Xi}{\partial\mu^2} = \frac{1}{\beta}\cdot\beta^2\left[\frac{1}{\Xi}\frac{\partial^2\Xi}{\partial(\beta\mu)^2} - \left(\frac{1}{\Xi}\frac{\partial\Xi}{\partial(\beta\mu)}\right)^2\right] = \beta\left(\langle N^2\rangle - \langle N\rangle^2\right)$$
$$\chi = \frac{\langle N^2\rangle - \langle N\rangle^2}{k_BT}$$
（粒子数の揺らぎ＝感受率。揺動散逸の一例）


#### 問4-4 ★ 光子気体の熱力学（青学第2-6回・立教2010春/2024春）


$D(\omega) = \dfrac{V\omega^2}{\pi^2c^3}$、$\mu = 0$。$\int_0^\infty\dfrac{x^3}{e^x-1}dx = \dfrac{\pi^4}{15}$。

(1) $U = \int D(\omega)\dfrac{\hbar\omega}{e^{\beta\hbar\omega}-1}d\omega = aVT^4$ を示し $a$ を求めよ。
(2) $F = k_BT\int D(\omega)\ln(1 - e^{-\beta\hbar\omega})d\omega$ を部分積分して $F = -U/3$ を示せ。
(3) $p = -\partial F/\partial V$、$S = -\partial F/\partial T$ を求め、$p = U/3V$ を確かめよ。
(4) $C_V$ を求め、断熱で $VT^3 = $ 一定を示せ。

**解答**

(1) 問2-1(4) と同じ：$a = \dfrac{\pi^2k_B^4}{15\hbar^3c^3}$。

(2) ボース（$\mu=0$）の $\Omega = k_BT\sum\ln(1 - e^{-\beta\hbar\omega})$。$x = \beta\hbar\omega$：
$$F = \frac{Vk_BT}{\pi^2c^3}\left(\frac{k_BT}{\hbar}\right)^3\int_0^\infty x^2\ln(1-e^{-x})dx$$
部分積分：$\int_0^\infty x^2\ln(1-e^{-x})dx = \left[\dfrac{x^3}{3}\ln(1-e^{-x})\right]_0^\infty - \int_0^\infty\dfrac{x^3}{3}\dfrac{e^{-x}}{1-e^{-x}}dx = -\dfrac{1}{3}\int_0^\infty\dfrac{x^3}{e^x-1}dx = -\dfrac{\pi^4}{45}$。
よって $F = -\dfrac{V\pi^2k_B^4T^4}{45\hbar^3c^3} = -\dfrac{1}{3}aVT^4 = -\dfrac{U}{3}$。

(3) $p = -\dfrac{\partial F}{\partial V} = \dfrac{aT^4}{3} = \dfrac{U}{3V}$。$S = -\dfrac{\partial F}{\partial T} = \dfrac{4}{3}aVT^3 = \dfrac{4U}{3T}$。

(4) $C_V = \dfrac{\partial U}{\partial T} = 4aVT^3$（$= 3S$）。断熱で $S \propto VT^3 = $ 一定。

---
