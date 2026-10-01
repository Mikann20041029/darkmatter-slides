#### 要点

固定するもの：$T, V, N$。出発点：**分配関数** $Z = \sum_{\text{状態}} e^{-\beta E}$。ポテンシャル：$F = -k_BT\ln Z$。

$$U = -\frac{\partial\ln Z}{\partial\beta}, \qquad S = -\left(\frac{\partial F}{\partial T}\right)_V, \qquad p = -\left(\frac{\partial F}{\partial V}\right)_T, \qquad C_V = \frac{\partial U}{\partial T}$$

**独立粒子系**：1粒子分配関数 $z$ に対して
- 区別できる（格子点に固定・スピンなど）：$Z = z^N$
- 区別できない（気体）：$Z = z^N/N!$

**便利な公式**
- $U = -\dfrac{\partial\ln Z}{\partial\beta} = k_BT^2\dfrac{\partial\ln Z}{\partial T}$
- $S = \dfrac{U - F}{T} = k_B\ln Z + \dfrac{U}{T}$
- 等比級数：$\sum_{n=0}^\infty x^n = \dfrac{1}{1-x}$、$\sum nx^n = \dfrac{x}{(1-x)^2}$（$|x| < 1$）


#### 問2-1 ★ 量子調和振動子と黒体輻射（立教2010春 大問IV・2024春 大問4）


(1) $E_n = \hbar\omega(n + \tfrac12)$ の分配関数 $z$ を求め、$\langle E\rangle = \dfrac{\hbar\omega}{2} + \dfrac{\hbar\omega}{e^{\beta\hbar\omega} - 1}$ を示せ。
(2) 体積 $V$ の空洞内の電磁波について、偏極2を考慮した運動量空間の状態数密度は $2V/(2\pi\hbar)^3$。角振動数 $\omega \sim \omega + d\omega$ のモード数 $D(\omega)d\omega$ を求めよ。
(3) 零点エネルギーを除いたエネルギー密度 $u(\omega) = \dfrac{\hbar}{\pi^2c^3}\dfrac{\omega^3}{e^{\beta\hbar\omega} - 1}$ を示せ。
(4) $u = \int_0^\infty u(\omega)d\omega = aT^4$ を示し、$a$ を求めよ。$\int_0^\infty \dfrac{x^3}{e^x - 1}dx = \dfrac{\pi^4}{15}$。
(5) 長波長極限でのレイリー・ジーンズの法則を導け。

**解答**

(1) $z = \sum_{n=0}^\infty e^{-\beta\hbar\omega(n+1/2)} = e^{-\beta\hbar\omega/2}\dfrac{1}{1 - e^{-\beta\hbar\omega}}$。
$\langle E\rangle = -\dfrac{\partial\ln z}{\partial\beta} = \dfrac{\hbar\omega}{2} + \dfrac{\hbar\omega e^{-\beta\hbar\omega}}{1 - e^{-\beta\hbar\omega}} = \dfrac{\hbar\omega}{2} + \dfrac{\hbar\omega}{e^{\beta\hbar\omega} - 1}$。

(2) 運動量 $p = \hbar k = \hbar\omega/c$。運動量空間の球殻 $4\pi p^2dp$ に状態数密度をかけて
$$D(\omega)d\omega = \frac{2V}{(2\pi\hbar)^3}4\pi p^2 dp = \frac{2V}{8\pi^3\hbar^3}\cdot4\pi\frac{\hbar^2\omega^2}{c^2}\cdot\frac{\hbar d\omega}{c} = \frac{V\omega^2}{\pi^2c^3}d\omega$$

(3) 各モードのエネルギー（零点除く）$\dfrac{\hbar\omega}{e^{\beta\hbar\omega}-1}$ にモード数をかけて $V$ で割る：
$$u(\omega) = \frac{1}{V}D(\omega)\frac{\hbar\omega}{e^{\beta\hbar\omega}-1} = \frac{\hbar}{\pi^2c^3}\frac{\omega^3}{e^{\beta\hbar\omega}-1}$$

(4) $x = \beta\hbar\omega$ と置換：$u = \dfrac{\hbar}{\pi^2c^3}\left(\dfrac{k_BT}{\hbar}\right)^4\int_0^\infty\dfrac{x^3}{e^x-1}dx = \dfrac{\pi^2k_B^4}{15\hbar^3c^3}T^4$。
$$a = \frac{\pi^2k_B^4}{15\hbar^3c^3}$$

(5) $\beta\hbar\omega \ll 1$ で $e^{\beta\hbar\omega} - 1 \simeq \beta\hbar\omega$。$u(\omega) \simeq \dfrac{\omega^2}{\pi^2c^3}k_BT$（$\hbar$ が消える＝古典的）。波長で書くと $u(\lambda) \propto k_BT/\lambda^4$。

> **偏極の2を忘れない**（第2-6回で落とした）。$D(\omega)$ に2がなければ $a$ が半分になる。


#### 問2-2 ★ 古典調和振動子（立教2012春 大問4）


質量 $m$、振動数 $\nu$ の古典的1次元調和振動子が多数独立に存在し温度 $T$。$\int_{-\infty}^\infty e^{-ax^2}dx = \sqrt{\pi/a}$。

(1) 振動子1つのカノニカル分配関数 $Z_1(T)$ を求めよ（位相空間積分、$h$ で割る）。
(2) 単位体積あたり $\rho$ 個あるとき、ヘルムホルツ自由エネルギー密度 $f(T,\rho)$ を求めよ。
(3) 1振動子あたりの平均エネルギーと熱容量を求めよ。

**解答**

(1) $H = \dfrac{p^2}{2m} + \dfrac{1}{2}m\omega^2x^2$（$\omega = 2\pi\nu$）。
$$Z_1 = \frac{1}{h}\int dx\,dp\,e^{-\beta H} = \frac{1}{h}\sqrt{\frac{2\pi m}{\beta}}\sqrt{\frac{2\pi}{\beta m\omega^2}} = \frac{2\pi}{h\beta\omega} = \frac{k_BT}{h\nu}$$

(2) $f = -\rho k_BT\ln Z_1 = -\rho k_BT\ln\dfrac{k_BT}{h\nu}$（区別できる振動子なので $N!$ なし）。

(3) $\langle E\rangle = -\dfrac{\partial\ln Z_1}{\partial\beta} = \dfrac{1}{\beta} = k_BT$（等分配則：運動と位置で $k_BT/2$ ずつ）。$C = k_B$。
