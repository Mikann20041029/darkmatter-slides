#### ① 板書

**基礎方程式**
$$\nabla^2\phi = -\frac{\rho}{\varepsilon_0}\;(\text{ポアソン}), \qquad \rho = 0\ \text{なら}\ \nabla^2\phi = 0\;(\text{ラプラス})$$

**極座標のラプラシアン**
$$\nabla^2 = \frac{1}{r^2}\frac{\partial}{\partial r}\left(r^2\frac{\partial}{\partial r}\right) + \frac{1}{r^2\sin\theta}\frac{\partial}{\partial\theta}\left(\sin\theta\frac{\partial}{\partial\theta}\right) + \frac{1}{r^2\sin^2\theta}\frac{\partial^2}{\partial\varphi^2}$$

**球対称**（$\phi = \phi(r)$）：$\nabla^2\phi = \dfrac{1}{r^2}\dfrac{d}{dr}\left(r^2\dfrac{d\phi}{dr}\right) = \phi'' + \dfrac{2}{r}\phi'$。ラプラスの解：$\phi = \dfrac{A}{r} + B$。

**軸対称・$\cos\theta$ 型**（$\phi = F(r)\cos\theta$）：$\theta$ 部分は $\dfrac{1}{\sin\theta}\dfrac{d}{d\theta}(\sin\theta\cdot(-\sin\theta)) = -2\cos\theta$ なので
$$\nabla^2\phi = \cos\theta\left[\frac{1}{r^2}(r^2F')' - \frac{2F}{r^2}\right] = 0 \quad\Rightarrow\quad r^2F'' + 2rF' - 2F = 0 \quad\Rightarrow\quad F = Ar + \frac{B}{r^2}$$
（$F = r^n$ を代入：$n(n-1) + 2n - 2 = 0$ → $n = 1, -2$）

**解き方の手順**
1. 対称性から $\phi$ の形を仮定（球対称なら $\phi(r)$、一様電場があれば $F(r)\cos\theta$）
2. ラプラス方程式に代入して $F$ の常微分方程式を解く
3. **境界条件**で定数を決める：無限遠での振る舞い、導体表面で $\phi = $ 一定、電荷面での $E_n$ の飛び
4. $\sigma = -\varepsilon_0\partial\phi/\partial n$ で表面電荷

**一様電場中の導体球**（頻出）：$\phi = -E_0\left(r - \dfrac{a^3}{r^2}\right)\cos\theta$、$\sigma = 3\varepsilon_0E_0\cos\theta$。誘導される双極子モーメント $p = 4\pi\varepsilon_0a^3E_0$。

#### ② 過去問（立教 2025年春 大問2）

真空中の電位 $\phi$。真空の誘電率 $\varepsilon_0$。

(a) $z$ 軸方向の一様な電場 $\boldsymbol E_0 = (0, 0, E_z)$ があるとき、直交座標で $\phi(x, y, z)$ を書け。原点の電位を 0 とする。
(b) (a) を3次元極座標 $(r, \theta, \varphi)$ で表せ。
(c) 外場のない空間に半径 $a$ の導体球（中心が原点）を置き電荷 $Q$ を与えた。球の外の電位。無限遠で 0。
(d) 一様電場 $\boldsymbol E_0$ 中に半径 $a$ の導体球（全電荷 0、接地されていない）を置いた。球の外の電位は $\phi = F(r)\cos\theta$ で表せる。導体球を電位 0 として球の外の $\phi$ を求めよ。極座標のラプラス演算子は上の通り。無限遠で導体球の影響は無視できる。
(e) $x$-$z$ 面での電気力線と等電位線の概略図。
(f) 導体球表面の電荷面密度 $\sigma$。

#### ③ 解説

**(a)** $\boldsymbol E = -\nabla\phi$ で $\phi = -E_zz$（原点で 0）。

**(b)** $z = r\cos\theta$ より $\phi = -E_zr\cos\theta$。

**(c)** 球対称でラプラス：$\phi = A/r + B$。無限遠で 0 → $B = 0$。ガウスの法則で $E = Q/(4\pi\varepsilon_0r^2)$ → $\phi = \dfrac{Q}{4\pi\varepsilon_0r}$。

**(d)** $\phi = F(r)\cos\theta$ を代入し $F = Ar + B/r^2$。境界条件：
- 無限遠：導体の影響が消え $\phi \to -E_zr\cos\theta$ → $A = -E_z$
- $r = a$：$\phi = 0$ → $F(a) = 0$ → $-E_za + B/a^2 = 0$ → $B = E_za^3$
$$\phi = -E_z\left(r - \frac{a^3}{r^2}\right)\cos\theta$$
（$1/r^2$ の項は双極子の電位。導体に誘起された双極子モーメント $p = 4\pi\varepsilon_0a^3E_z$）

**(e)** 等電位線：$\phi = 0$ は球面と赤道面 $\theta = \pi/2$。遠方では $z = $ 一定の平面。電気力線は遠方で $z$ 方向に平行、球面には垂直に出入りする。外場が $+z$ 向きなら正電荷は $+z$ 方向に押されるので**北極（$\theta = 0$）が正、南極が負**に帯電する。力線は北極から出て、南極に入る。

**(f)** $\sigma = -\varepsilon_0\dfrac{\partial\phi}{\partial r}\Big|_{r=a} = \varepsilon_0E_z\left(1 + \dfrac{2a^3}{a^3}\right)\cos\theta = 3\varepsilon_0E_z\cos\theta$。
総電荷 $\int\sigma\,dS = 3\varepsilon_0E_za^2\int_0^\pi\cos\theta\cdot2\pi\sin\theta\,d\theta = 0$ ✓（中性）。

#### ④ 確認問題

**確認2-A**（都立2024冬 物理学I[2]）：静電ポテンシャル $\phi(r) = \dfrac{A}{r}e^{-kr}$（$A, k > 0$）。
(1) 電場 $E(r)$。(2) 半径 $R$ の球面にガウスの法則を適用し $R \to 0$ で原点の点電荷 $q$。(3) 球対称のポアソン方程式 $\nabla^2 = \dfrac{d^2}{dr^2} + \dfrac{2}{r}\dfrac{d}{dr}$ で原点以外の電荷密度 $\rho(r)$。(4) $\rho$ を全空間で積分し $q$ で表せ。

**確認2-B**：一様電場 $E_0$ 中の半径 $a$ の**誘電体球**（誘電率 $\varepsilon$）。内部は一様電場 $E_{\rm in}$ と仮定し、$\phi_{\rm in} = -E_{\rm in}r\cos\theta$、$\phi_{\rm out} = -E_0(r - \beta a^3/r^2)\cos\theta$ と置いて、境界条件（$\phi$ 連続、$D_r$ 連続）から $E_{\rm in}$ と $\beta$ を求めよ。

**略解**
2-A：(1) $E = Ae^{-kr}\left(\dfrac{1}{r^2} + \dfrac{k}{r}\right)$。(2) $E\cdot4\pi R^2 \to 4\pi A$ → $q = 4\pi\varepsilon_0A$。(3) $\nabla^2\phi = \dfrac{Ak^2e^{-kr}}{r}$ → $\rho = -\dfrac{\varepsilon_0Ak^2e^{-kr}}{r}$。(4) $\int\rho\,4\pi r^2dr = -4\pi\varepsilon_0Ak^2\int_0^\infty re^{-kr}dr = -4\pi\varepsilon_0A = -q$（遮蔽：全電荷 0）。
2-B：$E_{\rm in} = \dfrac{3\varepsilon_0}{\varepsilon + 2\varepsilon_0}E_0$、$\beta = \dfrac{\varepsilon - \varepsilon_0}{\varepsilon + 2\varepsilon_0}$。$\varepsilon \to \infty$ で導体（$E_{\rm in} \to 0$、$\beta \to 1$）。

---
