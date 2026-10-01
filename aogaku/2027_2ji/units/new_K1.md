#### ① 板書

**単振動**：$m\ddot x = -kx$ → $\ddot x + \omega_0^2x = 0$、$\omega_0 = \sqrt{k/m}$。解は $x = A\cos\omega_0t + B\sin\omega_0t$。

**解き方の型（$x = e^{\lambda t}$ を代入する）**：線形の定数係数なら必ずこれ。$\lambda$ の2次方程式（特性方程式）を解いて、解を足す。

**減衰振動**：$m\ddot x = -kx - 2m\gamma\dot x$ → $\ddot x + 2\gamma\dot x + \omega_0^2x = 0$。$\lambda^2 + 2\gamma\lambda + \omega_0^2 = 0$ → $\lambda = -\gamma\pm\sqrt{\gamma^2 - \omega_0^2}$。

| 場合 | $\lambda$ | 一般解 | 見た目 |
| --- | --- | --- | --- |
| $\omega_0 > \gamma$（弱減衰） | $-\gamma\pm i\omega'$、$\omega' = \sqrt{\omega_0^2-\gamma^2}$ | $e^{-\gamma t}(A\cos\omega't + B\sin\omega't)$ | 振動しながら振幅が $e^{-\gamma t}$ で減る |
| $\omega_0 = \gamma$（臨界） | 重根 $-\gamma$ | $(A + Bt)e^{-\gamma t}$ | 振動せず最速で0へ |
| $\omega_0 < \gamma$（過減衰） | 実数2つ $-\gamma\pm\kappa$、$\kappa = \sqrt{\gamma^2-\omega_0^2}$ | $e^{-\gamma t}(A\cosh\kappa t + B\sinh\kappa t)$ | 振動せずゆっくり0へ |

**強制振動**：$\ddot x + 2\gamma\dot x + \omega_0^2x = f\cos\omega t$。十分時間が経った後の解（特解）は $x = A\cos(\omega t - \delta)$、
$$A = \frac{f}{\sqrt{(\omega_0^2-\omega^2)^2 + 4\gamma^2\omega^2}}, \qquad \tan\delta = \frac{2\gamma\omega}{\omega_0^2-\omega^2}$$
$\omega\simeq\omega_0$ で $A$ が最大（共鳴）。$\gamma\to0$ なら $A\to\infty$。

**定力が加わったバネ**：$m\ddot x = -kx - F$。平衡点 $x_{\rm eq} = -F/k$ にずれるだけ。$X = x - x_{\rm eq}$ とおけば普通の単振動。

**運動方程式からエネルギー保存を導く**：両辺に $\dot x$ を掛けて $\dfrac{d}{dt}(\cdots) = 0$ の形にする。$m\dot x\ddot x = \dfrac{d}{dt}\left(\frac12m\dot x^2\right)$、$kx\dot x = \dfrac{d}{dt}\left(\frac12kx^2\right)$、$F\dot x = \dfrac{d}{dt}(Fx)$。

#### ② 過去問

**(A)【上智 2025年春 問3・原文】**：$x$ 軸上を運動する質量 $m$ の物体が復元力 $-kx$ を受けて運動している。

1. 運動方程式を $\omega_0(=\sqrt{k/m})$ を用いて書け。
2. 解を $x = e^{\lambda t}$ と仮定し、$\lambda$ を決めて一般解を求めよ。
次に、復元力 $-kx$ と抵抗力 $-2m\gamma\dfrac{dx}{dt}$ がともに働く場合を考える。

3. 運動方程式を $\omega_0$ で書き、$x = e^{\lambda t}$ と仮定して $\lambda,\gamma,\omega_0$ の関係を求めよ。
4. $\omega_0 > \gamma$ の一般解を求め、$x$ の時間変化の概形を図示せよ。
5. $\omega_0 = \gamma$ の一般解を求めよ。

**(B)【上智 2025年秋 問3・原文】**：摩擦のない水平面上、バネ定数 $k$ のバネにつながった質量 $m$ の質点。自然長の位置を原点、伸びる向きに $x$ 軸。

1. 復元力に加えて $x$ 軸負の向きの一定の力 $F$ が常にかかる。(a) 運動方程式。(b) 原点で静止した質点に初速度 $v_0$（$x$ 正）を与えた。$t=0$ からの位置 $x(t)$。(c) 運動方程式を利用して力学的エネルギー保存則を導け。
2. $F$ の代わりに速度に比例する抵抗力 $Cv$（$C>0$）がかかる。(a) 運動方程式。(b) $x = x_0(>0)$ で静止させ手を離す。$x(t)$ を求めよ。$x(t) = Ae^{\alpha t}$ の形を利用してよい。

**(C)【上智 2025年秋 問2-1・原文】**：$\dfrac{d^2y}{dt^2} + 2\gamma\dfrac{dy}{dt} + \omega_0^2y = 0$ の一般解を $y = A\exp(-at)\cos(bt + \theta)$ と仮定する。$a, b$ を求めよ（$\omega_0 > \gamma > 0$）。

#### ③ 解説

**(A)**

1. $\ddot x + \omega_0^2x = 0$。
2. $\lambda^2 + \omega_0^2 = 0$ → $\lambda = \pm i\omega_0$。$x = C_1e^{i\omega_0t} + C_2e^{-i\omega_0t} = A\cos\omega_0t + B\sin\omega_0t$。
3. $\ddot x + 2\gamma\dot x + \omega_0^2x = 0$。$\lambda^2 + 2\gamma\lambda + \omega_0^2 = 0$ → $\lambda = -\gamma\pm\sqrt{\gamma^2-\omega_0^2}$。
4. $\lambda = -\gamma\pm i\omega'$、$\omega' = \sqrt{\omega_0^2-\gamma^2}$。$x = e^{-\gamma t}(A\cos\omega't + B\sin\omega't)$。概形：$\pm Ae^{-\gamma t}$ の2本の曲線（包絡線）を描き、その間で周期 $2\pi/\omega'$ の振動を描く。
5. 重根 $\lambda = -\gamma$。$x = (A + Bt)e^{-\gamma t}$。**重根のときは $t$ を掛けたものが2つ目の解**（これを忘れると解が1つ足りない）。

**(B)**
1.(a) $m\ddot x = -kx - F$。
(b) 平衡点 $x_{\rm eq} = -F/k$。$X = x + F/k$ とおくと $m\ddot X = -kX$。初期条件 $X(0) = F/k$、$\dot X(0) = v_0$：
$$X = \frac Fk\cos\omega_0t + \frac{v_0}{\omega_0}\sin\omega_0t \quad\Rightarrow\quad x(t) = \frac Fk(\cos\omega_0t - 1) + \frac{v_0}{\omega_0}\sin\omega_0t$$
検算：$t=0$ で $x = 0$ ✓、$\dot x(0) = v_0$ ✓。
(c) 両辺に $\dot x$ を掛ける：$m\dot x\ddot x = -kx\dot x - F\dot x$ → $\dfrac{d}{dt}\left[\frac12m\dot x^2 + \frac12kx^2 + Fx\right] = 0$。よって $\frac12mv^2 + \frac12kx^2 + Fx = $ 一定。（$Fx$ は一定力のポテンシャル）
2.(a) $m\ddot x = -kx - C\dot x$。
(b) $x = Ae^{\alpha t}$：$m\alpha^2 + C\alpha + k = 0$ → $\alpha = \dfrac{-C\pm\sqrt{C^2 - 4mk}}{2m}$。$\gamma = C/2m$、$\omega_0^2 = k/m$ とおく。

- $C^2 < 4mk$（弱減衰）：$\alpha = -\gamma\pm i\omega'$。$x = e^{-\gamma t}(A\cos\omega't + B\sin\omega't)$。$x(0) = x_0$ → $A = x_0$。$\dot x(0) = 0$ → $-\gamma A + \omega'B = 0$ → $B = \gamma x_0/\omega'$。
$$x(t) = x_0e^{-\gamma t}\left(\cos\omega't + \frac{\gamma}{\omega'}\sin\omega't\right)$$

- $C^2 > 4mk$（過減衰）：$\alpha = -\gamma\pm\kappa$、$x = x_0e^{-\gamma t}\left(\cosh\kappa t + \frac{\gamma}{\kappa}\sinh\kappa t\right)$。
（答案には場合分けを書く。片方だけだと減点）

**(C)** $y = Ae^{-at}\cos(bt+\theta)$ を代入。$\dot y = Ae^{-at}[-a\cos(\cdot) - b\sin(\cdot)]$、$\ddot y = Ae^{-at}[(a^2-b^2)\cos(\cdot) + 2ab\sin(\cdot)]$。代入して $\cos$ と $\sin$ の係数がそれぞれ0：
$\cos$：$a^2 - b^2 - 2\gamma a + \omega_0^2 = 0$、$\sin$：$2ab - 2\gamma b = 0$ → $a = \gamma$。前者に入れて $b^2 = \omega_0^2 - \gamma^2$。**$a = \gamma$、$b = \sqrt{\omega_0^2-\gamma^2}$**。（(A)4と同じ答え。上智は同じ型を3年連続で出している）

> **落とし穴**：①減衰項の係数が $2m\gamma$ か $C$ かで $\gamma$ の定義が変わる。問題の記号に合わせる。②初期条件「静止させ手を離す」＝ $\dot x(0) = 0$、$x(0) = x_0$。③重根で $t e^{\lambda t}$ を忘れる。

#### ④ 練習問題

**練習K1-A【立教 2023年春 大問1・原文】**：図のように、長さ $R$ の軽い糸の先に質量 $m$ の小球をつけた振り子の、糸が張った状態での鉛直面内の運動を考える。ただし、重力加速度の大きさを $g$ とし、糸の受ける空気抵抗は無視してよい。以下の問いに答えよ。
まず、小球の受ける空気抵抗を無視できる場合を考える。
(a) この振り子の運動方程式を、$\theta$ に関する微分方程式として具体的に書き下せ。
以下の問いでは $|\theta|\ll1$ として角度 $\theta$ に関して1次までの近似で扱えるものとする。
(b) 前問の運動方程式は単振動を表す形となるが、その角振動数 $\Omega_0$ を求めよ。
次いで、小球の受ける空気抵抗を考慮する場合を考える。
(c) 小球 $m$ の速度が $\boldsymbol v$ の時、空気抵抗力が $-\rho\boldsymbol v$ と書けるとする（$\rho$ は正の定数）。この時、運動方程式を書け。解答は $g$ を使わず必要に応じて $\Omega_0$ を含めて表せ。
(d) 前問に加えて、外力による支点回りの周期的なトルク $a\cos\Omega t$ が時刻 $t$ に、$\theta$ の正の向きにはたらく場合を考える。$a$ はトルクの次元を持つ定数、$\Omega$ は角振動数を表す定数である。この時、運動方程式を書け。解答は $g$ を使わず必要に応じて $\Omega_0$ を含めて表せ。
(e) 一般に時間 $t$ の関数 $x(t)$ が微分方程式 $\ddot x + 2\beta\dot x + \omega_0^2x = A\cos\omega t$ を満たすとき、これには特殊解 $x_p(t) = D\cos(\omega t - \delta)$ があり、$\tan\delta = \dfrac{2\beta\omega}{\omega_0^2-\omega^2}$ …(1)、$D = \dfrac{A}{\sqrt{(\omega_0^2-\omega^2)^2 + 4\omega^2\beta^2}}$ …(2) である。ここで $\beta,\omega_0,\omega,A$ は定数であり、この微分方程式はよく知られた強制振動の運動方程式が満たすものである。前問の運動方程式において、角振動数 $\Omega$ を様々な値に変える場合を考える。この時、特殊解 $x_p(t)$ に対応する $\theta(t)$ の解の振動の振幅を最大にする $\Omega$ を共鳴振動数 $\Omega_R$ と呼ぶ。共鳴が起きる条件 $dD/d\Omega|_{\Omega=\Omega_R} = 0$ を満たす $\Omega_R$ の値と、共鳴が起きる為に $\rho$ が満たすべき条件を、$g$ を使わず必要に応じて $\Omega_0$ を含めて表せ。

**練習K1-B**：$\ddot x + 2\gamma\dot x + \omega_0^2x = 0$ で、$\gamma = \omega_0$（臨界減衰）、$x(0) = 0$、$\dot x(0) = v_0$。$x(t)$ と、$x$ が最大になる時刻。

**練習K1-C**：$m\ddot x = -kx + F$（$F$ は $x$ 正向きの一定力）。$x(0) = 0$、$\dot x(0) = 0$ のとき $x(t)$ と、$x$ の最大値。

**略解**
K1-A：(a) 接線方向：$mR\ddot\theta = -mg\sin\theta$ → $\ddot\theta + \dfrac gR\sin\theta = 0$。(b) $\sin\theta\simeq\theta$ で $\Omega_0 = \sqrt{g/R}$。(c) 速さ $R\dot\theta$、抵抗の接線成分 $-\rho R\dot\theta$：$mR\ddot\theta = -mgR\theta/R\cdot R - \rho R\dot\theta$ → $\ddot\theta + \dfrac\rho m\dot\theta + \Omega_0^2\theta = 0$。(d) 支点まわりのトルクの式（$mR^2\ddot\theta = $ トルクの和）に $a\cos\Omega t$ を足す：$\ddot\theta + \dfrac\rho m\dot\theta + \Omega_0^2\theta = \dfrac{a}{mR^2}\cos\Omega t$。(e) $\beta = \rho/2m$、$\omega_0 = \Omega_0$。$D$ の分母の中身 $f(\Omega) = (\Omega_0^2-\Omega^2)^2 + 4\beta^2\Omega^2$ を最小化：$f' = -4\Omega(\Omega_0^2-\Omega^2) + 8\beta^2\Omega = 0$ → $\Omega_R^2 = \Omega_0^2 - 2\beta^2 = \Omega_0^2 - \dfrac{\rho^2}{2m^2}$。共鳴が起きる（$\Omega_R$ が実数）条件：$\rho < \sqrt2\,m\Omega_0$。
K1-B：$x = (A + Bt)e^{-\gamma t}$、$A = 0$、$B = v_0$。$x = v_0te^{-\gamma t}$。$\dot x = v_0e^{-\gamma t}(1 - \gamma t) = 0$ → $t = 1/\gamma$、$x_{\max} = v_0/(e\gamma)$。
K1-C：平衡点 $F/k$。$x = \dfrac Fk(1 - \cos\omega_0t)$。最大値 $2F/k$（平衡点の2倍まで行く）。
