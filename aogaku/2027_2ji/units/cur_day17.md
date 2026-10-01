#### ① 板書

**剛体の角運動量**：固定軸まわりで $L = I\omega$。外力のモーメントがゼロなら $L$ 保存。

**注意点**
- 質量分布が変わると $I$ が変わる。$L = I\omega$ 保存 → $\omega$ が変わる（フィギュアスケートの回転）
- そのとき**運動エネルギーは保存しない**。$E = L^2/(2I)$ なので $I$ が減ると $E$ が増える。増分は内力（腕を引き込む力）の仕事
- **衝突**の瞬間：撃力は大きいが時間が短いので、**衝突点まわりの角運動量**は保存する（撃力のモーメントがゼロ）。重心の角運動量は保存しない
- 点 $A$ まわりの角運動量 $= $ 重心の運動による分 $\boldsymbol r_G\times M\boldsymbol v_G$ ＋ 重心まわりの自転 $I_G\omega$

#### ② 過去問

**(A) 立教 2011年春 大問1**：両端に質量 $m$ の質点がついた長さ $l$ の軽い棒が、中心を通り紙面に垂直な軸まわりに角速度 $\omega_0$ で回転。
(a) $I_0$。(b) $L_0$。(c) $E_0$。(d) 二つの質点を回転中心へ、中心からの距離がそれぞれ $l/4$ になるまで引き込んだ。角速度 $\omega_1$ と運動エネルギー $E_1$。(e) $E_1 - E_0$ は何に由来するか。

**(B) 立教 2020年春 大問1**：質量 $M$ 半径 $R$ の一様な球が粗い水平面上を滑らずに転がり、中心は速さ $v_0$ で直進。高さ $h$（$0 < h < R$）の段差に衝突し、衝突点 $A$ まわりで滑らずに回転を始める。$I = \frac25MR^2$。
(a) 衝突の瞬間の $A$ まわりの角運動量 $L$ と角速度 $\omega$。(b) $\overrightarrow{AO}$ と鉛直上向きのなす角を $\theta$ として、エネルギー保存の式。(c) $A$ から受ける抗力 $T$ を $\theta, \omega$ で。(d) 段差を越える条件を $v_0$ で。

#### ③ 解説

**(A)**
(a) $I_0 = 2\cdot m(l/2)^2 = \dfrac{ml^2}{2}$。(b) $L_0 = I_0\omega_0 = \dfrac{ml^2\omega_0}{2}$。(c) $E_0 = \frac12I_0\omega_0^2 = \dfrac{ml^2\omega_0^2}{4}$。
(d) $I_1 = 2m(l/4)^2 = \dfrac{ml^2}{8}$。$L$ 保存：$\omega_1 = \dfrac{I_0}{I_1}\omega_0 = 4\omega_0$。$E_1 = \frac12I_1\omega_1^2 = \frac12\cdot\dfrac{ml^2}{8}\cdot16\omega_0^2 = ml^2\omega_0^2 = 4E_0$。
(e) 質点を引き込むとき、遠心力に逆らって仕事をする。その仕事が $E_1 - E_0 = 3E_0$。

**(B)**
(a) 衝突前、$A$ まわりの角運動量 = 重心運動の分 ＋ 自転の分。$A$ から重心 $O$ への鉛直距離は $R - h$、$\boldsymbol v_0$ は水平なので $|\boldsymbol r\times M\boldsymbol v_0| = Mv_0(R-h)$。自転 $\omega_0 = v_0/R$ で $I\omega_0 = \frac25MRv_0$。
$$L = Mv_0(R - h) + \frac25MRv_0 = Mv_0\left(\frac{7R}{5} - h\right)$$
衝突後は $A$ まわりの剛体回転：$I_A = I + MR^2 = \frac75MR^2$。$L = I_A\omega$ より
$$\omega = \frac{v_0(7R - 5h)}{7R^2}$$
(b) 衝突後は $A$ まわりの回転でエネルギー保存（抗力は $A$ で仕事をしない）。重心の高さ $R\cos\theta$：
$$\frac12I_A\dot\theta^2 + MgR\cos\theta = \frac12I_A\omega^2 + Mg(R - h)$$
（初期 $\cos\theta_0 = (R-h)/R$）
(c) 動径方向（$A \to O$ 方向）の運動方程式：$T - Mg\cos\theta = -MR\dot\theta^2$ → $T = Mg\cos\theta - MR\dot\theta^2$。
(d) 段差を越える = $\theta = 0$（$O$ が $A$ の真上）まで回れる。$\theta = 0$ で $\dot\theta^2 \ge 0$：
$$\frac12I_A\omega^2 \ge Mgh \quad\Rightarrow\quad \frac{7}{10}MR^2\cdot\frac{v_0^2(7R-5h)^2}{49R^4} \ge Mgh \quad\Rightarrow\quad v_0^2 \ge \frac{70gR^2h}{(7R - 5h)^2}$$

> **落とし穴**：衝突では「$A$ まわりの角運動量」が保存する。運動量もエネルギーも保存しない。

#### ④ 確認問題

**確認4-A**：半径 $a$ 質量 $M$ の一様な円板が中心軸まわりに $\omega_0$ で回転。縁に質量 $m$ の粘土を静かに落として付着させた。付着後の角速度と失われたエネルギー。

**確認4-B**：長さ $l$ 質量 $M$ の一様な棒が一端を軸に鉛直面内で自由に回転できる。水平に静止した状態から放す。最下点での角速度と、軸が棒に及ぼす力。

**略解**
4-A：$\omega = \dfrac{Ma^2/2}{Ma^2/2 + ma^2}\omega_0 = \dfrac{M}{M + 2m}\omega_0$。$\Delta E = -\frac12\cdot\frac{Ma^2}{2}\omega_0^2\cdot\frac{2m}{M+2m}$。
4-B：$I = Ml^2/3$、$\frac12I\omega^2 = Mg\frac{l}{2}$ → $\omega = \sqrt{3g/l}$。最下点で軸の力 $= Mg + M\frac{l}{2}\omega^2 = \frac52Mg$。

---
