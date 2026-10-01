数学 §3 確率分布・期待値・分散（上智2026春 問2(4)／立教 大問6 の誤差論と接続）


#### ① 板書

**連続確率変数**
- 分布関数 $F(x) = P(X \le x)$、確率密度 $f(x) = F'(x)$、$\int_{-\infty}^\infty f\,dx = 1$
- 期待値 $E[X] = \int xf(x)dx$、分散 $V[X] = E[X^2] - (E[X])^2$、標準偏差 $\sigma = \sqrt V$

**代表的分布**

| 分布 | $f(x)$ | $E$ | $V$ |
| --- | --- | --- | --- |
| 指数 | $\lambda e^{-\lambda x}$（$x \ge 0$） | $1/\lambda$ | $1/\lambda^2$ |
| 正規 | $\dfrac{1}{\sqrt{2\pi}\sigma}e^{-(x-\mu)^2/2\sigma^2}$ | $\mu$ | $\sigma^2$ |
| ポアソン（離散） | $\dfrac{\lambda^ke^{-\lambda}}{k!}$ | $\lambda$ | $\lambda$ |

**ポアソンと $\sqrt N$**：計数 $N$ の統計誤差は $\sqrt N$。相対誤差 $1/\sqrt N$。立教大問6の計数統計はこれ。

**誤差伝播**：$Z = f(A, B)$、独立な誤差 $\Delta A, \Delta B$ に対し $(\Delta Z)^2 = \left(\dfrac{\partial f}{\partial A}\right)^2(\Delta A)^2 + \left(\dfrac{\partial f}{\partial B}\right)^2(\Delta B)^2$。積や商なら相対誤差の2乗和。

#### ② 過去問（上智 2026年春 問2(4)）

確率変数 $x$ の分布関数を $F(x) = 1 - e^{-\lambda x}$（$x \ge 0$）、$F(x) = 0$（$x < 0$）とする（$\lambda > 0$）。
① 確率密度関数 $f(x)$。② 期待値 $E(x)$ と分散 $V(x)$。

#### ③ 解説

① $f(x) = F'(x) = \lambda e^{-\lambda x}$（$x \ge 0$）、$0$（$x < 0$）。$\int_0^\infty\lambda e^{-\lambda x}dx = 1$ ✓

② $E = \int_0^\infty x\lambda e^{-\lambda x}dx$。部分積分（または $\int_0^\infty x^ne^{-\lambda x}dx = n!/\lambda^{n+1}$）：$E = \dfrac{1}{\lambda}$。
$E[x^2] = \dfrac{2}{\lambda^2}$。$V = \dfrac{2}{\lambda^2} - \dfrac{1}{\lambda^2} = \dfrac{1}{\lambda^2}$。

#### ④ 確認問題

**確認3-A**（立教2022春 大問5 の型）：$A, B, C$ が独立な測定量で誤差 $\Delta A, \Delta B, \Delta C$。$p, q, r$ は定数。$Z$ の相対誤差 $\Delta Z/Z$ を求めよ。(i) $Z = \dfrac{pA^2B}{qC^3}$、(ii) $Z = e^{rA}$、(iii) $Z = A\ln B$。

**確認3-B**（立教2018春 大問6）：同じ測定を9回行った値：10.2, 9.7, 10.6, 9.4, 9.6, 10.5, 10.4, 9.3, 10.3。正規分布に従うとして最良推定値と推定誤差。

**確認3-C**（立教2022春）：計数管で1秒間に144個。計数率を1%以下の相対精度で測るには何秒必要か。

**略解**
3-A：(i) $\sqrt{4\left(\frac{\Delta A}{A}\right)^2 + \left(\frac{\Delta B}{B}\right)^2 + 9\left(\frac{\Delta C}{C}\right)^2}$。(ii) $r\Delta A$。(iii) $\sqrt{\left(\frac{\Delta A}{A}\right)^2 + \left(\frac{\Delta B}{B\ln B}\right)^2}$。
3-B：平均 $\bar x = 10.0$、標本標準偏差 $s \simeq 0.49$、推定誤差 $s/\sqrt9 \simeq 0.16$。$10.0 \pm 0.2$。
3-C：$1/\sqrt N \le 0.01$ → $N \ge 10^4$ → $10^4/144 \simeq 70$ 秒。

---


