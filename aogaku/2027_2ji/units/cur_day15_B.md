数学 §4 ガウス積分とパラメータ微分（上智2025春 問2／統計で頻用）


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
