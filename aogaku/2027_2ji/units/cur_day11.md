（要点は Day 8 を参照）


#### 問2-3 ★ スピン $S$ の常磁性（立教2013春 大問4）


大きさ $S$ のスピン $N$ 個が磁場 $H$ 中。エネルギー $\epsilon = -g\mu_BHm$、$m = -S, \ldots, S$。

(1) 1スピンの分配関数 $z$ を求めよ。$x = \beta g\mu_BH$ とおく。
(2) 磁化 $M = Ng\mu_B\langle m\rangle$ を $z$ を用いて表せ。
(3) 高温 $x \ll 1$ で $M \simeq \dfrac{Ng^2\mu_B^2S(S+1)}{3k_BT}H$（キュリーの法則）を示せ。
(4) 低温 $x \gg 1$ での $M$ を求めよ。

**解答**

(1) $z = \sum_{m=-S}^{S}e^{xm}$。等比級数（公比 $e^x$、$2S+1$ 項）：
$$z = \frac{e^{-xS}(e^{x(2S+1)} - 1)}{e^x - 1} = \frac{\sinh\left((S+\tfrac12)x\right)}{\sinh(x/2)}$$

(2) $\langle m\rangle = \dfrac{1}{z}\sum me^{xm} = \dfrac{\partial\ln z}{\partial x}$。$M = Ng\mu_B\dfrac{\partial\ln z}{\partial x}$。

(3) $x \ll 1$ で $z \simeq \sum(1 + xm + \tfrac12x^2m^2) = (2S+1) + \tfrac12x^2\sum m^2$（$\sum m = 0$）。$\sum_{m=-S}^S m^2 = \dfrac{S(S+1)(2S+1)}{3}$。よって $\ln z \simeq \ln(2S+1) + \dfrac{x^2S(S+1)}{6}$、$\langle m\rangle \simeq \dfrac{xS(S+1)}{3}$。
$$M \simeq Ng\mu_B\frac{S(S+1)}{3}\beta g\mu_BH = \frac{Ng^2\mu_B^2S(S+1)}{3k_BT}H$$

(4) $x \gg 1$ で $m = S$ の項が支配的：$\langle m\rangle \to S$、$M \to Ng\mu_BS$（飽和）。


#### 問2-4 ★ スピン1/2と断熱消磁（上智2026秋 問6・青学第2-5回）


$N$ 個の磁気モーメント $\mu$、磁場 $B$ 中でエネルギー $\mp\mu B$。$x = \beta\mu B$。

(1) $z$、$F$、$U$ を求めよ。
(2) $S$ を求め、$B/T$ のみの関数であることを示せ。
(3) $T \to \infty$、$T \to 0$ での $S$ の値を求めよ。
(4) $B_1, T_1$ から断熱的に $B_2 < B_1$ に下げたときの $T_2$ を求めよ。

**解答**

(1) $z = e^x + e^{-x} = 2\cosh x$。$F = -Nk_BT\ln(2\cosh x)$。$U = -N\dfrac{\partial\ln z}{\partial\beta} = -N\mu B\tanh x$。

(2) $S = \dfrac{U - F}{T} = Nk_B\left[\ln(2\cosh x) - x\tanh x\right]$。$x = \mu B/(k_BT)$ なので **$S$ は $B/T$ のみの関数**。

(3) $T \to \infty$（$x \to 0$）：$S \to Nk_B\ln 2$（$W = 2^N$）。$T \to 0$（$x \to \infty$）：$\ln(2\cosh x) \simeq x$、$\tanh x \to 1$、$S \to 0$。

(4) 断熱で $S$ 一定 → $x$ 一定 → $B/T$ 一定 → $T_2 = T_1\dfrac{B_2}{B_1}$。$B_2 < B_1$ で温度が下がる。実際の下限は残留内部磁場で決まる。


#### 問2-5 ★ 古典理想気体と化学ポテンシャル（立教2019夏 大問4）


質量 $m$ の単原子分子 $N$ 個、体積 $V$、温度 $T$。$N \gg 1$、$\ln N! \simeq N\ln N - N$。

(1) 1粒子分配関数 $z$ を求めよ（$\lambda = h/\sqrt{2\pi mk_BT}$ を熱的ド・ブロイ波長とする）。
(2) $Z = z^N/N!$ から $F$ を求めよ。
(3) $\mu = \left(\dfrac{\partial F}{\partial N}\right)_{T,V}$ を数密度 $n = N/V$ で表せ。
(4) $p = -\partial F/\partial V$ から状態方程式を導け。

**解答**

(1) $z = \dfrac{1}{h^3}\int d^3x\,d^3p\,e^{-\beta p^2/2m} = \dfrac{V}{h^3}(2\pi mk_BT)^{3/2} = \dfrac{V}{\lambda^3}$。

(2) $F = -k_BT[N\ln z - \ln N!] = -Nk_BT\left[\ln\dfrac{V}{N\lambda^3} + 1\right]$。

(3) $\mu = \dfrac{\partial F}{\partial N} = -k_BT\left[\ln\dfrac{V}{N\lambda^3} + 1\right] + k_BT = k_BT\ln(n\lambda^3)$。
古典条件 $n\lambda^3 \ll 1$ のとき $\mu < 0$。

(4) $p = -\dfrac{\partial F}{\partial V} = \dfrac{Nk_BT}{V}$。

---
