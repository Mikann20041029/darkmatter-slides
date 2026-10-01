#### ① 板書

**中心力場のシュレディンガー方程式（畑本Ch.6の前提）**
$$\left\{-\frac{\hbar^2}{2m}\Delta + V(|\mathbb{x}|)\right\}u(\mathbb{x}) = Eu(\mathbb{x})$$
極座標 $(r,\theta,\phi)$ で $\Delta = \dfrac1{r^2}\dfrac{\partial}{\partial r}\left(r^2\dfrac{\partial}{\partial r}\right) + \dfrac1{r^2\sin\theta}\dfrac{\partial}{\partial\theta}\left(\sin\theta\dfrac{\partial}{\partial\theta}\right) + \dfrac1{r^2\sin^2\theta}\dfrac{\partial^2}{\partial\phi^2}$。

$u(r,\theta,\phi) = R(r)Y(\theta,\phi)$ と変数分離すると、角度部分だけが閉じた方程式になる（動径部分は畑本Ch.6の遠心力項 $\hbar^2l(l+1)/2mr^2$ として現れる）：
$$\frac1{\sin\theta}\frac{\partial}{\partial\theta}\left(\sin\theta\frac{\partial Y}{\partial\theta}\right) + \frac1{\sin^2\theta}\frac{\partial^2 Y}{\partial\phi^2} = -l(l+1)Y$$

さらに $Y(\theta,\phi) = \Theta(\theta)\Phi(\phi)$ と分離すると、$\Phi$ の方程式は $\Phi'' = -m^2\Phi$（周期性 $\Phi(\phi+2\pi)=\Phi(\phi)$ から $m$ は整数）、$\Theta$ の方程式がルジャンドルの陪微分方程式になる。

**球面調和関数の一般式**
$$Y_{lm}(\theta,\phi) = (-1)^{(m+|m|)/2}\sqrt{\frac{(2l+1)(l-|m|)!}{4\pi(l+|m|)!}}P_l^{|m|}(\cos\theta)\exp(im\phi)$$

**$l=1$ の具体形**（畑本Ch.5 問題59〜61の型）
$$Y_{1,0} = \sqrt{\frac{3}{4\pi}}\cos\theta, \qquad Y_{1,\pm1} = \mp\sqrt{\frac{3}{8\pi}}\sin\theta\, e^{\pm i\phi}$$

**空間反転（パリティ）**：$\mathbb{x}\to-\mathbb{x}$ は極座標で $r\to r$、$\theta\to\pi-\theta$、$\phi\to\phi+\pi$。
- $\cos\theta \to \cos(\pi-\theta) = -\cos\theta$
- $e^{im\phi} \to e^{im(\phi+\pi)} = (-1)^m e^{im\phi}$
- ルジャンドル陪関数の偶奇性 $P_l^{|m|}(-x) = (-1)^{l+|m|}P_l^{|m|}(x)$

を合わせると $Y_{lm}(\pi-\theta,\phi+\pi) = (-1)^{l+|m|}\cdot(-1)^{|m|}Y_{lm}(\theta,\phi) = (-1)^l Y_{lm}(\theta,\phi)$。**パリティは $l$ だけで決まり、$m$ には依らない**（$(-1)^{2|m|}=1$ だから）。

#### ② 過去問（立教 2012年春 大問3）

3次元回転対称性を持ったポテンシャル $V(|\mathbb{x}|)$ 中の、質量 $m$ を持った粒子の量子力学的問題を考える。

(a) $\mathbb{x}$ を極座標 $(r,\theta,\phi)$ で表す。波動関数 $u(r,\theta,\phi) = R(r)Y(\theta,\phi)$ と分離するとき、球面調和関数 $Y(\theta,\phi)$ が満たす方程式を求めよ。
(b) $Y(\theta,\phi) = \Theta(\theta)\Phi(\phi)$ と分離できる。$\Theta(\theta)$ と $\Phi(\phi)$ が満たす方程式を求めよ。
(c) 球面調和関数の解は上の一般式で与えられる（$l=0,1,2,\ldots$、$m=0,\pm1,\ldots,\pm l$）。$l=1$ の場合の球面調和関数を求めよ。
(d) 球面調和関数 $Y_{lm}(\theta,\phi)$ を空間反転 $(\mathbb{x}\to-\mathbb{x})$ したとき、$A\times Y_{lm}(\theta,\phi)$ と表せる。この $A$ の値を求めよ。

#### ③ 解説

(a) 上の板書のとおり、動径部分と角度部分に分離すると角度部分だけの方程式が残る（$l(l+1)$ は分離定数として後から角運動量の固有値だと分かる）。
(b) $Y=\Theta\Phi$ を代入し $\sin^2\theta$ を掛けて整理すると、$\phi$ だけの項と $\theta$ だけの項に分かれる。$\phi$ 側 $=-m^2$（分離定数）とおくと $\Phi'' = -m^2\Phi$。$\theta$ 側はルジャンドルの陪微分方程式。
(c) 板書の $Y_{1,0}, Y_{1,\pm1}$ のとおり。
(d) 板書のパリティ計算のとおり $A = (-1)^l$。**この設問は「$m$ に依らず $l$ だけで決まる」ことに気づくのが核心**（青学本番でも似た"パリティは何で決まるか"を問う型が出た）。

#### ④ 確認問題

**確認23-A**：$l=0$ の球面調和関数 $Y_{0,0}$ を求め、パリティが $+1$ であることを直接確認せよ。

**確認23-B**：$l=2, m=0$ の球面調和関数は $Y_{2,0} = \sqrt{\dfrac{5}{16\pi}}(3\cos^2\theta-1)$ である。パリティが $(-1)^2=+1$ であることを直接確認せよ。

**確認23-C**（畑本Ch.6への橋渡し）：中心力場のシュレディンガー方程式に $u=R(r)Y_{lm}(\theta,\phi)$ を代入し、両辺を $Y_{lm}$ で割ることで、動径方向の方程式に遠心力項 $\hbar^2l(l+1)/(2mr^2)$ が現れることを示せ。

**略解**
23-A：$Y_{0,0} = 1/\sqrt{4\pi}$（定数）。$\theta\to\pi-\theta,\phi\to\phi+\pi$ としても値は変わらない → パリティ $+1 = (-1)^0$ と一致。
23-B：$\cos(\pi-\theta) = -\cos\theta$ なので $\cos^2\theta$ は不変 → $Y_{2,0}$ も不変 → パリティ $+1 = (-1)^2$ と一致。
23-C：$-\dfrac{\hbar^2}{2m}\dfrac1{r^2}\dfrac{d}{dr}\left(r^2\dfrac{dR}{dr}\right)Y - \dfrac{\hbar^2}{2mr^2}\left[l(l+1)\right]RY + V(r)RY = ERY$。$Y$ で割ると $-\dfrac{\hbar^2}{2m}\dfrac1{r^2}\dfrac{d}{dr}\left(r^2\dfrac{dR}{dr}\right) + \left[V(r)+\dfrac{\hbar^2l(l+1)}{2mr^2}\right]R = ER$ で、これが畑本Ch.6の動径方程式そのもの。
