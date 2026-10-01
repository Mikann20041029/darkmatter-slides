#### 要点

固定するもの：$E, V, N$。出発点：**状態数** $W(E, V, N)$。ポテンシャル：$S = k_B\ln W$。

$$\frac{1}{T} = \left(\frac{\partial S}{\partial E}\right)_{V,N}, \qquad \frac{p}{T} = \left(\frac{\partial S}{\partial V}\right)_{E,N}, \qquad \frac{\mu}{T} = -\left(\frac{\partial S}{\partial N}\right)_{E,V}$$

**スターリングの公式**：$\ln N! \simeq N\ln N - N$（$N \gg 1$）。必ず使う。

**場合の数の型**
- 区別できる $N$ 個から $n$ 個を選ぶ：$\binom{N}{n} = \dfrac{N!}{n!(N-n)!}$
- 区別できない $M$ 個を $N$ 個の箱に入れる（重複組合せ）：$\binom{M+N-1}{M} = \dfrac{(M+N-1)!}{M!(N-1)!}$


#### 問1-1 ★ 2準位系のミクロカノニカルと負温度（都立2025冬 物理学II[2]）


$N$ 個の独立粒子。各粒子は状態1（エネルギー $+\Delta$）か状態2（$-\Delta$）。状態 $i$ の粒子数を $N_i$。

(1) 全エネルギー $U$ を $N_1, N_2, \Delta$ で表せ。
(2) 状態数 $W$ を求めよ。
(3) $N_1 = n_1 N$ とおき、スターリングで $S$ を $N, n_1$ で表せ。
(4) 1粒子あたりの平均エネルギーを $\epsilon\Delta$（$U = N\epsilon\Delta$）とおくと
$$S = -k_BN\left[\frac{1+\epsilon}{2}\ln\frac{1+\epsilon}{2} + \frac{1-\epsilon}{2}\ln\frac{1-\epsilon}{2}\right]$$
を示せ。
(5) $1/T = \partial S/\partial U$ から $T$ を $\epsilon$ の関数として求め、$\epsilon > 0$ で $T < 0$（負温度）になることを示せ。

**解答**

(1) $U = N_1\Delta - N_2\Delta = (N_1 - N_2)\Delta$、$N_1 + N_2 = N$。

(2) $N$ 個から状態1の $N_1$ 個を選ぶ：$W = \dbinom{N}{N_1} = \dfrac{N!}{N_1!(N-N_1)!}$。

(3) $S = k_B[\ln N! - \ln N_1! - \ln(N-N_1)!]$。スターリングで
$$S = k_B[N\ln N - N_1\ln N_1 - (N-N_1)\ln(N-N_1)] = -k_BN[n_1\ln n_1 + (1-n_1)\ln(1-n_1)]$$

(4) $U = (2N_1 - N)\Delta = N\epsilon\Delta$ より $n_1 = \dfrac{1+\epsilon}{2}$、$1 - n_1 = \dfrac{1-\epsilon}{2}$。代入で題意の式。

(5) $\dfrac{1}{T} = \dfrac{\partial S}{\partial U} = \dfrac{1}{N\Delta}\dfrac{\partial S}{\partial\epsilon} = -\dfrac{k_B}{2\Delta}\ln\dfrac{1+\epsilon}{1-\epsilon}$。
$$T = -\frac{2\Delta}{k_B\ln\frac{1+\epsilon}{1-\epsilon}}$$
$\epsilon > 0$（上の準位に過半数）なら $\ln(\cdots) > 0$ で $T < 0$。$\epsilon = 0$（半々）で $T = \pm\infty$、$\epsilon \to -1$（全部下）で $T \to +0$。

> **物理的意味**：準位が有限個の系では、エネルギーを注ぎ込むと $S$ が減る領域があり、そこが負温度。負温度は「無限大より熱い」。


#### 問1-2 ★ 2つの壺（上智2026春 問6）


区別できる $N$ 個の球を壺A・Bに分ける。壺Bに $n$ 個ある状態を $(N, n)$、その微視的状態数を $W_N(n)$ とする。

(1) 巨視的状態の総数（$n = 0 \sim N$）と微視的状態の総数を求めよ。
(2) $W_N(0)$、$W_N(1)$ を求めよ。
(3) $S = k_B\ln W_N(n)$ が最小となる $n$ と $S_{\min}$、最大となる $n$ と $S_{\max}$（$N$ 偶数・奇数）を求めよ。
(4) 壺Aの球1個のエネルギーを $E_A$、Bを $E_B$ とし、球が A→B に移る確率と B→A に移る確率の比がボルツマン分布 $\dfrac{P_{A\to B}}{P_{B\to A}} = \exp\left(-\dfrac{E_B - E_A}{k_BT}\right)$ に従うとする。定常状態での $\langle N_A\rangle$ を $N, E_A, E_B, T$ で表せ。

**解答**

(1) 巨視的状態は $n = 0, 1, \ldots, N$ の $N+1$ 通り。微視的状態は各球がAかBの $2^N$ 通り。

(2) $W_N(0) = 1$、$W_N(1) = N$。一般に $W_N(n) = \dbinom{N}{n}$。

(3) $S_{\min}$：$n = 0$ または $N$ で $W = 1$、$S_{\min} = 0$。$S_{\max}$：$\binom{N}{n}$ は $n = N/2$ で最大。$N$ 偶数なら $n = N/2$ の1点、奇数なら $n = (N\pm1)/2$ の2点。$S_{\max} = k_B\ln\binom{N}{\lfloor N/2\rfloor}$。

(4) 定常で流れが釣り合う：$N_A P_{A\to B} = N_B P_{B\to A}$。よって $\dfrac{N_B}{N_A} = \dfrac{P_{A\to B}}{P_{B\to A}} = e^{-\beta(E_B - E_A)}$。$N_A + N_B = N$ より
$$\langle N_A\rangle = \frac{N}{1 + e^{-\beta(E_B - E_A)}} = \frac{N\,e^{-\beta E_A}}{e^{-\beta E_A} + e^{-\beta E_B}}$$
これは2準位系のカノニカル分布そのもの。


#### 問1-3 ★ 調和振動子のミクロカノニカル（青学第2-2回・立教2016夏に類似）


$N$ 個の独立な調和振動子（角振動数 $\omega$ 共通）。全エネルギー $E = (M + N/2)\hbar\omega$、$M = \sum n_i$。

(1) $W(N, M)$ を求めよ。
(2) スターリングで $S(N, M)$ を求めよ。
(3) $1/T = \partial S/\partial E$ から $M(T)$ と $E(T)$ を求めよ。
(4) 熱容量 $C$ を求め、高温で $Nk_B$、低温での主要項を示せ。

**解答**

(1) $M$ 個の量子を $N$ 個の振動子に分配（重複組合せ）：$W = \dfrac{(M+N-1)!}{M!(N-1)!}$。

(2) $N, M \gg 1$ で $W \simeq \dfrac{(M+N)!}{M!N!}$。
$$S = k_B\left[(M+N)\ln(M+N) - M\ln M - N\ln N\right] = k_B\left[M\ln\frac{M+N}{M} + N\ln\frac{M+N}{N}\right]$$

(3) $\dfrac{1}{T} = \dfrac{\partial S}{\partial E} = \dfrac{1}{\hbar\omega}\dfrac{\partial S}{\partial M} = \dfrac{k_B}{\hbar\omega}\ln\dfrac{M+N}{M}$。よって $\dfrac{M+N}{M} = e^{\beta\hbar\omega}$、
$$M = \frac{N}{e^{\beta\hbar\omega} - 1}, \qquad E = N\hbar\omega\left(\frac{1}{e^{\beta\hbar\omega} - 1} + \frac{1}{2}\right)$$

(4) $C = \dfrac{\partial E}{\partial T} = Nk_B\left(\dfrac{\hbar\omega}{k_BT}\right)^2\dfrac{e^{\beta\hbar\omega}}{(e^{\beta\hbar\omega}-1)^2}$。
高温（$x = \beta\hbar\omega \ll 1$）：$e^x - 1 \simeq x$ で $C \to Nk_B$（デュロン・プティ）。
低温（$x \gg 1$）：$C \simeq Nk_Bx^2e^{-x}$。**主要項は $e^{-x}$ で、指数関数的にゼロ。**

> **弱点A の本丸**：$\dfrac{d}{dx}\dfrac{1}{e^x - 1} = -\dfrac{e^x}{(e^x-1)^2}$。分子の $e^x$ を落とすと低温で $x^2e^{-2x}$ になる（誤）。

---
