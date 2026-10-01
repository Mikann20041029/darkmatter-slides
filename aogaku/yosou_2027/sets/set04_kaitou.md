# 解答・解説 — 予想問題 第 4 回

各大問 100 点。

## 1

**(1)（20 点）** $R_2-2R_1$、$R_3-R_1$ を行うと第 2・3 行はともに $(0,0,1,1,0)$ となり、第 4 行と一致する。

$$
A \to \begin{pmatrix} 1&2&1&0&1\\ 0&0&1&1&0\\ 0&0&0&0&0\\ 0&0&0&0&0\end{pmatrix}, \qquad \operatorname{rank}A = 2
$$

**(2)（20 点）** 主成分は第 1 列と第 3 列。

$$
\text{基底}\ \{(1,2,1,0)^\top,\ (1,3,2,1)^\top\},\qquad \dim\operatorname{Im}f = 2
$$

**(3)（30 点）** 階段形より $x_1+2x_2+x_3+x_5 = 0$、$x_3+x_4=0$。自由変数は $x_2, x_4, x_5$。

$$
x_3 = -x_4,\qquad x_1 = -2x_2 + x_4 - x_5
$$

$$
\text{基底}\ \left\{(-2,1,0,0,0)^\top,\ (1,0,-1,1,0)^\top,\ (-1,0,0,0,1)^\top\right\},\qquad \dim\operatorname{Ker}f = 3
$$

**(4)（10 点）** $3+2 = 5 = \dim\mathbb{R}^5$。成立。

**(5)（20 点）** $\boldsymbol b = c_1(1,2,1,0)^\top + c_2(1,3,2,1)^\top$ と書けるための条件を求める。第 4 成分から $c_2 = b_4$、第 1 成分から $c_1 = b_1-b_4$。これを第 2・第 3 成分に代入して

$$
\boxed{\ b_2 = 2b_1+b_4,\qquad b_3 = b_1+b_4\ }
$$

2 つの独立な条件が付くので $\operatorname{Im}f$ は $\mathbb{R}^4$ の 2 次元部分空間である（$\dim = 4-2 = 2$、(2) と整合）。

---

## 3（配点 100）

$s = x+y$ とおく。

$$
f_x = y(1-x)e^{-s}, \qquad f_y = x(1-y)e^{-s}
$$

**停留点（30 点）**: $e^{-s}\ne0$ より $y(1-x)=0$ かつ $x(1-y)=0$。

- $y=0$ のとき第 2 式は $x=0$ → $(0,0)$
- $x=1$ のとき第 2 式は $1-y=0$ → $(1,1)$

$$
\therefore\ (x,y) = (0,0),\ (1,1)
$$

**判定（70 点）**

$$
f_{xx} = y(x-2)e^{-s}, \qquad f_{yy} = x(y-2)e^{-s}, \qquad f_{xy} = (1-x)(1-y)e^{-s}
$$

- $(0,0)$: $f_{xx}=f_{yy}=0$、$f_{xy}=1$。$H = -1 < 0$ → **鞍点**
- $(1,1)$: $f_{xx}=f_{yy}=-e^{-2}$、$f_{xy}=0$。$H = e^{-4}>0$、$f_{xx}<0$ → **極大**

$$
f(1,1) = e^{-2} \simeq 0.1353
$$

（$xy$ を大きくしたいが $e^{-(x+y)}$ が減衰するので、両者の釣り合う点で極大になる）

---

## 4

**(1)（30 点）** 極座標 $x=r\cos\theta$, $y=r\sin\theta$ で

$$
\iint_{\mathbb{R}^2}e^{-(x^2+y^2)}dxdy = \int_0^{2\pi}\!\!d\theta\int_0^\infty e^{-r^2}r\,dr = 2\pi\left[-\frac{e^{-r^2}}{2}\right]_0^\infty = \pi
$$

一方この 2 重積分は直交座標で $\left(\int_{-\infty}^\infty e^{-x^2}dx\right)^2$ と分離できるので

$$
\int_{-\infty}^{\infty}e^{-x^2}dx = \sqrt\pi
$$

**(2)（40 点）** $x^2+y^2\le 2ay \iff x^2+(y-a)^2\le a^2$、すなわち中心 $(0,a)$・半径 $a$ の円板。極座標では $r \le 2a\sin\theta$（$0\le\theta\le\pi$）。

$$
\iint_D (x^2+y^2)dxdy = \int_0^\pi\!\!d\theta\int_0^{2a\sin\theta} r^2\cdot r\,dr
= \int_0^\pi \frac{(2a\sin\theta)^4}{4}d\theta = 4a^4\int_0^\pi\sin^4\theta\,d\theta
$$

$$
= 4a^4\cdot\frac{3\pi}{8} = \boxed{\frac{3\pi a^4}{2}}
$$

**(3)（30 点）** $z\ge0$ となるのは $x^2+y^2\le4$。

$$
V = \iint_{x^2+y^2\le4}(4-x^2-y^2)dxdy = 2\pi\int_0^2(4-r^2)r\,dr = 2\pi\left[2r^2-\frac{r^4}{4}\right]_0^2 = 2\pi(8-4) = \boxed{8\pi}
$$

（放物面の下の体積が、同じ底面・同じ高さの円柱の体積 $16\pi$ のちょうど半分になる）

---

## 7 ｜ 力学：回転座標系（配点 100）

**問 1（25 点）** 演算子として $\left(\frac{d}{dt}\right)_{\rm in} = \left(\frac{d}{dt}\right)_{\rm rot} + \boldsymbol\omega\times$ が成り立つ。位置に 2 回適用すると（$\boldsymbol\omega$ 一定）

$$
\boldsymbol a_{\rm in} = \left(\frac{d}{dt}\right)_{\rm rot}^2\boldsymbol r' + 2\boldsymbol\omega\times\boldsymbol v' + \boldsymbol\omega\times(\boldsymbol\omega\times\boldsymbol r')
$$

慣性系ではニュートンの法則 $m\boldsymbol a_{\rm in} = \boldsymbol F$ が成り立つので

$$
m\boldsymbol a' = \boldsymbol F - 2m\boldsymbol\omega\times\boldsymbol v' - m\boldsymbol\omega\times(\boldsymbol\omega\times\boldsymbol r')
$$

第 2 項が **コリオリ力**、第 3 項が **遠心力**（いずれも慣性力＝見かけの力）。コリオリ力は速度に依存し、遠心力は位置のみに依存する点が異なる。

**問 2（20 点）** 緯度 $\lambda$ の地点は自転軸から $R\cos\lambda$ 離れているので、遠心力の加速度は大きさ $\omega^2R\cos\lambda$、向きは軸から外向き。鉛直（地心方向）成分はこれに $\cos\lambda$ を掛けたもの。

$$
g_{\rm eff} \simeq g - \omega^2R\cos^2\lambda
$$

赤道での補正量は

$$
\omega^2R = (7.29\times10^{-5})^2\times6.37\times10^6 = 3.39\times10^{-2}\ \mathrm{m/s^2}
$$

すなわち赤道と極で $0.034\ \mathrm{m/s^2}$（約 0.35 %）の差。実測の差は約 $0.052\ \mathrm{m/s^2}$ で、残りは地球が扁平（赤道半径のほうが大きい）ことによる。

**問 3（25 点）** 局所座標を $x$: 東、$y$: 北、$z$: 上とすると $\boldsymbol\omega = \omega(0,\cos\lambda,\sin\lambda)$。0 次近似で $\boldsymbol v' \simeq (0,0,-gt)$ とすると

$$
\boldsymbol\omega\times\boldsymbol v' = \begin{vmatrix}\hat x&\hat y&\hat z\\ 0&\omega\cos\lambda&\omega\sin\lambda\\ 0&0&-gt\end{vmatrix} = (-\omega gt\cos\lambda,\,0,\,0)
$$

$$
\therefore\ a_x = -2(\boldsymbol\omega\times\boldsymbol v')_x = +2\omega gt\cos\lambda\ (>0,\ \text{東向き})
$$

2 回積分して（初速・初期変位ゼロ）

$$
\Delta x = \frac{1}{3}\omega g\cos\lambda\,t_f^3, \qquad t_f = \sqrt{\frac{2h}{g}}
$$

**東向きになる理由**: 慣性系で見ると、高さ $h$ にある物体は地表より自転軸から遠いので、より大きな東向きの接線速度を持っている。落下中もその速度を保つため、地表より東へ「先回り」する。

**問 4（15 点）** $\lambda = 35.7^\circ$、$h = 100$ m。

$$
t_f = \sqrt{\frac{2\times100}{9.80}} = 4.518\ \mathrm{s}, \qquad \cos\lambda = 0.8124
$$

$$
\Delta x = \frac13\times7.29\times10^{-5}\times9.80\times0.8124\times(4.518)^3 = 1.78\times10^{-2}\ \mathrm{m} \simeq \boxed{1.8\ \mathrm{cm}}
$$

**問 5（15 点）** フーコー振り子の振動面は、局所鉛直まわりの自転角速度成分 $\omega\sin\lambda$ で（地面に対して）回転する。水平面内の運動に効くのはコリオリ力の鉛直成分まわりの寄与だけだからである。したがって 1 回転に要する時間は

$$
T = \frac{2\pi}{\omega\sin\lambda} = \frac{24\ \mathrm{h}}{\sin\lambda}
$$

東京（$\lambda=35.7^\circ$、$\sin\lambda = 0.5835$）では

$$
T = \frac{24}{0.5835} = \boxed{41.1\ \mathrm{h}}
$$

南半球では $\lambda<0$ で $\sin\lambda$ の符号が変わるため、回転の向きが逆（北半球で時計回り、南半球で反時計回り）になる。赤道（$\lambda=0$）では回転しない。

---

## 8 ｜ 電磁気学（配点 100）

### 問 1（40 点）

**(1)** 像電荷を球の中心と $q$ を結ぶ線上、中心から距離 $b$ の位置に置く。球面上の任意の点（中心からの角を $\theta$）での電位は

$$
V = \frac{1}{4\pi\varepsilon_0}\left[\frac{q}{\sqrt{a^2+d^2-2ad\cos\theta}} + \frac{q'}{\sqrt{a^2+b^2-2ab\cos\theta}}\right]
$$

これが任意の $\theta$ でゼロになる条件から

$$
\boxed{q' = -\frac{a}{d}q, \qquad b = \frac{a^2}{d}}
$$

（実際に代入すると、第 2 項の分母が $\frac{a}{d}\sqrt{a^2+d^2-2ad\cos\theta}$ となり第 1 項と打ち消す）$b<a$ なので像電荷は球の内部にあり、球外の解として正当である。

**(2)** 接地された導体球に誘導される総電荷は像電荷に等しい。

$$
Q_{\rm ind} = q' = -\frac{a}{d}q
$$

**(3)** 力は $q$ と像電荷のクーロン力に等しい。距離は $d - b = d - a^2/d = (d^2-a^2)/d$。

$$
F = \frac{1}{4\pi\varepsilon_0}\frac{qq'}{(d-b)^2} = -\frac{1}{4\pi\varepsilon_0}\frac{aq^2d}{(d^2-a^2)^2}
$$

負号は **引力**を意味する（接地導体は常に電荷を引きつける）。$d\gg a$ では

$$
F \simeq -\frac{1}{4\pi\varepsilon_0}\frac{aq^2}{d^3}
$$

$1/d^3$ で減衰する。これは点電荷と、それが誘起した双極子との相互作用の形であり、球の分極率が $4\pi\varepsilon_0a^3$ であることに対応する。

### 問 2（30 点）

**(1)** 十分長いソレノイド内部は一様で $B_1 = \mu_0n_1I_1$（外部はゼロ）。

**(2)** 小コイル 1 巻きを貫く磁束は $\Phi = B_1S = \mu_0n_1I_1S$。$N_2$ 回巻きなので鎖交磁束は $N_2\Phi$。

$$
M = \frac{N_2\Phi}{I_1} = \boxed{\mu_0 n_1N_2S}
$$

**(3)** 小コイルに電流を流したときの磁場は複雑（双極子的に広がる）で、ソレノイド全体を貫く磁束を直接計算するのは面倒である。しかし相反定理 $M_{12}=M_{21}$ が成り立つので、計算しやすいほうの向きで求めればよい。

相反定理の根拠は、系の磁気エネルギーが状態量であって電流を立ち上げる順序によらないことにある。**計算の難しい配置を、計算しやすい逆向きの配置に置き換えられる**点が、この定理の実用上の価値である。

### 問 3（30 点）

**(1)**

$$
Z(\omega) = R + i\left(\omega L - \frac{1}{\omega C}\right), \qquad
I_0 = \frac{V_0}{|Z|} = \frac{V_0}{\sqrt{R^2+\left(\omega L-\frac{1}{\omega C}\right)^2}}
$$

電流は電圧に対して位相 $\phi = \arctan\dfrac{\omega L - 1/\omega C}{R}$ だけ遅れる（$\omega>\omega_0$ で誘導性、$\omega<\omega_0$ で容量性）。

**(2)** $|Z|$ が最小になるのはリアクタンスがゼロのとき。

$$
\omega_0 L = \frac{1}{\omega_0 C} \ \Longrightarrow\ \omega_0 = \frac{1}{\sqrt{LC}}
$$

**(3)** 平均電力は

$$
\bar P = \frac12 I_0^2R = \frac{V_0^2R}{2\left[R^2+\left(\omega L-\frac{1}{\omega C}\right)^2\right]}
$$

最大値は $\omega=\omega_0$ での $V_0^2/2R$。その半分になる条件は

$$
\left(\omega L-\frac{1}{\omega C}\right)^2 = R^2 \ \Longleftrightarrow\ \omega L - \frac{1}{\omega C} = \pm R
$$

$\omega^2 \mp \dfrac{R}{L}\omega - \dfrac{1}{LC} = 0$ の正根をとると

$$
\omega_\pm = \pm\frac{R}{2L} + \sqrt{\frac{R^2}{4L^2}+\frac{1}{LC}}
\ \Longrightarrow\ \Delta\omega = \omega_+-\omega_- = \frac{R}{L}
$$

$$
Q = \frac{\omega_0}{\Delta\omega} = \frac{1}{\sqrt{LC}}\cdot\frac{L}{R} = \boxed{\frac{1}{R}\sqrt{\frac{L}{C}}}
$$

---

## 9 ｜ 量子力学：1 次摂動論（配点 100）

**問 1（20 点）** $\hat H = \hat H_0 + \eta\hat V'$ とし

$$
|n\rangle = |n^{(0)}\rangle + \eta|n^{(1)}\rangle + \cdots, \qquad E_n = E_n^{(0)} + \eta E_n^{(1)} + \cdots
$$

を $\hat H|n\rangle = E_n|n\rangle$ に代入して $\eta$ の 1 次の項を集めると

$$
\hat H_0|n^{(1)}\rangle + \hat V'|n^{(0)}\rangle = E_n^{(0)}|n^{(1)}\rangle + E_n^{(1)}|n^{(0)}\rangle
$$

左から $\langle n^{(0)}|$ を掛け、$\langle n^{(0)}|\hat H_0 = E_n^{(0)}\langle n^{(0)}|$ を使うと第 1 項どうしが消えて

$$
E_n^{(1)} = \langle n^{(0)}|\hat V'|n^{(0)}\rangle
$$

**問 2（20 点）**

$$
E_n^{(1)} = V_0\int_0^{L/2}\frac{2}{L}\sin^2\frac{n\pi x}{L}dx
= V_0\cdot\frac{2}{L}\left[\frac{x}{2}-\frac{L\sin(2n\pi x/L)}{4n\pi}\right]_0^{L/2}
= V_0\cdot\frac{2}{L}\cdot\frac{L}{4} = \boxed{\frac{V_0}{2}}
$$

$\sin(n\pi)=0$ なので第 2 項は $n$ によらず消える。

物理的理由: $|\varphi_n(x)|^2 = \frac2L\sin^2\frac{n\pi x}{L}$ は $x = L/2$ に関して対称である（$\sin^2\frac{n\pi(L-x)}{L} = \sin^2\frac{n\pi x}{L}$）。したがって **どの準位でも粒子が左半分にいる確率はちょうど 1/2**。ポテンシャルを左半分だけ $V_0$ だけ持ち上げれば、期待値は必ず $V_0/2$ 上がる。

**問 3（20 点）** 積和公式を用いて

$$
\langle m|V'|n\rangle = \frac{2V_0}{L}\int_0^{L/2}\sin\frac{m\pi x}{L}\sin\frac{n\pi x}{L}dx
= \frac{V_0}{\pi}\left[\frac{\sin\frac{(m-n)\pi}{2}}{m-n} - \frac{\sin\frac{(m+n)\pi}{2}}{m+n}\right]
$$

$m-n$ が偶数なら $m+n$ も偶数で、$\sin(\text{整数}\times\pi)=0$ となり両項ともゼロ。**$m-n$ が奇数のときのみ非ゼロ。**

これは、$V'$ が $x=L/2$ に関して奇の成分（$V_0/2$ の定数部分を除いた符号関数）を持ち、$\varphi_m\varphi_n$ が $m-n$ 奇数のとき $x=L/2$ に関して奇になることの帰結である。

例: $\langle2|V'|1\rangle = \dfrac{V_0}{\pi}\left[\dfrac{\sin(\pi/2)}{1}-\dfrac{\sin(3\pi/2)}{3}\right] = \dfrac{V_0}{\pi}\left(1+\dfrac13\right) = \dfrac{4V_0}{3\pi}$

**問 4（20 点）** 1 次の波動関数補正の公式

$$
|n^{(1)}\rangle = \sum_{m\ne n}\frac{\langle m|V'|n\rangle}{E_n^{(0)}-E_m^{(0)}}|m\rangle
$$

$n=1$、$m=2$ の項のみ残す。$E_2^{(0)} = 4E_1^{(0)}$ より $E_1^{(0)}-E_2^{(0)} = -3E_1^{(0)}$。

$$
|1\rangle \simeq |1^{(0)}\rangle - \frac{4V_0}{9\pi E_1^{(0)}}|2^{(0)}\rangle, \qquad E_1^{(0)} = \frac{\hbar^2\pi^2}{2mL^2}
$$

符号の意味: $\varphi_2$ は左半分で正、右半分で負なので、これを負の係数で混ぜると **左半分の振幅が減り右半分が増える**。ポテンシャルが持ち上がった側から粒子が逃げるという直観と一致する。

**問 5（10 点）**

$$
E_1^{(2)} = \sum_{m\ne1}\frac{|\langle m|V'|1\rangle|^2}{E_1^{(0)}-E_m^{(0)}}
$$

分子は正、分母は $E_1^{(0)}$ が最低準位なのですべて負。したがって $E_1^{(2)} < 0$。**基底状態の 2 次補正は常に負**である（摂動は基底状態のエネルギーを必ず下げる）。

**問 6（10 点）** 摂動展開の各項が小さいための条件は

$$
\left|\frac{\langle m|V'|n\rangle}{E_n^{(0)}-E_m^{(0)}}\right| \ll 1
$$

最も厳しいのは準位間隔が小さい低い準位どうし、たとえば $n=1,m=2$ で

$$
\frac{4V_0/3\pi}{3E_1^{(0)}} \ll 1 \ \Longrightarrow\ V_0 \ll \frac{9\pi}{4}E_1^{(0)} \simeq 7E_1^{(0)}
$$

実用上は $V_0 \ll E_1^{(0)} = \dfrac{\hbar^2\pi^2}{2mL^2}$ と覚えておけばよい。

---

## 10 ｜ 統計力学：ゴム弾性（配点 100）

**問 1（10 点）** $N$ 個から $N_+$ 個を選ぶ組合せなので

$$
W = \frac{N!}{N_+!\,N_-!}, \qquad N_\pm = \frac{1}{2}\left(N\pm\frac{L}{a}\right)
$$

**問 2（20 点）** $S = k_B\ln W$ にスターリングの公式を適用して

$$
S = k_B\left(N\ln N - N_+\ln N_+ - N_-\ln N_-\right)
$$

**問 3（30 点）** $U=0$ なので $F = -TS$。$\partial N_\pm/\partial L = \pm1/(2a)$ を使って

$$
\frac{\partial S}{\partial L} = k_B\left[-\left(\ln N_++1\right)\frac{1}{2a} + \left(\ln N_-+1\right)\frac{1}{2a}\right] = -\frac{k_B}{2a}\ln\frac{N_+}{N_-}
$$

$$
f = \left(\frac{\partial F}{\partial L}\right)_T = -T\frac{\partial S}{\partial L} = \frac{k_BT}{2a}\ln\frac{N_+}{N_-}
= \boxed{\frac{k_BT}{2a}\ln\frac{1+L/Na}{1-L/Na}}
$$

**この張力は完全にエントロピー起源**である（$U=0$ なのでエネルギー的な寄与がない）。

**問 4（15 点）** $u = L/(Na) \ll 1$ で $\ln\dfrac{1+u}{1-u} \simeq 2u$。

$$
f \simeq \frac{k_BT}{2a}\cdot\frac{2L}{Na} = \frac{k_BT}{Na^2}L
\ \Longrightarrow\ \boxed{k = \frac{k_BT}{Na^2}}
$$

長い鎖（$N$ 大）ほど柔らかく、温度が高いほど硬い。

**問 5（15 点）** 一定張力 $f$ の下では $L = fNa^2/(k_BT)$ なので、**温度を上げるとゴムは縮む**。おもりを吊るしたゴムひもを加熱すると、おもりが持ち上がる。金属バネ（加熱すると熱膨張で伸び、ヤング率はむしろ下がる）とは正反対である。

理由: ゴムの張力は「伸びた状態は取りうる配置の数が少ない＝エントロピーが低い」ことに由来する。温度が高いほど、同じエントロピー減少に対する自由エネルギーの罰則 $-T\Delta S$ が大きくなるので、縮もうとする力が強くなる。

**問 6（10 点）** 全エントロピーを、鎖の配置エントロピー $S_{\rm conf}(L)$ と、原子振動などの熱的自由度のエントロピー $S_{\rm th}(T)$ に分ける。

断熱準静的に伸ばすと $dS_{\rm total}=0$。伸ばすと $S_{\rm conf}$ は減少する（配置数が減る）ので、$S_{\rm th}$ は増えなければならない。$S_{\rm th}$ は温度の増加関数なので、**温度が上がる**。

エネルギー的には、外部がした仕事 $f\,dL$ が熱的自由度に蓄えられたことになる。逆に縮めると温度が下がる。この効果を利用した「ゴム熱機関」も作れる（弾性熱量効果）。

---

## 11 ｜ 物性物理：強束縛バンド（配点 100）

**問 1（20 点）** $|k\rangle = \frac{1}{\sqrt N}\sum_n e^{ikna}|n\rangle$ に $\hat H$ を作用させ、$\langle n|$ を掛けると

$$
\langle n|\hat H|k\rangle = \frac{1}{\sqrt N}\left[\varepsilon_0 e^{ikna} - t\left(e^{ik(n+1)a}+e^{ik(n-1)a}\right)\right]
= \left[\varepsilon_0 - 2t\cos ka\right]\frac{e^{ikna}}{\sqrt N}
$$

右辺は $\langle n|k\rangle$ の定数倍なので $|k\rangle$ は固有状態であり

$$
\boxed{E(k) = \varepsilon_0 - 2t\cos ka}
$$

**問 2（10 点）** 周期境界条件から $k = \dfrac{2\pi j}{Na}$（$j$ は整数）。$k$ と $k+2\pi/a$ は同じ状態を与えるので、独立な $k$ は

$$
-\frac{\pi}{a} < k \le \frac{\pi}{a} \qquad (\text{第 1 ブリルアンゾーン、}N\text{ 個})
$$

バンド幅は $E_{\max}-E_{\min} = (\varepsilon_0+2t)-(\varepsilon_0-2t) = \boxed{4t}$。

**問 3（20 点）** $k\to0$ で $\cos ka \simeq 1 - \frac{(ka)^2}{2}$ より

$$
E(k) \simeq (\varepsilon_0-2t) + ta^2k^2
$$

$E = \dfrac{\hbar^2k^2}{2m^*}$ と比較して

$$
\boxed{m^* = \frac{\hbar^2}{2ta^2}}
$$

$t$ が大きい（隣接サイトへ飛び移りやすい）ほど $m^*$ は小さい。**遍歴しやすさがそのまま「軽さ」として現れる**。逆に $t\to0$（孤立した原子）では $m^*\to\infty$ となり、電子は動けない。

**問 4（20 点）** $k = \pi/a + q$ とすると $\cos ka = -\cos qa \simeq -1+\frac{(qa)^2}{2}$ より

$$
E \simeq (\varepsilon_0+2t) - ta^2q^2
$$

$\dfrac{d^2E}{dq^2} = -2ta^2 < 0$ なので $m^* = \dfrac{\hbar^2}{d^2E/dq^2} < 0$、すなわち **負の有効質量**。

このとき電子は外力と逆向きに加速される。この振る舞いは扱いにくいので、代わりに「バンドの空席（正の電荷 $+e$、正の有効質量 $|m^*|$ をもつ粒子）」＝**正孔**として記述する。ほぼ満たされたバンドを、少数の正孔で記述するほうが圧倒的に簡単である。

**問 5（20 点）** 単位長さあたりの状態密度は（スピンを除いて、$\pm k$ の 2 つを数えて）

$$
D(E) = \frac{2}{2\pi}\left|\frac{dk}{dE}\right| = \frac{1}{\pi}\left|\frac{dk}{dE}\right|
$$

$\dfrac{dE}{dk} = 2ta\sin ka$、$\sin ka = \sqrt{1-\left(\frac{\varepsilon_0-E}{2t}\right)^2}$ より

$$
\boxed{D(E) = \frac{1}{\pi a\sqrt{4t^2-(E-\varepsilon_0)^2}}}
$$

バンド端 $E = \varepsilon_0\pm2t$ で発散する（**ファン・ホーヴ特異点**）。群速度 $v_g = \hbar^{-1}dE/dk$ がバンド端でゼロになるためである。

3 次元では、等エネルギー面の面積が $k^{d-1}$ の因子を持ち、バンド端で面積がゼロに向かう。$1/v_g$ の発散とこの面積のゼロが競合し、結果として $D(E)\propto\sqrt{E-E_c}$ となって発散しない。**次元は等エネルギー面の次元 $d-1$ を通して効く。**

**問 6（10 点）** 欠けているのは **電子間クーロン相互作用**である。同一サイトに 2 個の電子が乗るときのエネルギー $U$（ハバード模型のオンサイト斥力）を取り入れると、$U \gg t$ の場合、半充填では各サイトに電子が 1 個ずつ局在するほうが得になり、電荷の移動に $U$ のギャップが生じる。これが **モット絶縁体**である。

また、格子を固定と仮定している点も不完全である。1 次元系では格子が二量体化して周期が $2a$ になり、$k=\pi/2a$ にギャップが開く **パイエルス転移** が起こりうる。いずれも「バンド理論だけでは金属になるはずの系が絶縁体になる」機構である。

---

## 12 ｜ 原子核：結合エネルギーと $Q$ 値（配点 100）

**問 1（10 点）**

$$
B = \left[Zm_p + (A-Z)m_n - M(Z,A)\right]c^2
$$

核子は核力で互いに引き合っており、束縛系を作るときにその分のエネルギーが放出される。系のエネルギーが下がった分だけ、相対論的な質量エネルギー等価性により質量が減る（質量欠損）。$B$ は逆に「核をばらばらの核子に分解するのに必要なエネルギー」である。

**問 2（20 点）**

$$
\Delta m = 2\times1.007276 + 2\times1.008665 - 4.001506 = 0.030376\ \mathrm{u}
$$

$$
B = 0.030376\times931.494 = \boxed{28.30\ \mathrm{MeV}}, \qquad \frac{B}{A} = \frac{28.30}{4} = \boxed{7.07\ \mathrm{MeV}}
$$

$^4$He は $A<12$ の軽い核としては際立って $B/A$ が大きい（魔法数 $Z=N=2$ の二重閉殻）。$\alpha$ 崩壊が起こるのはこの安定性による。

**問 3（20 点）** 概形: $A$ が小さいところから急激に立ち上がり、$A\simeq56$（$^{56}$Fe、$B/A\simeq8.8$ MeV）付近で最大となり、その後ゆるやかに減少して $^{238}$U では $7.6$ MeV 程度になる。$^4$He、$^{12}$C、$^{16}$O は曲線より上に飛び出す。

**核分裂**: 重い核（$B/A\simeq7.6$）が中程度の核（$B/A\simeq8.5$）2 つに分かれると、核子 1 個あたり約 0.9 MeV だけ束縛が強くなる。$A\simeq236$ を掛けて約 200 MeV が解放される。

**核融合**: 軽い核（$B/A$ が小さい）が結合してより $B/A$ の大きい核になると、その差が解放される。

要するに **どちらも「$^{56}$Fe に向かって坂を下る」反応**であり、鉄より軽い側では融合、重い側では分裂がエネルギーを出す。恒星の元素合成が鉄で止まるのもこのためである。

**問 4（20 点）**

$$
\Delta m = (2.014102+3.016049) - (4.002603+1.008665) = 5.030151-5.011268 = 0.018883\ \mathrm{u}
$$

$$
Q = 0.018883\times931.494 = \boxed{17.59\ \mathrm{MeV}}
$$

原子質量（電子を含む質量）を使ってよい理由: 反応の前後で電子の総数が変わらない（左辺 $1+1=2$ 個、右辺 $2+0=2$ 個）ので、電子の質量が差し引きで消える。電子の束縛エネルギー（数十 eV）は MeV に比べて無視できる。

**問 5（20 点）** 静止した状態から始まるので、生成粒子の運動量は大きさが等しく逆向き: $p_{\rm He} = p_n = p$。非相対論的に

$$
E_{\rm He} = \frac{p^2}{2m_{\rm He}}, \qquad E_n = \frac{p^2}{2m_n}
\ \Longrightarrow\ \frac{E_n}{E_{\rm He}} = \frac{m_{\rm He}}{m_n}
$$

**軽いほうが大きなエネルギーを持ち去る。**

$$
E_n = Q\frac{m_{\rm He}}{m_{\rm He}+m_n} = 17.59\times\frac{4.0026}{5.0113} = \boxed{14.1\ \mathrm{MeV}}
$$

$$
E_{\rm He} = 17.59 - 14.1 = \boxed{3.5\ \mathrm{MeV}}
$$

この 14 MeV 中性子が核融合炉での材料損傷とトリチウム増殖（ブランケット）の鍵を握る。3.5 MeV の $\alpha$ 粒子はプラズマ中に留まって加熱に寄与する（自己点火条件）。

**問 6（10 点）** D と T はともに正電荷を持つので、近づくにはクーロン障壁を越えねばならない。接触距離を $R \simeq r_0(A_1^{1/3}+A_2^{1/3}) \simeq 1.2\times(1.26+1.44) = 3.2$ fm とすると

$$
V_C = \frac{e^2}{4\pi\varepsilon_0R} = \frac{1.44\ \mathrm{MeV\cdot fm}}{3.2\ \mathrm{fm}} \simeq 0.45\ \mathrm{MeV}
$$

これを熱運動でまかなうには $k_BT\sim0.45$ MeV、すなわち $T\sim5\times10^9$ K が必要になる。しかし実際の核融合は $T\sim10^8$ K（$k_BT\sim10$ keV）で進む。

理由は 2 つある。

1. **トンネル効果**: 障壁を古典的に越える必要はなく、透過確率 $\propto e^{-2\pi\eta}$（ガモフ因子）で染み出せる。
2. **マクスウェル分布の高エネルギー裾**: 平均エネルギーが 10 keV でも、その数倍〜十数倍のエネルギーを持つ粒子が指数関数的に少数存在する。この「速い少数」が反応を担う。

指数関数的に減る分布の裾と、指数関数的に増えるトンネル確率の積が特定のエネルギーで極大を作る。これを **ガモフピーク** と呼び、恒星内の核燃焼でも同じ機構が働いている。
