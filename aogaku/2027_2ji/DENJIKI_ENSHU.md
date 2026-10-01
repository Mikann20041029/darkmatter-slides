# 電磁気学 演習書 — 青学対策に足りない4分野

既習（ガウス・同心球殻・ビオサバール・アンペール・電磁誘導・回路・電磁波・荷電粒子）はやらない。**足りない4つだけ。**

各分野：① 板書 → ② 過去問 → ③ 解説 → ④ 確認問題

作成 2026-09-12

---

## 1｜鏡像法（立教2010春・2012春・2017春／都立2025冬）— 電磁気の最頻型

### ① 板書

**導体の境界条件**：静電場中の導体は
- 内部で $\boldsymbol E = 0$、電荷は表面のみ
- 表面で電位 $\phi$ 一定、$\boldsymbol E$ は表面に垂直
- 表面電荷密度 $\sigma = \varepsilon_0E_n = -\varepsilon_0\dfrac{\partial\phi}{\partial n}$（$n$ は外向き法線）

**鏡像法の考え方**：導体を取り除き、代わりに仮想の電荷（鏡像電荷）を**導体の内側**に置いて、導体表面での境界条件（電位一定）を再現する。**一意性定理**（境界条件を満たすラプラス方程式の解は唯一）により、それが導体外側の正しい電場。

**2つの基本型**

| 型 | 鏡像電荷 | 位置 |
| --- | --- | --- |
| 無限平面導体（接地）＋点電荷 $q$（距離 $d$） | $-q$ | 面の裏側、距離 $d$ |
| 導体球（半径 $a$、接地）＋点電荷 $Q$（中心から $b > a$） | $q' = -\dfrac{a}{b}Q$ | 中心から $\dfrac{a^2}{b}$（球の内側） |

**導体球のバリエーション**
- 接地：上の $q'$ のみ。球の電位 0
- 絶縁・電荷 0：$q'$ に加えて中心に $-q' = +\dfrac{a}{b}Q$。球の電位 $= \dfrac{aQ/b}{4\pi\varepsilon_0a} = \dfrac{Q}{4\pi\varepsilon_0b}$
- 絶縁・電荷 $Q_0$：中心に $Q_0 - q'$

**鏡像電荷の位置の導出**（相似三角形）：球面上の任意の点 $L$、中心 $O$、点電荷 $K$、鏡像 $M$。$\triangle OLM \sim \triangle OKL$ となるように $M$ を取ると $\dfrac{OM}{OL} = \dfrac{OL}{OK}$ → $OM = \dfrac{a^2}{b}$。このとき $\dfrac{LM}{LK} = \dfrac{a}{b}$（球面上のどこでも）なので、$\dfrac{q'}{LM} + \dfrac{Q}{LK} = 0$ が全 $L$ で成り立つ。

**鏡像法で求まるもの**：外側の電位・電場、表面電荷分布、点電荷に働く力（鏡像電荷からの力）、点電荷を無限遠へ運ぶ仕事。**鏡像電荷は導体内部の場を表さない**（内部は $E = 0$）。

### ② 過去問（立教 2010年春 大問II）

真空中に絶縁された半径 $a$ の導体球（帯電していない）。中心 $O$ から $b$（$b > a$）の距離の点 $K$ に電荷 $Q$ の点電荷を置く。

1. 球面上の任意の点を $L$。$OK$ 上に点 $M$ をとり、$\triangle OLM$ と $\triangle OKL$ が相似形のとき、$OM$ の距離 $c$ を $a, b$ で表せ。
2. 鏡像法で解くため、導体球の代わりに点 $M$ に電荷 $q$ を置く。球面上の電位がどこでも同じになるように $q$ を求めよ。
3. 導体球は絶縁されているので電荷の総量は 0。総量が 0 になるように中心 $O$ にも鏡像電荷を置き、導体球の電位を求めよ。
4. 導体球と点電荷の間に働く力の大きさと向きを求めよ。

### ③ 解説

**1.** 相似より $\dfrac{OM}{OL} = \dfrac{OL}{OK}$ → $\dfrac{c}{a} = \dfrac{a}{b}$ → $c = \dfrac{a^2}{b}$。

**2.** 相似より $\dfrac{LM}{LK} = \dfrac{OL}{OK} = \dfrac{a}{b}$（$L$ によらない）。球面上の電位
$$\phi(L) = \frac{1}{4\pi\varepsilon_0}\left(\frac{Q}{LK} + \frac{q}{LM}\right) = \frac{1}{4\pi\varepsilon_0\,LK}\left(Q + q\frac{LK}{LM}\right) = \frac{1}{4\pi\varepsilon_0\,LK}\left(Q + q\frac{b}{a}\right)$$
これが $L$ によらず一定（実は 0）になるには $q = -\dfrac{a}{b}Q$。

**3.** 電荷総量 0 のため中心に $+\dfrac{a}{b}Q$。球面上の電位は、$M$ の $q$ と $K$ の $Q$ の寄与が打ち消し合うので中心電荷の分だけ：
$$\phi_{\text{球}} = \frac{1}{4\pi\varepsilon_0}\cdot\frac{aQ/b}{a} = \frac{Q}{4\pi\varepsilon_0b}$$

**4.** $K$ の $Q$ に働く力 ＝ $M$ の $q$ からの力 ＋ 中心の $+aQ/b$ からの力。$K$ から $M$ までの距離 $b - a^2/b = \dfrac{b^2 - a^2}{b}$。
$$F = \frac{Q}{4\pi\varepsilon_0}\left[\frac{-aQ/b}{\left(\frac{b^2-a^2}{b}\right)^2} + \frac{aQ/b}{b^2}\right] = \frac{aQ^2}{4\pi\varepsilon_0}\left[-\frac{b}{(b^2-a^2)^2} + \frac{1}{b^3}\right]$$
通分：$\dfrac{-b^4 + (b^2-a^2)^2}{b^3(b^2-a^2)^2} = \dfrac{a^2(a^2 - 2b^2)}{b^3(b^2-a^2)^2} < 0$（$b > a$）。
$$F = -\frac{a^3Q^2(2b^2 - a^2)}{4\pi\varepsilon_0b^3(b^2-a^2)^2} \quad(\text{引力})$$
中性の導体球でも引力になる（$q'$ の方が近いので勝つ）。

### ④ 確認問題

**確認1-A**（立教2012春 大問2 / 都立2025冬）：$x = a$（$a > 0$）に点電荷 $q$、$x < 0$ の領域全体に接地導体。
(i) $x > 0$ の電位 $\phi(x, y, z)$。(ii) 導体表面 $x = 0$ の誘導電荷密度 $\sigma(y, z)$ と総電荷。(iii) 点電荷に働く力。(iv) 点電荷を無限遠まで運ぶ仕事。

**確認1-B**：半径 $a$ の**接地**導体球と距離 $b$ の点電荷 $Q$。(i) 球面上の誘導電荷の総量。(ii) $Q$ に働く力。(iii) 絶縁・中性の場合（過去問の答え）との違いを述べよ。

**略解**
1-A：(i) $\phi = \dfrac{q}{4\pi\varepsilon_0}\left[\dfrac{1}{\sqrt{(x-a)^2+y^2+z^2}} - \dfrac{1}{\sqrt{(x+a)^2+y^2+z^2}}\right]$。(ii) $\sigma = -\varepsilon_0\dfrac{\partial\phi}{\partial x}\Big|_{x=0} = -\dfrac{qa}{2\pi(a^2+y^2+z^2)^{3/2}}$。総電荷 $-q$。(iii) $F = -\dfrac{q^2}{4\pi\varepsilon_0(2a)^2}$（引力）。(iv) $W = \int_a^\infty\dfrac{q^2}{16\pi\varepsilon_0x^2}dx = \dfrac{q^2}{16\pi\varepsilon_0a}$。
1-B：(i) $-\dfrac{a}{b}Q$。(ii) $F = -\dfrac{abQ^2}{4\pi\varepsilon_0(b^2-a^2)^2}$。(iii) 中性球は中心に $+aQ/b$ が加わる分、引力が弱まる。

---

## 2｜ラプラス・ポアソン方程式の境界値問題（立教2025春／都立2024冬・2026夏）

### ① 板書

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

### ② 過去問（立教 2025年春 大問2）

真空中の電位 $\phi$。真空の誘電率 $\varepsilon_0$。

(a) $z$ 軸方向の一様な電場 $\boldsymbol E_0 = (0, 0, E_z)$ があるとき、直交座標で $\phi(x, y, z)$ を書け。原点の電位を 0 とする。
(b) (a) を3次元極座標 $(r, \theta, \varphi)$ で表せ。
(c) 外場のない空間に半径 $a$ の導体球（中心が原点）を置き電荷 $Q$ を与えた。球の外の電位。無限遠で 0。
(d) 一様電場 $\boldsymbol E_0$ 中に半径 $a$ の導体球（全電荷 0、接地されていない）を置いた。球の外の電位は $\phi = F(r)\cos\theta$ で表せる。導体球を電位 0 として球の外の $\phi$ を求めよ。極座標のラプラス演算子は上の通り。無限遠で導体球の影響は無視できる。
(e) $x$-$z$ 面での電気力線と等電位線の概略図。
(f) 導体球表面の電荷面密度 $\sigma$。

### ③ 解説

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

### ④ 確認問題

**確認2-A**（都立2024冬 物理学I[2]）：静電ポテンシャル $\phi(r) = \dfrac{A}{r}e^{-kr}$（$A, k > 0$）。
(1) 電場 $E(r)$。(2) 半径 $R$ の球面にガウスの法則を適用し $R \to 0$ で原点の点電荷 $q$。(3) 球対称のポアソン方程式 $\nabla^2 = \dfrac{d^2}{dr^2} + \dfrac{2}{r}\dfrac{d}{dr}$ で原点以外の電荷密度 $\rho(r)$。(4) $\rho$ を全空間で積分し $q$ で表せ。

**確認2-B**：一様電場 $E_0$ 中の半径 $a$ の**誘電体球**（誘電率 $\varepsilon$）。内部は一様電場 $E_{\rm in}$ と仮定し、$\phi_{\rm in} = -E_{\rm in}r\cos\theta$、$\phi_{\rm out} = -E_0(r - \beta a^3/r^2)\cos\theta$ と置いて、境界条件（$\phi$ 連続、$D_r$ 連続）から $E_{\rm in}$ と $\beta$ を求めよ。

**略解**
2-A：(1) $E = Ae^{-kr}\left(\dfrac{1}{r^2} + \dfrac{k}{r}\right)$。(2) $E\cdot4\pi R^2 \to 4\pi A$ → $q = 4\pi\varepsilon_0A$。(3) $\nabla^2\phi = \dfrac{Ak^2e^{-kr}}{r}$ → $\rho = -\dfrac{\varepsilon_0Ak^2e^{-kr}}{r}$。(4) $\int\rho\,4\pi r^2dr = -4\pi\varepsilon_0Ak^2\int_0^\infty re^{-kr}dr = -4\pi\varepsilon_0A = -q$（遮蔽：全電荷 0）。
2-B：$E_{\rm in} = \dfrac{3\varepsilon_0}{\varepsilon + 2\varepsilon_0}E_0$、$\beta = \dfrac{\varepsilon - \varepsilon_0}{\varepsilon + 2\varepsilon_0}$。$\varepsilon \to \infty$ で導体（$E_{\rm in} \to 0$、$\beta \to 1$）。

---

## 3｜電気双極子（立教2023春）

### ① 板書

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

### ② 過去問（立教 2023年春 大問2）

正の電荷 $q$ と負の電荷 $-q$ を持つ2つの点電荷が $z$ 軸上のそれぞれ $z = d/2$、$z = -d/2$ に固定されている。この双極子が作る電位は、原点から十分遠い位置で $\phi(r) = \dfrac{1}{4\pi\varepsilon_0}\dfrac{p\cos\theta}{r^2}$（$p = qd$）。

(a) はじめに正の電荷 $q$ を $z = d/2$ に固定し、負の電荷 $-q$ を無限遠方から $z = -d/2$ までゆっくり移動させた。外力のした仕事を求めよ。
(b) 双極子が作る電場の $r$ 成分と $\theta$ 成分。
(c) 原点から十分離れた位置 $\boldsymbol r' = (x', 0, z')$ に電荷 $Q$ の点電荷を置いた。双極子が受ける力 $\boldsymbol F$ と原点まわりのトルク $\boldsymbol N$ の各成分。

### ③ 解説

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

### ④ 確認問題

**確認3-A**：一様電場 $\boldsymbol E_0 = E_0\hat{\boldsymbol z}$ 中で、双極子 $\boldsymbol p$ が $z$ 軸と角 $\alpha$ をなす。(i) 位置エネルギー $U(\alpha)$。(ii) トルクの大きさ。(iii) 微小振動の角振動数（慣性モーメント $I$）。

**確認3-B**：2つの双極子 $\boldsymbol p_1, \boldsymbol p_2$ がともに $z$ 方向を向き、$z$ 軸上に距離 $R$ 離れて置かれている。相互作用エネルギーと力を求めよ。

**略解**
3-A：(i) $U = -pE_0\cos\alpha$。(ii) $N = pE_0\sin\alpha$。(iii) $I\ddot\alpha = -pE_0\alpha$ → $\omega = \sqrt{pE_0/I}$。
3-B：$\boldsymbol p_2$ の位置での $\boldsymbol p_1$ の電場は $\theta = 0$ で $E_z = \dfrac{2p_1}{4\pi\varepsilon_0R^3}$。$U = -p_2E_z = -\dfrac{2p_1p_2}{4\pi\varepsilon_0R^3}$、$F = -\dfrac{dU}{dR} = -\dfrac{6p_1p_2}{4\pi\varepsilon_0R^4}$（引力）。

---

## 4｜ベクトル解析の演算（都立2026夏・2025冬／上智2025春・2025秋）

### ① 板書

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

### ② 過去問

**(A) 都立 2026年夏 物理学I[2] 問2**：3次元空間の位置ベクトル $\boldsymbol r$、$|\boldsymbol r| = r \ne 0$。
2-1) $\nabla\cdot\left(\dfrac{\boldsymbol r}{r^n}\right)$ を求めよ。
2-2) 原点の点電荷 $q$ が $\boldsymbol r$ に作る電場 $\boldsymbol E$ とその発散 $\nabla\cdot\boldsymbol E$。
2-3) $\boldsymbol E = -\nabla\phi$ であるとき $\nabla\times\boldsymbol E$。

**(B) 都立 2025年冬 数学 問2**：$f(r) = \log r$（$r > 0$）。
2-1) $\nabla f$ を $\boldsymbol r, r$ で表せ。2-2) $\Delta f$。

**(C) 上智 2025年秋 問4**：$\boldsymbol A = (2xyz, x^2z, x^2y)$。$\nabla\cdot\boldsymbol A$ と $\nabla\times\boldsymbol A$。

### ③ 解説

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

### ④ 確認問題

**確認4-A**：$\boldsymbol A = \boldsymbol\omega\times\boldsymbol r$（$\boldsymbol\omega$ 定ベクトル）。$\nabla\cdot\boldsymbol A$ と $\nabla\times\boldsymbol A$。

**確認4-B**：$\nabla\times(\nabla\times\boldsymbol E) = \nabla(\nabla\cdot\boldsymbol E) - \nabla^2\boldsymbol E$ を用い、真空中のマクスウェル方程式から $\nabla^2\boldsymbol E = \mu_0\varepsilon_0\dfrac{\partial^2\boldsymbol E}{\partial t^2}$ を導け（青学本番の電磁気 問3-1・第2-6回の正道）。

**略解**
4-A：$\nabla\cdot\boldsymbol A = 0$、$\nabla\times\boldsymbol A = 2\boldsymbol\omega$。
4-B：$\nabla\times\boldsymbol E = -\partial\boldsymbol B/\partial t$ の両辺に $\nabla\times$：左辺 $= \nabla(\nabla\cdot\boldsymbol E) - \nabla^2\boldsymbol E = -\nabla^2\boldsymbol E$（$\nabla\cdot\boldsymbol E = 0$）。右辺 $= -\dfrac{\partial}{\partial t}\nabla\times\boldsymbol B = -\mu_0\varepsilon_0\dfrac{\partial^2\boldsymbol E}{\partial t^2}$。
