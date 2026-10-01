# 準本命 10 題 — 解答・解説

各大問 100 点。

# 大問 7（力学）

## 7 ｜ 回転座標系：遠心力とコリオリ力（配点 100）　［第 4 回］

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

## 7 ｜ ラザフォード散乱（配点 100）　［第 6 回］

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

# 大問 8（電磁気）

## 8 ｜ 静電エネルギー / 磁気双極子 / ポインティング（配点 100）　［第 7 回］

### 問 1（35 点）

**(1)** 表面電荷なら $r<a$ で $E=0$、$r>a$ で $E = \frac{Q}{4\pi\varepsilon_0r^2}$。

$$
U_{\rm s} = \frac{\varepsilon_0}{2}\int_a^\infty\left(\frac{Q}{4\pi\varepsilon_0r^2}\right)^2 4\pi r^2dr
= \frac{Q^2}{8\pi\varepsilon_0}\int_a^\infty\frac{dr}{r^2} = \boxed{\frac{Q^2}{8\pi\varepsilon_0a}}
$$

**(2)** 一様体積分布なら $r<a$ で $E = \frac{Qr}{4\pi\varepsilon_0a^3}$。内部の寄与は

$$
U_{\rm in} = \frac{\varepsilon_0}{2}\int_0^a\left(\frac{Qr}{4\pi\varepsilon_0a^3}\right)^24\pi r^2dr = \frac{Q^2}{8\pi\varepsilon_0a^6}\cdot\frac{a^5}{5} = \frac{Q^2}{40\pi\varepsilon_0a}
$$

外部は (1) と同じ $\frac{Q^2}{8\pi\varepsilon_0 a} = \frac{5Q^2}{40\pi\varepsilon_0a}$ なので

$$
U_{\rm v} = \boxed{\frac{3Q^2}{20\pi\varepsilon_0a}} = 1.2\,U_{\rm s}
$$

内部にも電荷を詰め込むぶん、こちらのほうがエネルギーが高い。

**(3)** $m_ec^2 = \dfrac{e^2}{8\pi\varepsilon_0r_e}$ とおくと

$$
r_e = \frac{1}{2}\cdot\frac{e^2/(4\pi\varepsilon_0)}{m_ec^2} = \frac{1}{2}\cdot\frac{1.44}{0.511} = \boxed{1.41\ \mathrm{fm}}
$$

（表面電荷模型では慣用の「古典電子半径」$r_0 = e^2/(4\pi\varepsilon_0m_ec^2) = 2.82$ fm のちょうど半分になる。模型の細部で係数が変わることからも、この長さを「電子の大きさ」と読むべきではないことが分かる。実験的には電子は $10^{-4}$ fm 以下まで点状である）

### 問 2（30 点）

**(1)** 磁場中でループが受けるトルクは $\boldsymbol\tau = \boldsymbol m\times\boldsymbol B$、大きさ $mB\sin\theta$。角度 $\theta$ を変えるときの外部がする仕事は

$$
U(\theta)-U(\pi/2) = \int_{\pi/2}^{\theta}mB\sin\theta'\,d\theta' = -mB\cos\theta
$$

基準を $\theta=\pi/2$ にとれば $U = -\boldsymbol m\cdot\boldsymbol B$。

**(2)**

$$
\boldsymbol\tau = \boldsymbol m\times\boldsymbol B, \qquad \boldsymbol F = -\nabla U = \nabla(\boldsymbol m\cdot\boldsymbol B)
$$

$\boldsymbol B$ が一様なら $\boldsymbol m\cdot\boldsymbol B$ は位置によらないので $\boldsymbol F = 0$。**一様磁場は向きを揃えるだけで、並進の力を及ぼさない。**

**(3)** シュテルン–ゲルラッハの実験では、スピンの向きの違いを **空間的な軌道の違い**に変換して検出する。一様磁場ではトルクしか働かず、ビームは分裂しない。$z$ 方向に $\partial B_z/\partial z \ne 0$ の勾配を作れば

$$
F_z = m_z\frac{\partial B_z}{\partial z}
$$

となり、$m_z$ の符号によって上下に分かれる。したがって **不均一磁場が本質的に必要**である。実験で観測されたのが連続分布ではなく 2 本のスポットであったことが、角運動量の量子化の直接的証拠になった。

### 問 3（35 点）

**(1)** 定常電流なので抵抗体内部の電場は軸方向に一様で

$$
E_z = \frac{V}{L} = \frac{IR}{L}
$$

表面（$r=a$）の磁束密度はアンペールの法則より周方向に

$$
B_\phi = \frac{\mu_0I}{2\pi a}
$$

**(2)** $\hat{\boldsymbol z}\times\hat{\boldsymbol\phi} = -\hat{\boldsymbol r}$ なので、$\boldsymbol S$ は **半径方向内向き**（側面から抵抗体に入る向き）。

$$
|S| = \frac{E_zB_\phi}{\mu_0} = \frac{IR}{L}\cdot\frac{I}{2\pi a} = \frac{I^2R}{2\pi aL}
$$

**(3)** 側面積は $2\pi aL$ なので、流入する全エネルギー流束は

$$
P = |S|\times2\pi aL = I^2R
$$

ジュール熱に一致する。

**論述**: この計算は、エネルギーが導線の内部を電流と一緒に運ばれるのではなく、**導線を取り巻く電磁場を通って側面から入ってくる**ことを示している。導線は「エネルギーの通り道」ではなく「エネルギーの落ち口」である。

この描像は一見奇妙だが、次の点で本質的である。

- 同軸ケーブルで電力を送るとき、エネルギーは芯線の銅ではなく **芯線と外皮の間の誘電体空間**を流れている。導体を太くすることの意味は、エネルギーの通り道を広げることではなく、途中で余計に落ちるジュール損を減らすことにある。
- 超伝導線では $E=0$ なので側面から入る $\boldsymbol S$ もゼロになり、損失が生じないことと整合する。
- 電磁場がエネルギーと運動量を局所的に運ぶという描像は、電磁波の存在と合わせて、場が独立した物理的実体であることの根拠になっている。

---

## 8 ｜ 多重極展開 / 磁気モーメント / 渦電流（配点 100）　［第 9 回］

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

## 8 ｜ 誘電体にはたらく力 / ∇·B=0 / 伝送線（配点 100）　［第 11 回］

### 問 1（30 点）

**(1)** 空の部分（長さ $L-x$）と誘電体の入った部分（長さ $x$）の並列接続。

$$
C(x) = \frac{\varepsilon_0w(L-x)}{d}+\frac{\varepsilon wx}{d} = \frac{w}{d}\left[\varepsilon_0L+(\varepsilon-\varepsilon_0)x\right]
$$

**(2)** 電圧一定の場合、電池の仕事も勘定に入れると（第 10 回 大問 8 問 1 と同じ論法）

$$
F = +\frac12V^2\frac{dC}{dx} = \boxed{\frac{V^2w(\varepsilon-\varepsilon_0)}{2d}} > 0
$$

$\varepsilon>\varepsilon_0$ なので力は $x$ を増やす向き、すなわち誘電体は **引き込まれる**。

（電荷一定で計算しても向き・大きさは同じになる。力は実在するので当然である）

**(3)** 極板間の一様な電場だけを見ていると、電場は $x$ 方向に一様で、誘電体の中の電気力線も $x$ 方向の運動に対して何も変化しないため、$x$ 方向の力が出てこないように見える。

実際に力を生んでいるのは、**誘電体の先端がある位置、すなわち極板の内部で電場が一様でなくなっている領域（漏れ電場・フリンジ場）**である。誘電体は電場によって分極し、誘起双極子は $\nabla E^2$ の向き、すなわち **電場の強い側**へ引かれる。誘電体の先端では電場が急激に変化しており、そこで正味の力が生じる。

仮想仕事の原理の便利さは、この複雑な先端の電場をまったく計算せずに、系全体のエネルギー収支だけから正しい力が得られる点にある。

### 問 2（35 点）

**(1)**

$$
\oint_S\boldsymbol B\cdot d\boldsymbol S = 0 \qquad (\text{任意の閉曲面 }S)
$$

意味: 閉曲面から出ていく磁束と入ってくる磁束が必ず等しい。すなわち **磁力線には始点も終点もなく、必ず閉じている**。

ガウスの法則 $\oint\boldsymbol E\cdot d\boldsymbol S = Q/\varepsilon_0$ との違いは右辺である。電場には「湧き出し」＝電荷があるが、磁場には対応する **磁荷（磁気単極子）が存在しない**。棒磁石をいくら細かく割っても N 極だけを取り出せないのはこのためである。

**(2)** 発散がゼロのベクトル場は（単連結領域では）必ず別のベクトル場の回転として表せる（ポアンカレの補題）。

$$
\boldsymbol B = \nabla\times\boldsymbol A
$$

$\boldsymbol A$ は一意ではない。任意のスカラー関数 $\chi$ に対して

$$
\boldsymbol A' = \boldsymbol A+\nabla\chi \ \Longrightarrow\ \nabla\times\boldsymbol A' = \nabla\times\boldsymbol A + \nabla\times\nabla\chi = \boldsymbol B
$$

（$\nabla\times\nabla\chi\equiv0$）。この自由度を **ゲージ自由度**という。クーロンゲージ $\nabla\cdot\boldsymbol A = 0$ やローレンツゲージなどを課して固定する。

**(3)** **アハラノフ–ボーム効果**。

長いソレノイドの外側は $\boldsymbol B = 0$ であるにもかかわらず、$\boldsymbol A\ne0$ である。電子線をソレノイドの両側に分けて通し、再び重ねて干渉させると、干渉縞がソレノイド内部の磁束 $\Phi$ に依存して移動する。位相差は

$$
\Delta\varphi = \frac{e}{\hbar}\oint\boldsymbol A\cdot d\boldsymbol l = \frac{e\Phi}{\hbar}
$$

電子は $\boldsymbol B\ne0$ の領域を一度も通っていないのに、内部の磁束を「感じて」いる。局所的な $\boldsymbol B$ だけでは説明できず、$\boldsymbol A$（正確にはその周回積分＝磁束）に物理的な実在性があることを示している。1986 年に外村彰らが超伝導体で磁束を完全に遮蔽した実験により決定的に検証した。

### 問 3（35 点）

**(1)** 微小区間 $dx$ について、インダクタンス $\mathcal L\,dx$ による電圧降下とキャパシタンス $\mathcal C\,dx$ への充電電流を考えると

$$
V(x+dx)-V(x) = -\mathcal L\,dx\frac{\partial I}{\partial t}, \qquad
I(x+dx)-I(x) = -\mathcal C\,dx\frac{\partial V}{\partial t}
$$

$$
\frac{\partial V}{\partial x} = -\mathcal L\frac{\partial I}{\partial t}, \qquad
\frac{\partial I}{\partial x} = -\mathcal C\frac{\partial V}{\partial t}
$$

第 1 式を $x$ で、第 2 式を $t$ で微分して $I$ を消去すると

$$
\frac{\partial^2V}{\partial x^2} = \mathcal{LC}\frac{\partial^2V}{\partial t^2}
\ \Longrightarrow\ v = \frac{1}{\sqrt{\mathcal{LC}}}
$$

**(2)** 前進波 $V = f(x-vt)$、$I = g(x-vt)$ を第 1 式に代入すると $f' = \mathcal Lv\,g'$、すなわち $f = \mathcal Lv\,g$。

$$
Z_0 = \frac VI = \mathcal Lv = \frac{\mathcal L}{\sqrt{\mathcal{LC}}} = \boxed{\sqrt{\frac{\mathcal L}{\mathcal C}}}
$$

**(3)** 与えられた $\mathcal L$、$\mathcal C$ を代入すると $\ln(b/a)$ が約分されて

$$
v = \frac{1}{\sqrt{\mathcal{LC}}} = \frac{1}{\sqrt{\mu_0\varepsilon_0\varepsilon_r}} = \frac{c}{\sqrt{\varepsilon_r}}
$$

$$
Z_0 = \sqrt{\frac{\mathcal L}{\mathcal C}} = \frac{1}{2\pi}\sqrt{\frac{\mu_0}{\varepsilon_0\varepsilon_r}}\ln\frac ba
= \frac{377}{2\pi\sqrt{\varepsilon_r}}\ln\frac ba = \frac{60}{\sqrt{\varepsilon_r}}\ln\frac ba\ [\Omega]
$$

$\varepsilon_r = 2.25$ では $\sqrt{\varepsilon_r} = 1.5$ なので

$$
Z_0 = 40\ln\frac ba = 50 \ \Longrightarrow\ \ln\frac ba = 1.25 \ \Longrightarrow\ \boxed{\frac ba = e^{1.25} = 3.49}
$$

$$
v = \frac{3.00\times10^8}{1.5} = 2.0\times10^8\ \mathrm{m/s}\ (= 0.67c)
$$

（実際の 50 Ω 同軸ケーブル RG-58 の $b/a$ は約 3.5、波長短縮率は 0.66 で、この計算とよく一致する。放射線計測で信号を伝えるとき、ケーブル長 1 m あたり約 5 ns の遅延が生じるという実務的な数字はここから出る）

---

# 大問 10（統計）

## 10 ｜ ゴム弾性（配点 100）　［第 4 回］

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

## 10 ｜ ラングミュア吸着（配点 100）　［第 6 回］

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

## 10 ｜ 負温度（配点 100）　［第 7 回］

**問 1（15 点）** $N$ 個から励起状態にする $n$ 個を選ぶ組合せ。

$$
W(n) = \frac{N!}{n!(N-n)!}
$$

$$
S = k_B\ln W \simeq k_B\left[N\ln N - n\ln n - (N-n)\ln(N-n)\right]
$$

**問 2（15 点）** $E = n\Delta$ より $\dfrac{\partial}{\partial E} = \dfrac{1}{\Delta}\dfrac{\partial}{\partial n}$。

$$
\frac{\partial S}{\partial n} = k_B\left[-\ln n - 1 + \ln(N-n)+1\right] = k_B\ln\frac{N-n}{n}
$$

$$
\frac1T = \frac{\partial S}{\partial E} = \frac{k_B}{\Delta}\ln\frac{N-n}{n}
\ \Longrightarrow\ k_BT = \frac{\Delta}{\ln\frac{N-n}{n}}
$$

**問 3（15 点）**

- $n<N/2$: $\frac{N-n}{n}>1$、$\ln>0$ → $T>0$
- $n=N/2$: $\ln = 0$ → $1/T = 0$、すなわち $T = \pm\infty$
- $n>N/2$: $\frac{N-n}{n}<1$、$\ln<0$ → $\boxed{T<0}$

**問 4（20 点）** $E$ を $0$ から $N\Delta$ まで増やすと

- $T$: $0^+$ から増加 → $E = N\Delta/2$ で $+\infty$ → そこで符号が飛んで $-\infty$ → さらに増加して $E=N\Delta$ で $0^-$
- $\beta = 1/k_BT$: $+\infty$ から単調に減少し、$E=N\Delta/2$ で $0$ を横切り、$-\infty$ まで **連続的に**下がる

$T$ には $\pm\infty$ での不連続な飛びがあるが、$\beta$ は全域で連続かつ単調である。**熱力学的に自然な変数は $T$ ではなく $\beta$ である**。

「負の温度は絶対零度より低いのではなく無限大より高い」と言われるのは、温度を $\beta$ の順に並べると

$$
T = 0^+\ \to\ T\to+\infty\ \to\ T\to-\infty\ \to\ T = 0^-
$$

の順に「熱く」なっていくからである。実際、問 6 で見るように負温度の系は任意の正温度の系に熱を与える。

**問 5（15 点）** 条件は **エネルギーが上に有界であること**。上限があるからこそ、エネルギーを上げていくと状態数（＝エントロピー）が途中から減少に転じ、$\partial S/\partial E<0$ すなわち $T<0$ が可能になる。

普通の気体では運動エネルギー $p^2/2m$ に上限がなく、エネルギーを与えれば与えるほど位相空間体積が増える。$S(E)$ は単調増加なので $T>0$ しかありえない。

現実に負温度が実現されるのは、スピン系のように **並進自由度から切り離された有限準位系**で、かつスピン–格子緩和時間がスピン–スピン緩和時間より十分長い場合である（Purcell–Pound の核スピン実験、1951 年）。

**問 6（10 点）** 微小なエネルギー $dE_1$ が系 1 に移るとき

$$
dS_{\rm tot} = \frac{dE_1}{T_1}+\frac{dE_2}{T_2} = dE_1\left(\frac{1}{T_1}-\frac{1}{T_2}\right)
$$

$T_1<0<T_2$ なら $\frac1{T_1}<0<\frac1{T_2}$ なので括弧は負。$dS_{\rm tot}>0$ には $dE_1<0$ が必要である。

すなわち **エネルギーは負温度の系から正温度の系へ流れる**。この意味で負温度の系はどんな正温度の系よりも「熱い」。

**問 7（10 点）** 誘導放出と誘導吸収の断面積（アインシュタインの $B$ 係数）は等しい。入射光子 1 個あたり、上準位の粒子は誘導放出で光子を 1 個増やし、下準位の粒子は吸収で 1 個減らす。したがって正味の利得は占有数の差に比例する。

$$
\text{正味利得} \propto N_{\rm upper} - N_{\rm lower}
$$

増幅（$>0$）には $N_{\rm upper}>N_{\rm lower}$、すなわち **反転分布**が必要である。問 3 より、これは $T<0$ に対応する。

熱平衡（$T>0$）ではボルツマン分布により必ず $N_{\rm upper}<N_{\rm lower}$ なので、吸収が勝ってレーザー発振は起こらない。反転分布を作るには外部からのポンピングと、3 準位系・4 準位系のような非平衡な準位構造が必要になる。

---

## 10 ｜ ボース–アインシュタイン凝縮（配点 100）　［第 8 回］

**問 1（10 点）** 占有数は

$$
\langle n_\varepsilon\rangle = \frac{1}{e^{\beta(\varepsilon-\mu)}-1}
$$

これが正であるためには分母が正、すなわち $e^{\beta(\varepsilon-\mu)}>1$、$\varepsilon>\mu$ が **すべての** $\varepsilon$ で必要。基底状態のエネルギーを $\varepsilon=0$ にとれば

$$
\mu \le 0 \qquad (0\le z = e^{\beta\mu}\le1)
$$

**問 2（20 点）** $\dfrac{1}{e^x-1} = \sum_{k=1}^\infty e^{-kx}$（$x>0$）と展開して

$$
N_{\rm ex} = \int_0^\infty D(\varepsilon)\sum_{k=1}^\infty z^ke^{-k\beta\varepsilon}d\varepsilon
= \frac{V}{4\pi^2}\left(\frac{2m}{\hbar^2}\right)^{3/2}\sum_kz^k\int_0^\infty\sqrt\varepsilon\,e^{-k\beta\varepsilon}d\varepsilon
$$

$\displaystyle\int_0^\infty\sqrt\varepsilon e^{-k\beta\varepsilon}d\varepsilon = \frac{\sqrt\pi}{2}(k\beta)^{-3/2}$ を代入し、係数を整理すると

$$
N_{\rm ex} = \frac{V}{\lambda^3}\sum_k\frac{z^k}{k^{3/2}} = \frac{V}{\lambda^3}g_{3/2}(z)
$$

**問 3（25 点）** $z\le1$ より

$$
N_{\rm ex} \le \frac{V}{\lambda^3}\zeta(3/2)
$$

$\lambda\propto T^{-1/2}$ なので、温度を下げると右辺は $T^{3/2}$ に比例して **減少する**。ある温度で右辺が全粒子数 $N$ に届かなくなり、余った粒子は励起状態に収まりきらない。

これらの粒子は **すべて基底状態（$\varepsilon=0$）に落ち込む**。これがボース–アインシュタイン凝縮である。連続近似は $\varepsilon=0$ の 1 状態を（$D(0)=0$ なので）取りこぼしており、そこにマクロな数の粒子が溜まる。

臨界温度は $N = \dfrac{V}{\lambda_c^3}\zeta(3/2)$ から

$$
\boxed{T_c = \frac{2\pi\hbar^2}{mk_B}\left(\frac{n}{\zeta(3/2)}\right)^{2/3}}, \qquad n = \frac NV
$$

**問 4（15 点）** $T<T_c$ では $\mu = 0$（$z=1$）に張り付くので

$$
N_{\rm ex}(T) = \frac{V}{\lambda^3}\zeta(3/2) \propto T^{3/2}
$$

$T=T_c$ で $N_{\rm ex} = N$ だったから

$$
\frac{N_{\rm ex}}{N} = \left(\frac{T}{T_c}\right)^{3/2}
\ \Longrightarrow\ \boxed{\frac{N_0}{N} = 1-\left(\frac{T}{T_c}\right)^{3/2}}
$$

**問 5（15 点）** 2 次元では状態密度が **エネルギーによらない定数** $D_{2}(\varepsilon) = \dfrac{Am}{2\pi\hbar^2}$ になる。すると

$$
N_{\rm ex} = \frac{Am}{2\pi\hbar^2}\int_0^\infty\frac{d\varepsilon}{e^{\beta(\varepsilon-\mu)}-1}
$$

$\mu\to0$ の極限で、$\varepsilon\to0$ 付近の被積分関数は $\dfrac{1}{\beta\varepsilon}$ となり、積分は **対数発散**する。

$$
N_{\rm ex}\Big|_{\mu\to0} = \infty
$$

つまり励起状態はいくらでも粒子を収容でき、「あふれる」ことがない。したがって有限温度では凝縮が起こらない。

一般に $D(\varepsilon)\propto\varepsilon^{s}$ のとき、$\int\varepsilon^s/\varepsilon\,d\varepsilon$ が $\varepsilon\to0$ で収束する条件は $s>0$ である。3 次元では $s=1/2>0$ で収束、2 次元では $s=0$ で発散する。**次元が状態密度のべきを通して凝縮の可否を決める。**（ただし 2 次元でも調和トラップ中では $D\propto\varepsilon$ となり凝縮しうる）

**問 6（15 点）**

$$
m = 87\times1.661\times10^{-27} = 1.445\times10^{-25}\ \mathrm{kg}, \qquad n = 1.0\times10^{20}\ \mathrm{m^{-3}}
$$

$$
\frac{n}{\zeta(3/2)} = \frac{1.0\times10^{20}}{2.612} = 3.83\times10^{19}\ \mathrm{m^{-3}}
\ \Longrightarrow\ \left(\frac{n}{\zeta}\right)^{2/3} = 1.14\times10^{13}\ \mathrm{m^{-2}}
$$

$$
\frac{2\pi\hbar^2}{mk_B} = \frac{2\pi(1.055\times10^{-34})^2}{1.445\times10^{-25}\times1.381\times10^{-23}} = 3.50\times10^{-20}\ \mathrm{K\,m^2}
$$

$$
T_c = 3.50\times10^{-20}\times1.14\times10^{13} = \boxed{4.0\times10^{-7}\ \mathrm{K}} = 400\ \mathrm{nK}
$$

実際の希薄アルカリ原子気体の BEC はこの程度（数百 nK）で実現されており、1995 年の Cornell–Wieman（$^{87}$Rb）と Ketterle（$^{23}$Na）の実験値と桁が一致する。レーザー冷却だけでは届かず、蒸発冷却を組み合わせて到達する温度領域である。

---

## 10 ｜ 2 次元気体と状態密度の次元依存（配点 100）　［第 10 回］

**問 1（20 点）** 周期境界条件で $\boldsymbol k$ 空間の状態密度は $(L/2\pi)^d$。半径 $k$ の $d$ 次元球の体積を $V_dk^d$ とすると

$$
N(k) = \left(\frac{L}{2\pi}\right)^dV_dk^d
$$

$\varepsilon = \dfrac{\hbar^2k^2}{2m}$ より $k\propto\varepsilon^{1/2}$ なので $N(\varepsilon)\propto\varepsilon^{d/2}$、したがって

$$
D(\varepsilon) = \frac{dN}{d\varepsilon}\propto\varepsilon^{d/2-1}
$$

| 次元 | $D(\varepsilon)$ |
| --- | --- |
| $d=1$ | $\varepsilon^{-1/2}$（$\varepsilon\to0$ で **発散**） |
| $d=2$ | $\varepsilon^{0}$ = **一定** |
| $d=3$ | $\varepsilon^{1/2}$（$\varepsilon\to0$ で **ゼロ**） |

**問 2（15 点）** 1 粒子分配関数は運動量積分から

$$
Z_1 = \frac{A}{h^2}\int e^{-\beta p^2/2m}d^2p = \frac{A}{\lambda^2}, \qquad \lambda = \frac{h}{\sqrt{2\pi mk_BT}}
$$

区別できない $N$ 粒子では

$$
Z_N = \frac{1}{N!}\left(\frac{A}{\lambda^2}\right)^N
$$

**問 3（20 点）**

$$
\ln Z_N = N\ln A - 2N\ln\lambda-\ln N!
$$

$$
P = -\left(\frac{\partial F}{\partial A}\right)_T = k_BT\frac{\partial\ln Z_N}{\partial A} = \frac{Nk_BT}{A}
\ \Longrightarrow\ \boxed{PA = Nk_BT}
$$

$\lambda\propto\beta^{1/2}$ より $\ln\lambda = \frac12\ln\beta+$ 定数 なので

$$
U = -\frac{\partial\ln Z_N}{\partial\beta} = 2N\cdot\frac{1}{2\beta} = Nk_BT
$$

**3 次元との違い**: 一般に $U = \dfrac d2Nk_BT$ である。エネルギー等分配則により、2 次形式で表される自由度 1 個あたり $\frac12k_BT$ が配分される。運動量成分の数が $d$ 個なので、そのまま $d/2$ が出る。**状態方程式 $PV = Nk_BT$ は次元によらず同じ形**なのに、内部エネルギーだけが次元に依存する点が興味深い。

**問 4（15 点）** スピン縮退 2 を含めて、単位面積あたり

$$
D_2 = 2\cdot\frac{1}{(2\pi)^2}\cdot2\pi k\frac{dk}{d\varepsilon}
$$

$\varepsilon = \dfrac{\hbar^2k^2}{2m}$ より $\dfrac{dk}{d\varepsilon} = \dfrac{m}{\hbar^2k}$。$k$ が約分されて

$$
D_2 = 2\cdot\frac{k}{2\pi}\cdot\frac{m}{\hbar^2k} = \boxed{\frac{m}{\pi\hbar^2}}
$$

$\varepsilon$ に依存しない定数になる。$k$ 空間の面積要素 $2\pi k\,dk$ の $k$ と、群速度の逆数 $1/v_g\propto1/k$ の $k$ がちょうど打ち消し合うためである。

**問 5（20 点）**

$$
n = \int_0^\infty\frac{D_2\,d\varepsilon}{e^{\beta(\varepsilon-\mu)}+1} = D_2k_BT\int_0^\infty\frac{dx}{e^{x-\beta\mu}+1}
$$

$\dfrac{d}{dx}\left[x-\ln\left(e^{x-a}+1\right)\right] = \dfrac{1}{e^{x-a}+1}$ を利用して積分すると

$$
\int_0^\infty\frac{dx}{e^{x-a}+1} = \ln\left(1+e^{a}\right)
$$

$$
n = D_2k_BT\ln\left(1+e^{\beta\mu}\right)
\ \Longrightarrow\ \boxed{\mu(T) = k_BT\ln\left(e^{n/(D_2k_BT)}-1\right)}
$$

$T\to0$ では $\dfrac{n}{D_2k_BT}\to\infty$ なので $e^{n/(D_2k_BT)}\gg1$、よって

$$
\mu \to k_BT\cdot\frac{n}{D_2k_BT} = \frac{n}{D_2} = \varepsilon_F
$$

（$D_2$ が定数なので $\varepsilon_F = n/D_2$ は当然の結果）

**問 6（10 点）** 2 次元でだけ閉じた表式が得られるのは、$D(\varepsilon)$ が定数であるため、フェルミ–ディラック積分が

$$
\int\frac{d\varepsilon}{e^{\beta(\varepsilon-\mu)}+1}
$$

という初等関数で書ける形になるからである。3 次元では $D\propto\sqrt\varepsilon$ なので $\int\sqrt\varepsilon\,f(\varepsilon)d\varepsilon$ という **フェルミ積分** $F_{1/2}$ になり、初等関数で表せない（低温ではゾンマーフェルト展開で近似する）。

**実際の 2 次元電子系**:

1. **半導体ヘテロ接合／MOSFET の反転層**。GaAs/AlGaAs 界面や Si-MOS の界面に電子が井戸型ポテンシャルで閉じ込められ、面内には自由な 2 次元電子ガス（2DEG）が形成される。量子ホール効果はここで発見された。
2. **グラフェンなどの原子層物質**。厚さが原子 1 層なので本質的に 2 次元。ただしグラフェンは分散が線形（$\varepsilon = \hbar v_F|k|$）なので状態密度は $D\propto|\varepsilon|$ となり、本問の放物線分散とは異なる。

（他に液体ヘリウム薄膜、遷移金属ダイカルコゲナイド単層、銅酸化物高温超伝導体の $\mathrm{CuO_2}$ 面なども挙げられる）

---

