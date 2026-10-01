数学 §5 1階微分方程式（変数分離・線形）（上智2026春 問2(3)／力学全般で使う）


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
