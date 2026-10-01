#### 【A】数学 §3 確率分布・期待値・分散（上智2026春 問2(4)／立教 大問6 の誤差論と接続）


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


#### 【B】数学 §4 ガウス積分とパラメータ微分（上智2025春 問2／統計で頻用）


#### ① 板書

**基本**：$\displaystyle\int_{-\infty}^\infty e^{-\alpha x^2}dx = \sqrt{\frac{\pi}{\alpha}}$（$\alpha > 0$）

**パラメータ微分で高次モーメント**：両辺を $\alpha$ で微分
$$\int x^2e^{-\alpha x^2}dx = -\frac{d}{d\alpha}\sqrt{\frac{\pi}{\alpha}} = \frac{\sqrt\pi}{2}\alpha^{-3/2}, \qquad \int x^4e^{-\alpha x^2}dx = \frac{3\sqrt\pi}{4}\alpha^{-5/2}$$
一般に $\displaystyle\int x^{2n}e^{-\alpha x^2}dx = \frac{(2n-1)!!}{2^n}\sqrt\pi\,\alpha^{-(2n+1)/2}$。奇数次はゼロ。

**平行移動**：$\displaystyle\int e^{-\alpha(x - c)^2}dx = \sqrt{\pi/\alpha}$（実数 $c$）。**複素数 $c = ib$ でも同じ**（積分路を虚軸方向にずらしても値が変わらない：被積分関数が正則で、無限遠で消えるため）。

**片側**：$\displaystyle\int_0^\infty e^{-\alpha x^2}dx = \frac12\sqrt{\pi/\alpha}$、$\displaystyle\int_0^\infty xe^{-\alpha x^2}dx = \frac{1}{2\alpha}$、$\displaystyle\int_0^\infty x^ne^{-\alpha x}dx = \frac{n!}{\alpha^{n+1}}$。

**誤差関数**：$\mathrm{erf}(x) = \dfrac{2}{\sqrt\pi}\int_0^xe^{-t^2}dt$。$\mathrm{erf}(\pm\infty) = \pm1$、奇関数、$\mathrm{erf}(0) = 0$。

**統計力学での使い道**：マクスウェル分布の $\langle v^2\rangle$、古典調和振動子の分配関数、変分法の期待値。

#### ② 過去問（上智 2025年春 問2）

$f(x, \alpha) = \exp(-\alpha x^2)$、$\alpha > 0$。
1. $\displaystyle\int_{-\infty}^\infty f(x, \alpha)dx$。
2. 小問1を $\alpha$ で微分することにより $\displaystyle\int_{-\infty}^\infty x^nf(x, \alpha)dx$ を $n = 2, 4$ で求めよ。
3. $b$ を実数として $\displaystyle\int_{-\infty}^\infty f(x + ib, \alpha)dx$ が小問1と同じになることを、複素平面上の長方形の積分経路 $C$（実軸 $-\infty \to +\infty$、$x = +\infty$ で虚軸方向に $ib$、$\mathrm{Im} = b$ の線を $+\infty \to -\infty$、$x = -\infty$ で戻る）を考えることで示せ。
4. $F(x) = \dfrac{2}{\sqrt\pi}\displaystyle\int_0^xf(x', 1)dx'$ の概形を $-4 < x < 4$ で図示せよ。

#### ③ 解説

**1.** $\sqrt{\pi/\alpha}$。（証明：$I^2 = \iint e^{-\alpha(x^2+y^2)}dxdy = \int_0^{2\pi}\int_0^\infty e^{-\alpha r^2}rdrd\theta = \pi/\alpha$）

**2.** $\dfrac{d}{d\alpha}\int e^{-\alpha x^2}dx = -\int x^2e^{-\alpha x^2}dx$。左辺 $= \dfrac{d}{d\alpha}\sqrt\pi\alpha^{-1/2} = -\dfrac{\sqrt\pi}{2}\alpha^{-3/2}$。よって $\int x^2e^{-\alpha x^2}dx = \dfrac{\sqrt\pi}{2}\alpha^{-3/2}$。
もう一度微分：$\int x^4e^{-\alpha x^2}dx = \dfrac{3\sqrt\pi}{4}\alpha^{-5/2}$。

**3.** $g(z) = e^{-\alpha z^2}$ は全平面で正則。コーシーの定理で $\oint_Cg\,dz = 0$。
- 実軸：$\int_{-R}^Re^{-\alpha x^2}dx$
- 右の縦線 $z = R + iy$（$y: 0 \to b$）：$|e^{-\alpha(R+iy)^2}| = e^{-\alpha(R^2 - y^2)} \to 0$（$R \to \infty$）
- 上の線 $z = x + ib$（$x: R \to -R$）：$-\int_{-R}^Re^{-\alpha(x+ib)^2}dx$
- 左の縦線：同様に $\to 0$
よって $\int_{-\infty}^\infty e^{-\alpha x^2}dx - \int_{-\infty}^\infty e^{-\alpha(x+ib)^2}dx = 0$。

**4.** $F(x) = \mathrm{erf}(x)$。$F(0) = 0$、奇関数、$x \to \pm\infty$ で $\pm1$、$x = \pm2$ で $\pm0.995$ なのでほぼ飽和。原点で傾き $2/\sqrt\pi \simeq 1.13$。S字カーブ。

#### ④ 確認問題

**確認4-A**：$\displaystyle\int_{-\infty}^\infty x^2e^{-\alpha x^2 + \beta x}dx$ を求めよ（平方完成してから）。

**確認4-B**（マクスウェル分布）：3次元理想気体の速度分布 $f(\boldsymbol v) \propto e^{-mv^2/2k_BT}$。(i) 規格化定数。(ii) $\langle v_x^2\rangle$、$\langle v^2\rangle$。(iii) 等分配則 $\frac12m\langle v^2\rangle = \frac32k_BT$ を確かめよ。

**略解**
4-A：$-\alpha x^2 + \beta x = -\alpha(x - \frac{\beta}{2\alpha})^2 + \frac{\beta^2}{4\alpha}$。$u = x - \beta/2\alpha$ で $\int(u + \frac{\beta}{2\alpha})^2e^{-\alpha u^2}du\cdot e^{\beta^2/4\alpha} = \sqrt{\frac{\pi}{\alpha}}e^{\beta^2/4\alpha}\left(\frac{1}{2\alpha} + \frac{\beta^2}{4\alpha^2}\right)$。
4-B：(i) $\left(\frac{m}{2\pi k_BT}\right)^{3/2}$。(ii) $\langle v_x^2\rangle = k_BT/m$、$\langle v^2\rangle = 3k_BT/m$。
