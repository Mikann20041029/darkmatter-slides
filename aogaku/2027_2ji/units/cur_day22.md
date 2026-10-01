#### 【A】電磁気 §5 マクスウェル方程式から波動方程式へ（立教2022春・2024春／青学本番 問3-1）


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

#### 【B】力学 §6 回転座標系・遠心力と拘束（都立2026夏）


#### ① 板書

**極座標での運動方程式**（平面）
$$m(\ddot r - r\dot\theta^2) = F_r, \qquad m(r\ddot\theta + 2\dot r\dot\theta) = F_\theta$$
- $-mr\dot\theta^2$ の項が**遠心力**（回転する座標で見たときの見かけの力）
- $2m\dot r\dot\theta$ が**コリオリ力**の項
- 中心力（$F_\theta = 0$）なら $\dfrac{d}{dt}(mr^2\dot\theta) = 0$ → 角運動量 $L = mr^2\dot\theta$ 保存

**拘束条件のある2体**：糸で繋がれた2質点は「糸の長さ一定」が拘束。$r + z = \ell$ → $\dot r = -\dot z$。張力 $T$ は両方に同じ大きさで働く。**未知の $T$ は2本の運動方程式から消去する。**

**手順**
1. 各質点の運動方程式を書く（極座標なら遠心力込み）
2. 拘束条件で変数を減らす
3. 保存量（角運動量・エネルギー）を書き出す
4. 円運動の条件は $\ddot r = 0$（かつ $\dot r = 0$）

#### ② 過去問（都立 2026年夏 物理学I［1］）

図のように、水平面に空けられた小孔に十分に長い軽い糸を通し、その両端に同じ質量 $m$ の質点をそれぞれ繋げる。質点のうち一方（質点A）は小孔から鉛直下向きに垂れ下がった伸び縮みしない糸の先に繋がれ、もう一方（質点B）は水平面上にある。質点と水平面、および糸と小孔の間には摩擦はなく、糸はたるむことはないものとする。重力加速度の大きさを $g$ とする。

問1　質点Aは鉛直線上のみを運動するものとし、その座標を $(0, 0, z)$ で表す（$z$ 軸は鉛直下向きを正とする）。質点Bは水平面上を運動し、その位置を極座標 $\boldsymbol r = (r\cos\theta, r\sin\theta, 0)$ で表す。糸の張力の大きさを $T$ で表す。
　1-1) 質点Aの運動方程式を書け。
　1-2) 一般に $\dot\theta \ne 0$ のとき質点Bには遠心力がはたらく。このことに注意して、質点Bの動径方向の運動方程式を書け。
　1-3) 糸の長さを $\ell$ として、この系の力学的エネルギーを $r, \dot r, \dot\theta$ で表せ。位置エネルギーの基準は水平面とする。

問2　位置 $\boldsymbol r = (a, 0, 0)$ にある質点Bに時刻 $t = 0$ で初速度 $\boldsymbol v = (0, v_0, 0)$ を与えた（$a > 0$、$v_0 > 0$）。
　2-1) 質点Bの角運動量の大きさが $mav_0$ となることを示せ。
　2-2) 質点A、Bからなる全系の力学的エネルギーを $m, a, v_0, g$ で表せ。
　2-3) 質点Bが半径 $a$ の等速円運動を続けるための $v_0$ の条件を求めよ。

#### ③ 解説

**1-1)** Aには重力（下向き $+z$）と張力（上向き）：$m\ddot z = mg - T$。

**1-2)** Bには動径方向に張力（内向き）のみ。遠心力を含めた極座標の式：
$$m(\ddot r - r\dot\theta^2) = -T$$

**1-3)** 拘束 $r + z = \ell$ より $\dot z = -\dot r$。運動エネルギー $\frac12m(\dot r^2 + r^2\dot\theta^2) + \frac12m\dot z^2 = m\dot r^2 + \frac12mr^2\dot\theta^2$。位置エネルギー $-mgz = -mg(\ell - r)$。
$$E = m\dot r^2 + \frac12mr^2\dot\theta^2 - mg(\ell - r)$$

**2-1)** 張力は動径方向なので $\theta$ 方向の力はゼロ → $\dfrac{d}{dt}(mr^2\dot\theta) = 0$。初期値 $r = a$、$r\dot\theta = v_0$ より $L = mav_0$（一定）。

**2-2)** $t = 0$ で $\dot r = 0$、$r\dot\theta = v_0$：$E = \frac12mv_0^2 - mg(\ell - a)$。

**2-3)** 等速円運動は $r = a$ 一定、$\ddot r = 0$。1-2) より $T = ma\dot\theta^2 = mv_0^2/a$。1-1) で $\ddot z = 0$ より $T = mg$。よって
$$\frac{mv_0^2}{a} = mg \quad\Rightarrow\quad v_0 = \sqrt{ga}$$
（$v_0 > \sqrt{ga}$ なら遠心力が勝ってBは外へ、Aは上がる。$v_0 < \sqrt{ga}$ なら逆）

#### ④ 確認問題

**確認6-A**：問2の設定で、有効ポテンシャル $U_{\rm eff}(r) = \dfrac{L^2}{2mr^2}\cdot\dfrac{1}{2}$…ではなく、$E$ を $r, \dot r$ だけで書き直し（$\dot\theta = L/mr^2$ を代入）、$U_{\rm eff}(r)$ を求めよ。円軌道 $r = a$ が安定であることを $U''_{\rm eff}(a) > 0$ で確かめよ。

**確認6-B**：半径 $R$ の円環が鉛直軸まわりに角速度 $\omega$ で回転（青学第2-3回・立教2019夏）。円環上のビーズの運動方程式を、回転系で遠心力を含めて書き、相対静止点 $\cos\theta_0 = g/(R\omega^2)$ を導け。

**略解**
6-A：$E = m\dot r^2 + \dfrac{L^2}{2mr^2} + mgr - mg\ell$。$U_{\rm eff} = \dfrac{L^2}{2mr^2} + mgr$（運動項が $m\dot r^2$ で係数が通常の2倍なのに注意）。$U'_{\rm eff}(a) = 0$ で $v_0^2 = ga$、$U''_{\rm eff}(a) = 3L^2/(ma^4) > 0$。
6-B：$mR\ddot\theta = -mg\sin\theta + mR\omega^2\sin\theta\cos\theta$。静止点 $\sin\theta = 0$ または $\cos\theta = g/(R\omega^2)$。
