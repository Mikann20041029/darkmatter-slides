電磁気 §5 マクスウェル方程式から波動方程式へ（立教2022春・2024春／青学本番 問3-1）


#### ① 板書

**真空中のマクスウェル方程式**（$\rho = 0$、$\boldsymbol J = 0$）
$$\nabla\cdot\boldsymbol E = 0, \quad \nabla\cdot\boldsymbol B = 0, \quad \nabla\times\boldsymbol E = -\frac{\partial\boldsymbol B}{\partial t}, \quad \nabla\times\boldsymbol B = \mu_0\varepsilon_0\frac{\partial\boldsymbol E}{\partial t}$$

**波動方程式の導出（正道・3行）**
1. $\nabla\times\boldsymbol E = -\partial_t\boldsymbol B$ の両辺に $\nabla\times$ をかける
2. 左辺：恒等式 $\nabla\times(\nabla\times\boldsymbol E) = \nabla(\nabla\cdot\boldsymbol E) - \nabla^2\boldsymbol E = -\nabla^2\boldsymbol E$（$\nabla\cdot\boldsymbol E = 0$）
3. 右辺：$-\partial_t(\nabla\times\boldsymbol B) = -\mu_0\varepsilon_0\partial_t^2\boldsymbol E$
$$\nabla^2\boldsymbol E = \mu_0\varepsilon_0\frac{\partial^2\boldsymbol E}{\partial t^2}, \qquad c = \frac{1}{\sqrt{\mu_0\varepsilon_0}}$$

**平面波** $\boldsymbol E = \boldsymbol E_0\cos(\boldsymbol k\cdot\boldsymbol r - \omega t)$ をマクスウェル方程式に入れると
- $\nabla\cdot\boldsymbol E = 0$ → $\boldsymbol k\cdot\boldsymbol E_0 = 0$（横波）
- $\nabla\times\boldsymbol E = -\partial_t\boldsymbol B$ → $\boldsymbol k\times\boldsymbol E_0 = \omega\boldsymbol B_0$
- $\nabla\times\boldsymbol B = \mu_0\varepsilon_0\partial_t\boldsymbol E$ → $\boldsymbol k\times\boldsymbol B_0 = -\mu_0\varepsilon_0\omega\boldsymbol E_0$
- 3つを合わせて $\omega = ck$、$B_0 = E_0/c$、$\boldsymbol E_0\perp\boldsymbol B_0\perp\boldsymbol k$（右手系 $\boldsymbol E\times\boldsymbol B \parallel \boldsymbol k$）

**ポインティングベクトル** $\boldsymbol S = \dfrac{1}{\mu_0}\boldsymbol E\times\boldsymbol B$。時間平均 $\langle S\rangle = \dfrac{E_0^2}{2\mu_0c} = \dfrac12\varepsilon_0cE_0^2$。

**空洞のモード**（立教2024春）：一辺 $L$ の立方体、壁で $E_\parallel = 0$ → $k_i = n_i\pi/L$。$\omega = ck$ 以下のモード数 $= 2\times\dfrac18\cdot\dfrac43\pi\left(\dfrac{\omega L}{\pi c}\right)^3 = \dfrac{V\omega^3}{3\pi^2c^3}$（偏極2）→ $D(\omega) = \dfrac{V\omega^2}{\pi^2c^3}$。

#### ② 過去問（立教 2022年春 大問2）

真空中を伝搬する電磁波を考える。電磁波の電場及び磁場の振幅ベクトルをそれぞれ $\boldsymbol E_0$、$\boldsymbol B_0$、波数ベクトル及び角振動数をそれぞれ $\boldsymbol k$、$\omega$ とする。真空の誘電率及び透磁率をそれぞれ $\varepsilon_0$、$\mu_0$ とする。

(a) 電磁波の電場及び磁場をそれぞれ $\boldsymbol E(\boldsymbol r, t)$、$\boldsymbol B(\boldsymbol r, t)$ とする。それらを $\boldsymbol E_0, \boldsymbol B_0, \boldsymbol k, \omega$ を使って表せ。
(b) (a) で求めた電磁波がマクスウェル方程式を満たすために、$\boldsymbol E_0, \boldsymbol B_0, \boldsymbol k$ の方向に課される条件を述べよ。
(c) $\omega$ と $|\boldsymbol k|$ の間の関係を導け。
(d) $|\boldsymbol E_0|$ と $|\boldsymbol B_0|$ の間の関係を導け。
(e) この電磁波のポインティングベクトルの時間平均を求めよ。
(f) マクスウェル方程式から電場の波動方程式を導出せよ。

#### ③ 解説

**(a)** $\boldsymbol E = \boldsymbol E_0\cos(\boldsymbol k\cdot\boldsymbol r - \omega t)$、$\boldsymbol B = \boldsymbol B_0\cos(\boldsymbol k\cdot\boldsymbol r - \omega t)$（同位相）。

**(b)** $\nabla\cdot\boldsymbol E = -\boldsymbol k\cdot\boldsymbol E_0\sin(\cdots) = 0$ → $\boldsymbol k\perp\boldsymbol E_0$。同様に $\boldsymbol k\perp\boldsymbol B_0$。
$\nabla\times\boldsymbol E = -\boldsymbol k\times\boldsymbol E_0\sin(\cdots)$、$-\partial_t\boldsymbol B = -\omega\boldsymbol B_0\sin(\cdots)$ → $\boldsymbol k\times\boldsymbol E_0 = \omega\boldsymbol B_0$ → $\boldsymbol B_0\perp\boldsymbol E_0$。
**3つが互いに直交し、$\boldsymbol E_0\times\boldsymbol B_0$ が $\boldsymbol k$ の向き。**

**(c)** $\boldsymbol k\times\boldsymbol B_0 = -\mu_0\varepsilon_0\omega\boldsymbol E_0$ に $\boldsymbol B_0 = \boldsymbol k\times\boldsymbol E_0/\omega$ を代入：$\boldsymbol k\times(\boldsymbol k\times\boldsymbol E_0) = -k^2\boldsymbol E_0$（$\boldsymbol k\cdot\boldsymbol E_0 = 0$）。よって $-k^2/\omega = -\mu_0\varepsilon_0\omega$ → $\omega^2 = \dfrac{k^2}{\mu_0\varepsilon_0} = c^2k^2$。

**(d)** $|\boldsymbol B_0| = \dfrac{k|\boldsymbol E_0|}{\omega} = \dfrac{|\boldsymbol E_0|}{c}$。

**(e)** $\boldsymbol S = \dfrac{1}{\mu_0}\boldsymbol E\times\boldsymbol B = \dfrac{E_0B_0}{\mu_0}\cos^2(\cdots)\hat{\boldsymbol k}$。$\langle\cos^2\rangle = 1/2$：$\langle S\rangle = \dfrac{E_0^2}{2\mu_0c}$。

**(f)** 板書の3行。$\nabla\times(\nabla\times\boldsymbol E) = \nabla(\nabla\cdot\boldsymbol E) - \nabla^2\boldsymbol E$ を使うのが正道。積分形をこねる導出は根拠が曖昧になる（青学本番・第2-6回で減点された箇所）。

#### ④ 確認問題

**確認5-A**：$z$ 方向に進む平面波 $\boldsymbol E = E_0\cos(kz - \omega t)\hat{\boldsymbol x}$（青学第2-6回 問3-2）。$\boldsymbol B$ を向きも含めて求め、$\langle S\rangle$ を $E_0$ で表せ。

**確認5-B**：誘電率 $\varepsilon$、透磁率 $\mu$ の媒質中（立教2022夏）。波動方程式と位相速度 $v$、屈折率 $n = c/v$ を $\varepsilon, \mu$ で表せ。

**略解**
5-A：$\boldsymbol B = \dfrac{E_0}{c}\cos(kz - \omega t)\hat{\boldsymbol y}$、$\langle S\rangle = \dfrac{E_0^2}{2\mu_0c}$。
5-B：$\nabla^2\boldsymbol E = \mu\varepsilon\partial_t^2\boldsymbol E$、$v = 1/\sqrt{\mu\varepsilon}$、$n = \sqrt{\mu\varepsilon/(\mu_0\varepsilon_0)}$。

