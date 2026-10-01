# 力学 演習書 — 青学対策に足りない5分野

既習（中心力・ラグランジアン・剛体の慣性モーメント・減衰強制振動）はやらない。**足りない5つだけ。**

各分野：① 板書（概念）→ ② 過去問 → ③ 解説 → ④ 確認問題

作成 2026-09-12

---

## 1｜連成振動と基準モード（青学本番で落とした・上智2026秋）

### ① 板書

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

### ② 過去問（上智 2026年秋 問3）

同じ質量 $m$ の質点1・2がある。質点1は壁とバネ定数 $2k$ のバネで、質点1と2はバネ定数 $k$ のバネで、質点2は壁とバネ定数 $k$ のバネで繋がれている。つり合いからの変位を $x_1, x_2$ とする。

1. 質点1の運動方程式を書け。
2. 質点2の運動方程式を書け。
3. $\ddot{\boldsymbol x} = -\dfrac{k}{m}A\boldsymbol x$ の形に書いたときの行列 $A$ を求めよ。
4. $A$ の固有値と固有振動数を求めよ。
5. 各固有値に対応する固有ベクトル（基準モード）を求めよ。
6. $t = 0$ で $x_1 = x_0$、$x_2 = 0$、両方静止。$x_1(t)$ を求めよ。

### ③ 解説

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

### ④ 確認問題

**確認1-A**（青学本番の型）：質量 $m_1, m_2, m_3$ の3質点が一直線上にバネ定数 $k$ の2本のバネで $m_1 - m_2 - m_3$ と繋がれ、**両端は自由**。
(a) 3本の運動方程式を書け。(b) 永年方程式を立て、$\omega^2$ で括れることを示せ。(c) $\omega = 0$ の基準モードを求め、その物理的意味を述べよ。(d) $m_1 = m_3 = m$ のとき、残り2つの $\omega$ と基準モードを求めよ。

**確認1-B**：質量 $m$ の2質点が壁−$k$−$m$−$k$−$m$−$k$−壁（対称）。対称モードと反対称モードを仮定して固有振動数を求め、永年方程式を解いた結果と一致することを確かめよ。

**略解**
1-A (b)：$-k^2(m_1+m_2+m_3)\omega^2 + k(m_1m_2+m_2m_3+2m_1m_3)\omega^4 - m_1m_2m_3\omega^6 = 0$。(c) $\omega = 0$、$(1,1,1)$、全体の並進。(d) $\omega^2 = k/m$ で $(1, 0, -1)$、$\omega^2 = k(2m+m_2)/(mm_2)$ で対称モード。
1-B：対称 $(1,1)$：$\omega^2 = k/m$。反対称 $(1,-1)$：$\omega^2 = 3k/m$。

---

## 2｜正準形式（ハミルトン力学）（立教2011春・2020夏）

### ① 板書

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

### ② 過去問（立教 2011年春 大問4）

真空のエネルギーを持つ宇宙のモデル。スケール因子 $a(t)$ に対しラグランジアンが
$$L = \frac{3\pi c^4}{4G}\left\{-a\left(\frac{\dot a}{c}\right)^2 + a - \frac{a^3}{l^2}\right\}$$
（$G$ 重力定数、$c$ 光速、$l$ は真空のエネルギー密度で決まる定数）。

(a) 正準運動量 $p = \partial L/\partial\dot a$ を求め、ハミルトニアン $H$ を $a, p$ で表せ。
(b) 正準方程式を書け。
(c) 一般相対論の要請から $H = 0$ である。このとき $\dot a^2$ を $a$ で表せ。
(d) $a \gg l$ での $a(t)$ の振る舞いを求めよ。

### ③ 解説

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

### ④ 確認問題

**確認2-A**：中心力場 $V(r)$ 中の質点。極座標で $L = \frac12m(\dot r^2 + r^2\dot\theta^2) - V(r)$。
(a) $p_r, p_\theta$ を求めよ。(b) $H(r, \theta, p_r, p_\theta)$ を求めよ。(c) 正準方程式から $\dot p_\theta = 0$ を示し、$p_\theta$ の物理的意味を述べよ。(d) $\{p_\theta, H\} = 0$ を確かめよ。

**確認2-B**：$L = \frac12\dot q^2 e^{\gamma t} - \frac12\omega^2q^2e^{\gamma t}$（減衰振動のラグランジアン）。$p$、$H$ を求め、$H$ が保存しない理由を述べよ。

**略解**
2-A：$p_r = m\dot r$、$p_\theta = mr^2\dot\theta$、$H = \dfrac{p_r^2}{2m} + \dfrac{p_\theta^2}{2mr^2} + V(r)$。$\theta$ が循環座標 → $p_\theta$（角運動量）保存。
2-B：$p = \dot qe^{\gamma t}$、$H = \dfrac{p^2}{2}e^{-\gamma t} + \dfrac12\omega^2q^2e^{\gamma t}$。$H$ が $t$ を陽に含むので保存しない。

---

## 3｜可変質量系（ロケット・鎖）（立教2025夏・上智2026春）

### ① 板書

**原則**：質量が変わる系では $F = ma$ ではなく**運動量の変化** $\dfrac{d\boldsymbol p}{dt} = \boldsymbol F_{\rm ext}$ を使う。ただし「系」の取り方を固定して、**出入りする質量が持ち去る（持ち込む）運動量を数える。**

**ロケット**：時刻 $t$ に質量 $M(t)$、速度 $V(t)$。$dt$ の間に質量 $dm = \alpha\,dt$ をロケットに対して速さ $v$ で後方へ放出。
- $t$：運動量 $MV$
- $t + dt$：ロケット $(M - dm)(V + dV)$ ＋ 燃料 $dm(V - v)$
- 外力なしで等置し、2次の微小量を落とす：$M\,dV = v\,dm$
$$M\frac{dV}{dt} = \alpha v \quad(\text{推力} = \alpha v), \qquad M(t) = M_0 - \alpha t$$
$$V(t) = V_0 + v\ln\frac{M_0}{M(t)} \quad(\text{ツィオルコフスキーの式})$$

**鎖**：机の端から垂れた長さ $s$、線密度 $\lambda$。垂れた部分だけを系とすると、机上から質量 $\lambda\,ds$ が速度0で流入。
$$\frac{d}{dt}(\lambda sv) = \lambda sg$$
$\dfrac{d}{dt} = v\dfrac{d}{ds}$ に直して $s$ で積分するのが定石。

### ② 過去問

**(A) 立教 2025年夏 大問1**：重力・抵抗のない宇宙空間で速さ $V_0$ で等速直線運動しているロケットが $t = 0$ から加速。時刻 $t$ の質量 $M(t)$、速さ $V(t)$。燃料はロケットに対して一定の速さ $v$ で逆向きに、1秒あたり一定質量 $\alpha = -dM/dt$ で噴出。
(a) $M(t)$ を求めよ。(b) $V$ の従う微分方程式を導け。(c) $V(t)$ を求めよ。(d) 質量が半分になったときの速さ。

**(B) 上智 2026年春 問3-2**：線密度 $\lambda$ の鎖が机の端に静止。わずかに押すと落下開始。垂れた長さ $s$、速さ $v$。空気抵抗なし。
(1) 垂れた部分の運動方程式を書け。(2) $v$ と $s$ の関係を求めよ。$\dfrac{d}{dt} = \dfrac{ds}{dt}\dfrac{d}{ds}$、$2sv\dfrac{d}{ds}(sv) = \dfrac{d}{ds}(sv)^2$ を使ってよい。(3) 長さ $s$ になるまでに失った力学的エネルギー。

### ③ 解説

**(A)**
(a) $M(t) = M_0 - \alpha t$。
(b) 板書の導出通り $M\dfrac{dV}{dt} = \alpha v$。
(c) $\dfrac{dV}{dt} = \dfrac{\alpha v}{M_0 - \alpha t}$。積分：$V - V_0 = -v\ln(M_0 - \alpha t) + v\ln M_0 = v\ln\dfrac{M_0}{M_0 - \alpha t}$。
(d) $M = M_0/2$：$V = V_0 + v\ln 2$。

**(B)**
(1) 垂れた部分の運動量 $\lambda sv$、重力 $\lambda sg$：$\dfrac{d}{dt}(\lambda sv) = \lambda sg$、すなわち $\dfrac{d(sv)}{dt} = sg$。
(2) $\dfrac{d(sv)}{dt} = v\dfrac{d(sv)}{ds} = sg$。両辺に $2sv$ をかけると $\dfrac{d}{ds}(sv)^2 = 2gs^2$。積分（$s = 0$ で $v = 0$）：$(sv)^2 = \dfrac{2gs^3}{3}$ → $v^2 = \dfrac{2gs}{3}$。
（自由落下なら $v^2 = 2gs$。鎖は机上の部分を引きずるので遅い）
(3) 運動エネルギー $\frac12\lambda s\cdot v^2 = \frac12\lambda s\cdot\frac{2gs}{3} = \dfrac{\lambda gs^2}{3}$。失った位置エネルギー：垂れた部分の重心が $s/2$ 下がったので $\lambda sg\cdot\frac{s}{2} = \dfrac{\lambda gs^2}{2}$。差 $\dfrac{\lambda gs^2}{2} - \dfrac{\lambda gs^2}{3} = \dfrac{\lambda gs^2}{6}$ が失われた（机の端での非弾性的な引き込み）。

### ④ 確認問題

**確認3-A**：雨滴が落下しながら霧を取り込み質量が増える。$\dfrac{dm}{dt} = km$（$k$ 定数）、霧は静止。重力のみ。(a) 運動方程式を書け。(b) 終端速度があるか。あれば求めよ。

**確認3-B**：ロケットが地表から鉛直に打ち上がる（重力 $g$ 一定、空気抵抗なし）。$M\dfrac{dV}{dt} = \alpha v - Mg$ を導き、$V(t)$ を求めよ。離陸の条件は何か。

**略解**
3-A：$\dfrac{d(mv)}{dt} = mg$ → $m\dot v + kmv = mg$ → $\dot v = g - kv$。終端速度 $g/k$。
3-B：$V = v\ln\dfrac{M_0}{M_0 - \alpha t} - gt$。離陸には $\alpha v > M_0g$。

---

## 4｜剛体の角運動量保存（立教2011春・2020春）

### ① 板書

**剛体の角運動量**：固定軸まわりで $L = I\omega$。外力のモーメントがゼロなら $L$ 保存。

**注意点**
- 質量分布が変わると $I$ が変わる。$L = I\omega$ 保存 → $\omega$ が変わる（フィギュアスケートの回転）
- そのとき**運動エネルギーは保存しない**。$E = L^2/(2I)$ なので $I$ が減ると $E$ が増える。増分は内力（腕を引き込む力）の仕事
- **衝突**の瞬間：撃力は大きいが時間が短いので、**衝突点まわりの角運動量**は保存する（撃力のモーメントがゼロ）。重心の角運動量は保存しない
- 点 $A$ まわりの角運動量 $= $ 重心の運動による分 $\boldsymbol r_G\times M\boldsymbol v_G$ ＋ 重心まわりの自転 $I_G\omega$

### ② 過去問

**(A) 立教 2011年春 大問1**：両端に質量 $m$ の質点がついた長さ $l$ の軽い棒が、中心を通り紙面に垂直な軸まわりに角速度 $\omega_0$ で回転。
(a) $I_0$。(b) $L_0$。(c) $E_0$。(d) 二つの質点を回転中心へ、中心からの距離がそれぞれ $l/4$ になるまで引き込んだ。角速度 $\omega_1$ と運動エネルギー $E_1$。(e) $E_1 - E_0$ は何に由来するか。

**(B) 立教 2020年春 大問1**：質量 $M$ 半径 $R$ の一様な球が粗い水平面上を滑らずに転がり、中心は速さ $v_0$ で直進。高さ $h$（$0 < h < R$）の段差に衝突し、衝突点 $A$ まわりで滑らずに回転を始める。$I = \frac25MR^2$。
(a) 衝突の瞬間の $A$ まわりの角運動量 $L$ と角速度 $\omega$。(b) $\overrightarrow{AO}$ と鉛直上向きのなす角を $\theta$ として、エネルギー保存の式。(c) $A$ から受ける抗力 $T$ を $\theta, \omega$ で。(d) 段差を越える条件を $v_0$ で。

### ③ 解説

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

### ④ 確認問題

**確認4-A**：半径 $a$ 質量 $M$ の一様な円板が中心軸まわりに $\omega_0$ で回転。縁に質量 $m$ の粘土を静かに落として付着させた。付着後の角速度と失われたエネルギー。

**確認4-B**：長さ $l$ 質量 $M$ の一様な棒が一端を軸に鉛直面内で自由に回転できる。水平に静止した状態から放す。最下点での角速度と、軸が棒に及ぼす力。

**略解**
4-A：$\omega = \dfrac{Ma^2/2}{Ma^2/2 + ma^2}\omega_0 = \dfrac{M}{M + 2m}\omega_0$。$\Delta E = -\frac12\cdot\frac{Ma^2}{2}\omega_0^2\cdot\frac{2m}{M+2m}$。
4-B：$I = Ml^2/3$、$\frac12I\omega^2 = Mg\frac{l}{2}$ → $\omega = \sqrt{3g/l}$。最下点で軸の力 $= Mg + M\frac{l}{2}\omega^2 = \frac52Mg$。

---

## 5｜球面上の滑落と離れる条件（立教2012春・2020夏）

### ① 板書

**型**：滑らかな球面（半径 $R$）の頂上付近から質点が滑り落ちる。
1. **エネルギー保存**で速さ $v(\theta)$
2. **向心方向の運動方程式** $m\dfrac{v^2}{R} = mg\cos\theta - N$ で垂直抗力 $N(\theta)$
3. **$N = 0$ になる角** $\theta_1$ が離れる点

**基本結果**（頂上から静かに滑る場合）：$v^2 = 2gR(1 - \cos\theta)$、$N = mg(3\cos\theta - 2)$、$\cos\theta_1 = 2/3$。

**バリエーション**
- 初速 $v_0$ がある → $\cos\theta_1 = \dfrac23 + \dfrac{v_0^2}{3gR}$。$v_0^2 \ge gR$ なら最初から離れる
- 剛体（球・円柱）が転がる → 運動エネルギーに回転分が加わり、離れる角が変わる（青学2-6の棒と同じ構造）

### ② 過去問（立教 2012年春 大問1）

半径 $R$ の球面上に置かれた質量 $m$ の質点が、球の頂上から初速度 $v_0$ で滑り落ちる。重力加速度 $g$、摩擦なし。
(a) 頂上から角度 $\theta_0$ 滑り降りたときの速さ $v_1$。(b) 角度 $\theta_0$ での垂直抗力 $N$。(c) 球面から離れる角 $\theta_1$。(d) 初速度 $v_0$ がある値以上だと頂上で直ちに離れる。その値。

### ③ 解説

(a) $\frac12mv_1^2 = \frac12mv_0^2 + mgR(1 - \cos\theta_0)$ → $v_1^2 = v_0^2 + 2gR(1 - \cos\theta_0)$。
(b) 向心方向：$\dfrac{mv_1^2}{R} = mg\cos\theta_0 - N$ →
$$N = mg\cos\theta_0 - \frac{m}{R}\left[v_0^2 + 2gR(1 - \cos\theta_0)\right] = mg(3\cos\theta_0 - 2) - \frac{mv_0^2}{R}$$
(c) $N = 0$：$\cos\theta_1 = \dfrac23 + \dfrac{v_0^2}{3gR}$。
(d) $\theta_1 = 0$ すなわち $\cos\theta_1 = 1$：$v_0^2 = gR$。$v_0 \ge \sqrt{gR}$ なら頂上で $N \le 0$。

### ④ 確認問題

**確認5-A**：半径 $R$ の球面の頂上から、半径 $r$ 質量 $m$ の一様な小球（$I = \frac25mr^2$）が静かに転がり落ちる（滑らない）。離れる角 $\cos\theta_1$ を求めよ。

**確認5-B**：半径 $R$ の滑らかな**半球の内面**の縁から質点を静かに放す。最下点での速さと垂直抗力。

**略解**
5-A：エネルギー $\frac12mv^2 + \frac12\cdot\frac25mr^2\cdot\frac{v^2}{r^2} = \frac{7}{10}mv^2 = mg(R+r)(1-\cos\theta)$。$N = 0$ で $\frac{mv^2}{R+r} = mg\cos\theta$。→ $\cos\theta_1 = \dfrac{10}{17}$。
5-B：$v = \sqrt{2gR}$、$N = mg + \dfrac{mv^2}{R} = 3mg$。
