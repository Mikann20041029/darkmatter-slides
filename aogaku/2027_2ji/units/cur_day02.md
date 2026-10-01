#### ① 板書

**連成振動とは**：複数の質点がバネで繋がれ、互いに影響しながら振動する系。運動方程式は**連立の線形微分方程式**になる。

**解く手順（これが全部）**

1. 各質点の運動方程式を書く。$m_i\ddot x_i = \sum_j(\text{バネの力})$
2. 行列で書く：$M\ddot{\boldsymbol x} = -K\boldsymbol x$（$M$ 質量行列、$K$ バネ行列）
3. **試行解** $\boldsymbol x = \boldsymbol A e^{i\omega t}$ を代入 → $(K - \omega^2M)\boldsymbol A = 0$
4. **永年方程式** $\det(K - \omega^2M) = 0$ を解く → $\omega^2$ が質点の数だけ出る
5. 各 $\omega$ について $(K - \omega^2M)\boldsymbol A = 0$ を解き、**振幅比 $\boldsymbol A$** を求める。これが**基準モード（固有ベクトル）**
6. 一般解 $= \sum_k(\text{定数}_k)\boldsymbol A_k\cos(\omega_kt + \phi_k)$。初期条件で定数を決める

**用語**
- **永年方程式** = 4の $\det = 0$。$\omega$ についての方程式そのもの。「$x = Ae^{i\omega t}$ と置く」ことではない
- **基準モード（基準振動）** = 全質点が同じ $\omega$ で振動する特別な運動パターン。振幅の**比**で表す
- **固有振動数** = 永年方程式の解 $\omega_k$

**近道**
- **対称性**があれば対称モード $(1, 1)$ と反対称モード $(1, -1)$ で分解できる
- **両端が自由**なら $\omega = 0$（全体の並進）が必ず解。$\omega^2$ で括れて次数が下がる

#### ② 過去問（上智 2026年秋 問3）

同じ質量 $m$ の質点1・2がある。質点1は壁とバネ定数 $2k$ のバネで、質点1と2はバネ定数 $k$ のバネで、質点2は壁とバネ定数 $k$ のバネで繋がれている。つり合いからの変位を $x_1, x_2$ とする。

1. 質点1の運動方程式を書け。
2. 質点2の運動方程式を書け。
3. $\ddot{\boldsymbol x} = -\dfrac{k}{m}A\boldsymbol x$ の形に書いたときの行列 $A$ を求めよ。
4. $A$ の固有値と固有振動数を求めよ。
5. 各固有値に対応する固有ベクトル（基準モード）を求めよ。
6. $t = 0$ で $x_1 = x_0$、$x_2 = 0$、両方静止。$x_1(t)$ を求めよ。

#### ③ 解説

**1.** 質点1に働く力：壁バネ $-2kx_1$、中間バネ $-k(x_1 - x_2)$。
$$m\ddot x_1 = -2kx_1 - k(x_1 - x_2) = -3kx_1 + kx_2$$

**2.** 質点2：中間バネ $-k(x_2 - x_1)$、壁バネ $-kx_2$。
$$m\ddot x_2 = kx_1 - 2kx_2$$

**3.** $\ddot{\boldsymbol x} = -\dfrac{k}{m}\begin{pmatrix}3 & -1\\-1 & 2\end{pmatrix}\boldsymbol x$。$A = \begin{pmatrix}3 & -1\\-1 & 2\end{pmatrix}$。

**4.** $\boldsymbol x = \boldsymbol Ae^{i\omega t}$ で $\omega^2\boldsymbol A = \dfrac{k}{m}A\boldsymbol A$。$\lambda = m\omega^2/k$ が $A$ の固有値。
$$\det(A - \lambda I) = (3-\lambda)(2-\lambda) - 1 = \lambda^2 - 5\lambda + 5 = 0 \quad\Rightarrow\quad \lambda_\pm = \frac{5\pm\sqrt5}{2}$$
$$\omega_\pm = \sqrt{\frac{5\pm\sqrt5}{2}\cdot\frac{k}{m}}$$

**5.** $(A - \lambda I)\boldsymbol v = 0$ の第1行：$(3 - \lambda)v_1 - v_2 = 0$ → $v_2 = (3 - \lambda)v_1$。
$$\lambda_+: \boldsymbol v_+ = \begin{pmatrix}1\\ \frac{1-\sqrt5}{2}\end{pmatrix}, \qquad \lambda_-: \boldsymbol v_- = \begin{pmatrix}1\\ \frac{1+\sqrt5}{2}\end{pmatrix}$$
$\boldsymbol v_+$ は $v_2 < 0$ で逆位相（高い方の振動数）、$\boldsymbol v_-$ は同位相（低い方）。

**6.** 一般解 $\boldsymbol x(t) = c_+\boldsymbol v_+\cos\omega_+t + c_-\boldsymbol v_-\cos\omega_-t$（静止から始まるので $\sin$ なし）。
$t = 0$：$c_+ + c_- = x_0$、$c_+\frac{1-\sqrt5}{2} + c_-\frac{1+\sqrt5}{2} = 0$。
第2式：$(c_+ + c_-)\frac12 + (c_- - c_+)\frac{\sqrt5}{2} = 0$ → $\frac{x_0}{2} = \frac{\sqrt5}{2}(c_+ - c_-)$ → $c_+ - c_- = \frac{x_0}{\sqrt5}$。
$$c_\pm = \frac{x_0}{2}\left(1 \pm \frac{1}{\sqrt5}\right), \qquad x_1(t) = \frac{x_0}{2}\left[\left(1 + \tfrac{1}{\sqrt5}\right)\cos\omega_+t + \left(1 - \tfrac{1}{\sqrt5}\right)\cos\omega_-t\right]$$

> **ここが山場**：手順4で $\lambda$ を出したら、必ず手順5で振幅比まで書く。青学本番では $\det$ を出して6次式のまま止まり、基準モードを書かなかった。

#### ④ 確認問題

**確認1-A**（青学本番の型）：質量 $m_1, m_2, m_3$ の3質点が一直線上にバネ定数 $k$ の2本のバネで $m_1 - m_2 - m_3$ と繋がれ、**両端は自由**。
(a) 3本の運動方程式を書け。(b) 永年方程式を立て、$\omega^2$ で括れることを示せ。(c) $\omega = 0$ の基準モードを求め、その物理的意味を述べよ。(d) $m_1 = m_3 = m$ のとき、残り2つの $\omega$ と基準モードを求めよ。

**確認1-B**：質量 $m$ の2質点が壁−$k$−$m$−$k$−$m$−$k$−壁（対称）。対称モードと反対称モードを仮定して固有振動数を求め、永年方程式を解いた結果と一致することを確かめよ。

**略解**
1-A (b)：$-k^2(m_1+m_2+m_3)\omega^2 + k(m_1m_2+m_2m_3+2m_1m_3)\omega^4 - m_1m_2m_3\omega^6 = 0$。(c) $\omega = 0$、$(1,1,1)$、全体の並進。(d) $\omega^2 = k/m$ で $(1, 0, -1)$、$\omega^2 = k(2m+m_2)/(mm_2)$ で対称モード。
1-B：対称 $(1,1)$：$\omega^2 = k/m$。反対称 $(1,-1)$：$\omega^2 = 3k/m$。

---
