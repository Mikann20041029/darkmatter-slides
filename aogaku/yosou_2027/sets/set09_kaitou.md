# 解答・解説 — 予想問題 第 9 回

各大問 100 点。

## 1

**(1)（15 点）** $R_2-2R_1$、$R_3-3R_1$、$R_4-R_1$ を行うと第 2〜4 行がすべて $(0,-3,3,-6)$ となる。

$$
A\to\begin{pmatrix}1&2&-1&3\\0&-3&3&-6\\0&0&0&0\\0&0&0&0\end{pmatrix}, \qquad \operatorname{rank}A = 2
$$

**(2)（25 点）** 第 2 行より $x_2 = x_3-2x_4$、第 1 行より $x_1 = -2x_2+x_3-3x_4 = -x_3+x_4$。$x_3=s$、$x_4=t$ を自由変数として

$$
\boldsymbol x = s\begin{pmatrix}-1\\1\\1\\0\end{pmatrix}+t\begin{pmatrix}1\\-2\\0\\1\end{pmatrix},
\qquad \dim = 2
$$

**(3)（10 点）** $\dim\operatorname{Ker} + \operatorname{rank} = 2+2 = 4 = \dim\mathbb{R}^4$。成立。

**(4)（30 点）** $\operatorname{Im}f$ は主成分の列（第 1・第 2 列）が張る。

$$
\boldsymbol b = c_1(1,2,3,1)^\top + c_2(2,1,3,-1)^\top
$$

成分ごとに $b_1 = c_1+2c_2$、$b_2 = 2c_1+c_2$、$b_3 = 3c_1+3c_2$、$b_4 = c_1-c_2$。第 1・2 式から

$$
b_1+b_2 = 3(c_1+c_2) = b_3, \qquad b_2-b_1 = c_1-c_2 = b_4
$$

$$
\boxed{b_3 = b_1+b_2, \qquad b_4 = b_2-b_1}
$$

**(5)（20 点）** $\boldsymbol b = (1,1,2,0)^\top$ は $2 = 1+1$、$0 = 1-1$ を満たすので **解は存在する**。

$c_1+2c_2 = 1$、$2c_1+c_2 = 1$ を解いて $c_1 = c_2 = 1/3$。特殊解は $\left(\frac13,\frac13,0,0\right)^\top$。

$$
\boldsymbol x = \frac13\begin{pmatrix}1\\1\\0\\0\end{pmatrix}
+ s\begin{pmatrix}-1\\1\\1\\0\end{pmatrix}
+ t\begin{pmatrix}1\\-2\\0\\1\end{pmatrix}\qquad (s,t\in\mathbb{R})
$$

---

## 3（配点 100）

**(1)（35 点）**

$$
f_x = 2x+y-\frac{1}{x^2} = 0, \qquad f_y = x+2y-\frac{1}{y^2} = 0
$$

辺々引くと

$$
(x-y)+\left(\frac{1}{y^2}-\frac{1}{x^2}\right) = (x-y)+\frac{x^2-y^2}{x^2y^2}
= (x-y)\left[1+\frac{x+y}{x^2y^2}\right] = 0
$$

$x,y>0$ では角括弧は正なので $x=y$。これを $f_x=0$ に代入して

$$
3x = \frac{1}{x^2} \ \Longrightarrow\ x^3 = \frac13 \ \Longrightarrow\ x = y = 3^{-1/3} \simeq 0.6934
$$

停留点はこの 1 点のみ。

**(2)（40 点）**

$$
f_{xx} = 2+\frac{2}{x^3}, \qquad f_{yy} = 2+\frac{2}{y^3}, \qquad f_{xy} = 1
$$

$x^3 = 1/3$ より $2/x^3 = 6$ なので $f_{xx} = f_{yy} = 8$。

$$
H = 8\times8-1^2 = 63 > 0, \qquad f_{xx} = 8 > 0 \ \Longrightarrow\ \textbf{極小}
$$

$$
f = 3x^2+\frac2x = 3\cdot3^{-2/3}+2\cdot3^{1/3} = 3^{1/3}+2\cdot3^{1/3} = 3\cdot3^{1/3} = 3^{4/3} \simeq 4.327
$$

（$3\cdot3^{-2/3} = 3^{1/3}$、$2/x = 2\cdot3^{1/3}$ を使った）

**(3)（25 点）** 定義域 $x,y>0$ は開集合だが、境界と無限遠で $f\to+\infty$ となる。

- $x\to0^+$（$y$ 固定）: $1/x\to+\infty$
- $y\to0^+$: $1/y\to+\infty$
- $x^2+y^2\to\infty$: $x^2+xy+y^2 \ge \frac12(x^2+y^2)\to\infty$

したがって十分大きなコンパクト集合の外では $f$ が大きくなり、$f$ は内部で最小値をとる。最小値をとる点は停留点でなければならず、停留点は 1 つしかないので、それが最小点である。

$$
\min f = \boxed{3^{4/3}} = 3\sqrt[3]{3} \simeq 4.327 \qquad \left(x=y=3^{-1/3}\right)
$$

---

## 4

**(1)（40 点）** $u = xy$、$v = y/x$ とすると $x^2 = u/v$、$y^2 = uv$。

$$
\frac{\partial(u,v)}{\partial(x,y)} = \begin{vmatrix} y & x\\ -y/x^2 & 1/x\end{vmatrix} = \frac yx+\frac{y}{x} = \frac{2y}{x} = 2v
\ \Longrightarrow\ dx\,dy = \frac{du\,dv}{2v}
$$

被積分関数は

$$
x^2-y^2 = \frac uv - uv = \frac{u(1-v^2)}{v}
$$

領域は $1\le u\le2$、$1\le v\le3$ の長方形に移る。

$$
\iint_D(x^2-y^2)dxdy = \int_1^2\!\!u\,du\int_1^3\frac{1-v^2}{2v^2}dv
= \frac32\cdot\frac12\int_1^3\left(\frac{1}{v^2}-1\right)dv
$$

$$
\int_1^3\left(v^{-2}-1\right)dv = \left[-\frac1v-v\right]_1^3 = \left(-\frac13-3\right)-(-1-1) = -\frac{4}{3}
$$

$$
\therefore\ \frac32\cdot\frac12\cdot\left(-\frac43\right) = \boxed{-1}
$$

（$v>1$ すなわち $y>x$ の領域なので $x^2-y^2<0$、答えが負になるのは妥当）

**(2)（30 点）** $x = 1/t$ と置換すると $dx = -dt/t^2$、$\ln x = -\ln t$。

$$
\int_1^\infty\frac{\ln x}{1+x^2}dx = \int_1^0\frac{-\ln t}{1+1/t^2}\cdot\left(-\frac{dt}{t^2}\right) = -\int_0^1\frac{\ln t}{1+t^2}dt
$$

したがって $\displaystyle\int_0^1$ と $\displaystyle\int_1^\infty$ はちょうど符号が逆で打ち消し合う。

$$
\int_0^\infty\frac{\ln x}{1+x^2}dx = \boxed{0}
$$

（各部分は絶対収束するので、和をとる操作は正当。$x=1$ を中心に対数が奇関数的に振る舞うことが本質）

**(3)（30 点）** $e^{-x^2}$ は初等的な原始関数を持たないので順序を交換する。

領域は $\{0\le y\le2,\ y/2\le x\le1\}$、すなわち $\{0\le x\le1,\ 0\le y\le2x\}$。

$$
\int_0^1\!\!dx\int_0^{2x}e^{-x^2}dy = \int_0^1 2xe^{-x^2}dx = \left[-e^{-x^2}\right]_0^1 = \boxed{1-\frac1e} \simeq 0.6321
$$

---

## 7 ｜ 力学：慣性テンソル（配点 100）

**問 1（10 点）**

$$
I_{ij} = \int\rho(\boldsymbol r)\left(r^2\delta_{ij}-x_ix_j\right)dV
$$

$\delta_{ij}$ も $x_ix_j$ も添字の交換に対して不変なので $I_{ij} = I_{ji}$。実対称行列なので必ず直交行列で対角化でき、固有値（主慣性モーメント）は実数である。

**問 2（20 点）** 非対角成分の例:

$$
I_{xy} = -\int\rho\,xy\,dV = -\rho\int_{-a/2}^{a/2}\!\!x\,dx\int_{-b/2}^{b/2}\!\!y\,dy\int_{-c/2}^{c/2}\!\!dz = 0
$$

$x$ についての積分が奇関数の対称区間積分でゼロになる。他の非対角成分も同様。

対角成分は

$$
I_{xx} = \int\rho(y^2+z^2)dV = \frac{M}{abc}\left[\frac{b^3}{12}\cdot ac + \frac{c^3}{12}\cdot ab\right] = \boxed{\frac{M(b^2+c^2)}{12}}
$$

同様に $I_{yy} = \dfrac{M(c^2+a^2)}{12}$、$I_{zz} = \dfrac{M(a^2+b^2)}{12}$。

**問 3（10 点）** 直方体は 3 つの座標平面それぞれに関して鏡映対称である。$x\to-x$ の鏡映で $I_{xy}$、$I_{xz}$ の被積分関数は符号を変えるが、物体は不変なので積分値は自分自身の $-1$ 倍に等しく、したがってゼロでなければならない。

**主軸** とは、慣性テンソルを対角化する直交基底の方向、すなわち $I\boldsymbol e = I_k\boldsymbol e$ を満たす固有ベクトルの方向をいう。物体に鏡映面や回転対称軸があれば、それらは必ず主軸になる。

**問 4（20 点）** $\boldsymbol L = I\boldsymbol\omega$ が $\boldsymbol\omega$ と平行になるのは、$\boldsymbol\omega$ が $I$ の **固有ベクトル**、すなわち主軸方向を向くときに限る。

具体例: $xy$ 面内の面対角線方向 $\boldsymbol\omega = \dfrac{\omega}{\sqrt2}(1,1,0)$ で回すと

$$
\boldsymbol L = \frac{\omega}{\sqrt2}\left(I_{xx},\,I_{yy},\,0\right) = \frac{M\omega}{12\sqrt2}\left(b^2+c^2,\ c^2+a^2,\ 0\right)
$$

$\boldsymbol L\parallel\boldsymbol\omega$ には $b^2+c^2 = c^2+a^2$、すなわち $a=b$ が必要。$a\ne b$ なら平行にならない。

このとき $\boldsymbol L$ は $\boldsymbol\omega$ のまわりを回り続けるので、$d\boldsymbol L/dt\ne0$、すなわち **軸受けに周期的な力（振動）を及ぼす**。回転機械のバランス取りが必要な理由である。

**問 5（20 点）** $a=b=c$ なら

$$
I_{xx}=I_{yy}=I_{zz} = \frac{M(2a^2)}{12} = \frac{Ma^2}{6}, \qquad I = \frac{Ma^2}{6}E
$$

単位行列に比例するので、**任意のベクトルが固有ベクトル**である。したがってどの軸で回しても $\boldsymbol L = \frac{Ma^2}{6}\boldsymbol\omega \parallel \boldsymbol\omega$。

直観に反するように見えるが、これは慣性テンソルが **2 階の対称テンソル**であることによる。立方体の対称群（$O_h$）は体対角線まわりの 3 回回転を含み、この群の作用で不変な 2 階対称テンソルは $\delta_{ij}$ の定数倍しか存在しない。つまり「球のように丸いかどうか」ではなく、「3 回以上の回転対称軸が 2 本以上あるか」が効いている。同じ理由で正四面体・正八面体・正十二面体も慣性テンソルが等方的になる。

**問 6（20 点）** $\boldsymbol\omega = (\Omega,\epsilon_2,\epsilon_3)$（$\epsilon\ll\Omega$）として 1 軸まわりの回転を考える。$\epsilon$ の 1 次までで

$$
I_2\dot\epsilon_2 = (I_3-I_1)\Omega\epsilon_3, \qquad I_3\dot\epsilon_3 = (I_1-I_2)\Omega\epsilon_2
$$

（第 1 式より $\dot\omega_1 = O(\epsilon^2)$ なので $\Omega$ は一定としてよい）。両者を組み合わせて

$$
\ddot\epsilon_2 = \frac{(I_3-I_1)(I_1-I_2)}{I_2I_3}\Omega^2\,\epsilon_2
$$

係数が **負**なら振動（安定）、**正**なら指数関数的増大（不安定）。$K \equiv (I_3-I_1)(I_1-I_2)$ の符号を調べると

| 回転軸 | $I_3-I_1$ | $I_1-I_2$ | $K$ | 判定 |
| --- | --- | --- | --- | --- |
| 最小軸（$I_1$ が最小） | $+$ | $-$ | $-$ | **安定** |
| 中間軸（$I_1$ が中間） | $+$ | $+$ | $+$ | **不安定** |
| 最大軸（$I_1$ が最大） | $-$ | $+$ | $-$ | **安定** |

すなわち **最大・最小の主軸まわりは安定、中間軸まわりだけが不安定**である。テニスラケットやスマートフォンを空中に放り投げると、中間軸まわりでは必ず途中でひっくり返る（テニスラケット定理、ジャニベコフ効果）。人工衛星のスピン安定化で最大慣性軸を選ぶのもこの理由による。

---

## 8 ｜ 電磁気学（配点 100）

### 問 1（35 点）

**(1)** $r\gg r'$ で

$$
\frac{1}{|\boldsymbol r-\boldsymbol r'|} = \frac{1}{r}\left(1-\frac{2\boldsymbol r\cdot\boldsymbol r'}{r^2}+\frac{r'^2}{r^2}\right)^{-1/2}
= \frac1r+\frac{\boldsymbol r'\cdot\hat{\boldsymbol r}}{r^2}+O\!\left(\frac{r'^2}{r^3}\right)
$$

$$
V(\boldsymbol r) = \frac{1}{4\pi\varepsilon_0}\int\frac{\rho(\boldsymbol r')}{|\boldsymbol r-\boldsymbol r'|}dV'
= \frac{1}{4\pi\varepsilon_0}\left[\frac{Q}{r}+\frac{\boldsymbol p\cdot\hat{\boldsymbol r}}{r^2}+\cdots\right]
$$

$$
Q = \int\rho\,dV', \qquad \boldsymbol p = \int\rho\,\boldsymbol r'\,dV'
$$

**(2)** $V_{\rm dip} = \dfrac{1}{4\pi\varepsilon_0}\dfrac{\boldsymbol p\cdot\boldsymbol r}{r^3}$ を勾配する。

$$
\boldsymbol E = -\nabla V = -\frac{1}{4\pi\varepsilon_0}\left[\frac{\boldsymbol p}{r^3}-\frac{3(\boldsymbol p\cdot\boldsymbol r)\boldsymbol r}{r^5}\right]
= \frac{1}{4\pi\varepsilon_0}\frac{3(\boldsymbol p\cdot\hat{\boldsymbol r})\hat{\boldsymbol r}-\boldsymbol p}{r^3}
$$

**(3)** 原点を $\boldsymbol a$ だけずらすと、新しい座標では $\boldsymbol r'' = \boldsymbol r'-\boldsymbol a$。

$$
\boldsymbol p'' = \int\rho(\boldsymbol r'-\boldsymbol a)dV' = \boldsymbol p - \boldsymbol aQ
$$

$Q\ne0$ なら原点の取り方で $\boldsymbol p$ が変わる（$\boldsymbol p=0$ にする原点＝電荷の重心が選べる）。$Q=0$ なら $\boldsymbol p'' = \boldsymbol p$ で **原点によらない**。

一般に、多重極展開では「最低次の非ゼロ項だけが原点の取り方によらない」。中性分子の双極子モーメントが物質固有の量として意味を持つのはこのためである。

### 問 2（35 点）

**(1)** 細い線状電流では $\boldsymbol j\,dV' \to I\,d\boldsymbol l'$ なので

$$
\boldsymbol m = \frac{I}{2}\oint\boldsymbol r'\times d\boldsymbol l'
$$

$\frac12\boldsymbol r'\times d\boldsymbol l'$ は原点と線素が張る微小三角形の面積ベクトルなので、1 周積分すると平面図形の面積ベクトル $S\hat{\boldsymbol n}$ になる。

$$
\boldsymbol m = IS\hat{\boldsymbol n}
$$

**(2)** $\nabla\cdot\boldsymbol B = 0$、すなわち任意の閉曲面で $\oint\boldsymbol B\cdot d\boldsymbol S = 0$ である。電場の場合はこの積分がガウスの法則で $Q/\varepsilon_0$ になり、それが単極子項を生んだ。磁場では対応する「磁荷」が存在しないので、**単極子項は恒等的にゼロ**になり、展開は双極子項から始まる。

**(3)** 双極子項が残るので、遠方の磁場は

$$
\boldsymbol B = \frac{\mu_0}{4\pi}\frac{3(\boldsymbol m\cdot\hat{\boldsymbol r})\hat{\boldsymbol r}-\boldsymbol m}{r^3}
$$

と、電気双極子とまったく同じ形になる。

地球磁場の源は外核の流体運動であり、その広がりは地球半径の約 0.55 倍の領域に収まっている。多重極の $n$ 次項は $r^{-(n+2)}$ で減衰するので、地表（源の領域の約 2 倍の距離）ではすでに双極子成分が支配的（全磁場エネルギーの約 90 %）になる。人工衛星高度ではさらに双極子近似がよくなる。

### 問 3（30 点）

**(1)** 金属板が動くと、板の各部分を貫く磁束が時間変化する（磁場の非一様な領域を横切るとき、あるいは板が磁場領域に出入りするとき）。ファラデーの法則

$$
\oint\boldsymbol E\cdot d\boldsymbol l = -\frac{d\Phi}{dt}
$$

により板内部に渦状の起電力が生じ、導体なので渦電流が流れる。向きはレンツの法則により **磁束の変化を妨げる**向き、すなわち磁束が減るなら磁束を保とうとする向き、増えるなら打ち消す向きになる。

**(2)** 渦電流 $\boldsymbol j$ が磁場から受ける力は $\boldsymbol j\times\boldsymbol B$。レンツの法則から、この力は必ず **板の運動を妨げる向き**を向く。したがって板は減速する。

これが **電磁ブレーキ**（渦電流ブレーキ）である。機械的な接触がないので摩耗せず、高速域で強く効く（力が速度に比例する）。一方、静止すると渦電流が流れないので保持力はゼロになる。新幹線や大型トラック、遊園地のフリーフォールの減速に使われている。

**(3)** 変圧器の鉄心には交流磁束が通るので、鉄心自身が導体である以上、渦電流が流れてジュール熱として失われる（渦電流損）。この損失は電力を無駄にし、鉄心を発熱させる。

厚さ $d$ の板における単位体積あたりの渦電流損は

$$
P_{\rm eddy} \propto \sigma\,d^2B_{\max}^2f^2
$$

と厚さの **2 乗**に比例する。したがって、鉄心を厚さ $d/n$ の薄板 $n$ 枚に分割して互いに絶縁すれば（磁束は板面に平行に通し、渦電流の経路だけを断ち切る）、損失は $1/n^2$ になる。

$$
\text{積層厚を }1/n\text{ にすると渦電流損は }1/n^2
$$

実際の 50/60 Hz 用変圧器では 0.2〜0.5 mm 厚のケイ素鋼板が使われる。ケイ素を添加するのは $\sigma$ 自体を下げる（抵抗率を上げる）ためで、2 つの対策を併用している。高周波用ではさらに絶縁性のフェライトを使い、渦電流をほぼ完全に断つ。

---

## 9 ｜ 量子力学：スピンの歳差運動（配点 100）

**問 1（15 点）** $\hat S_z$ の固有値は $\pm\hbar/2$ なので

$$
E_\uparrow = -\frac{\gamma B\hbar}{2}\ (|\!\uparrow\rangle), \qquad E_\downarrow = +\frac{\gamma B\hbar}{2}\ (|\!\downarrow\rangle)
$$

$$
\Delta E = E_\downarrow-E_\uparrow = \gamma\hbar B \equiv \hbar\omega_L
$$

$\gamma>0$ なら磁場と同じ向きのスピンのほうがエネルギーが低い。

**問 2（15 点）** 固有状態の重ね合わせなので、それぞれに位相因子を掛けるだけでよい。$\omega_L = \gamma B$ とおくと

$$
|\psi(t)\rangle = \frac{1}{\sqrt2}\left(e^{-iE_\uparrow t/\hbar}|\!\uparrow\rangle + e^{-iE_\downarrow t/\hbar}|\!\downarrow\rangle\right)
= \frac{1}{\sqrt2}\left(e^{i\omega_Lt/2}|\!\uparrow\rangle + e^{-i\omega_Lt/2}|\!\downarrow\rangle\right)
$$

**問 3（30 点）** $a = \frac{1}{\sqrt2}e^{i\omega_Lt/2}$、$b = \frac{1}{\sqrt2}e^{-i\omega_Lt/2}$ とすると

$$
\langle\hat S_x\rangle = \frac\hbar2\cdot2\,\mathrm{Re}(a^*b) = \frac\hbar2\cos\omega_Lt
$$
$$
\langle\hat S_y\rangle = \frac\hbar2\cdot2\,\mathrm{Im}(a^*b) = -\frac\hbar2\sin\omega_Lt
$$
$$
\langle\hat S_z\rangle = \frac\hbar2\left(|a|^2-|b|^2\right) = 0
$$

期待値ベクトル $\langle\hat{\boldsymbol S}\rangle$ は、大きさ $\hbar/2$ を保ったまま $xy$ 平面内を **一定の角速度で回転**する。$+z$ から見て時計回り（$+x\to-y\to-x\to+y$）で、角振動数は

$$
\boxed{\omega_L = \gamma B \qquad (\text{ラーモア振動数})}
$$

**問 4（20 点）** ハイゼンベルグ方程式

$$
\frac{d\langle\hat S_i\rangle}{dt} = \frac{1}{i\hbar}\left\langle[\hat S_i,\hat H]\right\rangle
= \frac{-\gamma B}{i\hbar}\left\langle[\hat S_i,\hat S_z]\right\rangle
$$

角運動量の交換関係 $[\hat S_i,\hat S_j] = i\hbar\epsilon_{ijk}\hat S_k$ を使うと

$$
\frac{d\langle\hat{\boldsymbol S}\rangle}{dt} = \gamma\,\langle\hat{\boldsymbol S}\rangle\times\boldsymbol B
$$

これは古典的な磁気モーメント $\boldsymbol\mu = \gamma\boldsymbol S$ が受けるトルク $\boldsymbol\mu\times\boldsymbol B$ による歳差運動の式そのものである。

**重要な点**: 期待値の従う方程式が厳密に古典と同じ形になるのは、$\hat H$ が $\hat{\boldsymbol S}$ の 1 次式だからである。この意味で、スピンの歳差運動は「量子的だが古典的に描ける」珍しい例であり、NMR や MRI の直観的な描像（磁化ベクトルの回転）が正当化される。

**問 5（10 点）** 角振動数 $\omega$ で回転する座標系に移ると、静磁場の効果は $B_0-\omega/\gamma$ に置き換わる。$\omega = \gamma B_0$ のとき静磁場の寄与が **完全に消え**、回転系では $B_1$ だけが残る。

その結果、スピンは $B_1$ のまわりを角振動数 $\gamma B_1$ でゆっくり歳差する（**ラビ振動**）。適切な時間だけ $B_1$ を加えれば、スピンを 90$^\circ$ や 180$^\circ$ 倒せる（$\pi/2$ パルス、$\pi$ パルス）。倒れた横磁化が歳差しながらコイルに誘導起電力を生み、これが NMR 信号（自由誘導減衰）として観測される。

**問 6（10 点）**

$$
f = \frac{\gamma}{2\pi}B_0 = 42.58\times1.5 = \boxed{63.9\ \mathrm{MHz}}
$$

信号強度は、上下 2 準位の **占有数差** に比例する。ボルツマン分布から

$$
\frac{\Delta N}{N} \simeq \frac{\Delta E}{2k_BT} = \frac{\gamma\hbar B_0}{2k_BT}
$$

これは $B_0$ に **比例**する。1.5 T、室温では

$$
\frac{\Delta N}{N} = \frac{hf}{2k_BT} = \frac{6.63\times10^{-34}\times6.39\times10^7}{2\times1.38\times10^{-23}\times300} \simeq 5\times10^{-6}
$$

100 万個に 5 個程度の偏りしかない。これが NMR の感度が本質的に低い理由であり、逆に **強磁場化が最も直接的な感度向上策**である理由でもある（さらに検出コイルの誘導起電力も $\omega\propto B_0$ に比例するので、信号は $B_0$ の 2 乗近くで効く）。臨床 MRI が 1.5 T → 3 T → 7 T と高磁場化してきたのはこのためである。

---

## 10 ｜ 熱力学と統計力学（配点 100）

**問 1（15 点）**

$$
dU = TdS-PdV
$$
$$
H = U+PV: \qquad dH = TdS+VdP
$$
$$
F = U-TS: \qquad dF = -SdT-PdV
$$
$$
G = H-TS = U+PV-TS: \qquad dG = -SdT+VdP
$$

いずれも $U(S,V)$ から、独立変数を「共役な変数」に取り替える **ルジャンドル変換**で得られる（$S\to T$、$V\to P$）。実験で制御しやすい変数（$T$、$P$）を独立変数にするための操作である。

**問 2（20 点）** $dU = TdS-PdV$ が完全微分なら $\dfrac{\partial^2U}{\partial V\partial S} = \dfrac{\partial^2U}{\partial S\partial V}$、すなわち

$$
\left(\frac{\partial T}{\partial V}\right)_S = -\left(\frac{\partial P}{\partial S}\right)_V
$$

同様に $H, F, G$ から

$$
\left(\frac{\partial T}{\partial P}\right)_S = \left(\frac{\partial V}{\partial S}\right)_P, \qquad
\boxed{\left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial P}{\partial T}\right)_V}, \qquad
\left(\frac{\partial S}{\partial P}\right)_T = -\left(\frac{\partial V}{\partial T}\right)_P
$$

第 3 式が特に有用で、「測りにくい $S$ の変化」を「測りやすい $P$–$T$ 関係」に置き換えられる。

**問 3（15 点）** $dU = TdS-PdV$ を $V$ で $T$ 一定のもと偏微分して

$$
\left(\frac{\partial U}{\partial V}\right)_T = T\left(\frac{\partial S}{\partial V}\right)_T - P
$$

第 3 マクスウェル関係式を代入して

$$
\left(\frac{\partial U}{\partial V}\right)_T = T\left(\frac{\partial P}{\partial T}\right)_V - P
$$

理想気体 $P = nRT/V$ では $\left(\partial P/\partial T\right)_V = nR/V = P/T$ なので

$$
\left(\frac{\partial U}{\partial V}\right)_T = T\cdot\frac PT - P = 0
$$

**理想気体の内部エネルギーは温度だけの関数**（ジュールの法則）であることが、状態方程式だけから熱力学的に導かれる。

**問 4（20 点）** ファンデルワールスの状態方程式を $P$ について解くと

$$
P = \frac{nRT}{V-nb}-\frac{an^2}{V^2}
$$

$$
\left(\frac{\partial P}{\partial T}\right)_V = \frac{nR}{V-nb}
$$

$$
\left(\frac{\partial U}{\partial V}\right)_T = \frac{nRT}{V-nb}-P = \boxed{\frac{an^2}{V^2}} > 0
$$

**物理的意味**: 温度一定のまま体積を増やすと内部エネルギーが増える。これは分子間に **引力**（$a$ の項）があるためで、分子どうしを引き離すのに仕事が必要だからである。$b$（排除体積）はこの量に効かない。

この項こそが、実在気体を自由膨張させたときに温度が下がる理由であり、ジュール–トムソン効果による気体液化の原理でもある（内部エネルギーの一部が引力に打ち勝つために使われ、その分だけ運動エネルギー＝温度が減る）。

**問 5（20 点）** $S(T,V)$ と $S(T,P)$ の関係から出発する。$C_P = T\left(\partial S/\partial T\right)_P$、$C_V = T\left(\partial S/\partial T\right)_V$ で、連鎖律により

$$
\left(\frac{\partial S}{\partial T}\right)_P = \left(\frac{\partial S}{\partial T}\right)_V + \left(\frac{\partial S}{\partial V}\right)_T\left(\frac{\partial V}{\partial T}\right)_P
$$

第 3 マクスウェル関係式を使って

$$
C_P-C_V = T\left(\frac{\partial P}{\partial T}\right)_V\left(\frac{\partial V}{\partial T}\right)_P
$$

さらに三重積の関係 $\left(\dfrac{\partial P}{\partial T}\right)_V = -\dfrac{(\partial V/\partial T)_P}{(\partial V/\partial P)_T}$ を代入して

$$
C_P-C_V = -T\frac{\left(\partial V/\partial T\right)_P^2}{\left(\partial V/\partial P\right)_T}
$$

**非負である理由**: 分子は 2 乗なので非負、$T>0$。分母は、力学的安定性の要請（圧力を上げれば体積は減る）から等温圧縮率 $\kappa_T = -\frac1V\left(\partial V/\partial P\right)_T > 0$、すなわち $\left(\partial V/\partial P\right)_T<0$。全体として非負になる。

理想気体では $\left(\partial V/\partial T\right)_P = nR/P$、$\left(\partial V/\partial P\right)_T = -nRT/P^2$ なので

$$
C_P-C_V = -T\cdot\frac{(nR/P)^2}{-nRT/P^2} = nR \quad\checkmark
$$

**問 6（10 点）**

$$
F = -k_BT\ln Z, \qquad
S = -\left(\frac{\partial F}{\partial T}\right)_V, \qquad
P = -\left(\frac{\partial F}{\partial V}\right)_T, \qquad
U = F+TS = -\frac{\partial\ln Z}{\partial\beta}
$$

**すべての熱力学的関係が自動的に満たされる理由**: 統計力学は $F(T,V)$ という **1 つの関数**を与え、他のすべての量をその偏微分として定義している。マクスウェル関係式は「$F$ の 2 階偏微分の順序交換」以上のものではないから、$F$ が滑らかな関数として存在する限り恒等的に成り立つ。

言い換えれば、熱力学は「ある熱力学ポテンシャルが存在する」という仮定から導かれる関係式の体系であり、統計力学はそのポテンシャルを微視的な情報（ハミルトニアン）から実際に構成してみせる理論である。両者の役割分担がここに現れている。

---

## 11 ｜ 物性物理：ロンドン理論（配点 100）

**問 1（20 点）** 散乱項がないので

$$
m\frac{d\boldsymbol v}{dt} = -e\boldsymbol E
$$

$\boldsymbol j_s = -en_s\boldsymbol v$ より $\dfrac{d\boldsymbol v}{dt} = -\dfrac{1}{en_s}\dfrac{\partial\boldsymbol j_s}{\partial t}$ を代入して

$$
\frac{\partial\boldsymbol j_s}{\partial t} = \frac{n_se^2}{m}\boldsymbol E
$$

**なぜまだマイスナー効果ではないか**: この式は「定常電流が流れているとき $\boldsymbol E=0$」を意味する。すると $\nabla\times\boldsymbol E = -\partial\boldsymbol B/\partial t = 0$、すなわち **$\boldsymbol B$ は時間変化しない**としか言えない。

したがって完全導体を磁場中で冷却すると、そのときの磁束が内部に **凍結されたまま**残る。ところが実験（Meissner–Ochsenfeld、1933）では、磁場中で冷却しても超伝導体は磁束を **能動的に追い出す**。$\boldsymbol B = 0$ そのものは、$\partial\boldsymbol B/\partial t = 0$ からは出てこない。

**問 2（20 点）** ロンドン兄弟は、時間微分を外した形（積分定数をゼロと選ぶ）を仮定した。

$$
\nabla\times\boldsymbol j_s = -\frac{n_se^2}{m}\boldsymbol B
$$

アンペールの法則 $\nabla\times\boldsymbol B = \mu_0\boldsymbol j_s$ の回転をとると

$$
\nabla(\nabla\cdot\boldsymbol B)-\nabla^2\boldsymbol B = \mu_0\nabla\times\boldsymbol j_s = -\frac{\mu_0n_se^2}{m}\boldsymbol B
$$

$\nabla\cdot\boldsymbol B=0$ より

$$
\nabla^2\boldsymbol B = \frac{\boldsymbol B}{\lambda_L^2}, \qquad
\boxed{\lambda_L = \sqrt{\frac{m}{\mu_0n_se^2}}}
$$

**問 3（15 点）** 表面を $z=0$、磁場を $x$ 方向として $B_x(z)$ とすると

$$
\frac{d^2B_x}{dz^2} = \frac{B_x}{\lambda_L^2}
$$

一般解は $B_x = Ae^{-z/\lambda_L}+Ce^{+z/\lambda_L}$。内部で発散しない条件から $C=0$、表面の値から $A=B_0$。

$$
B_x(z) = B_0e^{-z/\lambda_L}
$$

磁場は表面から $\lambda_L$ 程度の薄い層にしか侵入せず、内部では **完全にゼロ**になる。これがマイスナー効果である。表面層には遮蔽電流（$j_s$）が流れ、これが外部磁場を打ち消している。

**問 4（15 点）**

$$
\mu_0n_se^2 = 1.257\times10^{-6}\times1.0\times10^{28}\times(1.602\times10^{-19})^2 = 3.23\times10^{-16}
$$

$$
\lambda_L = \sqrt{\frac{9.11\times10^{-31}}{3.23\times10^{-16}}} = \sqrt{2.82\times10^{-15}} = 5.3\times10^{-8}\ \mathrm{m} = \boxed{53\ \mathrm{nm}}
$$

実測値（Pb で約 37 nm、Al で約 50 nm）とよく一致する。ナノメートルスケールの薄膜では膜厚が $\lambda_L$ と同程度になり、マイスナー効果が不完全になる。

**問 5（15 点）** コヒーレンス長 $\xi$ は「超伝導秩序変数が変化できる最短の距離」を表す。両者の比 $\kappa = \lambda_L/\xi$ で分類される。

- **第 1 種**（$\kappa<1/\sqrt2$、純金属の多く）: 常伝導–超伝導界面の表面エネルギーが **正**。界面を作るのは損なので、磁場を完全に排除し続け、臨界磁場 $H_c$ で一気に常伝導へ転移する。$H_c$ は小さい（数十 mT）。
- **第 2 種**（$\kappa>1/\sqrt2$、合金・酸化物超伝導体）: 界面エネルギーが **負**。界面を増やすほど得なので、$H_{c1}$ を超えると磁束が細い糸（渦糸）として部分的に侵入する **混合状態**になり、$H_{c2}$（数十 T に達しうる）まで超伝導が保たれる。

強磁場マグネット（MRI、加速器）に使われるのはすべて第 2 種である。第 1 種では $H_c$ が低すぎて役に立たない。

**問 6（15 点）**

$$
\Phi_0 = \frac{h}{2e} = \frac{6.626\times10^{-34}}{2\times1.602\times10^{-19}} = \boxed{2.07\times10^{-15}\ \mathrm{Wb}}
$$

**分母が $2e$ であることの意味**: 磁束の量子化は、超伝導体を一周する巨視的な波動関数の位相が $2\pi$ の整数倍でなければならない（一価性）ことから来る。その際に現れる電荷は、超伝導を担うキャリアの電荷である。

実験で $h/2e$（$h/e$ ではない）が観測されたことは、**超伝導のキャリアが電荷 $2e$ をもつ複合粒子＝クーパー対である**ことの直接的な証拠になった（Deaver–Fairbank、Doll–Näbauer、1961 年）。BCS 理論が予言した電子対形成を、単一の測定量で裏づけた点で決定的な実験である。

現在では、ジョセフソン効果を通じて $\Phi_0 = h/2e$ が電圧標準（ジョセフソン電圧標準）として使われており、逆に $h/e$ の精密決定に寄与している。

---

## 12 ｜ 宇宙線：GZK 限界（配点 100）

**問 1（10 点）**

$$
k_BT = 8.617\times10^{-5}\times2.725 = 2.348\times10^{-4}\ \mathrm{eV}
$$

$$
\langle E_\gamma\rangle = 2.70\times2.348\times10^{-4} = \boxed{6.34\times10^{-4}\ \mathrm{eV}}
$$

（マイクロ波領域、波長にして約 2 mm）

**問 2（25 点）** 4 元運動量の不変量

$$
s = \left(p_p+p_\gamma\right)^2 = m_p^2c^4 + 2\left(E_pE_\gamma + p_pc\,E_\gamma\right)
$$

（正面衝突なので運動量の内積が $-p_pc\,E_\gamma$ となり、$-2p\cdot k$ の符号で $+$ になる）。$E_p\gg m_pc^2$ では $p_pc\simeq E_p$ なので

$$
s \simeq m_p^2c^4 + 4E_pE_\gamma
$$

しきい値は終状態（$p$ と $\pi^0$）が重心系で静止する場合で $\sqrt s = (m_p+m_\pi)c^2$。

$$
m_p^2c^4+4E_p^{\rm th}E_\gamma = \left(m_p+m_\pi\right)^2c^4 = m_p^2c^4+2m_pm_\pi c^4+m_\pi^2c^4
$$

$$
\boxed{E_p^{\rm th} = \frac{m_\pi c^2\left(2m_pc^2+m_\pi c^2\right)}{4E_\gamma}}
$$

**問 3（20 点）**

$$
m_\pi c^2\left(2m_pc^2+m_\pi c^2\right) = 135.0\times(2\times938.3+135.0) = 135.0\times2011.6 = 2.716\times10^5\ \mathrm{MeV^2}
$$

$$
E_\gamma = 6.34\times10^{-4}\ \mathrm{eV} = 6.34\times10^{-10}\ \mathrm{MeV}
$$

$$
E_p^{\rm th} = \frac{2.716\times10^5}{4\times6.34\times10^{-10}} = 1.07\times10^{14}\ \mathrm{MeV} = \boxed{1.1\times10^{20}\ \mathrm{eV}}
$$

**文献値との差の理由**:

1. **CMB はプランク分布であり、平均値より高エネルギーの光子が指数関数的な裾として存在する**。しきい値は $E_\gamma$ に反比例するので、裾の光子（たとえば $10\,k_BT$）と衝突すれば、陽子のエネルギーがもっと低くてもπ生成が起こる。
2. 実際に問題になるのは「運動学的に許されるか」ではなく「**十分な頻度でエネルギーを失うか**」である。したがって観測的な意味での「GZK カットオフ」は、エネルギー損失長が急落するエネルギー（$4$–$6\times10^{19}$ eV）で定義される。
3. $\Delta^+$ 共鳴には幅（約 120 MeV）があり、しきい値付近でも断面積が立ち上がる。

つまり $1.1\times10^{20}$ eV は「平均的な CMB 光子との正面衝突に対する厳密なしきい値」であって、両者は矛盾しない。

**問 4（15 点）**

$$
\lambda = \frac{1}{n_\gamma\sigma} = \frac{1}{411\times3.0\times10^{-28}} = \frac{1}{1.23\times10^{-25}} = 8.1\times10^{24}\ \mathrm{cm}
$$

$$
\lambda = \frac{8.1\times10^{24}}{3.086\times10^{24}} = \boxed{2.6\ \mathrm{Mpc}}
$$

**問 5（15 点）** 1 回の反応でエネルギーが $0.8$ 倍になるので、$N$ 回で $0.8^N$ 倍。$1/e$ になる条件は

$$
0.8^N = e^{-1} \ \Longrightarrow\ N = \frac{1}{|\ln0.8|} = \frac{1}{0.223} = 4.5
$$

$$
\text{減衰長} \simeq 4.5\times2.6\ \mathrm{Mpc} \simeq \boxed{12\ \mathrm{Mpc}}
$$

（ここでは共鳴ピーク付近の断面積を使ったので、これは短めの見積もりである。エネルギーが下がると断面積も落ちるため、実際の減衰長は数十 Mpc、$10^{20}$ eV 付近で約 50–100 Mpc とされる。オーダーとしては「宇宙論的な距離に比べて圧倒的に短い」が結論である）

**問 6（15 点）** 宇宙の大きさ（ハッブル距離 $\sim4000$ Mpc）に比べて減衰長は 2 桁小さい。したがって

$$
\boxed{10^{20}\ \mathrm{eV}\ \text{級の宇宙線の発生源は、100 Mpc 程度以内の「近傍宇宙」になければならない}}
$$

遠方の源からの粒子は途中で必ず GZK 過程でエネルギーを失い、しきい値以下まで落ちてしまう（この意味で宇宙は超高エネルギー宇宙線に対して不透明である）。結果として、

- エネルギースペクトルは $5\times10^{19}$ eV 付近で急に落ち込むはず（**GZK カットオフ**）
- 到来方向は、近傍の大規模構造（銀河団・活動銀河核・スターバースト銀河）と相関するはず

**観測による検証**: 1990 年代に日本の AGASA がカットオフを超える事象を多数報告し、大論争になった。その後、

- **HiRes**（2008）と **Pierre Auger Observatory**（2008）が、いずれも $4$–$6\times10^{19}$ eV 以上でフラックスの有意な抑制を検出し、GZK カットオフと整合する結果を得た（AGASA のエネルギー決定に系統誤差があったと理解されている）
- **Auger**（2017）は $8\times10^{18}$ eV 以上で、銀河中心と反対方向を向く大規模双極子異方性を $5.2\sigma$ で検出し、超高エネルギー宇宙線が **銀河系外起源**であることを示した
- **Telescope Array** は北天に事象の集中（ホットスポット）を報告している

ただし、抑制の起源が GZK 過程なのか、それとも源そのものの加速限界（最大加速エネルギー）なのかは、組成（陽子か重原子核か）の測定と合わせてなお議論が続いている。
