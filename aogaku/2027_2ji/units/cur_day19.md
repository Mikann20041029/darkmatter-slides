#### ① 板書

**3つの演算**（直交座標）
- 勾配 $\nabla f = \left(\dfrac{\partial f}{\partial x}, \dfrac{\partial f}{\partial y}, \dfrac{\partial f}{\partial z}\right)$
- 発散 $\nabla\cdot\boldsymbol A = \dfrac{\partial A_x}{\partial x} + \dfrac{\partial A_y}{\partial y} + \dfrac{\partial A_z}{\partial z}$
- 回転 $\nabla\times\boldsymbol A = \left(\dfrac{\partial A_z}{\partial y} - \dfrac{\partial A_y}{\partial z},\ \dfrac{\partial A_x}{\partial z} - \dfrac{\partial A_z}{\partial x},\ \dfrac{\partial A_y}{\partial x} - \dfrac{\partial A_x}{\partial y}\right)$

**恒等式**（覚える）
- $\nabla\times(\nabla f) = 0$（勾配の回転はゼロ）→ 静電場 $\boldsymbol E = -\nabla\phi$ は $\nabla\times\boldsymbol E = 0$
- $\nabla\cdot(\nabla\times\boldsymbol A) = 0$（回転の発散はゼロ）→ $\boldsymbol B = \nabla\times\boldsymbol A$ は $\nabla\cdot\boldsymbol B = 0$
- $\nabla\times(\nabla\times\boldsymbol A) = \nabla(\nabla\cdot\boldsymbol A) - \nabla^2\boldsymbol A$（電磁波の波動方程式導出で使う）

**$r$ の関数**（$r = \sqrt{x^2+y^2+z^2}$、$\boldsymbol r = (x, y, z)$）
- $\nabla r = \dfrac{\boldsymbol r}{r} = \hat{\boldsymbol r}$、$\nabla f(r) = f'(r)\hat{\boldsymbol r}$
- $\nabla\cdot\boldsymbol r = 3$
- $\nabla\cdot(f(r)\boldsymbol r) = 3f + rf'$。特に $\nabla\cdot\dfrac{\boldsymbol r}{r^n} = \dfrac{3 - n}{r^n}$。$n = 3$（点電荷の $\boldsymbol E$）でゼロ（$r \ne 0$）
- $\nabla^2f(r) = f'' + \dfrac{2}{r}f'$

**積分定理**
- ガウス：$\int_V\nabla\cdot\boldsymbol A\,dV = \oint_S\boldsymbol A\cdot d\boldsymbol S$
- ストークス：$\int_S(\nabla\times\boldsymbol A)\cdot d\boldsymbol S = \oint_C\boldsymbol A\cdot d\boldsymbol l$

#### ② 過去問

**(A) 都立 2026年夏 物理学I[2] 問2**：3次元空間の位置ベクトル $\boldsymbol r$、$|\boldsymbol r| = r \ne 0$。
2-1) $\nabla\cdot\left(\dfrac{\boldsymbol r}{r^n}\right)$ を求めよ。
2-2) 原点の点電荷 $q$ が $\boldsymbol r$ に作る電場 $\boldsymbol E$ とその発散 $\nabla\cdot\boldsymbol E$。
2-3) $\boldsymbol E = -\nabla\phi$ であるとき $\nabla\times\boldsymbol E$。

**(B) 都立 2025年冬 数学 問2**：$f(r) = \log r$（$r > 0$）。
2-1) $\nabla f$ を $\boldsymbol r, r$ で表せ。2-2) $\Delta f$。

**(C) 上智 2025年秋 問4**：$\boldsymbol A = (2xyz, x^2z, x^2y)$。$\nabla\cdot\boldsymbol A$ と $\nabla\times\boldsymbol A$。

#### ③ 解説

**(A)**
2-1) $\dfrac{\partial}{\partial x}\left(\dfrac{x}{r^n}\right) = \dfrac{1}{r^n} - \dfrac{nx}{r^{n+1}}\cdot\dfrac{x}{r} = \dfrac{1}{r^n} - \dfrac{nx^2}{r^{n+2}}$。3成分足して $\dfrac{3}{r^n} - \dfrac{n(x^2+y^2+z^2)}{r^{n+2}} = \dfrac{3 - n}{r^n}$。
2-2) $\boldsymbol E = \dfrac{q}{4\pi\varepsilon_0}\dfrac{\boldsymbol r}{r^3}$。$n = 3$ で $\nabla\cdot\boldsymbol E = 0$（$r \ne 0$）。原点にだけ電荷がある（デルタ関数）。
2-3) $\nabla\times(\nabla\phi) = 0$ より $\nabla\times\boldsymbol E = 0$。

**(B)**
2-1) $\nabla\log r = \dfrac{1}{r}\nabla r = \dfrac{\boldsymbol r}{r^2}$。
2-2) $\Delta\log r = \nabla\cdot\dfrac{\boldsymbol r}{r^2} = \dfrac{3-2}{r^2} = \dfrac{1}{r^2}$。（2次元なら $\Delta\log r = 0$ になる。3次元では違う）

**(C)**
$\nabla\cdot\boldsymbol A = 2yz + 0 + 0 = 2yz$。
$\nabla\times\boldsymbol A = \left(\dfrac{\partial(x^2y)}{\partial y} - \dfrac{\partial(x^2z)}{\partial z},\ \dfrac{\partial(2xyz)}{\partial z} - \dfrac{\partial(x^2y)}{\partial x},\ \dfrac{\partial(x^2z)}{\partial x} - \dfrac{\partial(2xyz)}{\partial y}\right) = (x^2 - x^2,\ 2xy - 2xy,\ 2xz - 2xz) = \boldsymbol 0$。
回転がゼロなので $\boldsymbol A = \nabla f$ と書ける：$f = x^2yz$ で確認。

#### ④ 確認問題

**確認4-A**：$\boldsymbol A = \boldsymbol\omega\times\boldsymbol r$（$\boldsymbol\omega$ 定ベクトル）。$\nabla\cdot\boldsymbol A$ と $\nabla\times\boldsymbol A$。

**確認4-B**：$\nabla\times(\nabla\times\boldsymbol E) = \nabla(\nabla\cdot\boldsymbol E) - \nabla^2\boldsymbol E$ を用い、真空中のマクスウェル方程式から $\nabla^2\boldsymbol E = \mu_0\varepsilon_0\dfrac{\partial^2\boldsymbol E}{\partial t^2}$ を導け（青学本番の電磁気 問3-1・第2-6回の正道）。

**略解**
4-A：$\nabla\cdot\boldsymbol A = 0$、$\nabla\times\boldsymbol A = 2\boldsymbol\omega$。
4-B：$\nabla\times\boldsymbol E = -\partial\boldsymbol B/\partial t$ の両辺に $\nabla\times$：左辺 $= \nabla(\nabla\cdot\boldsymbol E) - \nabla^2\boldsymbol E = -\nabla^2\boldsymbol E$（$\nabla\cdot\boldsymbol E = 0$）。右辺 $= -\dfrac{\partial}{\partial t}\nabla\times\boldsymbol B = -\mu_0\varepsilon_0\dfrac{\partial^2\boldsymbol E}{\partial t^2}$。
