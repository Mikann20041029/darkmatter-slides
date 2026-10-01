# 解答・解説 — 予想問題 第 6 回

各大問 100 点。

## 1

$J$ を全成分 1 の 3 次行列とすると $A = 3E - J$ と書ける。$J$ の固有値は $3$（固有ベクトル $(1,1,1)^\top$）と $0$（2 重）なので、$A$ の固有値は $0$（1 重）と $3$（2 重）。

**(1)（15 点）** 固有値 0 の重複度が 1 なので $\dim\operatorname{Ker} = 1$、したがって $\operatorname{rank}A = 2$。

**(2)（20 点）** $A\boldsymbol x = 0$ は $(1,1,1)^\top$ の定数倍。

$$
\text{基底}\ \{(1,1,1)^\top\},\qquad \dim\operatorname{Ker}f = 1
$$

**(3)（25 点）** $A$ の各行の成分の和は $2-1-1 = 0$ なので、任意の $\boldsymbol x$ に対して $(A\boldsymbol x)_1+(A\boldsymbol x)_2+(A\boldsymbol x)_3 = 0$。よって

$$
\operatorname{Im}f \subseteq \{\boldsymbol y \mid y_1+y_2+y_3 = 0\}
$$

右辺は 2 次元で $\dim\operatorname{Im}f = 2$ だから両者は一致する。

$$
\text{基底}\ \{(1,-1,0)^\top,\ (1,0,-1)^\top\}, \qquad \operatorname{Im}f: y_1+y_2+y_3 = 0
$$

**(4)（20 点）** $J^2 = 3J$ を使って

$$
A^2 = (3E-J)^2 = 9E - 6J + J^2 = 9E - 3J = 3(3E-J) = 3A
$$

$P = A/3$ とすると $P^2 = A^2/9 = 3A/9 = A/3 = P$。**べき等**である。

**(5)（20 点）** $P$ はべき等かつ対称（$P^\top = P$）なので **直交射影**である。射影先は $\operatorname{Im}P = \operatorname{Im}f$、すなわち平面 $y_1+y_2+y_3=0$。射影の方向（つぶれる向き）は $\operatorname{Ker}P = \operatorname{Ker}f = \operatorname{span}\{(1,1,1)\}$ で、これはちょうどその平面の **法線** である。

したがって $f$ は「$(1,1,1)$ 方向の成分を取り除いて平面に垂直に落とし、3 倍する」写像である。$\mathbb{R}^3 = \operatorname{Ker}f \oplus \operatorname{Im}f$ という直交直和分解が成り立っている（一般の線形写像では核と像が直和になるとは限らないので、これはべき等性に固有の性質）。

---

## 3（配点 100）

$$
f_x = e^{-x}\left(2x - x^2 - y^2\right), \qquad f_y = 2y\,e^{-x}
$$

**停留点（30 点）**: $f_y = 0$ より $y = 0$。これを $f_x=0$ に入れて $2x-x^2 = x(2-x) = 0$。

$$
(x,y) = (0,0),\ (2,0)
$$

**判定（70 点）**

$$
f_{xx} = e^{-x}\left(2-4x+x^2+y^2\right), \qquad f_{yy} = 2e^{-x}, \qquad f_{xy} = -2y\,e^{-x}
$$

- $(0,0)$: $f_{xx}=2$、$f_{yy}=2$、$f_{xy}=0$。$H = 4>0$、$f_{xx}>0$ → **極小**、$f(0,0) = 0$
- $(2,0)$: $f_{xx} = e^{-2}(2-8+4) = -2e^{-2}$、$f_{yy} = 2e^{-2}$、$f_{xy}=0$。$H = -4e^{-4}<0$ → **鞍点**、$f(2,0) = 4e^{-2} \simeq 0.541$

補足: $f = (x^2+y^2)e^{-x} \ge 0$ で等号は原点のみだから、$(0,0)$ は **最小値** $0$ を与える。一方 $x\to-\infty$ で $f\to+\infty$ なので最大値はない。

---

## 4

**(1)（30 点）** 極座標で $D$ は $0\le r\le a$、$0\le\theta\le\pi$。

$$
\iint_D y\,dxdy = \int_0^\pi\!\!\int_0^a (r\sin\theta)\,r\,dr\,d\theta = \frac{a^3}{3}\int_0^\pi\sin\theta\,d\theta = \frac{a^3}{3}\cdot2 = \boxed{\frac{2a^3}{3}}
$$

（重心の $y$ 座標が $\frac{2a^3/3}{\pi a^2/2} = \frac{4a}{3\pi}$ となることに対応）

**(2)（35 点）** $x\to+0$ で被積分関数は $x^{-1/2}\ln x$ で発散するが、$|x^{-1/2}\ln x| \le C x^{-1/2+\delta}$（任意の小さな $\delta>0$）と評価でき、$\int_0^1 x^{-1/2+\delta}dx$ は収束する。よって広義積分は収束する。

部分積分（$u = \ln x$、$dv = x^{-1/2}dx$、$v = 2\sqrt x$）:

$$
\int_\epsilon^1\frac{\ln x}{\sqrt x}dx = \left[2\sqrt x\ln x\right]_\epsilon^1 - \int_\epsilon^1\frac{2}{\sqrt x}dx
= -2\sqrt\epsilon\ln\epsilon - \left[4\sqrt x\right]_\epsilon^1
$$

$\epsilon\to0$ で $\sqrt\epsilon\ln\epsilon\to0$ だから

$$
\int_0^1\frac{\ln x}{\sqrt x}dx = 0 - 4 = \boxed{-4}
$$

**(3)（35 点）** $e^{x^2}$ は初等的な原始関数を持たないので、$y$ を先に積分する。$D$ は $0\le x\le1$、$0\le y\le x$。

$$
\int_0^1\!\!dx\int_0^x e^{x^2}dy = \int_0^1 xe^{x^2}dx = \left[\frac{e^{x^2}}{2}\right]_0^1 = \boxed{\frac{e-1}{2}} \simeq 0.8591
$$

---

## 7 ｜ 力学：ラザフォード散乱（配点 100）

**問 1（20 点）** 角運動量 $\ell = mv_\infty b$、エネルギー $E = \frac12mv_\infty^2$ が保存する。斥力クーロン場の軌道は双曲線であり、漸近線のなす角から

$$
\tan\frac{\theta}{2} = \frac{k}{2Eb} \ \Longleftrightarrow\ \boxed{b = \frac{k}{2E}\cot\frac{\theta}{2}}
$$

（$b\to\infty$ で $\theta\to0$、$b\to0$ で $\theta\to\pi$ と、直観と整合する）

**問 2（25 点）** 上式より

$$
\frac{db}{d\theta} = -\frac{k}{4E}\csc^2\frac{\theta}{2}
$$

$\sin\theta = 2\sin\frac\theta2\cos\frac\theta2$ を用いて

$$
\frac{d\sigma}{d\Omega} = \frac{b}{\sin\theta}\left|\frac{db}{d\theta}\right|
= \frac{\frac{k}{2E}\frac{\cos(\theta/2)}{\sin(\theta/2)}}{2\sin\frac\theta2\cos\frac\theta2}\cdot\frac{k}{4E}\frac{1}{\sin^2(\theta/2)}
= \boxed{\left(\frac{k}{4E}\right)^2\frac{1}{\sin^4(\theta/2)}}
$$

**問 3（10 点）** 正面衝突では全運動エネルギーがポテンシャルエネルギーに変わる。

$$
E = \frac{k}{d} \ \Longrightarrow\ d = \frac{k}{E}
$$

**問 4（20 点）**

$$
k = Zz\cdot1.44 = 79\times2\times1.44 = 227.5\ \mathrm{MeV\cdot fm}
$$

$$
d = \frac{227.5}{5.0} = \boxed{45.5\ \mathrm{fm}}
$$

金の核半径は

$$
R = 1.2\times197^{1/3} = 1.2\times5.82 = 7.0\ \mathrm{fm}
$$

$d \simeq 45\ \mathrm{fm} \gg R \simeq 7\ \mathrm{fm}$ なので、$\alpha$ 粒子は核表面にまったく届かず、**純粋なクーロン力しか感じない**。核力（到達距離 $\sim$ 数 fm）が効かないので、点電荷どうしの散乱として導いたラザフォードの公式がそのまま成り立つ。

（逆に入射エネルギーを上げて $d \lesssim R$ にすると公式からのずれが現れ、そのずれから核半径を決められる。これが実際に行われた核半径測定の手法である）

**問 5（15 点）**

$$
\sigma_{\rm tot} = \int\frac{d\sigma}{d\Omega}2\pi\sin\theta\,d\theta \propto \int_0 \frac{\sin\theta}{\sin^4(\theta/2)}d\theta \sim \int_0\frac{\theta}{\theta^4}d\theta = \int_0\frac{d\theta}{\theta^3}
$$

$\theta\to0$（＝ $b\to\infty$）で発散する。

物理的理由: クーロン力は $1/r^2$ で無限遠まで届くので、**どんなに大きな衝突径数でも必ずわずかに曲がる**。「散乱されなかった」粒子が存在しないため、全断面積は無限大になる。

実験で問題にならない理由: (i) 実際の標的では原子核の電荷が軌道電子に遮蔽されており、$b$ が原子サイズ（$\sim10^5$ fm）を超えると力が急速に消える。(ii) 検出器には有限の角度分解能があり、ある最小角より小さい散乱は「散乱されなかった」ものと区別できない。いずれも $\theta$ に下限を与え、実測される断面積は有限になる。

**問 6（10 点）** トムソンの「ぶどうパン模型」では、正電荷が原子全体（$\sim10^{-10}$ m）に薄く広がっているため電場が弱く、$\alpha$ 粒子は多数回の小角散乱を重ねてもせいぜい 1$^\circ$ 程度しか曲がらない。統計的にも 90$^\circ$ を超える確率は $10^{-3500}$ 程度と、事実上ゼロである。

ところが実験では約 8000 個に 1 個が 90$^\circ$ 以上に跳ね返された。これは **1 回の近接遭遇で巨大な力積を受けた**としか説明できない。$\theta$ が大きい事象は $b$ が小さい事象であり、問 1 から $b\sim k/2E$、すなわち $10^{-14}$ m のスケールまで近づいて初めて起こる。したがって正電荷は原子の $10^{-4}$ 倍程度の領域に集中していなければならない。ラザフォード自身の「15 インチ砲弾をティッシュペーパーに撃ったら跳ね返ってきたようなもの」という表現はこの論理を指している。

---

## 8 ｜ 電磁気学（配点 100）

### 問 1（30 点）

**(1)** 境界をまたぐ薄い円柱（パイルボックス）にガウスの法則 $\oint\boldsymbol D\cdot d\boldsymbol S = Q_{\rm free}$ を適用する。側面の寄与は厚さ $\to0$ で消え、自由電荷がないので

$$
D_{1n} = D_{2n}
$$

境界をまたぐ細長い長方形ループに $\oint\boldsymbol E\cdot d\boldsymbol l = -\frac{d\Phi_B}{dt}$ を適用する。ループの面積 $\to0$ で右辺は消え

$$
E_{1t} = E_{2t}
$$

**(2)** 法線からの角を $\theta$ とすると $\tan\theta = E_t/E_n$。$E_{1t}=E_{2t}$ かつ $\varepsilon_1E_{1n} = \varepsilon_2E_{2n}$ より

$$
\frac{\tan\theta_1}{\tan\theta_2} = \frac{E_{1t}/E_{1n}}{E_{2t}/E_{2n}} = \frac{E_{2n}}{E_{1n}} = \frac{\varepsilon_1}{\varepsilon_2}
$$

**(3)** $\varepsilon_2\gg\varepsilon_1$ なら $\tan\theta_2 = \frac{\varepsilon_2}{\varepsilon_1}\tan\theta_1 \gg 1$、すなわち $\theta_2\to90^\circ$。誘電率の高い媒質の中では電気力線がほとんど境界面に平行に走る。

意味: 誘電率の高い物質は電気力線を **中に取り込んで導く** ように働く（電束が高 $\varepsilon$ 領域に集中する）。これは高透磁率の鉄心が磁束を導く（磁気回路、ヨーク、磁気シールド）のと完全に対応する静電気版であり、高誘電率材料を使った電界緩和（絶縁設計）の基礎になっている。

### 問 2（35 点）

**(1)** $\boldsymbol M = M\hat{\boldsymbol z}$ は一様なので

$$
\boldsymbol j_b = \nabla\times\boldsymbol M = \boldsymbol 0 \quad(\text{体積磁化電流はゼロ})
$$

側面（外向き法線 $\hat{\boldsymbol r}$）では

$$
\boldsymbol K_b = \boldsymbol M\times\hat{\boldsymbol n} = M\hat{\boldsymbol z}\times\hat{\boldsymbol r} = M\hat{\boldsymbol\phi}
$$

すなわち、円柱の側面に単位長さあたり $M$ の周回電流が流れているのと等価。

**(2)** これは「単位長さあたりの $nI$ が $M$ に等しい無限に長いソレノイド」と同じである。

$$
\boldsymbol B_{\rm in} = \mu_0M\hat{\boldsymbol z}, \qquad \boldsymbol B_{\rm out} = \boldsymbol 0
$$

**(3)**

$$
\boldsymbol H_{\rm in} = \frac{\boldsymbol B_{\rm in}}{\mu_0}-\boldsymbol M = M\hat{\boldsymbol z} - M\hat{\boldsymbol z} = \boldsymbol 0
$$

外部でも $\boldsymbol B = \boldsymbol M = 0$ なので $\boldsymbol H = 0$。**磁化した物体の中でゼロになるのは $\boldsymbol H$ のほう**である。

役割の違い: $\boldsymbol B$ は $\nabla\cdot\boldsymbol B = 0$ を満たす基本的な場で、ローレンツ力を与えるのはこちらである。$\boldsymbol H$ は $\nabla\times\boldsymbol H = \boldsymbol j_{\rm free}$ を満たす補助場で、**自由電流だけを源とする**。本問には自由電流が一切ないので $\boldsymbol H$ は至るところゼロになり、それでも $\boldsymbol B$ は内部に存在する。「$\boldsymbol H$ がゼロだから磁場がない」と考えるのは誤りである。

（なお、無限円柱ではなく有限の棒磁石なら端に磁極（$\nabla\cdot\boldsymbol M \ne 0$）が現れ、内部の $\boldsymbol H$ は $\boldsymbol M$ と逆向きの「反磁場」として残る）

### 問 3（35 点）

**(1)** コンデンサーを充電中の回路で、同じ閉曲線 $C$ を縁とする 2 つの曲面を考える。1 つは導線を横切り（貫く電流 $I$）、もう 1 つは極板の間を通る（貫く導電流 $0$）。もとのアンペールの法則 $\oint\boldsymbol B\cdot d\boldsymbol l = \mu_0I_{\rm enc}$ では、選ぶ曲面によって右辺が変わってしまい矛盾する。

極板間には $\partial\boldsymbol E/\partial t$ があり、$\varepsilon_0\partial\boldsymbol E/\partial t$（変位電流）を加えると、どちらの曲面でも同じ値になる。数学的には、$\nabla\cdot(\nabla\times\boldsymbol B) = 0$ が電荷保存則 $\nabla\cdot\boldsymbol j + \partial\rho/\partial t = 0$ と両立するために必要な項である。

**(2)** $\rho=0$、$\boldsymbol j=0$ のとき

$$
\nabla\times(\nabla\times\boldsymbol E) = \nabla(\nabla\cdot\boldsymbol E) - \nabla^2\boldsymbol E = -\nabla^2\boldsymbol E
$$

一方 $\nabla\times\boldsymbol E = -\partial\boldsymbol B/\partial t$ より

$$
\nabla\times(\nabla\times\boldsymbol E) = -\frac{\partial}{\partial t}(\nabla\times\boldsymbol B) = -\varepsilon_0\mu_0\frac{\partial^2\boldsymbol E}{\partial t^2}
$$

$$
\therefore\ \nabla^2\boldsymbol E = \varepsilon_0\mu_0\frac{\partial^2\boldsymbol E}{\partial t^2} \ \Longrightarrow\ c = \frac{1}{\sqrt{\varepsilon_0\mu_0}}
$$

**(3)** $\boldsymbol E = E_0\sin(kz-\omega t)\hat{\boldsymbol x}$ とすると、$\nabla\times\boldsymbol E = -\partial\boldsymbol B/\partial t$ より

$$
\boldsymbol B = \frac{k}{\omega}E_0\sin(kz-\omega t)\hat{\boldsymbol y} = \frac{E}{c}\hat{\boldsymbol y}
$$

（$\omega/k = c$）。したがって $|E| = c|B|$ で、$\boldsymbol E$、$\boldsymbol B$、進行方向はこの順に右手系をなす。

$$
\boldsymbol S = \frac{\boldsymbol E\times\boldsymbol B}{\mu_0}, \qquad
\langle|S|\rangle = \frac{E_0^2}{2\mu_0c} = \frac{1}{2}\varepsilon_0cE_0^2
$$

---

## 9 ｜ 量子力学：水素原子（配点 100）

**問 1（20 点）** 球座標のラプラシアンを用い $\psi = R(r)Y_{\ell m}$ と置くと、角度部分が $\hat L^2Y_{\ell m} = \hbar^2\ell(\ell+1)Y_{\ell m}$ を与え

$$
-\frac{\hbar^2}{2mr^2}\frac{d}{dr}\left(r^2\frac{dR}{dr}\right) + \left[\frac{\hbar^2\ell(\ell+1)}{2mr^2} - \frac{e^2}{4\pi\varepsilon_0r}\right]R = ER
$$

$u = rR$ と置くと $\dfrac{1}{r}\dfrac{d^2u}{dr^2} = \dfrac{1}{r^2}\dfrac{d}{dr}\left(r^2\dfrac{dR}{dr}\right)$ が成り立ち

$$
-\frac{\hbar^2}{2m}\frac{d^2u}{dr^2} + V_{\rm eff}(r)u = Eu, \qquad
\boxed{V_{\rm eff}(r) = -\frac{e^2}{4\pi\varepsilon_0r} + \frac{\hbar^2\ell(\ell+1)}{2mr^2}}
$$

**問 2（10 点）**

- $\ell=0$: $V_{\rm eff} = -\frac{e^2}{4\pi\varepsilon_0r}$。$r\to0$ で $-\infty$、単調増加して 0 に近づく。
- $\ell\ne0$: $r\to0$ で遠心力項 $\propto r^{-2}$ がクーロン項 $\propto r^{-1}$ に打ち勝つので $V_{\rm eff}\to+\infty$。$r$ が大きいところに極小を持つ井戸型になる。

$\ell\ne0$ では **遠心力障壁** が原点を守るので、電子は原点付近に存在できない（実際 $R\propto r^\ell$ で原点で消える）。角運動量が大きいほど障壁が高く、電子は外側に押しやられる。

**問 3（10 点）** $u(0) = 0$。

理由: $R = u/r$ が原点で有限であるためには $u\to0$ でなければならない。より厳密には、$R$ が原点で $1/r$ のように振る舞うと $\nabla^2(1/r) = -4\pi\delta^3(\boldsymbol r)$ によりシュレディンガー方程式に原点でのデルタ関数源が現れてしまい、方程式を満たさない。

**問 4（25 点）** $u = Are^{-r/a}$ を代入する。

$$
u'' = A e^{-r/a}\left(-\frac{2}{a}+\frac{r}{a^2}\right)
$$

$\ell = 0$ の方程式に入れ、$Ae^{-r/a}$ で割ると

$$
-\frac{\hbar^2}{2m}\left(-\frac2a+\frac{r}{a^2}\right) - \frac{e^2}{4\pi\varepsilon_0} = Er
$$

$r$ の 0 次と 1 次を比較して

$$
\frac{\hbar^2}{ma} = \frac{e^2}{4\pi\varepsilon_0} \ \Longrightarrow\ \boxed{a = \frac{4\pi\varepsilon_0\hbar^2}{me^2} = 0.0529\ \mathrm{nm}}
$$

$$
-\frac{\hbar^2}{2ma^2} = E \ \Longrightarrow\ \boxed{E = -\frac{\hbar^2}{2ma^2} = -13.6\ \mathrm{eV}}
$$

**問 5（20 点）** 規格化条件は $\int_0^\infty|u|^2dr = 1$。$\int_0^\infty r^2e^{-2r/a}dr = \dfrac{2!}{(2/a)^3} = \dfrac{a^3}{4}$ より

$$
|A|^2\frac{a^3}{4} = 1 \ \Longrightarrow\ A = \frac{2}{a^{3/2}}
$$

$$
\langle r\rangle = \int_0^\infty r|u|^2dr = \frac{4}{a^3}\cdot\frac{3!}{(2/a)^4} = \frac{4}{a^3}\cdot\frac{3a^4}{8} = \boxed{\frac{3a}{2}}
$$

動径確率密度 $|u|^2 \propto r^2e^{-2r/a}$ の最大値は

$$
\frac{d}{dr}\left(r^2e^{-2r/a}\right) = 0 \ \Longrightarrow\ 2r - \frac{2r^2}{a} = 0 \ \Longrightarrow\ r_{\rm max} = a
$$

違いの説明: $r_{\rm max} = a$ は分布の **最頻値**、$\langle r\rangle = 1.5a$ は **平均値**である。動径確率密度は右側（大きい $r$）に長い裾を引く非対称分布なので、平均は最頻値より大きくなる。ボーア模型が与えるのは $r_{\rm max}=a$ のほうである。

**問 6（15 点）** クーロンポテンシャル $\propto 1/r$ には、通常の回転対称性に加えて **ルンゲ–レンツベクトルの保存**という余分な対称性（力学的対称性 SO(4)）がある。この「偶然の縮退」により、$E$ が $\ell$ に依存せず $n$ だけで決まり、縮退度が $\sum_{\ell=0}^{n-1}(2\ell+1) = n^2$ となる。

ポテンシャルが純粋な $1/r$ からずれると、この余分な対称性が破れて **$\ell$ 縮退が解ける**。アルカリ金属の価電子は、内殻電子に遮蔽された核電荷を感じるため、遠方では $-e^2/4\pi\varepsilon_0 r$ だが近距離では遮蔽が効かず、より強く引かれる。$\ell$ の小さい軌道ほど核近くに侵入する確率が高いので、より強く束縛される。

$$
E_{ns} < E_{np} < E_{nd} < \cdots
$$

これがアルカリ原子スペクトルに $s, p, d$ 系列が別々の位置に現れる理由であり、また周期表で 4s 軌道が 3d 軌道より先に埋まる理由でもある。

---

## 10 ｜ 統計力学：ラングミュア吸着（配点 100）

**問 1（15 点）** 1 サイトは「空（$N=0$、$E=0$）」か「吸着（$N=1$、$E=-\varepsilon$）」の 2 状態のみ。

$$
\Xi_1 = 1 + e^{\beta(\mu+\varepsilon)}, \qquad \Xi = \Xi_1^M = \left(1+e^{\beta(\mu+\varepsilon)}\right)^M
$$

**問 2（15 点）**

$$
\theta = \frac{e^{\beta(\mu+\varepsilon)}}{1+e^{\beta(\mu+\varepsilon)}} = \boxed{\frac{1}{1+e^{-\beta(\mu+\varepsilon)}}}
$$

（2 準位系のフェルミ分布と同じ形。1 サイトに 1 個までという排他性が効いている）

**問 3（25 点）** 与式より $e^{\beta\mu} = \dfrac{P\lambda^3}{k_BT}$ なので

$$
e^{-\beta(\mu+\varepsilon)} = \frac{k_BT}{P\lambda^3}e^{-\beta\varepsilon}
$$

$$
\theta = \frac{1}{1+\frac{k_BT e^{-\beta\varepsilon}}{P\lambda^3}} = \frac{P}{P+P_0(T)},
\qquad \boxed{P_0(T) = \frac{k_BT}{\lambda^3}e^{-\varepsilon/k_BT}}
$$

**問 4（15 点）**

- **低圧** $P\ll P_0$: $\theta \simeq P/P_0 \propto P$。被覆率が圧力に比例する。これを **ヘンリーの法則** という。
- **高圧** $P\gg P_0$: $\theta\to1$。サイトが埋まり尽くして飽和する（単分子層で頭打ちになる）。

**問 5（15 点）** $\lambda \propto T^{-1/2}$ より $\lambda^{-3}\propto T^{3/2}$、したがって

$$
P_0(T) \propto T^{5/2}e^{-\varepsilon/k_BT} \ \Longrightarrow\ \ln\frac{P_0}{T^{5/2}} = \text{const} - \frac{\varepsilon}{k_B}\cdot\frac{1}{T}
$$

手順:

1. いくつかの温度で吸着等温線を測り、各温度で $\theta = 1/2$ となる圧力から $P_0(T)$ を読み取る。
2. $\ln\left(P_0/T^{5/2}\right)$ を $1/T$ に対してプロットする。
3. 直線の傾きが $-\varepsilon/k_B$ となり、吸着エネルギーが決まる。

（$T^{5/2}$ の因子は指数関数に比べて緩やかなので、粗く $\ln P_0$ 対 $1/T$ でも $\varepsilon$ のおおよその値は得られる。これは吸着熱の測定に使われる標準的な方法である）

**問 6（15 点）**

- **吸着分子どうしの相互作用**: 引力があると、すでに吸着した分子の隣に吸着しやすくなる（協同効果）。等温線は S 字（シグモイド）状になり、低温では 2 次元的な凝縮に対応する不連続なステップが現れる。斥力があると逆に等温線はなだらかになり、$\theta = 1/2$ 付近で秩序構造（市松模様）が安定化して段が生じることがある。
- **サイトの不均一性**: 吸着エネルギー $\varepsilon$ に分布があると、強いサイトから順に埋まっていくので、等温線はラングミュア型より緩やかな立ち上がりになる。経験的に $\theta\propto P^{1/n}$（フロインドリッヒ型）で表されることが多い。
- **多層吸着**: 1 層目が埋まった後も分子が積み重なる場合、$P$ が飽和蒸気圧に近づくと $\theta$ が発散する。これを扱うのが BET 理論で、比表面積の測定に広く使われている。

---

## 11 ｜ 物性物理：ドルーデ模型とプラズマ振動数（配点 100）

**問 1（15 点）** $\boldsymbol v \propto e^{-i\omega t}$ と置くと

$$
-i\omega m\boldsymbol v = -e\boldsymbol E - \frac{m\boldsymbol v}{\tau} \ \Longrightarrow\ \boldsymbol v = \frac{-e\tau}{m(1-i\omega\tau)}\boldsymbol E
$$

$$
\boldsymbol j = -ne\boldsymbol v = \frac{ne^2\tau}{m(1-i\omega\tau)}\boldsymbol E \ \Longrightarrow\ \boxed{\sigma(\omega) = \frac{\sigma_0}{1-i\omega\tau}},\quad \sigma_0 = \frac{ne^2\tau}{m}
$$

$\omega\to0$ で $\sigma\to\sigma_0$。

**問 2（20 点）** アンペール–マクスウェルの法則の右辺は

$$
\mu_0\boldsymbol j + \mu_0\varepsilon_0\frac{\partial\boldsymbol E}{\partial t}
= \mu_0\left(\sigma - i\omega\varepsilon_0\right)\boldsymbol E
= -i\omega\mu_0\varepsilon_0\left[1+\frac{i\sigma}{\varepsilon_0\omega}\right]\boldsymbol E
$$

したがって実効的な誘電関数は

$$
\varepsilon(\omega) = 1 + \frac{i\sigma(\omega)}{\varepsilon_0\omega} = 1 + \frac{i\,ne^2\tau}{m\varepsilon_0\omega(1-i\omega\tau)}
$$

分母を有理化して整理すると

$$
\varepsilon(\omega) = 1 - \frac{\omega_p^2}{\omega^2+i\omega/\tau}, \qquad \omega_p^2 = \frac{ne^2}{\varepsilon_0m}
$$

**問 3（15 点）** $\omega\tau\gg1$ で $\varepsilon(\omega)\simeq1-\omega_p^2/\omega^2$（実数）。

- $\omega<\omega_p$: $\varepsilon<0$ なので屈折率 $n = \sqrt\varepsilon$ が **純虚数**。波は物質中で $e^{-z/\delta}$ と指数減衰し（エバネッセント）、伝播できない。エネルギーは吸収されずに戻るので **全反射** となる。
- $\omega>\omega_p$: $\varepsilon>0$、$0<n<1$ で波は伝播する。金属は **透明** になる。

**問 4（25 点）**

$$
\omega_p = \sqrt{\frac{ne^2}{\varepsilon_0m}} = \sqrt{\frac{2.5\times10^{28}\times(1.602\times10^{-19})^2}{8.854\times10^{-12}\times9.109\times10^{-31}}}
= \sqrt{7.96\times10^{31}} = \boxed{8.92\times10^{15}\ \mathrm{rad/s}}
$$

$$
\hbar\omega_p = 1.055\times10^{-34}\times8.92\times10^{15} = 9.41\times10^{-19}\ \mathrm{J} = \boxed{5.87\ \mathrm{eV}}
$$

$$
\lambda_p = \frac{2\pi c}{\omega_p} = \frac{2\pi\times3.00\times10^8}{8.92\times10^{15}} = 2.11\times10^{-7}\ \mathrm{m} = \boxed{211\ \mathrm{nm}}
$$

**問 5（10 点）** 可視光は $1.6$–$3.1$ eV（$400$–$780$ nm）で、いずれも $\hbar\omega < \hbar\omega_p = 5.87$ eV。すなわち $\omega<\omega_p$ なので、可視光は **すべて反射される**。反射率がほぼ波長によらず高いため、色のつかない銀白色の金属光沢になる。

一方、波長 211 nm より短い紫外線は $\omega>\omega_p$ となり、ナトリウムは **透明** になる。この「アルカリ金属の紫外透過」は 1930 年代に実験で確認されており、自由電子模型の劇的な成功例である。

（銅や金が赤みを帯びるのは、$d$ バンドから伝導帯への **バンド間遷移** が可視域にあり、青い側の光を吸収するためで、自由電子模型だけでは説明できない）

**問 6（15 点）** 正イオンの背景（一様、密度 $n$）に対して、電子気体全体を $x$ だけ一様に $+x$ 方向へずらす。すると板の両端に面電荷 $\mp nex$ が現れ、内部に一様電場

$$
E = \frac{nex}{\varepsilon_0}
$$

が生じる（平行平板コンデンサーと同じ）。電子 1 個にはたらく復元力は

$$
F = -eE = -\frac{ne^2}{\varepsilon_0}x
$$

$$
m\ddot x = -\frac{ne^2}{\varepsilon_0}x \ \Longrightarrow\ \omega^2 = \frac{ne^2}{\varepsilon_0m} = \omega_p^2
$$

すなわち電子気体は角振動数 $\omega_p$ で集団振動する。この量子が **プラズモン**（ナトリウムで $5.9$ eV）であり、電子線エネルギー損失分光でエネルギー損失ピークとして直接観測できる。

---

## 12 ｜ 相対論・天体（配点 100）

**問 1（20 点）** 光源の静止系での放射周期を $T_0 = 1/\nu_{\rm src}$ とする。観測者の系では時間の遅れにより、連続する 2 つの波面が放出される時間間隔は $\gamma T_0$ である。

その間に光源は $v\gamma T_0$ だけ遠ざかるので、2 つ目の波面は $v\gamma T_0/c$ だけ余分な伝播時間を要する。したがって観測される周期は

$$
T_{\rm obs} = \gamma T_0 + \frac{v\gamma T_0}{c} = \gamma T_0(1+\beta) = \frac{1+\beta}{\sqrt{1-\beta^2}}T_0 = \sqrt{\frac{1+\beta}{1-\beta}}\,T_0
$$

$$
\therefore\ \nu_{\rm obs} = \nu_{\rm src}\sqrt{\frac{1-\beta}{1+\beta}}
$$

**問 2（15 点）** 視線に垂直な運動では、1 次の伝播時間の変化がない（距離が瞬間的に変わらない）。残るのは時間の遅れだけなので

$$
\nu_{\rm obs} = \frac{\nu_{\rm src}}{\gamma} = \nu_{\rm src}\sqrt{1-\beta^2}
$$

必ず赤方偏移する。古典的なドップラー効果は音源と観測者の距離変化率のみで決まるので、垂直方向では効果がゼロである。したがって **横ドップラー効果は時間の遅れそのものの直接的な現れ**であり、特殊相対論に固有である（アイヴス–スティルウェルの実験で検証された）。

**問 3（20 点）**

$$
1+z = \frac{\lambda_{\rm obs}}{\lambda_{\rm src}} = \frac{\nu_{\rm src}}{\nu_{\rm obs}} = \sqrt{\frac{1+\beta}{1-\beta}}
$$

$z = 1.0$ のとき $1+z = 2$、両辺 2 乗して

$$
4 = \frac{1+\beta}{1-\beta} \ \Longrightarrow\ 4-4\beta = 1+\beta \ \Longrightarrow\ \boxed{\beta = 0.60}
$$

**問 4（15 点）** 特殊相対論のドップラー公式は、**平坦な時空の中で 2 つの慣性系が相対速度を持つ**状況に対する式である。膨張宇宙（FRW 時空）では

- 時空が曲がっており、遠く離れた 2 点の速度を比較する大域的な慣性系が存在しない
- 銀河は空間の中を動いているのではなく、空間の目盛りそのものが伸びている（共動座標では静止している）
- そのため「後退速度」は $c$ を超えることも許され、$\beta<1$ という制約は意味を持たない

したがって $\beta$ を問 3 の式から逆算しても物理的な意味はない。正しい関係は

$$
1+z = \frac{a_0}{a_{\rm emit}}
$$

（放出時から現在までに空間が何倍に伸びたか）であり、これは光の波長が空間とともに引き伸ばされることの直接の帰結として厳密に成り立つ。

**問 5（15 点）** 時間は $(1+z)$ 倍に伸び、エネルギーは $(1+z)$ 分の 1 になる。

$$
T_{\rm obs} = (1+z)\,T_{\rm src}, \qquad E_{\rm peak,obs} = \frac{E_{\rm peak,src}}{1+z}
$$

**問 6（10 点）** $z=1.0$ より $1+z = 2$。

$$
T_{\rm src} = \frac{20}{2} = \boxed{10\ \mathrm{s}}, \qquad E_{\rm peak,src} = 150\times2 = \boxed{300\ \mathrm{keV}}
$$

（GRB のスペクトル解析で $E_{\rm peak}$ を議論するときに、観測値と静止系の値を混同しないことが重要である。アマティ関係など経験則はいずれも静止系の量で書かれている）

**問 7（5 点）** **ビーミング（放射の指向性）**。放射が半開き角 $\theta_j$ のジェットに絞られている場合、ジェットの円錐内にいる観測者は「全天に等方放射されている」と誤解する。真のエネルギーは立体角の比

$$
\frac{\Delta\Omega}{4\pi} = \frac{2\times2\pi(1-\cos\theta_j)}{4\pi} \simeq \frac{\theta_j^2}{2}
$$

だけ小さい。$\theta_j\simeq5^\circ$ なら真のエネルギーは $E_{\rm iso}$ の $1/500$ 程度になる。GRB の $E_{\rm iso}$ が $10^{54}$ erg に達することがあるのに、ジェット補正後は $10^{51}$ erg 前後に集中するのはこのためである。
