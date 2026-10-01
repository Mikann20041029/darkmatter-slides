#### ① 板書

**極座標のラグランジアン**（平面、中心力 $V(r)$）
$$L = \frac12m(\dot r^2 + r^2\dot\theta^2) - V(r)$$
**オイラー・ラグランジュ方程式**：$\dfrac{d}{dt}\dfrac{\partial L}{\partial\dot q} - \dfrac{\partial L}{\partial q} = 0$。

- $\theta$：$L$ に $\theta$ が入らない（循環座標）→ $\dfrac{d}{dt}(mr^2\dot\theta) = 0$ → **角運動量 $\ell = mr^2\dot\theta$ が保存**（＝面積速度一定・ケプラー第2法則）
- $r$：$m\ddot r - mr\dot\theta^2 + V'(r) = 0$ → $m\ddot r = -V'(r) + \dfrac{\ell^2}{mr^3}$

**有効ポテンシャル**：$\dot\theta$ を $\ell$ で消して
$$E = \frac12m\dot r^2 + \underbrace{\frac{\ell^2}{2mr^2} + V(r)}_{U_{\rm eff}(r)}$$
1次元問題に化ける。**円軌道 ⟺ $U_{\rm eff}'(r_0) = 0$**、安定 ⟺ $U_{\rm eff}''(r_0) > 0$。円軌道からの微小ずれの振動数 $\omega_r^2 = U_{\rm eff}''(r_0)/m$。

**万有引力 $V = -GMm/r$**

- 円軌道：$\dfrac{mv^2}{r} = \dfrac{GMm}{r^2}$ → $v = \sqrt{GM/r}$、周期 $T = 2\pi\sqrt{r^3/GM}$（第3法則 $T^2\propto r^3$）
- 楕円軌道の近星点 $r_1$・遠星点 $r_2$：$\dot r = 0$ なので **角運動量保存 $r_1v_1 = r_2v_2$ とエネルギー保存** の2本で $v_1, v_2$ が出る
- $E<0$ 楕円、$E=0$ 放物線、$E>0$ 双曲線

**ラグランジアンを書く手順**：①座標を決める（極座標・円筒座標）②$T$ を書く（$\frac12m(\dot r^2 + r^2\dot\theta^2 + \dot z^2)$）③$V$ を書く④循環座標を探す（保存量）⑤残りの座標で EL。

#### ② 過去問【再構成：立教2025春 大問1 の型を私が書き直したもの。原文は `kakomon/rikkyo/2025-Feb.pdf` 大問1】

質量 $M$ の恒星のまわりを質量 $m$（$\ll M$）の惑星が運動する。恒星を原点とする極座標 $(r,\theta)$ を使う。
(a) ラグランジアン $L$ を書け。
(b) $\theta$ についてのオイラー・ラグランジュ方程式から保存量を求め、その物理的意味を述べよ。
(c) $r$ についての運動方程式を書き、(b) の保存量 $\ell$ で $\dot\theta$ を消去せよ。
(d) 円軌道の半径 $r_0$ と角運動量 $\ell$ の関係、円軌道の周期 $T$。
(e) 惑星が近星点 $r_1$ で速さ $v_1$ のとき、遠星点での距離 $r_2$ と速さ $v_2$ を $r_1, v_1, GM$ で表せ。

#### ③ 解説

**(a)** $L = \dfrac12m(\dot r^2 + r^2\dot\theta^2) + \dfrac{GMm}{r}$。

**(b)** $\dfrac{\partial L}{\partial\theta} = 0$ なので $\dfrac{d}{dt}\dfrac{\partial L}{\partial\dot\theta} = \dfrac{d}{dt}(mr^2\dot\theta) = 0$。$\ell = mr^2\dot\theta$（恒星まわりの角運動量）が保存。$\frac12r^2\dot\theta$ は面積速度なので、これはケプラー第2法則。

**(c)** $m\ddot r = mr\dot\theta^2 - \dfrac{GMm}{r^2}$。$\dot\theta = \ell/(mr^2)$ を入れて
$$m\ddot r = \frac{\ell^2}{mr^3} - \frac{GMm}{r^2} = -\frac{d}{dr}\left[\frac{\ell^2}{2mr^2} - \frac{GMm}{r}\right] = -U_{\rm eff}'(r)$$

**(d)** 円軌道は $\ddot r = 0$：$\dfrac{\ell^2}{mr_0^3} = \dfrac{GMm}{r_0^2}$ → $\ell^2 = GMm^2r_0$。周期：$\dot\theta = \ell/(mr_0^2) = \sqrt{GM/r_0^3}$ → $T = 2\pi\sqrt{r_0^3/GM}$。
安定性：$U_{\rm eff}'' = \dfrac{3\ell^2}{mr_0^4} - \dfrac{2GMm}{r_0^3} = \dfrac{GMm}{r_0^3} > 0$ ✓ 安定。

**(e)** 近星点・遠星点では $\dot r = 0$ なので速度は $\theta$ 方向のみ。
角運動量保存：$r_1v_1 = r_2v_2$。エネルギー保存：$\frac12v_1^2 - \dfrac{GM}{r_1} = \frac12v_2^2 - \dfrac{GM}{r_2}$。
$v_2 = r_1v_1/r_2$ を入れて整理すると $r_2$ の2次方程式：$\left(v_1^2 - \dfrac{2GM}{r_1}\right)r_2^2 + 2GMr_2 - r_1^2v_1^2 = 0$。$r_2 = r_1$ は自明解なので割って
$$r_2 = \frac{r_1^2v_1^2}{2GM - r_1v_1^2},\qquad v_2 = \frac{r_1v_1}{r_2} = \frac{2GM - r_1v_1^2}{r_1v_1}$$
検算：$v_1^2 = GM/r_1$（円軌道）なら $r_2 = r_1$、$v_2 = v_1$ ✓。$r_1v_1^2\to2GM$ で $r_2\to\infty$（脱出速度）✓。

> **落とし穴**：①$T$ を $\frac12m(\dot r^2 + \dot\theta^2)$ と書く（$r^2$ を忘れる）。②有効ポテンシャルの遠心力項は $+\ell^2/2mr^2$（プラス）。③近星点で「エネルギー保存だけ」で解こうとして未知数が足りなくなる。角運動量保存を必ず併用。

#### ④ 練習問題

**練習K5-A**：$V(r) = \frac12kr^2$（等方調和振動子）。円軌道の角速度と、円軌道からの動径方向の微小振動の角振動数 $\omega_r$。$\omega_r/\omega_\theta$ はいくつか（軌道は閉じるか）。

**練習K5-B**：円筒座標 $(r,\theta,z)$ で、$z$ 軸まわりに角速度 $\Omega$ で回転する円錐面（頂角 $2\alpha$）の内側を滑る質点。$z = r\cot\alpha$ の拘束のもとでラグランジアンを書き、循環座標と保存量を挙げよ。

**練習K5-C**：万有引力で、$r_1$ で速さ $v_1$ のとき軌道が楕円・放物線・双曲線になる条件を $v_1$ で書け。

**略解**
K5-A：$U_{\rm eff} = \ell^2/2mr^2 + kr^2/2$。$U' = 0$ → $\ell^2 = mkr_0^4$、$\omega_\theta = \sqrt{k/m}$。$U'' = 3\ell^2/mr_0^4 + k = 4k$ → $\omega_r = 2\sqrt{k/m}$。比は2（動径2往復で1周、軌道は閉じる楕円）。
K5-B：$L = \frac12m(\dot r^2 + r^2\dot\theta^2 + \dot r^2\cot^2\alpha) - mgr\cot\alpha$。$\theta$ が循環、$mr^2\dot\theta$ 保存。
K5-C：$E = \frac12v_1^2 - GM/r_1$。$v_1 < \sqrt{2GM/r_1}$ 楕円、$=$ 放物線、$>$ 双曲線。
