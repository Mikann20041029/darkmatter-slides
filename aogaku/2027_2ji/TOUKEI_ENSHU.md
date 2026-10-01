# 統計力学・熱力学 演習書

**過去問に出た型だけで組んだ**演習書。各問に「元になった過去問」を明記。

構成は `TOUKEI_ZENTAIZOU.md` の5層に対応：第0章 熱力学 → 第1章 ミクロカノニカル → 第2章 カノニカル → 第3章 グランドカノニカル → 第4章 量子理想気体・光子 → 第5章 揺らぎ・相互作用系

**使い方**：各章の「要点」を読んでから問題を解く。解答は見ずに紙で解き、答え合わせをする。★は必修、☆は余裕があれば。

記号：$k_B$ ボルツマン定数、$\beta = 1/(k_BT)$、$\hbar = h/2\pi$

作成 2026-09-12

---

## 0｜熱力学（統計力学の手前・青学本番で落とした層）

### 要点

**第一法則**：$dU = TdS - pdV$（＋$\mu dN$）。これが全ての出発点。

**熱力学ポテンシャルと自然な変数**

| ポテンシャル | 定義 | 全微分 | 自然な変数 |
| --- | --- | --- | --- |
| 内部エネルギー $U$ | — | $dU = TdS - pdV$ | $(S, V)$ |
| ヘルムホルツ $F$ | $F = U - TS$ | $dF = -SdT - pdV$ | $(T, V)$ |
| エンタルピー $H$ | $H = U + pV$ | $dH = TdS + Vdp$ | $(S, p)$ |
| ギブス $G$ | $G = H - TS$ | $dG = -SdT + Vdp$ | $(T, p)$ |

**マクスウェル関係式**：全微分の2階偏微分は順序によらない。例えば $dF = -SdT - pdV$ から
$$\left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial p}{\partial T}\right)_V$$
これが「測れない量 $(\partial S/\partial V)_T$」を「測れる量 $(\partial p/\partial T)_V$」に変換する道具。

**最重要公式**（立教2020春・2011春で出た）
$$\left(\frac{\partial U}{\partial V}\right)_T = -p + T\left(\frac{\partial p}{\partial T}\right)_V$$
導出：$dU = TdS - pdV$ を $T$ 一定で $V$ で割り、マクスウェル関係式を入れる。

**準静的過程**
- 等温：$T$ 一定。理想気体なら $\Delta S = nR\ln(V_2/V_1)$
- 断熱（準静的＝可逆）：$S$ 一定。$dQ = 0$ かつ $dS = 0$

### 問0-1 ★ 理想気体のエントロピーと等温・断熱変化（青学本番）

単原子理想気体（$n$ mol、$C_V = \frac{3}{2}nR$、$pV = nRT$）について、

(1) $dU = TdS - pdV$ を用いて $S(T, V)$ を求めよ。積分定数を $S_0$ とする。
(2) 準静的等温変化で体積を $V_1 \to V_2$ にした。エントロピーは変化するか。$\Delta S$ を求めよ。
(3) 準静的断熱変化で体積を $V_1 \to V_2$ にした。エントロピーは変化するか。到達温度 $T_2$ を $T_1, V_1, V_2$ で表せ。

**解答**

(1) $dS = \dfrac{dU}{T} + \dfrac{p}{T}dV$。$dU = C_V dT$、$p/T = nR/V$ なので
$$dS = C_V\frac{dT}{T} + nR\frac{dV}{V} \quad\Rightarrow\quad S = C_V \ln T + nR\ln V + S_0 = \frac{3}{2}nR\ln T + nR\ln V + S_0$$

(2) 等温なので第1項は変化しない。**変化する**：
$$\Delta S = nR\ln\frac{V_2}{V_1}$$
膨張なら正（増加）、圧縮なら負。

(3) 準静的断熱は可逆断熱＝等エントロピー。**変化しない**、$\Delta S = 0$。(1) の式で $S$ 一定とすると
$$C_V\ln\frac{T_2}{T_1} = -nR\ln\frac{V_2}{V_1} \quad\Rightarrow\quad T_2 = T_1\left(\frac{V_1}{V_2}\right)^{nR/C_V} = T_1\left(\frac{V_1}{V_2}\right)^{2/3}$$
$\gamma = C_p/C_V = 5/3$ なので $nR/C_V = \gamma - 1 = 2/3$。$TV^{\gamma-1} = $ 一定 と同じ。

> **落とし穴**：等温で「変化しない」、断熱で「変化する」と逆に書きやすい。「断熱・準静的＝$S$ 一定」を先に固定する。

### 問0-2 ★ $(\partial U/\partial V)_T$ の一般式（立教2020春 大問4）

(1) 状態方程式の形によらず $\left(\dfrac{\partial U}{\partial V}\right)_T = -p + T\left(\dfrac{\partial p}{\partial T}\right)_V$ が成り立つことを示せ。
(2) 状態方程式が $pV = \alpha U(T, V)$（$\alpha$ は定数）で与えられるとき、$U = V^{-\alpha}A(TV^\alpha)$、$S = B(TV^\alpha)$ の形になることを導け（$A, B$ は任意関数）。
(3) 理想気体（$\alpha = 2/3$）、光子気体（$\alpha = 1/3$）でそれぞれ何が言えるか。

**解答**

(1) $dU = TdS - pdV$ の両辺を $T$ 一定で $dV$ で割る：
$$\left(\frac{\partial U}{\partial V}\right)_T = T\left(\frac{\partial S}{\partial V}\right)_T - p$$
マクスウェル関係式 $\left(\dfrac{\partial S}{\partial V}\right)_T = \left(\dfrac{\partial p}{\partial T}\right)_V$（$dF = -SdT - pdV$ から）を代入して完成。

(2) $p = \alpha U/V$ を (1) に代入：
$$\left(\frac{\partial U}{\partial V}\right)_T = -\frac{\alpha U}{V} + \frac{\alpha T}{V}\left(\frac{\partial U}{\partial T}\right)_V$$
整理すると $V\dfrac{\partial U}{\partial V} - \alpha T\dfrac{\partial U}{\partial T} = -\alpha U$。変数 $x = TV^\alpha$ を導入すると、$U = V^{-\alpha}A(x)$ がこの1階偏微分方程式を満たすことが直接代入で確かめられる。
$S$ については $dS = \dfrac{1}{T}dU + \dfrac{p}{T}dV$ に上の $U$ と $p = \alpha U/V$ を入れると $dS = \dfrac{A'(x)}{T}\,dx \cdot V^{-\alpha}$…整理して $S = B(TV^\alpha)$。

(3) $\alpha = 2/3$：断熱で $TV^{2/3} = $ 一定（問0-1と一致）。$\alpha = 1/3$：$TV^{1/3} = $ 一定、$U \propto V^{-1/3}A(TV^{1/3})$ で $U = aVT^4$ の形と整合する。

### 問0-3 ★ ファンデルワールス気体（立教2011春 大問3）

$p = \dfrac{RT}{V - b} - \dfrac{a}{V^2}$（1 mol）について

(1) 膨張率 $\alpha_p = \dfrac{1}{V}\left(\dfrac{\partial V}{\partial T}\right)_p$ を求めよ。
(2) $\left(\dfrac{\partial U}{\partial V}\right)_T$ を求めよ。
(3) $C_V$ が $T$ のみの関数であることを示せ。
(4) $C_p - C_V$ を求めよ。

**解答**

(1) $p$ 一定で全微分：$0 = \dfrac{R}{V-b}dT - \left[\dfrac{RT}{(V-b)^2} - \dfrac{2a}{V^3}\right]dV$ より
$$\alpha_p = \frac{1}{V}\cdot\frac{R/(V-b)}{RT/(V-b)^2 - 2a/V^3} = \frac{R(V-b)V^2}{V\left[RTV^3 - 2a(V-b)^2\right]}$$

(2) 問0-2(1) の式に $\left(\dfrac{\partial p}{\partial T}\right)_V = \dfrac{R}{V-b}$ を入れる：
$$\left(\frac{\partial U}{\partial V}\right)_T = -\frac{RT}{V-b} + \frac{a}{V^2} + \frac{RT}{V-b} = \frac{a}{V^2}$$
理想気体（$a = 0$）ではゼロ。分子間引力 $a$ があると膨張で $U$ が増える。

(3) $\dfrac{\partial C_V}{\partial V} = \dfrac{\partial}{\partial V}\left(\dfrac{\partial U}{\partial T}\right)_V = \dfrac{\partial}{\partial T}\left(\dfrac{\partial U}{\partial V}\right)_T = \dfrac{\partial}{\partial T}\dfrac{a}{V^2} = 0$。よって $C_V = C_V(T)$。

(4) 一般式 $C_p - C_V = T\left(\dfrac{\partial p}{\partial T}\right)_V\left(\dfrac{\partial V}{\partial T}\right)_p = TV\alpha_p\dfrac{R}{V-b}$。(1) を代入して
$$C_p - C_V = \frac{R}{1 - \dfrac{2a(V-b)^2}{RTV^3}}$$
$a \to 0$ で $R$ に戻る。

### 問0-4 ★ ゴム糸の熱力学（都立2024冬 物理学II[2]）

張力 $X$ のゴム糸を長さ $L \to L + \Delta L$ 断熱的に伸ばすと $\Delta U = X\Delta L$。長さ一定での張力は $X = AT$（$A > 0$）。

(1) $F = U - TS$ の全微分が $dF = XdL - SdT$ となることを示せ。
(2) マクスウェル関係式 $\left(\dfrac{\partial S}{\partial L}\right)_T = -\left(\dfrac{\partial X}{\partial T}\right)_L$ を導け。
(3) $\left(\dfrac{\partial S}{\partial L}\right)_T < 0$ を示せ（等温で伸ばすとエントロピーが減る）。
(4) $\left(\dfrac{\partial U}{\partial L}\right)_T = 0$ を示せ。
(5) $\left(\dfrac{\partial T}{\partial L}\right)_S > 0$ を示せ（断熱で伸ばすと温度が上がる）。

**解答**

(1) $dU = TdS + XdL$（気体の $-pdV$ が $+XdL$ に対応。伸ばすと仕事をされる）。$dF = dU - TdS - SdT = XdL - SdT$。

(2) $dF$ の2階偏微分：$\dfrac{\partial^2 F}{\partial T\partial L} = \left(\dfrac{\partial X}{\partial T}\right)_L = -\left(\dfrac{\partial S}{\partial L}\right)_T$。

(3) $X = AT$ より $\left(\dfrac{\partial X}{\partial T}\right)_L = A > 0$。よって $\left(\dfrac{\partial S}{\partial L}\right)_T = -A < 0$。

(4) $U = F + TS$ より $\left(\dfrac{\partial U}{\partial L}\right)_T = \left(\dfrac{\partial F}{\partial L}\right)_T + T\left(\dfrac{\partial S}{\partial L}\right)_T = X - TA = AT - TA = 0$。

(5) $dS = \left(\dfrac{\partial S}{\partial T}\right)_L dT + \left(\dfrac{\partial S}{\partial L}\right)_T dL = 0$ より
$$\left(\frac{\partial T}{\partial L}\right)_S = -\frac{(\partial S/\partial L)_T}{(\partial S/\partial T)_L} = \frac{A}{C_L/T} = \frac{AT}{C_L} > 0$$
（$C_L = T(\partial S/\partial T)_L > 0$）。ゴムを急に伸ばすと熱くなる。

### 問0-5 ☆ エンタルピーとジュール・トムソン係数（上智2025秋 問6）

(1) $H = U + pV$ を定義し、$C_p = \left(\dfrac{\partial H}{\partial T}\right)_p$ を示せ。
(2) ジュール・トムソン係数 $\mu_{JT} = \left(\dfrac{\partial T}{\partial p}\right)_H$ を $C_p$、$V$、膨張率 $\alpha_p$ で表せ。
(3) 理想気体で $\mu_{JT} = 0$ を示せ。

**解答**

(1) $dH = TdS + Vdp$。$p$ 一定で $dH = TdS = dQ$。よって $C_p = (dQ/dT)_p = (\partial H/\partial T)_p$。

(2) $dH = 0$ で $dT/dp$ を求める。$dH = C_p dT + \left[T\left(\dfrac{\partial S}{\partial p}\right)_T + V\right]dp$。マクスウェル関係式（$dG = -SdT + Vdp$ から）$\left(\dfrac{\partial S}{\partial p}\right)_T = -\left(\dfrac{\partial V}{\partial T}\right)_p = -V\alpha_p$。よって
$$\mu_{JT} = \frac{TV\alpha_p - V}{C_p} = \frac{V}{C_p}(T\alpha_p - 1)$$

(3) 理想気体 $V = nRT/p$ で $\alpha_p = 1/T$。$T\alpha_p - 1 = 0$。

---

## 1｜ミクロカノニカル分布

### 要点

固定するもの：$E, V, N$。出発点：**状態数** $W(E, V, N)$。ポテンシャル：$S = k_B\ln W$。

$$\frac{1}{T} = \left(\frac{\partial S}{\partial E}\right)_{V,N}, \qquad \frac{p}{T} = \left(\frac{\partial S}{\partial V}\right)_{E,N}, \qquad \frac{\mu}{T} = -\left(\frac{\partial S}{\partial N}\right)_{E,V}$$

**スターリングの公式**：$\ln N! \simeq N\ln N - N$（$N \gg 1$）。必ず使う。

**場合の数の型**
- 区別できる $N$ 個から $n$ 個を選ぶ：$\binom{N}{n} = \dfrac{N!}{n!(N-n)!}$
- 区別できない $M$ 個を $N$ 個の箱に入れる（重複組合せ）：$\binom{M+N-1}{M} = \dfrac{(M+N-1)!}{M!(N-1)!}$

### 問1-1 ★ 2準位系のミクロカノニカルと負温度（都立2025冬 物理学II[2]）

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

### 問1-2 ★ 2つの壺（上智2026春 問6）

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

### 問1-3 ★ 調和振動子のミクロカノニカル（青学第2-2回・立教2016夏に類似）

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

## 2｜カノニカル分布

### 要点

固定するもの：$T, V, N$。出発点：**分配関数** $Z = \sum_{\text{状態}} e^{-\beta E}$。ポテンシャル：$F = -k_BT\ln Z$。

$$U = -\frac{\partial\ln Z}{\partial\beta}, \qquad S = -\left(\frac{\partial F}{\partial T}\right)_V, \qquad p = -\left(\frac{\partial F}{\partial V}\right)_T, \qquad C_V = \frac{\partial U}{\partial T}$$

**独立粒子系**：1粒子分配関数 $z$ に対して
- 区別できる（格子点に固定・スピンなど）：$Z = z^N$
- 区別できない（気体）：$Z = z^N/N!$

**便利な公式**
- $U = -\dfrac{\partial\ln Z}{\partial\beta} = k_BT^2\dfrac{\partial\ln Z}{\partial T}$
- $S = \dfrac{U - F}{T} = k_B\ln Z + \dfrac{U}{T}$
- 等比級数：$\sum_{n=0}^\infty x^n = \dfrac{1}{1-x}$、$\sum nx^n = \dfrac{x}{(1-x)^2}$（$|x| < 1$）

### 問2-1 ★ 量子調和振動子と黒体輻射（立教2010春 大問IV・2024春 大問4）

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

### 問2-2 ★ 古典調和振動子（立教2012春 大問4）

質量 $m$、振動数 $\nu$ の古典的1次元調和振動子が多数独立に存在し温度 $T$。$\int_{-\infty}^\infty e^{-ax^2}dx = \sqrt{\pi/a}$。

(1) 振動子1つのカノニカル分配関数 $Z_1(T)$ を求めよ（位相空間積分、$h$ で割る）。
(2) 単位体積あたり $\rho$ 個あるとき、ヘルムホルツ自由エネルギー密度 $f(T,\rho)$ を求めよ。
(3) 1振動子あたりの平均エネルギーと熱容量を求めよ。

**解答**

(1) $H = \dfrac{p^2}{2m} + \dfrac{1}{2}m\omega^2x^2$（$\omega = 2\pi\nu$）。
$$Z_1 = \frac{1}{h}\int dx\,dp\,e^{-\beta H} = \frac{1}{h}\sqrt{\frac{2\pi m}{\beta}}\sqrt{\frac{2\pi}{\beta m\omega^2}} = \frac{2\pi}{h\beta\omega} = \frac{k_BT}{h\nu}$$

(2) $f = -\rho k_BT\ln Z_1 = -\rho k_BT\ln\dfrac{k_BT}{h\nu}$（区別できる振動子なので $N!$ なし）。

(3) $\langle E\rangle = -\dfrac{\partial\ln Z_1}{\partial\beta} = \dfrac{1}{\beta} = k_BT$（等分配則：運動と位置で $k_BT/2$ ずつ）。$C = k_B$。

### 問2-3 ★ スピン $S$ の常磁性（立教2013春 大問4）

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

### 問2-4 ★ スピン1/2と断熱消磁（上智2026秋 問6・青学第2-5回）

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

### 問2-5 ★ 古典理想気体と化学ポテンシャル（立教2019夏 大問4）

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

## 3｜グランドカノニカル分布

### 要点

固定するもの：$T, V, \mu$。出発点：**大分配関数**
$$\Xi = \sum_{N=0}^\infty e^{\beta\mu N}Z_N = \sum_{\text{全状態}}e^{-\beta(E - \mu N)}$$
ポテンシャル：$\Omega = -k_BT\ln\Xi = F - \mu N = -pV$。
$$\langle N\rangle = -\left(\frac{\partial\Omega}{\partial\mu}\right)_{T,V} = k_BT\frac{\partial\ln\Xi}{\partial\mu}, \qquad S = -\left(\frac{\partial\Omega}{\partial T}\right)_{V,\mu}, \qquad p = -\frac{\Omega}{V}$$

**独立粒子系での分解**：1粒子状態 $r$（エネルギー $\epsilon_r$）ごとに独立なので
$$\Xi = \prod_r\xi_r, \qquad \xi_r = \sum_{n_r}e^{-\beta(\epsilon_r - \mu)n_r}$$
- フェルミ（$n_r = 0, 1$）：$\xi_r = 1 + e^{-\beta(\epsilon_r-\mu)}$
- ボース（$n_r = 0, 1, 2, \ldots$）：$\xi_r = \dfrac{1}{1 - e^{-\beta(\epsilon_r-\mu)}}$

**占有数** $\langle n_r\rangle = -\dfrac{\partial\ln\xi_r}{\partial(\beta\epsilon_r)} = \dfrac{1}{e^{\beta(\epsilon_r-\mu)} \pm 1}$（＋フェルミ、−ボース）

### 問3-1 ★ フェルミ分布・ボース分布の導出（立教2023春 大問4）

理想量子気体。分配関数 $Z(\beta, V, N) = \sum_{\{n_i\}}\exp(-\beta\sum_i n_i\epsilon_i)$、$\sum n_i = N$。

(1) 大分配関数 $\Xi(\beta, V, \mu) = \sum_N Z(\beta,V,N)e^{\beta\mu N}$ がフェルミ粒子で $\Xi = \prod_i[1 + e^{-\beta(\epsilon_i - \mu)}]$ となることを示せ。
(2) 1粒子状態 $i$ の粒子数の期待値 $\langle n_i\rangle$ を求め、十分低温での $\epsilon_i$ 依存性を図示せよ。
(3) 1粒子のエネルギーが $\epsilon = c|\boldsymbol p|$（光速 $c$）で与えられる相対論的粒子について、状態密度 $D(\epsilon)$ とフェルミエネルギー $\epsilon_F$ を求めよ（スピン縮退なし）。
(4) ボース粒子について $\Xi$ を求め、$\mu$ の上限を答えよ。$\langle n_i\rangle$ も求めよ。

**解答**

(1) $\sum_N e^{\beta\mu N}\sum_{\{n_i\},\sum n_i=N} = \sum_{\{n_i\}}$（$N$ の制約が外れる）。よって
$$\Xi = \sum_{\{n_i\}}\prod_i e^{-\beta(\epsilon_i-\mu)n_i} = \prod_i\sum_{n_i=0}^{1}e^{-\beta(\epsilon_i-\mu)n_i} = \prod_i\left[1 + e^{-\beta(\epsilon_i-\mu)}\right]$$

(2) $\langle n_i\rangle = \dfrac{1}{\Xi}\sum n_ie^{\cdots} = -\dfrac{1}{\beta}\dfrac{\partial\ln\Xi}{\partial\epsilon_i} = \dfrac{e^{-\beta(\epsilon_i-\mu)}}{1 + e^{-\beta(\epsilon_i-\mu)}} = \dfrac{1}{e^{\beta(\epsilon_i-\mu)} + 1}$。
低温：$\epsilon < \mu$ で 1、$\epsilon > \mu$ で 0 の階段。幅 $\sim k_BT$ でなまる。

(3) 状態数 $= \dfrac{V}{h^3}4\pi p^2dp$、$p = \epsilon/c$：$D(\epsilon) = \dfrac{4\pi V\epsilon^2}{h^3c^3}$。$T = 0$ で $N = \int_0^{\epsilon_F}D\,d\epsilon = \dfrac{4\pi V\epsilon_F^3}{3h^3c^3}$ より
$$\epsilon_F = hc\left(\frac{3n}{4\pi}\right)^{1/3}, \quad n = N/V$$

(4) $\xi_i = \sum_{n=0}^\infty e^{-\beta(\epsilon_i-\mu)n} = \dfrac{1}{1 - e^{-\beta(\epsilon_i-\mu)}}$。収束条件 $\epsilon_i - \mu > 0$ が全 $i$ で必要 → **$\mu < \epsilon_0$（最低準位）**。$\Xi = \prod_i[1 - e^{-\beta(\epsilon_i-\mu)}]^{-1}$、$\langle n_i\rangle = \dfrac{1}{e^{\beta(\epsilon_i-\mu)} - 1}$。

### 問3-2 ☆ 表面吸着（立教2019夏 大問4）

理想気体（問2-5）が吸着面に接する。吸着サイトが $M$ 個あり、各サイトは粒子0個か1個（吸着エネルギー $-\epsilon_0$）。気体と吸着面で $\mu$ が等しい。

(1) 吸着面の大分配関数 $\Xi_{\rm ads}$ を求めよ。
(2) 吸着粒子数 $N_{\rm ads}$ を $\mu$ で表せ。
(3) 気体の $\mu = k_BT\ln(n\lambda^3)$ を使い、被覆率 $\theta = N_{\rm ads}/M$ を気体の圧力 $p$ で表せ（ラングミュアの吸着等温式）。

**解答**

(1) 各サイトは独立な2状態：$\xi = 1 + e^{\beta(\epsilon_0 + \mu)}$、$\Xi_{\rm ads} = \xi^M$。

(2) $N_{\rm ads} = k_BT\dfrac{\partial\ln\Xi}{\partial\mu} = M\dfrac{e^{\beta(\epsilon_0+\mu)}}{1 + e^{\beta(\epsilon_0+\mu)}}$。

(3) $e^{\beta\mu} = n\lambda^3 = \dfrac{p\lambda^3}{k_BT}$（$p = nk_BT$）。$\theta = \dfrac{p\lambda^3e^{\beta\epsilon_0}/k_BT}{1 + p\lambda^3e^{\beta\epsilon_0}/k_BT} = \dfrac{p}{p + p_0(T)}$、$p_0 = \dfrac{k_BT}{\lambda^3}e^{-\beta\epsilon_0}$。

---

## 4｜量子理想気体（フェルミ気体・光子気体）

### 要点

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

### 問4-1 ★ 立方体中の粒子と状態密度（立教2014春・2015春 大問4）

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

### 問4-2 ★ 相対論的フェルミ気体（立教2022夏・2020夏 大問4）

1粒子エネルギー $\epsilon(p) = \sqrt{c^2p^2 + m^2c^4}$。スピン縮退なし。

(1) 状態密度 $D(\epsilon)$ を求めよ。
(2) 超相対論極限 $\epsilon \gg mc^2$ での $D(\epsilon)$ と、$T = 0$ でのフェルミエネルギー $\epsilon_F$。
(3) $\ln\Xi$ を $p$ の積分で表せ。

**解答**

(1) $D(\epsilon)d\epsilon = \dfrac{V}{(2\pi\hbar)^3}4\pi p^2dp$。$\epsilon d\epsilon = c^2p\,dp$ より $dp = \dfrac{\epsilon\,d\epsilon}{c^2p}$、$p = \dfrac{\sqrt{\epsilon^2 - m^2c^4}}{c}$：
$$D(\epsilon) = \frac{V}{2\pi^2\hbar^3c^3}\epsilon\sqrt{\epsilon^2 - m^2c^4}$$

(2) $\epsilon \gg mc^2$ で $D \simeq \dfrac{V\epsilon^2}{2\pi^2\hbar^3c^3}$。$N = \dfrac{V\epsilon_F^3}{6\pi^2\hbar^3c^3}$ より $\epsilon_F = \hbar c(6\pi^2n)^{1/3}$。

(3) $\ln\Xi = \sum_{\boldsymbol p}\ln[1 + e^{-\beta(\epsilon(p) - \mu)}] = \dfrac{V}{2\pi^2\hbar^3}\int_0^\infty p^2\ln\left[1 + e^{-\beta(\sqrt{c^2p^2+m^2c^4} - \mu)}\right]dp$。

### 問4-3 ★ フェルミ気体の感受率と揺らぎ（都立2026冬 物理学II[2]）

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

### 問4-4 ★ 光子気体の熱力学（青学第2-6回・立教2010春/2024春）

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

## 5｜揺らぎ・ギブス・デュエム・相互作用系

### 問5-1 ★ エネルギー揺らぎと熱容量

カノニカル分布で $\langle(\Delta E)^2\rangle = \langle E^2\rangle - \langle E\rangle^2 = k_BT^2C_V$ を示せ。

**解答**

$\langle E\rangle = -\dfrac{\partial\ln Z}{\partial\beta}$。$\dfrac{\partial\langle E\rangle}{\partial\beta} = -\dfrac{\partial^2\ln Z}{\partial\beta^2} = -\left[\dfrac{1}{Z}\dfrac{\partial^2Z}{\partial\beta^2} - \left(\dfrac{1}{Z}\dfrac{\partial Z}{\partial\beta}\right)^2\right] = -(\langle E^2\rangle - \langle E\rangle^2)$。
一方 $\dfrac{\partial\langle E\rangle}{\partial\beta} = \dfrac{\partial\langle E\rangle}{\partial T}\dfrac{dT}{d\beta} = -k_BT^2C_V$。よって $\langle(\Delta E)^2\rangle = k_BT^2C_V$。
相対揺らぎ $\sqrt{\langle(\Delta E)^2\rangle}/\langle E\rangle \propto 1/\sqrt N$。

### 問5-2 ★ ギブス・デュエムと圧縮率（都立2026冬 物理学II[2] 問2）

ギブス・デュエムの関係 $-SdT + Vdp - Nd\mu = 0$ を用いて
$$\left(\frac{\partial\mu}{\partial N}\right)_{T,V} = \frac{V}{N^2}\frac{1}{\kappa}, \qquad \kappa = -\frac{1}{V}\left(\frac{\partial V}{\partial p}\right)_{T,N}$$
を示せ。$p$ の $N, V$ 依存性は密度 $n = N/V$ を通してのみ。

**解答**

$T$ 一定：$Vdp = Nd\mu$ → $\left(\dfrac{\partial\mu}{\partial p}\right)_T = \dfrac{V}{N} = \dfrac{1}{n}$。
$p = p(n)$ なので $\left(\dfrac{\partial p}{\partial N}\right)_{T,V} = \dfrac{dp}{dn}\cdot\dfrac{1}{V}$。
圧縮率：$V = N/n$ より $\left(\dfrac{\partial V}{\partial p}\right)_{T,N} = -\dfrac{N}{n^2}\dfrac{dn}{dp}$、$\kappa = \dfrac{N}{Vn^2}\dfrac{dn}{dp} = \dfrac{1}{n}\dfrac{dn}{dp}$。よって $\dfrac{dp}{dn} = \dfrac{1}{n\kappa}$。
$$\left(\frac{\partial\mu}{\partial N}\right)_{T,V} = \left(\frac{\partial\mu}{\partial p}\right)_T\left(\frac{\partial p}{\partial N}\right)_{T,V} = \frac{1}{n}\cdot\frac{1}{V}\cdot\frac{1}{n\kappa} = \frac{1}{Nn\kappa} = \frac{V}{N^2\kappa}$$

### 問5-3 ☆ イジング模型の平均場近似（立教2018夏 大問4）

$i$ 番目のスピン（$\sigma_i = \pm1$）のハミルトニアン $\hat H_i = -Jz\langle\sigma\rangle\sigma_i - \mu H\sigma_i$。$z$ は隣接数、$\langle\sigma\rangle$ は自己無撞着に決める平均場。

(1) 1スピンの分配関数と $\langle\sigma\rangle$ の自己無撞着方程式を書け。
(2) $H = 0$ で $\langle\sigma\rangle \ne 0$ の解が存在する温度 $T_c$ を求めよ。
(3) $T > T_c$、$H \to 0$ での磁化率 $\chi = \partial\langle\sigma\rangle/\partial H$ を求めよ（キュリー・ワイス）。

**解答**

(1) 有効磁場 $h = Jz\langle\sigma\rangle + \mu H$。$z_1 = 2\cosh(\beta h)$、$\langle\sigma\rangle = \tanh\left[\beta(Jz\langle\sigma\rangle + \mu H)\right]$。

(2) $H = 0$：$m = \tanh(\beta Jzm)$。$m \ne 0$ の解は $\tanh$ の原点での傾き $\beta Jz > 1$ のとき存在。$T_c = Jz/k_B$。

(3) $m$ 小で $\tanh x \simeq x$：$m \simeq \beta(Jzm + \mu H)$ → $m(1 - \beta Jz) = \beta\mu H$ → $\chi = \dfrac{\mu}{k_B(T - T_c)}$。$T_c$ で発散。

### 問5-4 ☆ 1次元リング格子と転送行列（立教2025春 大問4）

$L$ 個の格子点が環状。区別できない粒子、各格子に高々1個、隣接不可。$N$ 個の配置数を $Z_{L,N}$、$\Xi_L(x) = \sum_N Z_{L,N}x^N$。

(1) $Z_{4,2}$ を求めよ。
(2) $\Xi_4(x)$ を求めよ。
(3) $L \ge 3$ で $Z_{L,2}$ を $L$ で表せ。
(4) $t_{n,n'} = x^{(n+n')/2}(1 - nn')$ を成分とする転送行列 $T$ で $\Xi_L = \mathrm{Tr}\,T^L$ と書けることを用い、$\Xi_L$ を $x, L$ で表せ。
(5) $F(x) = \lim_{L\to\infty}\dfrac{1}{L}\ln\Xi_L$ の $F(1)$ を求めよ。

**解答**

(1) 4点の環で隣接しない2点：$\{1,3\}, \{2,4\}$ の2通り。$Z_{4,2} = 2$。

(2) $Z_{4,0} = 1$、$Z_{4,1} = 4$、$Z_{4,2} = 2$、$Z_{4,3} = Z_{4,4} = 0$。$\Xi_4 = 1 + 4x + 2x^2$。

(3) 全ペア $\binom L2$ から隣接ペア $L$ 個を引く：$Z_{L,2} = \dfrac{L(L-1)}{2} - L = \dfrac{L(L-3)}{2}$。

(4) $T = \begin{pmatrix}1 & \sqrt x\\ \sqrt x & 0\end{pmatrix}$（$n, n' \in \{0, 1\}$）。固有値 $\lambda_\pm = \dfrac{1 \pm\sqrt{1+4x}}{2}$。$\Xi_L = \lambda_+^L + \lambda_-^L$。
検算：$L = 4$ で $\lambda_+^4 + \lambda_-^4 = (\lambda_+^2+\lambda_-^2)^2 - 2(\lambda_+\lambda_-)^2$、$\lambda_+ + \lambda_- = 1$、$\lambda_+\lambda_- = -x$ より $\lambda_+^2 + \lambda_-^2 = 1 + 2x$、$\Xi_4 = (1+2x)^2 - 2x^2 = 1 + 4x + 2x^2$ ✓

(5) $|\lambda_+| > |\lambda_-|$ なので $\Xi_L \simeq \lambda_+^L$、$F(x) = \ln\lambda_+(x)$。$F(1) = \ln\dfrac{1+\sqrt5}{2} \simeq 0.481$（黄金比の対数）。

---

## 付録｜型と過去問の対応表

| 問 | 型 | 元の過去問 | 必修 |
| --- | --- | --- | --- |
| 0-1 | 理想気体のS・等温断熱 | 青学本番 | ★ |
| 0-2 | $(\partial U/\partial V)_T$ 一般式 | 立教2020春・2011春 | ★ |
| 0-3 | ファンデルワールス | 立教2011春 | ★ |
| 0-4 | ゴム糸 | 都立2024冬 | ★ |
| 0-5 | ジュール・トムソン | 上智2025秋 | ☆ |
| 1-1 | 2準位・負温度 | 都立2025冬 | ★ |
| 1-2 | 2つの壺 | 上智2026春 | ★ |
| 1-3 | 調和振動子ミクロカノニカル | 青学2-2・立教2016夏 | ★ |
| 2-1 | 調和振動子Z→黒体 | 立教2010春・2024春 | ★ |
| 2-2 | 古典調和振動子 | 立教2012春 | ★ |
| 2-3 | スピンS常磁性 | 立教2013春 | ★ |
| 2-4 | スピン1/2・断熱消磁 | 上智2026秋・青学2-5 | ★ |
| 2-5 | 古典理想気体・μ | 立教2019夏 | ★ |
| 3-1 | フェルミ/ボース分布の導出 | 立教2023春 | ★ |
| 3-2 | 吸着 | 立教2019夏 | ☆ |
| 4-1 | 箱の中の粒子・D(ε)・εF | 立教2014春・2015春 | ★ |
| 4-2 | 相対論的フェルミ気体 | 立教2022夏・2020夏 | ★ |
| 4-3 | 感受率・揺らぎ | 都立2026冬 | ★ |
| 4-4 | 光子気体 F=−U/3 | 青学2-6・立教2024春 | ★ |
| 5-1 | エネルギー揺らぎ | 一般 | ★ |
| 5-2 | ギブス・デュエム・圧縮率 | 都立2026冬 | ★ |
| 5-3 | イジング平均場 | 立教2018夏 | ☆ |
| 5-4 | 転送行列 | 立教2025春 | ☆ |
