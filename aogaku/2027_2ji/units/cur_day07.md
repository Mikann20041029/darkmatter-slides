#### ① 板書

**ラグランジアンからハミルトニアンへ**

| 段階 | 式 |
| --- | --- |
| ラグランジアン | $L(q, \dot q, t) = T - V$ |
| **正準運動量** | $p \equiv \dfrac{\partial L}{\partial\dot q}$ |
| **ハミルトニアン**（ルジャンドル変換） | $H(q, p, t) \equiv p\dot q - L$。**$\dot q$ を消去して $p$ で書く** |
| **正準方程式** | $\dot q = \dfrac{\partial H}{\partial p}, \qquad \dot p = -\dfrac{\partial H}{\partial q}$ |

**普通の場合** $L = \frac12m\dot q^2 - V(q)$ → $p = m\dot q$ → $H = \dfrac{p^2}{2m} + V(q)$ = 全エネルギー。

**ポイント**
- $H$ は必ず $(q, p)$ で書く。$\dot q$ が残っていたら未完成
- $L$ が $t$ を陽に含まなければ $H$ は保存量（$dH/dt = 0$）
- 循環座標（$L$ に $q$ が入らない）→ $\dot p = 0$ → $p$ 保存
- $L$ の運動項の係数が $q$ に依存するとき（極座標、宇宙モデルなど）、$p$ も $q$ に依存する。**丁寧にルジャンドル変換する**

**ポアソン括弧**：$\{f, g\} = \dfrac{\partial f}{\partial q}\dfrac{\partial g}{\partial p} - \dfrac{\partial f}{\partial p}\dfrac{\partial g}{\partial q}$、任意の物理量の時間発展 $\dot f = \{f, H\}$。

#### ② 過去問（立教 2011年春 大問4）

真空のエネルギーを持つ宇宙のモデル。スケール因子 $a(t)$ に対しラグランジアンが
$$L = \frac{3\pi c^4}{4G}\left\{-a\left(\frac{\dot a}{c}\right)^2 + a - \frac{a^3}{l^2}\right\}$$
（$G$ 重力定数、$c$ 光速、$l$ は真空のエネルギー密度で決まる定数）。

(a) 正準運動量 $p = \partial L/\partial\dot a$ を求め、ハミルトニアン $H$ を $a, p$ で表せ。
(b) 正準方程式を書け。
(c) 一般相対論の要請から $H = 0$ である。このとき $\dot a^2$ を $a$ で表せ。
(d) $a \gg l$ での $a(t)$ の振る舞いを求めよ。

#### ③ 解説

**(a)** $L$ の $\dot a$ 依存は第1項のみ。
$$p = \frac{\partial L}{\partial\dot a} = \frac{3\pi c^4}{4G}\cdot\left(-\frac{2a\dot a}{c^2}\right) = -\frac{3\pi c^2}{2G}a\dot a$$
逆に解いて $\dot a = -\dfrac{2G}{3\pi c^2}\dfrac{p}{a}$。
$$H = p\dot a - L = -\frac{2G}{3\pi c^2}\frac{p^2}{a} - \frac{3\pi c^4}{4G}\left\{-\frac{a}{c^2}\cdot\frac{4G^2p^2}{9\pi^2c^4a^2} + a - \frac{a^3}{l^2}\right\}$$
第2項の中の $\dot a^2$ 項を整理：$\dfrac{3\pi c^4}{4G}\cdot\dfrac{a}{c^2}\cdot\dfrac{4G^2p^2}{9\pi^2c^4a^2} = \dfrac{Gp^2}{3\pi c^2a}$。よって
$$H = -\frac{2Gp^2}{3\pi c^2a} + \frac{Gp^2}{3\pi c^2a} - \frac{3\pi c^4}{4G}\left(a - \frac{a^3}{l^2}\right) = -\frac{Gp^2}{3\pi c^2a} - \frac{3\pi c^4}{4G}\left(a - \frac{a^3}{l^2}\right)$$

**(b)** $\dot a = \dfrac{\partial H}{\partial p} = -\dfrac{2Gp}{3\pi c^2a}$（(a) と一致 ✓）、$\dot p = -\dfrac{\partial H}{\partial a} = -\dfrac{Gp^2}{3\pi c^2a^2} + \dfrac{3\pi c^4}{4G}\left(1 - \dfrac{3a^2}{l^2}\right)$。

**(c)** $H = 0$ に $p = -\dfrac{3\pi c^2}{2G}a\dot a$ を戻す：$-\dfrac{G}{3\pi c^2a}\cdot\dfrac{9\pi^2c^4a^2\dot a^2}{4G^2} = -\dfrac{3\pi c^2a\dot a^2}{4G}$。
$$-\frac{3\pi c^2a\dot a^2}{4G} = \frac{3\pi c^4}{4G}\left(a - \frac{a^3}{l^2}\right) \quad\Rightarrow\quad \dot a^2 = c^2\left(\frac{a^2}{l^2} - 1\right)$$
（フリードマン方程式の一形。$a > l$ で実解）

**(d)** $a \gg l$：$\dot a \simeq ca/l$ → $a \propto e^{ct/l}$。指数関数的膨張（ド・ジッター宇宙）。

> **注意**：符号が負の運動項でも手順は同じ。$p$ を出す → $\dot q$ を $p$ で書く → $H = p\dot q - L$ に代入。機械的にやる。

#### ④ 確認問題

**確認2-A**：中心力場 $V(r)$ 中の質点。極座標で $L = \frac12m(\dot r^2 + r^2\dot\theta^2) - V(r)$。
(a) $p_r, p_\theta$ を求めよ。(b) $H(r, \theta, p_r, p_\theta)$ を求めよ。(c) 正準方程式から $\dot p_\theta = 0$ を示し、$p_\theta$ の物理的意味を述べよ。(d) $\{p_\theta, H\} = 0$ を確かめよ。

**確認2-B**：$L = \frac12\dot q^2 e^{\gamma t} - \frac12\omega^2q^2e^{\gamma t}$（減衰振動のラグランジアン）。$p$、$H$ を求め、$H$ が保存しない理由を述べよ。

**略解**
2-A：$p_r = m\dot r$、$p_\theta = mr^2\dot\theta$、$H = \dfrac{p_r^2}{2m} + \dfrac{p_\theta^2}{2mr^2} + V(r)$。$\theta$ が循環座標 → $p_\theta$（角運動量）保存。
2-B：$p = \dot qe^{\gamma t}$、$H = \dfrac{p^2}{2}e^{-\gamma t} + \dfrac12\omega^2q^2e^{\gamma t}$。$H$ が $t$ を陽に含むので保存しない。

---
