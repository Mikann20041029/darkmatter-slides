#### ① 板書

**慣性モーメント（暗記4つ）**：細い棒（中心）$\frac{1}{12}Ml^2$、円板・円柱（中心軸）$\frac12MR^2$、薄い円筒 $MR^2$、一様球 $\frac25MR^2$。
**平行軸定理**：$I = I_G + Md^2$（重心からの距離 $d$ の軸）。棒の端なら $\frac13Ml^2$。

**転がりの運動方程式**（斜面角 $\alpha$、摩擦力 $f$ を斜面上向きに仮定）

- 並進：$M\dot v = Mg\sin\alpha - f$
- 回転（重心まわり）：$I\dot\omega = fR$
- **滑らない条件**：$v = R\omega$（$\dot v = R\dot\omega$）

3本を連立して $\dot v = \dfrac{g\sin\alpha}{1 + I/MR^2}$、$f = \dfrac{Mg\sin\alpha}{1 + MR^2/I}$。$I/MR^2 = \frac12$（円柱）、$\frac25$（球）、$1$（円筒）。**$I$ が小さいほど速く転がる**（球＞円柱＞円筒）。

**滑らないための条件**：$f\le\mu N = \mu Mg\cos\alpha$ → $\tan\alpha\le\mu\left(1 + \dfrac{MR^2}{I}\right)$。これを超えると滑りながら転がる（$f = \mu N$ で固定、$v\ne R\omega$）。

**エネルギー**：転がりの運動エネルギー $= \frac12Mv^2 + \frac12I\omega^2 = \frac12Mv^2\left(1 + \dfrac{I}{MR^2}\right)$。滑らなければ摩擦は仕事をしない → エネルギー保存が使える。

**転がりvs滑り（速さの比較）**：同じ高さ $h$ から降りたとき、滑る（摩擦なし）なら $v^2 = 2gh$、転がるなら $v^2 = \dfrac{2gh}{1 + I/MR^2}$。

#### ② 過去問【立教 2014年春 大問1・原文】

一様密度で質量 $M$、半径 $a$、長さ $l$ の円柱A（図1）と、同じく一様密度で同じ質量 $M$、外半径 $a$、内半径 $b$、長さ $l$ の円筒B（図2）がある（$0<b<a$）。これらの物体を水平面と角度 $\phi$ をなす斜面に置き（図3）、時刻 $t=0$ で手を離した。これらの物体は滑ることなく転がるとする。以下の問に答えよ。
(a) 円柱Aの中心軸まわりの慣性モーメントを求めよ。
(b) 円筒Bの中心軸まわりの慣性モーメントを求めよ。
(c) これらの物体の並進運動の運動方程式を書け。なお物体と斜面の間に働く摩擦力を $F$ とする。坂道に沿って下る方向を正として座標軸を取り、それを $x$ 軸とする。
(d) 慣性モーメントを $I$ として、これらの物体の回転運動の方程式を書け。物体の回転角を $\theta$ とする。
(e) (c),(d)で得られた結果から $F$ を消去することで物体の並進運動の運動方程式を求めよ。それを解き物体の位置と速さを時刻 $t$ の関数として求めよ。
(f) 運動エネルギー（並進と回転の両方を含む）$K$ と位置エネルギー $U$ を $x$ と $\dot x$ の関数として求めよ。時刻 $t=0$ の位置を高さの基準とする。
(g) ラグランジュ関数 $L$ を $x$ と $\dot x$ の関数として表し、ラグランジュの運動方程式を書け。
(h) 物体AとBの運動のちがいを記述せよ。

#### ③ 解説

**(a)** 半径 $r$、厚さ $dr$ の円筒殻：$dm = \dfrac{M}{\pi a^2}2\pi r\,dr$。$I_A = \displaystyle\int_0^ar^2dm = \frac{2M}{a^2}\cdot\frac{a^4}{4} = \frac12Ma^2$。
**(b)** 同じ計算を $b$ から $a$ まで、密度は $\dfrac{M}{\pi(a^2-b^2)}$：$I_B = \dfrac{2M}{a^2-b^2}\cdot\dfrac{a^4-b^4}{4} = \dfrac12M(a^2+b^2)$。
**(c)** $M\ddot x = Mg\sin\phi - F$（$F$ は斜面上向き）。
**(d)** $I\ddot\theta = Fa$（摩擦力のモーメントが回転を作る）。
**(e)** 滑らない：$x = a\theta$ → $\ddot\theta = \ddot x/a$。(d)より $F = I\ddot x/a^2$。(c)に入れて $\left(M + \dfrac{I}{a^2}\right)\ddot x = Mg\sin\phi$ →
$$\ddot x = \frac{g\sin\phi}{1 + I/Ma^2},\qquad x(t) = \frac12\ddot x\,t^2,\quad \dot x(t) = \ddot x\,t$$
A：$\ddot x = \frac23g\sin\phi$。B：$\ddot x = \dfrac{2a^2}{3a^2+b^2}g\sin\phi$。
**(f)** $K = \frac12M\dot x^2 + \frac12I\left(\dfrac{\dot x}{a}\right)^2 = \frac12\left(M + \dfrac I{a^2}\right)\dot x^2$、$U = -Mgx\sin\phi$（$x$ だけ下ると高さが $x\sin\phi$ 下がる）。
**(g)** $L = K - U = \frac12\left(M + \dfrac I{a^2}\right)\dot x^2 + Mgx\sin\phi$。$\dfrac{d}{dt}\dfrac{\partial L}{\partial\dot x} = \dfrac{\partial L}{\partial x}$ → $\left(M + \dfrac I{a^2}\right)\ddot x = Mg\sin\phi$。(e)と一致 ✓。
**(h)** $I_B > I_A$（質量が外側にある）ので B の加速度が小さい。**円柱Aが先に降りる。** 同じ高さを降りたときの速さも A の方が大きい（回転に取られるエネルギーが少ない）。

> **落とし穴**：(b)で密度を $M/\pi a^2$ のまま使う。(f)で $U$ の符号（下るほど $U$ は減る）。

#### ④ 練習問題

**練習K7-A**：一様球（$I = \frac25MR^2$）が斜面を滑らずに転がるときの加速度と、滑らない条件。

**練習K7-B**：長さ $l$ の一様棒の一端を軸にした慣性モーメントを、(i) 積分で、(ii) 平行軸定理で求め、一致を確認せよ。

**練習K7-C【自作】**：半径 $R$ の固定円筒の上を、半径 $r$ の小円柱が滑らずに転がり落ちる。小円柱の中心が頂点から角 $\theta$ の位置に来たときの中心の速さ（エネルギー保存）。

**略解**
K7-A：$\dot v = \frac57g\sin\alpha$、$f = \frac27Mg\sin\alpha$、$\tan\alpha\le\frac72\mu$。
K7-B：(i) $\int_0^l\frac Mlx^2dx = \frac13Ml^2$。(ii) $\frac1{12}Ml^2 + M(l/2)^2 = \frac13Ml^2$ ✓。
K7-C：中心は半径 $R+r$ の円周上。$Mg(R+r)(1-\cos\theta) = \frac12Mv^2(1 + \frac12) $ → $v^2 = \frac43g(R+r)(1-\cos\theta)$。
