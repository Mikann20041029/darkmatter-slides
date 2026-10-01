#### ① 板書

**定義**：$+q$ を $\boldsymbol d/2$、$-q$ を $-\boldsymbol d/2$ に置いた対。双極子モーメント $\boldsymbol p = q\boldsymbol d$。

**遠方（$r \gg d$）の電位**（$\boldsymbol p$ を $z$ 方向に）
$$\phi = \frac{1}{4\pi\varepsilon_0}\frac{\boldsymbol p\cdot\hat{\boldsymbol r}}{r^2} = \frac{p\cos\theta}{4\pi\varepsilon_0r^2}$$
導出：$\phi = \dfrac{q}{4\pi\varepsilon_0}\left(\dfrac{1}{r_+} - \dfrac{1}{r_-}\right)$、$\dfrac{1}{r_\pm} \simeq \dfrac{1}{r}\left(1 \pm \dfrac{d\cos\theta}{2r}\right)$。

**電場**（極座標成分）
$$E_r = -\frac{\partial\phi}{\partial r} = \frac{2p\cos\theta}{4\pi\varepsilon_0r^3}, \qquad E_\theta = -\frac{1}{r}\frac{\partial\phi}{\partial\theta} = \frac{p\sin\theta}{4\pi\varepsilon_0r^3}$$
直交座標では $\boldsymbol E = \dfrac{1}{4\pi\varepsilon_0}\dfrac{3(\boldsymbol p\cdot\hat{\boldsymbol r})\hat{\boldsymbol r} - \boldsymbol p}{r^3}$。

**外場中の双極子**
- 位置エネルギー $U = -\boldsymbol p\cdot\boldsymbol E$
- トルク $\boldsymbol N = \boldsymbol p\times\boldsymbol E$（外場に揃おうとする）
- 力 $\boldsymbol F = (\boldsymbol p\cdot\nabla)\boldsymbol E = \nabla(\boldsymbol p\cdot\boldsymbol E)$（一様電場では力ゼロ、勾配があると引かれる）

#### ② 過去問（立教 2023年春 大問2）

正の電荷 $q$ と負の電荷 $-q$ を持つ2つの点電荷が $z$ 軸上のそれぞれ $z = d/2$、$z = -d/2$ に固定されている。この双極子が作る電位は、原点から十分遠い位置で $\phi(r) = \dfrac{1}{4\pi\varepsilon_0}\dfrac{p\cos\theta}{r^2}$（$p = qd$）。

(a) はじめに正の電荷 $q$ を $z = d/2$ に固定し、負の電荷 $-q$ を無限遠方から $z = -d/2$ までゆっくり移動させた。外力のした仕事を求めよ。
(b) 双極子が作る電場の $r$ 成分と $\theta$ 成分。
(c) 原点から十分離れた位置 $\boldsymbol r' = (x', 0, z')$ に電荷 $Q$ の点電荷を置いた。双極子が受ける力 $\boldsymbol F$ と原点まわりのトルク $\boldsymbol N$ の各成分。

#### ③ 解説

**(a)** $-q$ を運ぶ仕事 ＝ $(-q)\times$（$+q$ が $z = -d/2$ に作る電位）$= -q\cdot\dfrac{q}{4\pi\varepsilon_0d} = -\dfrac{q^2}{4\pi\varepsilon_0d}$。負 ＝ 引力に沿って運ぶので外力は負の仕事。

**(b)** 板書の通り $E_r = \dfrac{2p\cos\theta}{4\pi\varepsilon_0r^3}$、$E_\theta = \dfrac{p\sin\theta}{4\pi\varepsilon_0r^3}$。

**(c)** **力**：作用反作用で、双極子が受ける力 $= -$（$Q$ が受ける力）$= -Q\boldsymbol E_{\rm dip}(\boldsymbol r')$。直交座標で $\phi = \dfrac{pz}{4\pi\varepsilon_0r^3}$ から
$$\boldsymbol E_{\rm dip} = -\nabla\phi = \frac{p}{4\pi\varepsilon_0}\left(\frac{3z\boldsymbol r}{r^5} - \frac{\hat{\boldsymbol z}}{r^3}\right)$$
$\boldsymbol r' = (x', 0, z')$、$r'^2 = x'^2 + z'^2$ で
$$\boldsymbol E_{\rm dip}(\boldsymbol r') = \frac{p}{4\pi\varepsilon_0r'^5}\left(3x'z',\ 0,\ 3z'^2 - r'^2\right) = \frac{p}{4\pi\varepsilon_0r'^5}\left(3x'z',\ 0,\ 2z'^2 - x'^2\right)$$
$$\boldsymbol F = -\frac{pQ}{4\pi\varepsilon_0r'^5}\left(3x'z',\ 0,\ 2z'^2 - x'^2\right)$$
**トルク**：$\boldsymbol N = \boldsymbol p\times\boldsymbol E_Q(0)$。$Q$ が原点に作る電場 $\boldsymbol E_Q(0) = \dfrac{Q}{4\pi\varepsilon_0}\dfrac{(0 - \boldsymbol r')}{r'^3} = -\dfrac{Q}{4\pi\varepsilon_0r'^3}(x', 0, z')$。$\boldsymbol p = (0, 0, p)$：
$$\boldsymbol N = \boldsymbol p\times\boldsymbol E_Q = \left(0\cdot E_z - p\cdot0,\ p\cdot E_x - 0,\ 0\right) = \left(0,\ -\frac{pQx'}{4\pi\varepsilon_0r'^3},\ 0\right)$$
（$x' > 0$、$Q > 0$ なら $N_y < 0$：双極子は $+x$ 方向へ倒れようとする＝負電荷側が $Q$ に近づく）

#### ④ 確認問題

**確認3-A**：一様電場 $\boldsymbol E_0 = E_0\hat{\boldsymbol z}$ 中で、双極子 $\boldsymbol p$ が $z$ 軸と角 $\alpha$ をなす。(i) 位置エネルギー $U(\alpha)$。(ii) トルクの大きさ。(iii) 微小振動の角振動数（慣性モーメント $I$）。

**確認3-B**：2つの双極子 $\boldsymbol p_1, \boldsymbol p_2$ がともに $z$ 方向を向き、$z$ 軸上に距離 $R$ 離れて置かれている。相互作用エネルギーと力を求めよ。

**略解**
3-A：(i) $U = -pE_0\cos\alpha$。(ii) $N = pE_0\sin\alpha$。(iii) $I\ddot\alpha = -pE_0\alpha$ → $\omega = \sqrt{pE_0/I}$。
3-B：$\boldsymbol p_2$ の位置での $\boldsymbol p_1$ の電場は $\theta = 0$ で $E_z = \dfrac{2p_1}{4\pi\varepsilon_0R^3}$。$U = -p_2E_z = -\dfrac{2p_1p_2}{4\pi\varepsilon_0R^3}$、$F = -\dfrac{dU}{dR} = -\dfrac{6p_1p_2}{4\pi\varepsilon_0R^4}$（引力）。

---
