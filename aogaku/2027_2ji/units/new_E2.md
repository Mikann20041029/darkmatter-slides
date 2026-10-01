#### ① 板書

**一様帯電球（半径 $R$、全電荷 $Q$）の電場**：内 $E = \dfrac{Qr}{4\pi\varepsilon_0R^3}$（$r$ に比例）、外 $E = \dfrac{Q}{4\pi\varepsilon_0r^2}$。

**「$r$ に比例する復元力」＝単振動**：球内に $-q$ を置くと $F = -qE = -\dfrac{qQ}{4\pi\varepsilon_0R^3}x$ → $\omega_0^2 = \dfrac{qQ}{4\pi\varepsilon_0mR^3}$。バネ定数の代わりに $qQ/(4\pi\varepsilon_0R^3)$。

**磁場中の運動方程式**：$m\ddot{\boldsymbol r} = q(\boldsymbol E + \dot{\boldsymbol r}\times\boldsymbol B)$。$\boldsymbol B = B\hat z$ のとき $\dot{\boldsymbol r}\times\boldsymbol B = (\dot yB,\ -\dot xB,\ 0)$。

**複素変数の技**：$x$ と $y$ の連立が「$\dot y$ が $x$ の式に、$\dot x$ が $y$ の式に」と交差して現れるときは、$u = x + iy$ とおくと**1本の方程式にまとまる**。$\dot y\to$ 虚部、$-\dot x\to$ … の組み合わせが $i\dot u$ になる。

**サイクロトロン角振動数**：$\omega_c = \dfrac{qB}{m}$。磁場だけなら円運動の角振動数。

#### ② 過去問【上智 2026年秋 問4・原文】

真空の誘電率 $\varepsilon_0$。

1. 原点に置かれた半径 $R$ の球の内部に電荷が一様に分布し、全電荷 $+Q$。内外で場合分けし、$\boldsymbol E(r)$ の向きと大きさ。
2. 球内の $x$ 軸上の点 $x_0$（$0<x_0<R$）に電気量 $-q$ の点電荷（有効質量 $m$）を置くと単振動した。角振動数 $\omega_0$。
3. $z$ 方向に磁束密度 $B$ をかけて同じことをすると $x$-$y$ 面内で運動した。$x(t), y(t)$ の運動方程式を、$\omega_c = q|B|/m$ と $\omega_0$ で書け。
4. $u(t) = x(t) + iy(t)$ の運動方程式を導け。
5. $u = Ce^{i\omega t}$ とおくと $\omega$ に2つの解 $\omega_1,\omega_2$。一般解 $u = C_1e^{i\omega_1t} + C_2e^{i\omega_2t}$ から $x(t), y(t)$ の一般解を書け。
6. 二つの単振動の角振動数の差を求めよ（$\omega_1,\omega_2$ のどちらかは負）。

#### ③ 解説

**1.** 内 $\boldsymbol E = \dfrac{Q}{4\pi\varepsilon_0R^3}\boldsymbol r$、外 $\boldsymbol E = \dfrac{Q}{4\pi\varepsilon_0r^2}\hat r$。どちらも動径外向き（$Q>0$）。

**2.** $m\ddot x = -qE_x = -\dfrac{qQ}{4\pi\varepsilon_0R^3}x$ → $\omega_0 = \sqrt{\dfrac{qQ}{4\pi\varepsilon_0mR^3}}$。

**3.** 力 $= -q(\boldsymbol E + \boldsymbol v\times\boldsymbol B)$、$\boldsymbol v\times\boldsymbol B = (\dot yB, -\dot xB, 0)$：
$$m\ddot x = -m\omega_0^2x - qB\dot y,\qquad m\ddot y = -m\omega_0^2y + qB\dot x$$
$$\ddot x = -\omega_0^2x - \omega_c\dot y,\qquad \ddot y = -\omega_0^2y + \omega_c\dot x$$

**4.** $\ddot u = \ddot x + i\ddot y = -\omega_0^2(x+iy) - \omega_c\dot y + i\omega_c\dot x = -\omega_0^2u + i\omega_c(\dot x + i\dot y) = -\omega_0^2u + i\omega_c\dot u$。
$$\ddot u - i\omega_c\dot u + \omega_0^2u = 0$$

**5.** $u = Ce^{i\omega t}$ を代入：$-\omega^2 + \omega_c\omega + \omega_0^2 = 0$ → $\omega^2 - \omega_c\omega - \omega_0^2 = 0$ →
$$\omega_{1,2} = \frac{\omega_c\pm\sqrt{\omega_c^2 + 4\omega_0^2}}{2}\quad(\omega_1>0,\ \omega_2<0)$$
$C_k = |C_k|e^{i\phi_k}$ として実部・虚部：
$$x(t) = |C_1|\cos(\omega_1t + \phi_1) + |C_2|\cos(\omega_2t + \phi_2),\quad y(t) = |C_1|\sin(\omega_1t + \phi_1) + |C_2|\sin(\omega_2t + \phi_2)$$
（$\omega_2<0$ の項は逆回りの円運動）

**6.** 正の角振動数として見ると $\omega_1$ と $|\omega_2| = -\omega_2$。差は $\omega_1 - |\omega_2| = \omega_1 + \omega_2 = $ **$\omega_c$**（2次方程式の解の和）。磁場で単振動が2つに割れ、その差がちょうどサイクロトロン振動数——ゼーマン分裂の古典版。
検算：$B\to0$ で $\omega_c\to0$、$\omega_{1,2}\to\pm\omega_0$（差0、元の単振動）✓。

> **落とし穴**：①$\boldsymbol v\times\boldsymbol B$ の符号（$(\dot x,\dot y,0)\times(0,0,B) = (\dot yB, -\dot xB, 0)$）。②4で $i\omega_c\dot u$ の符号。$-\omega_c\dot y + i\omega_c\dot x = i\omega_c(\dot x + i\dot y)$ を確認。③6は「$\omega_1 - \omega_2$」と書くと $\sqrt{\omega_c^2+4\omega_0^2}$ になってしまう。問題文の注意書きが「絶対値で見ろ」の合図。

#### ④ 練習問題

**練習E2-A**：$\boldsymbol E = 0$、$\boldsymbol B = B\hat z$ だけのとき、4の方程式はどうなるか。$u$ を解いて円運動（半径 $v_0/\omega_c$）になることを示せ。

**練習E2-B**：$\omega_c\ll\omega_0$ のとき $\omega_{1,2}\simeq\pm\omega_0 + \omega_c/2$ を示せ（平方根を展開）。

**練習E2-C【立教 2020年春 大問2・原文】**：陰極線管を用いて電子の質量を求める実験を考える。図1の偏向磁場領域は長さ $a$ で磁束密度は $B$、飛行領域の長さを $L$、素電荷を $e$、電子の質量を $m$ とし、陰極線管の内部は真空で、加速電場領域以外での電場の影響は考えなくてよい。以下の問いに答えよ。
(a) まず、陰極から電子を発生させる前の状態を考える。図1の加速電場を作る陰極と陽極は平行平板コンデンサーであるとみなせる。陰極と陽極の極板面積を $S$、極板間隔を $d$、電圧を $V$、真空中の誘電率を $\epsilon_0$ とする。図1のスイッチが切られていた状態から、スイッチを入れて十分時間が経った。その間に陰極に蓄積された電子の数 $n_0$ を求めよ。ただし、$d$ は小さいとみなしてよい。
(b) 前問で、次いで電源のスイッチを切った。抵抗を $R$ として、スイッチを切ってから電子の数が $n_0$ の $1/2$ になるまでの時間を求めよ。
(c) 再びスイッチを入れる。図1の陰極から電子を発生させ、静電場で加速した後に偏向磁場に通す。そして図1の蛍光板上での変位 $\delta$ を計測した。偏向磁場は一様で偏向磁場領域の中だけにあり、電子の速度 $v$ は既知として偏向磁場領域内での電子の軌道の曲率半径 $\rho$ を式で表せ。次いで、$e, B, a, L, m, v$ を用いて $\delta$ を表わせ。ただし、磁場による偏向角はわずかで、$\delta\ll L$、及び $a\ll L$ として近似してよい。
(d) 次に同じ装置で図2の様に偏向磁場をゼロにし、蛍光板の位置に収集電極を設置してその上に陰極線を一定時間、照射した。収集電極は絶縁されており、また、断熱されているため、収集電極上には電荷と熱が蓄積される。電子の速度 $v$ は既知として、収集電極に蓄積された熱量 $H$ と電荷 $Q$ の比 $H/Q$ を求めよ。
(e) (c)の結果と、(d)の結果から $v$ を消去し、$\delta, H, Q, B, a, L$ を用いて電子質量 $m_e$ と素電荷 $e$ の比 $m_e/e$ を表せ。
(f) 別の実験から素電荷 $e$ の値が求められたものとする。これと前問の結果、および下記の実験結果を用いて、$H$ を使わずに電子質量 $m_e$ を表せ。
　(c)の実験：設定値 $a, L, B$ の条件の実験で、$\delta$ が計測された。
　(d)の実験：陰極線を照射した前後で、収集電極の温度は $\Delta T$ 上昇した。収集電極は質量 $M$ の銅の板で、室温近辺において銅の比熱は一定値 $\gamma$ であり、電極全体が等温であると考えてよい。また、照射前に0であった収集電極に蓄積された電荷は、照射後に計測した結果、$Q$ であった。

**略解**
E2-A：$\ddot u = i\omega_c\dot u$ → $\dot u = v_0e^{i\omega_ct}$ → $u = \dfrac{v_0}{i\omega_c}e^{i\omega_ct} + $ 定数。半径 $v_0/\omega_c$ の円。
E2-B：$\sqrt{\omega_c^2 + 4\omega_0^2}\simeq2\omega_0(1 + \omega_c^2/8\omega_0^2)$。$\omega_{1,2}\simeq\pm\omega_0 + \omega_c/2$。
E2-C：(a) $Q = CV$、$C = \epsilon_0S/d$ → $n_0 = \dfrac{\epsilon_0SV}{ed}$。(b) RC放電 $q = q_0e^{-t/RC}$ → $t_{1/2} = RC\ln2 = \dfrac{\epsilon_0SR}{d}\ln2$。(c) $evB = mv^2/\rho$ → $\rho = \dfrac{mv}{eB}$。磁場領域で曲がる角 $\alpha\simeq a/\rho = \dfrac{eBa}{mv}$、飛行領域でのずれ $\delta\simeq L\alpha = \dfrac{eBaL}{mv}$。(d) 電子1個が運ぶ熱 $\frac12mv^2$、電荷 $e$ → $\dfrac HQ = \dfrac{mv^2}{2e}$。(e) (c)より $v = \dfrac{eBaL}{m\delta}$。(d)に代入：$\dfrac HQ = \dfrac{m}{2e}\cdot\dfrac{e^2B^2a^2L^2}{m^2\delta^2} = \dfrac{eB^2a^2L^2}{2m\delta^2}$ → $\dfrac{m_e}{e} = \dfrac{B^2a^2L^2Q}{2H\delta^2}$。(f) $H = M\gamma\Delta T$ → $m_e = \dfrac{eB^2a^2L^2Q}{2M\gamma\Delta T\,\delta^2}$。
