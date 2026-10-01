#### 【A】力学 §5 球面上の滑落と離れる条件（立教2012春・2020夏）


#### ① 板書

**型**：滑らかな球面（半径 $R$）の頂上付近から質点が滑り落ちる。
1. **エネルギー保存**で速さ $v(\theta)$
2. **向心方向の運動方程式** $m\dfrac{v^2}{R} = mg\cos\theta - N$ で垂直抗力 $N(\theta)$
3. **$N = 0$ になる角** $\theta_1$ が離れる点

**基本結果**（頂上から静かに滑る場合）：$v^2 = 2gR(1 - \cos\theta)$、$N = mg(3\cos\theta - 2)$、$\cos\theta_1 = 2/3$。

**バリエーション**
- 初速 $v_0$ がある → $\cos\theta_1 = \dfrac23 + \dfrac{v_0^2}{3gR}$。$v_0^2 \ge gR$ なら最初から離れる
- 剛体（球・円柱）が転がる → 運動エネルギーに回転分が加わり、離れる角が変わる（青学2-6の棒と同じ構造）

#### ② 過去問（立教 2012年春 大問1）

半径 $R$ の球面上に置かれた質量 $m$ の質点が、球の頂上から初速度 $v_0$ で滑り落ちる。重力加速度 $g$、摩擦なし。
(a) 頂上から角度 $\theta_0$ 滑り降りたときの速さ $v_1$。(b) 角度 $\theta_0$ での垂直抗力 $N$。(c) 球面から離れる角 $\theta_1$。(d) 初速度 $v_0$ がある値以上だと頂上で直ちに離れる。その値。

#### ③ 解説

(a) $\frac12mv_1^2 = \frac12mv_0^2 + mgR(1 - \cos\theta_0)$ → $v_1^2 = v_0^2 + 2gR(1 - \cos\theta_0)$。
(b) 向心方向：$\dfrac{mv_1^2}{R} = mg\cos\theta_0 - N$ →
$$N = mg\cos\theta_0 - \frac{m}{R}\left[v_0^2 + 2gR(1 - \cos\theta_0)\right] = mg(3\cos\theta_0 - 2) - \frac{mv_0^2}{R}$$
(c) $N = 0$：$\cos\theta_1 = \dfrac23 + \dfrac{v_0^2}{3gR}$。
(d) $\theta_1 = 0$ すなわち $\cos\theta_1 = 1$：$v_0^2 = gR$。$v_0 \ge \sqrt{gR}$ なら頂上で $N \le 0$。

#### ④ 確認問題

**確認5-A**：半径 $R$ の球面の頂上から、半径 $r$ 質量 $m$ の一様な小球（$I = \frac25mr^2$）が静かに転がり落ちる（滑らない）。離れる角 $\cos\theta_1$ を求めよ。

**確認5-B**：半径 $R$ の滑らかな**半球の内面**の縁から質点を静かに放す。最下点での速さと垂直抗力。

**略解**
5-A：エネルギー $\frac12mv^2 + \frac12\cdot\frac25mr^2\cdot\frac{v^2}{r^2} = \frac{7}{10}mv^2 = mg(R+r)(1-\cos\theta)$。$N = 0$ で $\frac{mv^2}{R+r} = mg\cos\theta$。→ $\cos\theta_1 = \dfrac{10}{17}$。
5-B：$v = \sqrt{2gR}$、$N = mg + \dfrac{mv^2}{R} = 3mg$。

#### 【B】数学 §5 1階微分方程式（変数分離・線形）（上智2026春 問2(3)／力学全般で使う）


#### ① 板書

**変数分離型** $\dfrac{dy}{dx} = f(x)g(y)$ → $\displaystyle\int\frac{dy}{g(y)} = \int f(x)dx + C$。

**1階線形** $y' + P(x)y = Q(x)$ → 積分因子 $e^{\int P\,dx}$ をかける：$\left(ye^{\int P}\right)' = Qe^{\int P}$。
物理での頻出形：$m\dot v = -bv + F$（減衰・可変質量）、$\dot N = -\lambda N$（崩壊）、$RC$ 回路。

**2階定数係数** $\ddot x + 2\gamma\dot x + \omega_0^2x = 0$ → $x = e^{\lambda t}$ で $\lambda = -\gamma\pm\sqrt{\gamma^2 - \omega_0^2}$。減衰振動（$\gamma < \omega_0$）、臨界（$=$、解は $(A + Bt)e^{-\gamma t}$）、過減衰。上智の問3は毎回これ。

#### ② 過去問（上智 2026年春 問2(3)）

微分方程式 $4x^2y\dfrac{dy}{dx} - x(y^2 + 1) = 0$ について、$y$ を $x$ の関数として解いたときの一般解を求めよ。

#### ③ 解説

$x \ne 0$ で割る：$4xy\dfrac{dy}{dx} = y^2 + 1$ → $\dfrac{4y\,dy}{y^2 + 1} = \dfrac{dx}{x}$。
左辺：$\int\dfrac{4y}{y^2+1}dy = 2\ln(y^2 + 1)$。右辺：$\ln|x| + C$。
$$2\ln(y^2 + 1) = \ln|x| + C \quad\Rightarrow\quad (y^2 + 1)^2 = C'|x| \quad\Rightarrow\quad y^2 = \sqrt{C'|x|} - 1$$
一般解 $y = \pm\sqrt{\sqrt{C'|x|} - 1}$（$C' > 0$）。

#### ④ 確認問題

**確認5-A**（上智2025秋 問3の型）：$m\ddot x = -kx - C\dot x$ の一般解を $C^2 > 4mk$（過減衰）の場合に求めよ。

**確認5-B**：$\dfrac{dy}{dx} = \dfrac{y}{x} + x^2$。積分因子で解け。

**略解**
5-A：$x = Ae^{\lambda_+t} + Be^{\lambda_-t}$、$\lambda_\pm = \dfrac{-C\pm\sqrt{C^2 - 4mk}}{2m}$。
5-B：$y' - y/x = x^2$。積分因子 $1/x$：$(y/x)' = x$ → $y = x^3/2 + Cx$。
