# 解答・解説 — 2027 年度 予想問題 第 2 巡（第 2-1 回 〜 第 2-6 回）

各大問 100 点。小問の配点は各問の冒頭に括弧で示す。

**採点のとき**: 計算が合っているのに「最後の 1 行」（値・結論の文）が無い場合は、
その小問の配点の 3〜5 割を引く。本番の採点もそうなる。

---

## 7 ｜ 第 2-1 回　力学（中心力・有効ポテンシャル）

**問 1（15 点）** 引力 $-k/r^2$ のポテンシャルは $U(r) = -k/r$（無限遠で $0$）。平面極座標で

$$
L = \frac12 m(\dot r^2 + r^2\dot\theta^2) + \frac{k}{r}
$$

$L$ は $\theta$ を含まない（循環座標）から $\dfrac{d}{dt}\dfrac{\partial L}{\partial\dot\theta} = \dfrac{\partial L}{\partial\theta} = 0$、すなわち $\dfrac{\partial L}{\partial\dot\theta} = mr^2\dot\theta = \ell$ は保存する。**よって角運動量が保存する。**

**問 2（25 点）** $r$ の方程式は $m\ddot r = mr\dot\theta^2 - k/r^2$。$\dot\theta = \ell/(mr^2)$ を代入して

$$
m\ddot r = \frac{\ell^2}{mr^3} - \frac{k}{r^2} = -\frac{d}{dr}\underbrace{\left[\frac{\ell^2}{2mr^2} - \frac{k}{r}\right]}_{U_{\rm eff}(r)}
$$

$$
\boxed{\;U_{\rm eff}(r) = \frac{\ell^2}{2mr^2} - \frac{k}{r}\;}
$$

🔴 **符号に注意**: 引力だから $-k/r$。$+k/r$ にすると $U_{\rm eff}$ は単調減少になり、極小（＝円軌道）が存在しなくなる。**次の小問で $r_0$ が出た時点で矛盾に気づけるので、必ず突き合わせること。**

$U_{\rm eff}'(r) = -\ell^2/(mr^3) + k/r^2 = 0$ より

$$
\boxed{\;r_0 = \frac{\ell^2}{mk}\;},\qquad
U_{\rm eff}(r_0) = \frac{mk^2}{2\ell^2} - \frac{mk^2}{\ell^2} = \boxed{-\frac{mk^2}{2\ell^2}}
$$

概形は $r\to0$ で $+\infty$（遠心力障壁）、$r\to\infty$ で $0^-$、途中に 1 つだけ極小をもつ谷。$E = U_{\rm eff}(r_0)$ が円軌道、$U_{\rm eff}(r_0)<E<0$ が $r_{\min}\le r\le r_{\max}$ の束縛楕円軌道、$E\ge0$ が非束縛。

**問 3（25 点）**

$$
U_{\rm eff}''(r) = \frac{3\ell^2}{mr^4} - \frac{2k}{r^3}
\;\xrightarrow{\;r=r_0,\ \ell^2 = mkr_0\;}\;
\frac{3k}{r_0^3} - \frac{2k}{r_0^3} = \frac{k}{r_0^3}
$$

$$
\omega_r = \sqrt{\frac{U_{\rm eff}''(r_0)}{m}} = \boxed{\sqrt{\frac{k}{mr_0^3}}}
$$

一方 $\omega_\theta = \dfrac{\ell}{mr_0^2} = \dfrac{\sqrt{mkr_0}}{mr_0^2} = \sqrt{\dfrac{k}{mr_0^3}}$。

**$\omega_r = \omega_\theta$。** 動径が 1 往復する間にちょうど $2\pi$ だけ公転するので、質点は 1 周で元の位置に戻る。**よって軌道は閉じる**（逆 2 乗力に固有の性質。ベルトランの定理）。

**問 4（20 点）** $U(r) = -\dfrac{k}{(n-1)r^{n-1}}$、$U'(r) = k/r^n$、$U''(r) = -nk/r^{n+1}$。

$$
U_{\rm eff}' = -\frac{\ell^2}{mr^3} + \frac{k}{r^n} = 0 \;\Rightarrow\; \frac{\ell^2}{m} = k\,r_0^{3-n}
$$

$$
U_{\rm eff}''(r_0) = \frac{3\ell^2}{mr_0^4} - \frac{nk}{r_0^{n+1}}
= \frac{3k}{r_0^{n+1}} - \frac{nk}{r_0^{n+1}} = \frac{k(3-n)}{r_0^{n+1}}
$$

安定条件は $U_{\rm eff}''(r_0)>0$、すなわち $\boxed{n<3}$。$n=2$（重力・クーロン）と $n=-1$（等方調和振動子）はいずれも満たす。$n=3$ はちょうど中立、$n>3$ は不安定。

**問 5（15 点）** $T = 2\pi/\omega_\theta$ で、問 3 より $\omega_\theta^2 = k/(mr_0^3)$ だから

$$
\boxed{\;T = 2\pi\sqrt{\frac{mr_0^3}{k}}\;},\qquad T^2 = \frac{4\pi^2 m}{k}\,r_0^3 \propto r_0^3
$$

万有引力なら $k = GMm$ なので $T^2 = 4\pi^2r_0^3/(GM)$ となり、比例係数が中心天体の質量だけで決まる（ケプラーの第 3 法則）。

---

## 8 ｜ 第 2-1 回　電磁気学（同心導体球殻 / 平行電流 / RC）

**問 1（35 点）**

**(1)（15 点）** 球対称なので半径 $r$ の球面をガウス面にとると $E(r)\cdot4\pi r^2 = Q_{\rm enc}/\varepsilon_0$。

| 領域 | $Q_{\rm enc}$ | $E(r)$ |
| --- | --- | --- |
| $r<a$ | $0$（導体内部） | $0$ |
| $a<r<b$ | $Q$ | $\dfrac{Q}{4\pi\varepsilon_0r^2}$ |
| $b<r<c$ | $Q + (-Q) = 0$（導体内部） | $0$ |
| $r>c$ | $Q$ | $\dfrac{Q}{4\pi\varepsilon_0r^2}$ |

**(2)（10 点）** 球殻の内部（$b<r<c$）で $E=0$ でなければならないから、$r=b$ の内面に $\boxed{-Q}$。球殻全体は中性だから $r=c$ の外面に $\boxed{+Q}$。

**(3)（10 点）** $E=0$ の領域は電位差に寄与しない。

$$
V(a) = \int_a^\infty E\,dr = \frac{Q}{4\pi\varepsilon_0}\left[\int_a^b\frac{dr}{r^2} + \int_c^\infty\frac{dr}{r^2}\right]
= \boxed{\frac{Q}{4\pi\varepsilon_0}\left(\frac1a - \frac1b + \frac1c\right)}
$$

検算: $b\to a$ かつ $c\to a$ の極限で $Q/(4\pi\varepsilon_0a)$（孤立導体球）に戻る。

**問 2（25 点）**

**(1)（12 点）** 軸対称なので半径 $r$ の同心円をアンペール閉路にとると $B\cdot2\pi r = \mu_0 I$、

$$
\boxed{B(r) = \frac{\mu_0I}{2\pi r}}
$$

**(2)（13 点）** 導線 1 が導線 2 の位置に作る磁束密度は $B_1 = \mu_0I_1/(2\pi d)$。長さ $L$ の部分が受ける力は $F = I_2LB_1$ だから

$$
\boxed{\frac{F}{L} = \frac{\mu_0I_1I_2}{2\pi d}}
$$

向きは $\boldsymbol F = I_2\boldsymbol L\times\boldsymbol B_1$ を評価すると相手に向く。**同じ向きの電流どうしは引力**（逆向きなら斥力）。

**問 3（40 点）**

**(1)（12 点）** $V_0 = RI + Q/C$、$I = dQ/dt$ より $R\dot Q + Q/C = V_0$。$Q(0)=0$ の下で

$$
\boxed{Q(t) = CV_0\left(1 - e^{-t/\tau}\right)},\qquad \boxed{\tau = RC}
$$

**(2)（20 点）** 最終電荷は $Q_\infty = CV_0$。

- (i) 電池がした仕事: $W_{\rm batt} = \displaystyle\int_0^\infty V_0I\,dt = V_0Q_\infty = \boxed{CV_0^2}$
- (ii) コンデンサーのエネルギー: $U_C = \dfrac{Q_\infty^2}{2C} = \boxed{\dfrac12CV_0^2}$
- (iii) 抵抗のジュール熱: $W_R = W_{\rm batt} - U_C = \boxed{\dfrac12CV_0^2}$

（直接計算しても同じ: $I = (V_0/R)e^{-t/RC}$ より $\int_0^\infty RI^2dt = (V_0^2/R)\cdot RC/2 = CV_0^2/2$。）

🔴 **ここが検算ポイント**: $CV_0^2 = \tfrac12CV_0^2 + \tfrac12CV_0^2$。3 つを**並べて足す**だけでエネルギー保存が確認できる。$U_C$ を $CV_0^2$ と書いてしまうと $CV_0^2 \ne CV_0^2 + \tfrac12CV_0^2$ で即座に破綻する。

**(3)（8 点）** **3 つとも変わらない。** $W_{\rm batt}, U_C, W_R$ はいずれも $C$ と $V_0$ だけで決まり、$R$ を含まない。$R$ が決めるのは時定数 $\tau=RC$（＝どれだけの時間をかけて移るか）だけである。**抵抗で捨てる分は必ず蓄える分と等しく、充電の効率は $R$ によらず常に 50 %。**

---

## 10 ｜ 第 2-1 回　統計力学（縮退した 2 準位系）

**問 1（12 点）** 励起状態は $g$ 個あるので

$$
\boxed{z = 1 + g\,e^{-\beta\Delta} = 1 + g\,e^{-x}}
$$

**問 2（18 点）** 粒子は独立（区別できる格子点上の粒子とみなす）なので $Z = z^N$。

$$
\boxed{F = -Nk_BT\ln\left(1+ge^{-x}\right)},\qquad
U = -\frac{\partial\ln Z}{\partial\beta} = \boxed{\frac{N\Delta\,ge^{-x}}{1+ge^{-x}}}
$$

検算: $T\to\infty$（$x\to0$）で $U\to N\Delta\,g/(1+g)$（$g+1$ 個の状態に等分配され、そのうち $g$ 個がエネルギー $\Delta$）。$T\to0$ で $U\to0$。$0\le U\le N\Delta$ を満たす。

**問 3（25 点）** $C = dU/dT = (dU/dx)(dx/dT)$、$dx/dT = -x/T$。$u \equiv ge^{-x}$ とおくと $U = N\Delta\,u/(1+u)$、$du/dx = -u$ より

$$
\frac{dU}{dx} = N\Delta\frac{1}{(1+u)^2}\frac{du}{dx} = -\frac{N\Delta\,u}{(1+u)^2}
$$

$$
\boxed{\;C = N k_B\,x^2\,\frac{ge^{-x}}{\left(1+ge^{-x}\right)^2}
= Nk_B\left(\frac{\Delta}{k_BT}\right)^2\frac{ge^{-\Delta/k_BT}}{\left(1+ge^{-\Delta/k_BT}\right)^2}\;}
$$

- **高温極限**（$x\ll1$）: $e^{-x}\to1$ なので $C \simeq \dfrac{g}{(1+g)^2}Nk_Bx^2 \propto \dfrac{1}{T^2}$（**べきで落ちる**）
- **低温極限**（$x\gg1$）: 分母 $\to1$ なので $C \simeq gNk_B\,x^2e^{-x} = gNk_B\left(\dfrac{\Delta}{k_BT}\right)^2e^{-\Delta/k_BT}$（**指数関数的にゼロ**）

低温側で指数的に落ちるのは、$\Delta$ より小さいエネルギーの励起が存在しない（エネルギーギャップ）ためである。この山型が**ショットキー比熱**。

**問 4（25 点）** $S = (U-F)/T$ より

$$
\boxed{\;S = Nk_B\left[\ln\left(1+ge^{-x}\right) + \frac{x\,ge^{-x}}{1+ge^{-x}}\right]\;}
$$

- $T\to0$（$x\to\infty$）: $S\to0$。基底状態は縮退度 1 なので $W=1$、$S = k_B\ln1 = 0$。**熱力学第 3 法則と整合。**
- $T\to\infty$（$x\to0$）: $S\to Nk_B\ln(1+g)$。各粒子が $1+g$ 個の状態を等確率でとるから $W = (1+g)^N$、$S = k_B\ln W = Nk_B\ln(1+g)$。**一致する。**

（$g=1$ なら $Nk_B\ln2$ という見慣れた値になる。**$S$ がこの上限を超えたら計算間違い。**）

**問 5（20 点）** $u = ge^{-x}$ として $C = Nk_Bx^2u/(1+u)^2$。$du/dx = -u$ に注意して $dC/dx = 0$ とすると

$$
2x\frac{u}{(1+u)^2} + x^2\frac{(1-u)}{(1+u)^3}(-u) = 0
\;\Longrightarrow\;
\boxed{\;x = \frac{2(1+u)}{1-u},\qquad u = ge^{-x}\;}
$$

$g=1$ では $x\simeq2.40$、すなわち $k_BT/\Delta \simeq 0.417$。

$g$ を大きくすると $u$ が大きくなるので、上式を満たす $x$ は大きくなる（$g=3$ では $x\simeq2.85$、$k_BT/\Delta\simeq0.35$）。$x = \Delta/k_BT$ が大きい＝温度が低いから、**ピークは低温側へ動く。**

**物理的な理由**: 励起状態の数が多いほど「励起することで得られるエントロピー」$\ln g$ が大きく、自由エネルギー $\Delta - k_BT\ln g$ の観点で、より低い温度から励起が起こりはじめる。実際、励起が半分ほど進む温度は $ge^{-\Delta/k_BT}\sim1$ すなわち $k_BT \sim \Delta/\ln g$ で、$g$ とともに下がる。

---

## 7 ｜ 第 2-2 回　力学（慣性モーメントとヨーヨー）

**問 1（25 点）**

**(1) 円柱（10 点）** 半径 $r$、厚み $dr$ の薄い円筒殻に分ける。密度 $\rho = M/(\pi a^2h)$、$dm = \rho\,2\pi r h\,dr$。

$$
I = \int_0^a r^2\,dm = 2\pi\rho h\int_0^a r^3dr = 2\pi\rho h\cdot\frac{a^4}{4} = \frac{\pi\rho ha^4}{2} = \boxed{\frac12Ma^2}
$$

**(2) 円錐（15 点）** 頂点を原点、対称軸を $z$ 軸にとり、高さ $z$ での半径は $r(z) = az/h$。厚み $dz$ の薄い円板の質量は $dm = \rho\pi r^2dz$、その軸まわりの慣性モーメントは $dI = \tfrac12 dm\,r^2$。

$$
I = \frac12\rho\pi\int_0^h r^4dz = \frac{\rho\pi a^4}{2h^4}\int_0^h z^4dz
= \frac{\rho\pi a^4}{2h^4}\cdot\frac{h^5}{5} = \frac{\rho\pi a^4h}{10}
$$

🔴 **原始関数を落とさないこと**: $\int_0^h z^4dz = h^5/5$ であって $h^4$ ではない。ここで 1 つ落とすと最終形の $a$ と $h$ の次数が合わなくなる。

質量は $M = \rho\cdot\tfrac13\pi a^2h$、すなわち $\rho\pi a^2h = 3M$。したがって

$$
I = \frac{(\rho\pi a^2h)a^2}{10} = \boxed{\frac{3}{10}Ma^2}
$$

**検算**: $\tfrac12Ma^2 \le Ma^2$、$\tfrac3{10}Ma^2 \le Ma^2$ でともに OK。円錐のほうが質量が軸の近くに寄っているので $I$ が小さいのも合理的。（$I>Ma^2$ が出たら、その時点で計算間違い。すべての質量が最外周にある円筒殻の $Ma^2$ が上限。）

**問 2（20 点）** 重心の並進と重心まわりの回転に分ける。糸が滑らずほどけるので $a_{\rm cm} = a\alpha$。

$$
Mg - T = Ma_{\rm cm},\qquad Ta = I\alpha = \frac12Ma^2\cdot\frac{a_{\rm cm}}{a}\;\Rightarrow\; T = \frac12Ma_{\rm cm}
$$

$$
Mg = \frac32Ma_{\rm cm} \;\Rightarrow\;
\boxed{a_{\rm cm} = \frac23g},\qquad \boxed{T = \frac13Mg}
$$

**問 3（20 点）** 等加速度運動だから

$$
v = \sqrt{2a_{\rm cm}h_0} = \boxed{\sqrt{\frac{4gh_0}{3}}}
$$

$$
K_{\rm trans} = \frac12Mv^2 = \frac23Mgh_0,\qquad
K_{\rm rot} = \frac12I\omega^2 = \frac12\cdot\frac12Ma^2\cdot\frac{v^2}{a^2} = \frac14Mv^2 = \frac13Mgh_0
$$

$$
\boxed{K_{\rm trans}:K_{\rm rot} = 2:1},\qquad K_{\rm trans}+K_{\rm rot} = Mgh_0\;\checkmark
$$

**問 4（20 点）** 慣性モーメントは円柱本体のもの $\tfrac12Ma^2$ のままだが、糸の作用線までの腕は $b$ になる。$a_{\rm cm} = b\alpha$ に注意して

$$
Mg - T = Ma_{\rm cm},\qquad Tb = \frac12Ma^2\frac{a_{\rm cm}}{b}\;\Rightarrow\; T = \frac{Ma^2a_{\rm cm}}{2b^2}
$$

$$
\boxed{\;a_{\rm cm} = \frac{g}{1+\dfrac{a^2}{2b^2}} = \frac{2b^2g}{2b^2+a^2}\;}
$$

$b=a$ とすると $\tfrac23g$ で問 2 に戻る（**検算**）。$b\to0$ では $a_{\rm cm}\to0$: 巻き取り半径が小さいほど、失う位置エネルギーのほとんどが回転運動に回り、重心はほとんど落下しなくなる（同時に張力 $T\to Mg$）。

**問 5（15 点）** 重心が $h_0$ 落下する間、

- 張力が重心の並進に対してする仕事: $W_{\rm trans} = -Th_0 = \boxed{-\dfrac13Mgh_0}$（張力は上向き、変位は下向き）
- 張力のモーメントが回転に対してする仕事: 糸がほどける長さ＝落下距離なので回転角は $\phi = h_0/a$。$W_{\rm rot} = (Ta)\phi = Th_0 = \boxed{+\dfrac13Mgh_0}$

**和はちょうど $0$。** 糸と円柱の接点は瞬間的に速度ゼロ（糸は伸びず、上端は固定）なので、糸は系に対して正味の仕事をしない。エネルギー収支は
$K_{\rm trans} = Mgh_0 - \tfrac13Mgh_0 = \tfrac23Mgh_0$、$K_{\rm rot} = \tfrac13Mgh_0$ となり問 3 と一致する。

---

## 8 ｜ 第 2-2 回　電磁気学（帯電円柱 / 円柱電流 / RL）

**問 1（30 点）**

**(1)（15 点）** 無限長で軸対称なので、半径 $r$、長さ $L$ の同軸円筒をガウス面にとる。側面のみ寄与し $E(r)\cdot2\pi rL = Q_{\rm enc}/\varepsilon_0$。

$$
r<a:\; Q_{\rm enc} = \rho\pi r^2L \;\Rightarrow\; \boxed{E = \frac{\rho r}{2\varepsilon_0}},\qquad
r>a:\; Q_{\rm enc} = \rho\pi a^2L \;\Rightarrow\; \boxed{E = \frac{\rho a^2}{2\varepsilon_0 r}}
$$

（ガウス面の側面積は $2\pi rL$。$\pi r^2L$ と書かないこと。）

**(2)（15 点）** $V(r) = -\displaystyle\int_a^r E\,dr'$（$V(a)=0$）。

$$
r<a:\;V(r) = -\int_a^r\frac{\rho r'}{2\varepsilon_0}dr' = \boxed{\frac{\rho}{4\varepsilon_0}\left(a^2-r^2\right)}\;(>0)
$$

$$
r>a:\;V(r) = -\int_a^r\frac{\rho a^2}{2\varepsilon_0r'}dr' = \boxed{-\frac{\rho a^2}{2\varepsilon_0}\ln\frac ra}\;(<0)
$$

**検算**: $\rho>0$ なら中心が最も電位が高く、外へ行くほど下がる。両式とも $r=a$ で $0$、$r=a$ で微分係数も連続（$-\rho a/2\varepsilon_0$）。

**問 2（30 点）**

**(1)（12 点）** 電流密度は $j = I/(\pi a^2)$。半径 $r$ の同心円をアンペール閉路にとる。

$$
r<a:\;B\cdot2\pi r = \mu_0 j\pi r^2 \;\Rightarrow\; \boxed{B = \frac{\mu_0Ir}{2\pi a^2}},\qquad
r>a:\;\boxed{B = \frac{\mu_0I}{2\pi r}}
$$

**(2)（18 点）** 単位長さあたりの内部の磁気エネルギーは

$$
\frac{W}{\ell} = \int_0^a\frac{B^2}{2\mu_0}2\pi r\,dr
= \int_0^a\frac{1}{2\mu_0}\left(\frac{\mu_0Ir}{2\pi a^2}\right)^2 2\pi r\,dr
= \frac{\mu_0I^2}{4\pi a^4}\int_0^a r^3dr = \frac{\mu_0I^2}{16\pi}
$$

$W = \tfrac12L_{\rm int}I^2$ と比べて

$$
\boxed{\;\frac{L_{\rm int}}{\ell} = \frac{\mu_0}{8\pi}\;}
$$

**$a$ を含まない。** 太い導線でも細い導線でも、内部インダクタンスは単位長さあたり $\mu_0/8\pi \simeq 5\times10^{-8}$ H/m で共通である（半径を変えると $B$ の大きさと体積が互いに打ち消しあうため）。

**問 3（40 点）**

**(1)（12 点）** $V_0 = RI + L\,dI/dt$、$I(0)=0$ より

$$
\boxed{I(t) = \frac{V_0}{R}\left(1-e^{-t/\tau}\right)},\qquad \boxed{\tau = \frac LR}
$$

**(2)（16 点）** 切り離す直前の電流は $I_0 = V_0/R$。コイルに蓄えられた磁気エネルギーがすべて抵抗で熱になるので

$$
W = \frac12LI_0^2 = \boxed{\frac{LV_0^2}{2R^2}}
$$

**次元チェック**: $[LV_0^2/R^2] = \mathrm{H\cdot V^2/\Omega^2} = \mathrm{H\cdot A^2} = \mathrm{J}$。$\checkmark$（$V_0$ を 1 乗で書いてしまうと次元が合わない。）

**(3)（12 点）** **$L$ を小さくする。** 最終電流は $V_0/R$ で $R$ だけで決まるから、$R$ を大きくすると立ち上がりは速くなる（$\tau = L/R$）が最終電流まで下がってしまい、要求を満たさない。$L$ を小さくすれば最終電流を変えずに $\tau$ だけ短くできる。

---

## 10 ｜ 第 2-2 回　統計力学（調和振動子・ミクロカノニカル）

**問 1（18 点）** $N$ 個の振動子に合計 $M$ 個の量子を配る場合の数（重複組合せ）。$M$ 個の玉と $N-1$ 本の仕切りを並べる問題だから

$$
\boxed{\;W(N,M) = \binom{M+N-1}{M} = \frac{(M+N-1)!}{M!\,(N-1)!}\;}
$$

**問 2（15 点）** $N\gg1$ で $N-1\simeq N$、$M+N-1\simeq M+N$ とし、$\ln n!\simeq n\ln n - n$ を使う。$-n$ の項は $(M+N)-M-N=0$ で消える。

$$
\boxed{\;S = k_B\left[(M+N)\ln(M+N) - M\ln M - N\ln N\right]\;}
$$

**問 3（27 点）** $E = (M+N/2)\hbar\omega$ より $\partial M/\partial E = 1/(\hbar\omega)$。

$$
\frac1T = \frac{\partial S}{\partial E} = \frac{1}{\hbar\omega}\frac{\partial S}{\partial M}
= \frac{k_B}{\hbar\omega}\Big[\ln(M+N) - \ln M\Big]
= \frac{k_B}{\hbar\omega}\ln\left(1+\frac NM\right)
$$

したがって $\dfrac{\hbar\omega}{k_BT} = \ln\left(1+\dfrac NM\right)$。$x\equiv\beta\hbar\omega$ とおくと

$$
1+\frac NM = e^{x} \;\Longrightarrow\; \boxed{\;M = \frac{N}{e^{\beta\hbar\omega}-1}\;}
$$

$$
\boxed{\;E = N\hbar\omega\left[\frac12 + \frac{1}{e^{\beta\hbar\omega}-1}\right]
= \frac{N\hbar\omega}{2}\coth\frac{\beta\hbar\omega}{2}\;}
$$

これはカノニカル集団で得られる式とまったく同じである（集団の等価性）。$M$ は 1 振動子あたりの平均量子数で、プランク分布 $\langle n\rangle = 1/(e^{\beta\hbar\omega}-1)$ に一致する。

**問 4（25 点）** $E = N\hbar\omega/2 + N\hbar\omega(e^x-1)^{-1}$、$dx/dT = -x/T$ より

$$
C = \frac{dE}{dT} = N\hbar\omega\cdot\left(-\frac{e^x}{(e^x-1)^2}\right)\cdot\left(-\frac xT\right)
= \boxed{\;Nk_B\,\frac{x^2e^{x}}{\left(e^{x}-1\right)^2}\;},\qquad x = \frac{\hbar\omega}{k_BT}
$$

🔴 $(e^x-1)^2$ と $(e^{x/2}-e^{-x/2})^2$ を混同しないこと。両者は $e^x$ 倍だけ違い、**高温極限ではどちらも $x^2$ になって差が隠れ、低温極限ではじめて表面化する。**

- **高温極限**（$x\ll1$）: $e^x-1\simeq x$、$e^x\simeq1$ より $C \to Nk_B$。1 次元のデュロン–プティ則。$\checkmark$
- **低温極限**（$x\gg1$）: $(e^x-1)^2\simeq e^{2x}$ より $\boxed{C \simeq Nk_B\,x^2e^{-x} = Nk_B\left(\dfrac{\hbar\omega}{k_BT}\right)^2e^{-\hbar\omega/k_BT}}$

**問 5（15 点）**

**高温**: 1 次元調和振動子 1 個には運動エネルギーの 2 次形式が 1 つ、ポテンシャルの 2 次形式が 1 つ、計 2 つの 2 次自由度がある。エネルギー等分配則によりそれぞれ $\tfrac12k_BT$ ずつ、合わせて 1 個あたり $k_BT$。$N$ 個で $U = Nk_BT$ となり $C = Nk_B$。（3 次元なら 3 倍して $3Nk_B$ ＝通常のデュロン–プティ則。）

**低温**: 準位が $\hbar\omega$ 間隔で離散的なので、$k_BT \ll \hbar\omega$ では熱ゆらぎで 1 つの量子すら励起できない。励起確率は $e^{-\hbar\omega/k_BT}$ という**ボルツマン因子**で抑えられ、自由度が「凍結」する。指数関数の落ち方がべき $x^2$ に勝つので $C\to0$。これが古典論（等分配則）が低温で破れる典型例である。

---

## 7 ｜ 第 2-3 回　力学（回転する円環上のビーズ）

**問 1（18 点）** 円環の回転軸からの距離は $R\sin\theta$、最下点からの高さは $R(1-\cos\theta)$。速度の 2 乗は「円環に沿う成分」と「円環とともに回る成分」の和で

$$
v^2 = R^2\dot\theta^2 + \left(R\sin\theta\right)^2\omega^2
$$

$$
\boxed{\;L = \frac12mR^2\left(\dot\theta^2 + \omega^2\sin^2\theta\right) - mgR(1-\cos\theta)\;}
$$

**問 2（17 点）**

$$
\frac{d}{dt}\left(mR^2\dot\theta\right) = mR^2\omega^2\sin\theta\cos\theta - mgR\sin\theta
$$

$$
\boxed{\;mR^2\ddot\theta = -\frac{dU_{\rm eff}}{d\theta},\qquad
U_{\rm eff}(\theta) = -\frac12mR^2\omega^2\sin^2\theta + mgR(1-\cos\theta)\;}
$$

第 1 項は遠心力による見かけのポテンシャル（$\theta$ が大きいほど下がる＝外へ押し出す）、第 2 項が重力。**回転のエネルギー項が $-$ 符号で入る**のがこの種の問題の要点で、$\omega$ が大きいと $\theta=0$ の谷を潰す。

**問 3（22 点）**

$$
\frac{dU_{\rm eff}}{d\theta} = mR\sin\theta\left(g - R\omega^2\cos\theta\right) = 0
$$

- $\sin\theta = 0$ より $\theta = 0$（最下点）と $\theta = \pi$（最上点）。**これは $\omega$ によらず常につり合い。**
- $\cos\theta_0 = \dfrac{g}{R\omega^2}$。これが $[-1,1]$ に入る、すなわち $R\omega^2 \ge g$ のときだけ存在する。

$$
\boxed{\;\omega_c = \sqrt{\frac gR}\;},\qquad \boxed{\;\cos\theta_0 = \frac{g}{R\omega^2} = \frac{\omega_c^2}{\omega^2}\;}
$$

**次元チェック**: $\cos\theta_0$ は無次元。$[g/(R\omega^2)] = (\mathrm{m/s^2})/(\mathrm{m\cdot s^{-2}})$ は無次元 $\checkmark$

**問 4（21 点）**

$$
\frac{d^2U_{\rm eff}}{d\theta^2} = mR\left[\cos\theta\left(g - R\omega^2\cos\theta\right) + R\omega^2\sin^2\theta\right]
$$

- $\theta=0$: $U_{\rm eff}'' = mR(g - R\omega^2)$。安定条件 $U_{\rm eff}''>0$ は $\boxed{\omega<\omega_c = \sqrt{g/R}}$。
  $\omega>\omega_c$ では最下点は**不安定**になる（ビーズは自発的に横へずれる）。
- $\theta=\theta_0$: 第 1 項は $g - R\omega^2\cos\theta_0 = 0$ で消え、$U_{\rm eff}'' = mR^2\omega^2\sin^2\theta_0 > 0$。**したがって安定。**

これは連続対称性の自発的破れの最も簡単な例で、$\omega = \omega_c$ を境に安定な平衡が 1 つから 2 つ（$\pm\theta_0$）に分岐する（ピッチフォーク分岐）。$\theta=\pi$ は常に不安定（$U_{\rm eff}''=mR(-g-R\omega^2)<0$）。

**問 5（22 点）**

$$
\Omega^2 = \frac{U_{\rm eff}''(\theta_0)}{mR^2} = \omega^2\sin^2\theta_0
= \omega^2\left(1-\frac{g^2}{R^2\omega^4}\right)
$$

$$
\boxed{\;\Omega = \sqrt{\omega^2 - \frac{g^2}{R^2\omega^2}}
= \omega\sqrt{1 - \left(\frac{\omega_c}{\omega}\right)^4}\;}
$$

$\omega\to\omega_c^+$ で $\Omega\to0$（分岐点では復元力が消える）。$\omega\to\infty$ では $\boxed{\Omega\to\omega}$: 重力が無視でき、遠心力だけで決まる運動になり、ビーズは実質的に「水平面内の円環上を回る」ので振動数が回転数に一致する。

---

## 8 ｜ 第 2-3 回　電磁気学（半分誘電体 / トロイド / 変位電流）

**問 1（35 点）**

**(1)（15 点）** 2 つの領域は**同じ電位差**をもつので**並列**である。

$$
C = \frac{\varepsilon_0(S/2)}{d} + \frac{\varepsilon_0\varepsilon_r(S/2)}{d}
= \boxed{\frac{\varepsilon_0S(1+\varepsilon_r)}{2d}}
$$

$\varepsilon_r=1$ で $\varepsilon_0S/d$（**検算**）。

**(2)（20 点）** 両極板はそれぞれ等電位で、間隔も $d$ で共通だから、**極板間の電位差 $V$ は左右どちらの領域でも同じ**。一様電場なので $E = V/d$ も左右で等しい。

$$
V = \frac QC = \frac{2Qd}{\varepsilon_0S(1+\varepsilon_r)},\qquad
\boxed{E = \frac Vd = \frac{2Q}{\varepsilon_0S(1+\varepsilon_r)}}
$$

誘電体中の分極は $P = \varepsilon_0(\varepsilon_r-1)E$、束縛電荷面密度はその大きさに等しいので

$$
\boxed{\;\sigma_b = \varepsilon_0(\varepsilon_r-1)E = \frac{2Q(\varepsilon_r-1)}{S(1+\varepsilon_r)}\;}
$$

（正極板に接する誘電体面には $-\sigma_b$、負極板側には $+\sigma_b$ が現れる。）
$\varepsilon_r\to1$ で $\sigma_b\to0$ $\checkmark$。また $\varepsilon_r\to\infty$ で $\sigma_b\to2Q/S$ と有限にとどまるのも合理的。

**検算（自由電荷の総和）**: 誘電体側の極板の自由電荷面密度は $D_1 = \varepsilon_0\varepsilon_rE$、真空側は $D_2 = \varepsilon_0E$。合計 $\left(D_1+D_2\right)\dfrac S2 = \varepsilon_0E\dfrac{S(1+\varepsilon_r)}{2} = Q$ $\checkmark$

**問 2（30 点）**

**(1)（12 点）** 半径 $r$ の円をアンペール閉路にとると、それを貫く電流は $NI$。

$$
B\cdot2\pi r = \mu_0NI \;\Rightarrow\; \boxed{B(r) = \frac{\mu_0NI}{2\pi r}}\quad(a<r<b)
$$

**(2)（18 点）** 1 巻きを貫く磁束は

$$
\Phi_1 = \int_a^b B(r)\,h\,dr = \frac{\mu_0NIh}{2\pi}\ln\frac ba
$$

**相互・自己インダクタンスの定義は $N\Phi_1 = LI$**（全巻数を掛けるのを忘れない）。

$$
\boxed{\;L = \frac{\mu_0N^2h}{2\pi}\ln\frac ba\;}
$$

$b = a+w$、$w\ll a$ では $\ln(b/a) = \ln(1+w/a)\simeq w/a$ だから

$$
L \simeq \frac{\mu_0N^2hw}{2\pi a} = \frac{\mu_0N^2S}{\ell}\qquad(S=hw,\ \ell=2\pi a)\;\checkmark
$$

**問 3（35 点）**

**(1)（15 点）** 極板の電荷を $Q(t)$ とすると $E = Q/(\varepsilon_0\pi a^2)$。変位電流密度は

$$
j_d = \varepsilon_0\frac{\partial E}{\partial t} = \frac{1}{\pi a^2}\frac{dQ}{dt} = \boxed{\frac{I}{\pi a^2}}
$$

（伝導電流を極板の面積で割ったものに等しい。**これが「電流の連続性」を回復させる。**）

**(2)（20 点）** 極板間には伝導電流がないので、アンペール–マクスウェルの法則は

$$
\oint\boldsymbol B\cdot d\boldsymbol l = \mu_0\int j_d\,dS
$$

半径 $r\ (<a)$ の円をとると右辺は $\mu_0 j_d\pi r^2 = \mu_0Ir^2/a^2$。

$$
B\cdot2\pi r = \frac{\mu_0Ir^2}{a^2} \;\Rightarrow\; \boxed{\;B(r) = \frac{\mu_0Ir}{2\pi a^2}\;}
$$

$r=a$ で $\mu_0I/(2\pi a)$ となり、導線のまわりの磁場と連続的につながる（**検算**）。形も一様電流の流れる円柱の内部磁場と同じ。

---

## 10 ｜ 第 2-3 回　統計力学（格子気体と状態方程式）

**問 1（15 点）** $M$ 個のセルから、分子を入れる $N$ 個を選ぶ組合せである。分子は区別できず、1 セルに高々 1 個だから

$$
\boxed{\;W(M,N) = \binom{M}{N} = \frac{M!}{N!\,(M-N)!}\;}
$$

🔴 **重複組合せ $\binom{M+N-1}{N}$ と混同しないこと。** 「1 セルに何個でも入る」なら重複組合せ、
**「高々 1 個」なら単純な二項係数**である。第 2-2 回の調和振動子（量子は 1 準位に何個でも入る）は前者、
この格子気体は後者。**どちらかを問題文の 1 行から即座に判定できること。**

**問 2（20 点）** スターリングの公式より

$$
\frac{S}{k_B} = \ln W = M\ln M - N\ln N - (M-N)\ln(M-N)
$$

$N = \phi M$、$M-N = (1-\phi)M$ を代入すると $\ln M$ の項が $M[1-\phi-(1-\phi)]\ln M = 0$ で消えて

$$
\boxed{\;S = -Mk_B\left[\phi\ln\phi + (1-\phi)\ln(1-\phi)\right]\;}
$$

（2 値の混合エントロピーの形。$M$ に比例する＝**示量的**であることを確認しておくとよい。）

- $\phi\to0$: $\phi\ln\phi\to0$ より $\boxed{S\to0}$。分子が無く、配置は「全セル空」の 1 通りだから $W=1$。
- $\phi\to1$: 同様に $\boxed{S\to0}$。全セルが埋まり、配置はやはり 1 通り。

$dS/d\phi = -Mk_B\ln[\phi/(1-\phi)] = 0$ より $\boxed{\phi = 1/2}$、**そのときの値は**

$$
\boxed{\;S_{\max} = Mk_B\ln2\;}
$$

🔴 **検算**: 各セルは「空 / 詰まっている」の 2 状態しかないので、$S$ は**必ず** $Mk_B\ln2$ 以下である。
$S$ がこれを超えたら計算間違い。$\phi=1/2$ でちょうど上限に達するのは、
$\binom{M}{M/2}\simeq2^M$ に対応する。

**問 3（15 点）** $U=0$ だから

$$
F = U - TS = -TS = \boxed{\;Mk_BT\left[\phi\ln\phi + (1-\phi)\ln(1-\phi)\right]\;}
$$

（$F<0$。$0<\phi<1$ で括弧の中は負なので符号も正しい。）

**問 4（25 点）** $V = Mv_0$ で $v_0$ は定数だから、$N$ を固定したまま $V$ を変えることは $M$ を変えることであり

$$
\left(\frac{\partial}{\partial V}\right)_{T,N} = \frac{1}{v_0}\left(\frac{\partial}{\partial M}\right)_{T,N}
$$

$\phi = N/M$ を代入し戻さず、$F$ を $M,N$ のままで書いて微分するのが安全である。

$$
F = -k_BT\left[M\ln M - N\ln N - (M-N)\ln(M-N)\right]
$$

$$
\left(\frac{\partial F}{\partial M}\right)_{N}
= -k_BT\left[(\ln M + 1) - (\ln(M-N)+1)\right]
= -k_BT\ln\frac{M}{M-N}
$$

$$
P = -\frac{1}{v_0}\left(\frac{\partial F}{\partial M}\right)_N
= \frac{k_BT}{v_0}\ln\frac{M}{M-N}
= \boxed{\;-\frac{k_BT}{v_0}\ln(1-\phi)\;}
$$

**次元の確認**: $[k_BT] = $ J、$[v_0] = $ m$^3$ だから $[k_BT/v_0] = $ J/m$^3$ = Pa。$\ln$ の中は無次元。**圧力になっている。**
また $0<\phi<1$ で $\ln(1-\phi)<0$ だから $P>0$。**負の圧力が出たら計算間違い。**

**問 5（15 点）** $-\ln(1-\phi) = \phi + \dfrac{\phi^2}{2} + \dfrac{\phi^3}{3}+\cdots$ より

$$
P = \frac{k_BT}{v_0}\left(\phi + \frac{\phi^2}{2} + O(\phi^3)\right)
$$

**1 次の項**: $\phi = N/M$、$Mv_0 = V$ だから

$$
P \simeq \frac{k_BT}{v_0}\cdot\frac{N}{M} = \frac{Nk_BT}{Mv_0} = \frac{Nk_BT}{V}
\;\Longrightarrow\; \boxed{PV = Nk_BT}
$$

**理想気体の状態方程式に帰着する。** $\checkmark$

**2 次の項**: まとめると

$$
P = \frac{Nk_BT}{V}\left(1 + \frac{\phi}{2}+\cdots\right)
= \frac{Nk_BT}{V}\left(1 + \frac{N v_0}{2V}+\cdots\right)
$$

**物理的な効果**: 補正は**正**、すなわち同じ密度・温度でも圧力は理想気体より**高くなる**。
原因は**排除体積**である。分子が有限の大きさ $v_0$ をもつため、ある分子から見て他の分子が使える体積は
$V$ より小さく、実効的に混みあう。これが第 2 ビリアル係数 $B_2 = v_0/2\ (>0)$ にあたり、
ファンデルワールス方程式の斥力項（定数 $b$）に対応する。**引力が無い模型なので補正は必ず斥力的（正）になる。**

**問 6（10 点）** $\phi\to1$ で $\ln(1-\phi)\to-\infty$ だから

$$
\boxed{\;P\to+\infty\;}
$$

**意味**: 全セルが埋まった状態（最密充填）がこの模型の体積の下限であり、それ以上は圧縮できない。
有限の圧力では $\phi=1$ に到達できず、押し込むほど圧力が発散する。
**剛体分子に体積があることの直接の帰結**であり、実在気体が有限の温度でも一定体積以下に圧縮できないことに対応する。

---

## 7 ｜ 第 2-4 回　力学（減衰振動と強制振動）

**問 1（18 点）** $m\ddot x = -kx - b\dot x$、すなわち

$$
\ddot x + 2\gamma\dot x + \omega_0^2x = 0
$$

$x\propto e^{\lambda t}$ とおくと $\lambda^2+2\gamma\lambda+\omega_0^2=0$、$\lambda = -\gamma\pm i\sqrt{\omega_0^2-\gamma^2}$。$\gamma<\omega_0$ なので

$$
\boxed{\;x(t) = Ae^{-\gamma t}\cos(\omega_dt+\varphi),\qquad \omega_d = \sqrt{\omega_0^2-\gamma^2}\;}
$$

$A,\varphi$ は初期条件で決まる 2 つの定数。$\omega_d<\omega_0$（抵抗があると振動はゆっくりになる）。

**問 2（20 点）** 包絡線は $Ae^{-\gamma t}$ だから

$$
e^{-\gamma t_{1/e}} = e^{-1}\;\Longrightarrow\; \boxed{t_{1/e} = \frac1\gamma = \frac{2m}{b}}
$$

力学的エネルギーは振幅の 2 乗に比例するので $E(t)\propto e^{-2\gamma t}$。$\gamma\ll\omega_0$ なら 1 周期 $T\simeq2\pi/\omega_0$ の間の減少は

$$
\frac{\Delta E}{E} = 1-e^{-2\gamma T}\simeq 2\gamma T = \frac{4\pi\gamma}{\omega_0}
= \boxed{\frac{2\pi}{Q}},\qquad Q = \frac{\omega_0}{2\gamma}
$$

**$Q$ は「1 ラジアン進む間に失うエネルギーの割合の逆数」**という意味をもつ。$Q$ が大きいほど振動が長く続く。

**問 3（20 点）** $\ddot x + 2\gamma\dot x+\omega_0^2x = (F_0/m)\cos\Omega t$。複素表示 $x = \mathrm{Re}\,[\tilde Ae^{i\Omega t}]$ で

$$
\tilde A\left(-\Omega^2 + 2i\gamma\Omega + \omega_0^2\right) = \frac{F_0}{m}
$$

$$
\boxed{\;A(\Omega) = \frac{F_0/m}{\sqrt{\left(\omega_0^2-\Omega^2\right)^2 + 4\gamma^2\Omega^2}}\;},\qquad
\boxed{\;\tan\delta = \frac{2\gamma\Omega}{\omega_0^2-\Omega^2}\;}
$$

$\Omega\ll\omega_0$ で $\delta\to0$（外力に追随）、$\Omega=\omega_0$ で $\delta=\pi/2$、$\Omega\gg\omega_0$ で $\delta\to\pi$（逆位相）。

**問 4（22 点）** $A$ が最大 ⟺ 根号の中身 $g(\Omega^2) \equiv (\omega_0^2-\Omega^2)^2+4\gamma^2\Omega^2$ が最小。$u=\Omega^2$ とおくと

$$
\frac{dg}{du} = -2(\omega_0^2-u) + 4\gamma^2 = 0 \;\Longrightarrow\; u = \omega_0^2-2\gamma^2
$$

$$
\boxed{\;\Omega_{\max} = \sqrt{\omega_0^2-2\gamma^2}\;}\qquad(\gamma<\omega_0/\sqrt2\ \text{のとき存在})
$$

このとき

$$
g = (2\gamma^2)^2 + 4\gamma^2(\omega_0^2-2\gamma^2) = 4\gamma^2\left(\omega_0^2-\gamma^2\right) = 4\gamma^2\omega_d^2
$$

$$
\boxed{\;A_{\max} = \frac{F_0/m}{2\gamma\omega_d} = \frac{F_0}{2m\gamma\sqrt{\omega_0^2-\gamma^2}} = \frac{F_0}{b\,\omega_d}\;}
$$

🔴 **「$\Omega_{\max}$ を求めよ」で止めないこと。$A_{\max}$ の値まで書いて初めて満点。** $\gamma\to0$ で $A_{\max}\to\infty$（無限大の共振）となるのも整合的。

**問 5（20 点）** $\gamma\ll\omega_0$ なら共振は $\Omega\simeq\omega_0$ の狭い範囲に集中する。$\Omega = \omega_0+\epsilon$（$|\epsilon|\ll\omega_0$）として

$$
\omega_0^2-\Omega^2 = (\omega_0-\Omega)(\omega_0+\Omega) \simeq -2\omega_0\epsilon
$$

$$
A^2 \simeq \frac{(F_0/m)^2}{4\omega_0^2\epsilon^2 + 4\gamma^2\omega_0^2}
$$

最大値は $\epsilon=0$ の $(F_0/m)^2/(4\gamma^2\omega_0^2)$。その半分になるのは分母が 2 倍、すなわち $\epsilon^2=\gamma^2$、$\epsilon=\pm\gamma$。したがって

$$
\boxed{\;\Delta\Omega = 2\gamma\;},\qquad
\frac{\omega_0}{\Delta\Omega} = \frac{\omega_0}{2\gamma} = Q\;\checkmark
$$

**$Q$ には「減衰の遅さ」（問 2）と「共振の鋭さ」（問 5）という 2 つの顔があり、両者は同じ量である。** 大問 8（第 2-5 回）の LCR 直列共振はこの完全な電気的対応物で、$\omega_0=1/\sqrt{LC}$、$2\gamma = R/L$、$Q=(1/R)\sqrt{L/C}$ と読み替えられる。

---

## 8 ｜ 第 2-4 回　電磁気学（平行面電荷 / 面電流と A / LC）

**問 1（30 点）**

**(1)（15 点）** 対称性: 無限に広い一様な面電荷なので、$\boldsymbol E$ は面に垂直で、大きさは $|z|$ のみに依存し、面をはさんで逆向き（$z\to-z$ の鏡映対称性）。

面を貫く断面積 $S$ の円筒（両底面が面から等距離）をガウス面にとると、側面の寄与はゼロで

$$
2ES = \frac{\sigma S}{\varepsilon_0}\;\Longrightarrow\;\boxed{E = \frac{\sigma}{2\varepsilon_0}}\quad(\text{面から遠ざかる向き})
$$

**(2)（15 点）** 重ね合わせる。$+\sigma$ の面は外向き、$-\sigma$ の面は内向きの寄与を与える。

| 領域 | $E_z$ |
| --- | --- |
| $z<0$ | $-\dfrac{\sigma}{2\varepsilon_0}+\dfrac{\sigma}{2\varepsilon_0} = 0$ |
| $0<z<d$ | $+\dfrac{\sigma}{2\varepsilon_0}+\dfrac{\sigma}{2\varepsilon_0} = \dfrac{\sigma}{\varepsilon_0}$ |
| $z>d$ | $+\dfrac{\sigma}{2\varepsilon_0}-\dfrac{\sigma}{2\varepsilon_0} = 0$ |

**外部は完全に打ち消しあってゼロ**（平行板コンデンサーの基本性質）。$V(z) = -\int_0^zE_z\,dz'$ より

$$
\boxed{\;V(z) = \begin{cases} 0 & (z\le0)\\[2pt] -\dfrac{\sigma z}{\varepsilon_0} & (0\le z\le d)\\[6pt] -\dfrac{\sigma d}{\varepsilon_0} & (z\ge d)\end{cases}}
$$

極板間の電位差の大きさは $\sigma d/\varepsilon_0 = Qd/(\varepsilon_0S)$ で、$C = \varepsilon_0S/d$ と整合する（**検算**）。

**問 2（35 点）**

**(1)（18 点）** 対称性: $\boldsymbol B$ は面に平行で $\boldsymbol K$ に垂直、大きさは $|z|$ のみに依存し、面をはさんで逆向き。長方形のアンペール閉路（$yz$ 平面内、$z=\pm h$ に長さ $\ell$ の辺）をとると、$\ell$ 辺だけが寄与して

$$
2B\ell = \mu_0K\ell \;\Longrightarrow\; B = \frac{\mu_0K}{2}
$$

向きは $\boldsymbol B = \dfrac{\mu_0}{2}\boldsymbol K\times\hat{\boldsymbol n}$（$\hat{\boldsymbol n}$ は面から観測点へ向かう単位ベクトル）で決まる。

$$
\boxed{\;\boldsymbol B = -\frac{\mu_0K}{2}\hat{\boldsymbol y}\;(z>0),\qquad
\boldsymbol B = +\frac{\mu_0K}{2}\hat{\boldsymbol y}\;(z<0)\;}
$$

**(2)（17 点）** $\boldsymbol A$ は $\boldsymbol K$ と同じ $x$ 方向を向き、$z$ のみの関数と置ける: $\boldsymbol A = A_x(z)\hat{\boldsymbol x}$。このとき $\nabla\cdot\boldsymbol A = \partial A_x/\partial x = 0$ が自動的に満たされる。

$$
\nabla\times\boldsymbol A = \left(\partial_zA_x-\partial_xA_z\right)\hat{\boldsymbol y} = \frac{dA_x}{dz}\hat{\boldsymbol y} = \boldsymbol B
$$

$z>0$: $dA_x/dz = -\mu_0K/2$ より $A_x = -\mu_0Kz/2$。$z<0$: $dA_x/dz = +\mu_0K/2$ より $A_x = +\mu_0Kz/2$。$A_x(0)=0$ と合わせて

$$
\boxed{\;\boldsymbol A(z) = -\frac{\mu_0K|z|}{2}\hat{\boldsymbol x}\;}
$$

（**2026-08-30 訂正**: 旧版は $(\nabla\times\boldsymbol A)_y=-dA_x/dz$ と符号を誤り、$\boldsymbol A=+\mu_0K|z|/2\,\hat x$ としていた。
検算: 電流と同じ向きの $\boldsymbol A$ は電流から遠ざかるほど減る（無限直線電流の $A_x\propto-\ln r$ と同じ）。）

$\boldsymbol A$ は面上で連続だが、その微分は不連続（$\boldsymbol B$ の飛び $\mu_0K$ に対応）。これは面電荷に対する $V \propto -\sigma|z|/(2\varepsilon_0)$ と完全に平行な構造である。

**問 3（35 点）**

**(1)（15 点）** $L\dfrac{dI}{dt} + \dfrac QC = 0$、$I = -\dfrac{dQ}{dt}$（放電向きを正にとる）より $\ddot Q + \dfrac{Q}{LC} = 0$。

$$
\boxed{\;Q(t) = Q_0\cos\omega_0t,\qquad I(t) = -\frac{dQ}{dt}= Q_0\omega_0\sin\omega_0t,\qquad \omega_0 = \frac{1}{\sqrt{LC}}\;}
$$

**(2)（20 点）**

$$
U_E = \frac{Q^2}{2C} = \frac{Q_0^2}{2C}\cos^2\omega_0t,\qquad
U_B = \frac12LI^2 = \frac12LQ_0^2\omega_0^2\sin^2\omega_0t = \frac{Q_0^2}{2C}\sin^2\omega_0t
$$

（$L\omega_0^2 = 1/C$ を使った。）

$$
U_E+U_B = \frac{Q_0^2}{2C}\left(\cos^2+\sin^2\right) = \frac{Q_0^2}{2C} = \text{一定}\;\checkmark
$$

$\langle\cos^2\rangle = \langle\sin^2\rangle = 1/2$ だから

$$
\boxed{\;\langle U_E\rangle = \langle U_B\rangle = \frac{Q_0^2}{4C}\;}
$$

**エネルギーは電場と磁場の間を角振動数 $2\omega_0$ で往復し、平均は等分される。** 力学の $\tfrac12kx^2$ と $\tfrac12mv^2$ の対応（$Q\leftrightarrow x$、$L\leftrightarrow m$、$1/C\leftrightarrow k$）そのもの。

---

## 10 ｜ 第 2-4 回　統計力学（2 次元理想気体）

**問 1（18 点）** 面積 $A$ の 2 次元箱で、運動量の大きさが $p$ 以下の状態数は位相空間体積を $h^2$ で割って

$$
N(\varepsilon) = \frac{A\cdot\pi p^2}{h^2} = \frac{A\cdot\pi\cdot2m\varepsilon}{h^2}
$$

$$
\boxed{\;D(\varepsilon) = \frac{dN}{d\varepsilon} = \frac{2\pi mA}{h^2} = \frac{mA}{2\pi\hbar^2} = \text{一定}\;}
$$

3 次元では $N(\varepsilon)\propto V p^3 \propto V\varepsilon^{3/2}$ なので $D\propto\sqrt\varepsilon$。**次元 $d$ では $D(\varepsilon)\propto\varepsilon^{d/2-1}$ で、$d=2$ だけがちょうど定数になる。**

**問 2（20 点）**

$$
z = \int_0^\infty D(\varepsilon)e^{-\beta\varepsilon}d\varepsilon = \frac{2\pi mA}{h^2}\cdot k_BT
= \frac{A}{\lambda^2},\qquad \lambda = \frac{h}{\sqrt{2\pi mk_BT}}
$$

$$
Z = \frac{z^N}{N!},\qquad
F = -k_BT\ln Z = -Nk_BT\left[\ln\frac{A}{N\lambda^2} + 1\right]
$$

**問 3（22 点）** $\lambda^2\propto1/T$ なので、$F = -Nk_BT[\ln A - \ln N - \ln\lambda^2 + 1]$ で $A$ 依存性は $\ln A$ の項だけ。

$$
P = -\frac{\partial F}{\partial A} = \frac{Nk_BT}{A}\;\Longrightarrow\;\boxed{PA = Nk_BT}
$$

内部エネルギーは $\ln Z = N\ln(A/\lambda^2)-\ln N!$ で $\lambda^2\propto\beta$ だから $\ln Z = -N\ln\beta + \text{（$\beta$ によらない項）}$、

$$
U = -\frac{\partial\ln Z}{\partial\beta} = \frac N\beta = \boxed{Nk_BT},\qquad
\boxed{C_A = \left(\frac{\partial U}{\partial T}\right)_A = Nk_B}
$$

等分配則: 1 粒子の運動エネルギーは $\left(p_x^2+p_y^2\right)/2m$ で 2 次形式が 2 個。1 個あたり $\tfrac12k_BT$ で $U = 2\times\tfrac12Nk_BT = Nk_BT$ $\checkmark$（3 次元なら $\tfrac32Nk_BT$）。

**問 4（22 点）**

$$
S = -\frac{\partial F}{\partial T}
= Nk_B\left[\ln\frac{A}{N\lambda^2}+1\right] + Nk_BT\cdot\frac1T
= \boxed{\;Nk_B\left[\ln\frac{A}{N\lambda^2}+2\right]\;}
$$

（$\lambda^2\propto T^{-1}$ なので $\partial\ln\lambda^{-2}/\partial T = 1/T$ を使った。2 次元版のザックール–テトローデ式。）

$T\to0$ では $\lambda\to\infty$ より $\ln(A/N\lambda^2)\to-\infty$、すなわち $\boxed{S\to-\infty}$。

**これは熱力学第 3 法則（$T\to0$ で $S\to$ 有限値、通常 $0$）に反する。** エントロピーが負になること自体、$S=k_B\ln W$ で $W<1$ を意味するので物理的にありえない。

**原因**: 古典（マクスウェル–ボルツマン）近似が使えるのは、粒子の波束が重ならない条件 $A/(N\lambda^2)\gg1$（$d$ 次元では $n\lambda^d\ll1$）のときだけである。$T$ を下げると $\lambda$ が伸びて必ずこの条件が破れる。

**正しい扱い**: 低温では量子統計（ボース–アインシュタイン統計またはフェルミ–ディラック統計）で扱う。そうすると基底状態の縮退度で $S$ が決まり、$T\to0$ で $S\to0$（または残留エントロピー）となって第 3 法則が回復する。（2024 年度の大問 10 で「負のエントロピー」が問われたのと同じ論点。）

**問 5（18 点）** 励起状態にいる粒子数は $\mu\to0^-$ で最大になり、

$$
N_{\rm ex}^{\max} = \int_0^\infty \frac{D(\varepsilon)}{e^{\beta\varepsilon}-1}d\varepsilon
$$

**この積分が収束するかどうか**が凝縮の有無を決める。低エネルギー側では $e^{\beta\varepsilon}-1\simeq\beta\varepsilon$ なので、被積分関数は $D(\varepsilon)/(\beta\varepsilon)$ のように振る舞う。

- **3 次元**: $D\propto\varepsilon^{1/2}$ だから被積分関数 $\propto\varepsilon^{-1/2}$。$\int_0 \varepsilon^{-1/2}d\varepsilon$ は**収束**する。よって $N_{\rm ex}^{\max}$ が有限で、$N$ がこれを超えた分は基底状態に落ちるしかない ⟹ **ボース–アインシュタイン凝縮が起こる。**
- **2 次元**: $D = $ 一定だから被積分関数 $\propto\varepsilon^{-1}$。$\int_0 d\varepsilon/\varepsilon$ は**対数発散**する。$N_{\rm ex}^{\max} = \infty$ なので、どれだけ粒子を入れても励起状態が収容してしまい、**有限温度では凝縮が起こらない。**

要するに **2 次元は低エネルギー側の状態が「多すぎる」**（$D$ が $\varepsilon\to0$ でゼロに落ちない）ことが本質である。

---

## 7 ｜ 第 2-5 回　力学（台車の上の振り子）

**問 1（20 点）** おもりの位置は $(x+\ell\sin\theta,\ -\ell\cos\theta)$、速度は $(\dot x+\ell\dot\theta\cos\theta,\ \ell\dot\theta\sin\theta)$ だから

$$
v_m^2 = \dot x^2 + 2\ell\dot x\dot\theta\cos\theta + \ell^2\dot\theta^2
$$

$$
\boxed{\;L = \frac12M\dot x^2 + \frac12m\left(\dot x^2+2\ell\dot x\dot\theta\cos\theta+\ell^2\dot\theta^2\right) + mg\ell\cos\theta\;}
$$

（位置エネルギーは支点を基準に $-mg\ell\cos\theta$。）

**問 2（15 点）** $L$ には $x$ が現れず $\dot x$ しか現れない（水平方向に一様）から $x$ は循環座標で

$$
p_x = \frac{\partial L}{\partial\dot x} = \boxed{(M+m)\dot x + m\ell\dot\theta\cos\theta = \text{一定}}
$$

これは**系全体の水平方向の運動量**である。床がなめらかで水平方向に外力がはたらかないから保存する。とくに初め静止していたなら $p_x=0$ で、おもりが右へ振れると台車は左へ動き、系の重心の水平位置は動かない。

**問 3（30 点）** $\cos\theta\simeq1$、$\sin\theta\simeq\theta$、$\dot\theta^2$ の項を落として線形化する。

$x$ の式（$p_x$ の保存を微分しても同じ）:

$$
(M+m)\ddot x + m\ell\ddot\theta = 0 \;\Longrightarrow\; \ddot x = -\frac{m\ell}{M+m}\ddot\theta \tag{i}
$$

$\theta$ の式: $\dfrac{d}{dt}\left(m\ell\dot x\cos\theta+m\ell^2\dot\theta\right) = -m\ell\dot x\dot\theta\sin\theta - mg\ell\sin\theta$ を線形化して

$$
\ell\ddot\theta + \ddot x + g\theta = 0 \tag{ii}
$$

(i) を (ii) に代入すると

$$
\ell\ddot\theta\left(1-\frac{m}{M+m}\right) + g\theta = 0
\;\Longrightarrow\;
\frac{M\ell}{M+m}\ddot\theta + g\theta = 0
$$

$$
\boxed{\;\omega = \sqrt{\frac{(M+m)g}{M\ell}}\;}
$$

**問 4（20 点）**

- **$M\to\infty$**: $\omega\to\sqrt{g/\ell}$。台車が重すぎて動かないので、**支点が固定された普通の単振り子**になる。$\checkmark$（この極限が出ないなら式が間違っている。）
- **$M\to0$**: $\omega\to\infty$。台車が軽いと、水平運動量保存のためにおもりはほとんど動かず、代わりに台車が大きく振られる。復元力に対して系の実効的な慣性がいくらでも小さくなるので、振動は無限に速くなる。

**問 5（15 点）** $\omega^2 = g/L_{\rm eff}$ と置くと

$$
\boxed{\;L_{\rm eff} = \frac{M\ell}{M+m} = \frac{\ell}{1+m/M}\;}
$$

$M\to\infty$ で $L_{\rm eff}\to\ell$ $\checkmark$。$L_{\rm eff}<\ell$ が常に成り立つ（支点が逃げる分だけ「短い振り子」として振る舞う）。$\ell$ は換算質量 $\mu = Mm/(M+m)$ を使って $L_{\rm eff} = (\mu/m)\ell$ とも書ける。

---

## 8 ｜ 第 2-5 回　電磁気学（誘電体球殻 / ヘルムホルツコイル / LCR 共振）

**問 1（35 点）**

**(1)（20 点）** 球対称なので $\boldsymbol D$ にガウスの法則を適用する（自由電荷だけが源）。$r>a$ の全領域で

$$
D(r)\cdot4\pi r^2 = Q\;\Longrightarrow\;\boxed{D(r) = \frac{Q}{4\pi r^2}}
$$

$$
E(r) = \frac{D}{\varepsilon} = \boxed{\frac{Q}{4\pi\varepsilon r^2}}\;(a<r<b),\qquad
E(r) = \boxed{\frac{Q}{4\pi\varepsilon_0r^2}}\;(r>b),\qquad E=0\;(r<a)
$$

$$
V(a) = \int_a^bE\,dr + \int_b^\infty E\,dr
= \boxed{\;\frac{Q}{4\pi\varepsilon}\left(\frac1a-\frac1b\right) + \frac{Q}{4\pi\varepsilon_0b}\;}
$$

$$
\boxed{\;C = \frac{Q}{V(a)} = \frac{4\pi}{\dfrac1\varepsilon\left(\dfrac1a-\dfrac1b\right)+\dfrac{1}{\varepsilon_0b}}\;}
$$

検算: $\varepsilon=\varepsilon_0$ なら $C = 4\pi\varepsilon_0a$（孤立導体球）。$b\to\infty$ なら $C = 4\pi\varepsilon a$。

**(2)（15 点）** 誘電体中の分極は $\boldsymbol P = \boldsymbol D - \varepsilon_0\boldsymbol E = \left(1-\dfrac{\varepsilon_0}{\varepsilon}\right)\dfrac{Q}{4\pi r^2}\hat{\boldsymbol r}$。束縛電荷面密度は $\sigma_b = \boldsymbol P\cdot\hat{\boldsymbol n}$（$\hat{\boldsymbol n}$ は誘電体から外へ向かう法線）。

- $r=a$（法線は $-\hat{\boldsymbol r}$）: $\displaystyle \boxed{\sigma_b(a) = -\left(1-\frac{\varepsilon_0}{\varepsilon}\right)\frac{Q}{4\pi a^2}}\;(<0)$
- $r=b$（法線は $+\hat{\boldsymbol r}$）: $\displaystyle \boxed{\sigma_b(b) = +\left(1-\frac{\varepsilon_0}{\varepsilon}\right)\frac{Q}{4\pi b^2}}\;(>0)$

**総和の検算**:

$$
\sigma_b(a)\cdot4\pi a^2 + \sigma_b(b)\cdot4\pi b^2
= -\left(1-\frac{\varepsilon_0}{\varepsilon}\right)Q + \left(1-\frac{\varepsilon_0}{\varepsilon}\right)Q = 0\;\checkmark
$$

（誘電体は中性なので当然そうならなければならない。**$a^2$ と $b^2$ が正しく効いているかの検算になる。**）
$\varepsilon\to\varepsilon_0$ で括弧が $0$ になり両方消える $\checkmark$。

**問 2（30 点）**

**(1)（15 点）** 円形コイルの微小部分 $Id\boldsymbol l$ が作る $d\boldsymbol B$ は大きさ $\dfrac{\mu_0I\,dl}{4\pi(a^2+z^2)}$。1 周まわると軸に垂直な成分は打ち消し、軸方向成分だけが残る。その割合は $\dfrac{a}{\sqrt{a^2+z^2}}$ だから

$$
B(z) = \frac{\mu_0I}{4\pi(a^2+z^2)}\cdot\frac{a}{\sqrt{a^2+z^2}}\cdot2\pi a
= \boxed{\;\frac{\mu_0Ia^2}{2\left(a^2+z^2\right)^{3/2}}\;}
$$

$z=0$ で $\mu_0I/2a$、$z\gg a$ で $\mu_0(I\pi a^2)/(2\pi z^3) = \mu_0m/(2\pi z^3)$（磁気双極子）$\checkmark$

**(2)（15 点）** 中点を原点、コイルを $z=\pm d/2$ に置く。$f(u) \equiv \dfrac{\mu_0Ia^2}{2}\left(a^2+u^2\right)^{-3/2}$ として

$$
B(z) = f\left(z-\tfrac d2\right) + f\left(z+\tfrac d2\right)
$$

配置が $z\to-z$ で対称なので奇数階微分は中点で自動的に $0$。2 階微分は

$$
\frac{d^2}{du^2}\left(a^2+u^2\right)^{-3/2}
= -3\left(a^2+u^2\right)^{-5/2} + 15u^2\left(a^2+u^2\right)^{-7/2}
= 3\left(a^2+u^2\right)^{-7/2}\left(4u^2-a^2\right)
$$

$$
B''(0) = 2f''\!\left(\tfrac d2\right) = 0
\;\Longleftrightarrow\; 4\left(\frac d2\right)^2 = a^2
\;\Longleftrightarrow\; \boxed{\;d = a\;}
$$

🔴 **問われているのは間隔 $d$ である。$z=a/2$（コイルの位置）で止めてはいけない。** 「コイルの間隔をコイルの半径に等しくとる」がヘルムホルツ配置で、このとき中点付近で $B$ は 3 次まで平坦になり、$B(0) = \dfrac{8\mu_0I}{5\sqrt5\,a}$ の一様磁場が得られる。

**問 3（35 点）**

**(1)（12 点）**

$$
\boxed{\;|Z| = \sqrt{R^2+\left(\omega L-\frac{1}{\omega C}\right)^2}\;},\qquad
\boxed{\;\tan\varphi = \frac{\omega L - 1/(\omega C)}{R}\;}
$$

電流振幅 $V_0/|Z|$ が最大 ⟺ $|Z|$ が最小。$R$ は $\omega$ によらないので、**リアクタンス項の 2 乗が $0$ になるとき**。

$$
\omega L = \frac{1}{\omega C}\;\Longrightarrow\;\boxed{\omega_0 = \frac{1}{\sqrt{LC}}}
$$

（「$R^2+(\omega L-1/\omega C)^2=0$」は $R\ne0$ では成り立たない偽の式。**「第 2 項が $0$ で $|Z|$ が最小」と書くこと。**）

**(2)（10 点）** 電流は $I(t) = \dfrac{V_0}{|Z|}\cos(\omega t-\varphi)$。平均電力は抵抗での消費に等しく

$$
\bar P(\omega) = \frac12\frac{V_0^2}{|Z|^2}R
= \boxed{\;\frac{V_0^2R}{2\left[R^2+\left(\omega L-1/\omega C\right)^2\right]}\;},\qquad
\bar P(\omega_0) = \boxed{\frac{V_0^2}{2R}}
$$

**(3)（13 点）** $\bar P = \bar P_{\max}/2$ となるのは分母が 2 倍、すなわち

$$
\left(\omega L-\frac{1}{\omega C}\right)^2 = R^2 \;\Longleftrightarrow\; \omega L - \frac{1}{\omega C} = \pm R
$$

$$
L\omega^2 \mp R\omega - \frac1C = 0
\;\Longrightarrow\;
\omega = \frac{\pm R + \sqrt{R^2 + 4L/C}}{2L}\quad(\text{正の根})
$$

**判別式は $\sqrt{R^2+4L/C}$。**（次元は $[R^2]=\Omega^2$、$[L/C]=\mathrm{H/F}=\Omega^2$ で一致する。$\sqrt{L^2R^2+4LC}$ のような形が出たらその場で棄却できる。）

2 つの正の根の差は平方根の項が消えて**厳密に**

$$
\boxed{\;\Delta\omega = \omega_+-\omega_- = \frac{2R}{2L} = \frac RL\;}
$$

$$
\boxed{\;Q = \frac{\omega_0}{\Delta\omega} = \frac{1}{\sqrt{LC}}\cdot\frac LR = \frac1R\sqrt{\frac LC}\;}
$$

$R$ が小さいほど共振は鋭い。力学の減衰強制振動（第 2-4 回 問 5）と同じ構造で、$2\gamma\leftrightarrow R/L$ の対応。

---

## 10 ｜ 第 2-5 回　統計力学（スピン 1 の常磁性・断熱消磁）

**問 1（12 点）** エネルギーは $E = -m\mu B$（$m=-1,0,+1$）。$x = \mu B/(k_BT) = \beta\mu B$ とおくと

$$
z = e^{x} + 1 + e^{-x} = \boxed{1+2\cosh x}
$$

検算: $x\to0$ で $z\to3$（3 状態が等確率）$\checkmark$

**問 2（20 点）** 1 個あたりの平均磁気モーメントは $\mu\langle m\rangle = \dfrac1\beta\dfrac{\partial\ln z}{\partial B}$。

$$
\boxed{\;M_z = N\mu\,\frac{2\sinh x}{1+2\cosh x}\;}
$$

- **飽和磁化**: $x\to\infty$ で $2\sinh x/(1+2\cosh x)\to1$、すなわち $\boxed{M_z\to N\mu}$。
  全モーメントが $m=+1$ に揃った状態で、**$M_z$ がこれを超えたら計算間違い**（$0\le M_z\le N\mu$）。
- **高温**（$x\ll1$）: $\sinh x\simeq x$、$\cosh x\simeq1$ より $M_z \simeq \dfrac{2}{3}N\mu x = \dfrac{2N\mu^2B}{3k_BT}$。

$$
\boxed{\;\chi = \frac{\partial M_z}{\partial B} = \frac{2N\mu^2}{3k_BT} = \frac{C_{\rm Curie}}{T}\;},\qquad
C_{\rm Curie} = \frac{2N\mu^2}{3k_B}
$$

**キュリーの法則** $\chi\propto1/T$。一般の $J$ に対する $\chi = N\mu^2J(J+1)\big/(3k_BT)$ で $J=1$、$J(J+1)=2$ とした場合に一致する（**検算**）。

**問 3（25 点）** $f(x)\equiv\dfrac{2\sinh x}{1+2\cosh x}$ とおくと $U = -N\mu B f(x) = -Nk_BT\,x f(x)$。

$$
\boxed{\;U = -N\mu B\,\frac{2\sinh x}{1+2\cosh x}\;}
$$

$C = dU/dT$ で $dx/dT = -x/T$ を使うと $C = Nk_Bx^2f'(x)$。

$$
f'(x) = \frac{2\cosh x\left(1+2\cosh x\right) - 4\sinh^2x}{\left(1+2\cosh x\right)^2}
= \frac{2\cosh x + 4}{\left(1+2\cosh x\right)^2}
$$

（$4\cosh^2x-4\sinh^2x = 4$ を使った。）

$$
\boxed{\;C = Nk_B\,x^2\,\frac{2\cosh x+4}{\left(1+2\cosh x\right)^2}\;}
$$

- **高温**（$x\ll1$）: $\cosh x\to1$ より $C\simeq \dfrac69Nk_Bx^2 = \boxed{\dfrac23Nk_B\left(\dfrac{\mu B}{k_BT}\right)^2\propto\dfrac{1}{T^2}}$（べき）
- **低温**（$x\gg1$）: $\cosh x\simeq e^x/2$ より分子 $\simeq e^x$、分母 $\simeq e^{2x}$、$\boxed{C\simeq Nk_Bx^2e^{-x}}$（指数）

ギャップ $\mu B$ をもつ離散準位系なので、ショットキー型の山になる。

**問 4（25 点）** $F = -Nk_BT\ln\left(1+2\cosh x\right)$、$S = (U-F)/T$ より

$$
\boxed{\;S = Nk_B\left[\ln\left(1+2\cosh x\right) - \frac{2x\sinh x}{1+2\cosh x}\right]\;}
$$

**$S$ は $x = \mu B/(k_BT)$ だけの関数である。** $\mu$ と $k_B$ は定数だから、**$S$ は比 $B/T$ のみの関数**であり、$B$ と $T$ を同じ割合で変えても $S$ は変わらない。（この 1 行が断熱消磁の全根拠なので、必ず書くこと。）

- $T\to\infty$（$x\to0$）: $\ln3 - 0$、すなわち $\boxed{S\to Nk_B\ln3}$。各モーメントが 3 状態を等確率でとるので $W = 3^N$、$S = k_B\ln W = Nk_B\ln3$ $\checkmark$
- $T\to0$（$x\to\infty$）: $\ln(1+2\cosh x)\simeq x + e^{-x}$、$\dfrac{2\sinh x}{1+2\cosh x}\simeq1-e^{-x}$ より

$$
S \simeq Nk_B\left[x+e^{-x} - x\left(1-e^{-x}\right)\right] = Nk_B(1+x)e^{-x}\to \boxed{0}
$$

基底状態は $m=+1$ の 1 通りだけなので $W=1$、$S=0$。**第 3 法則と整合。**

**問 5（18 点）** 断熱かつ準静的な変化ではエントロピーが一定。問 4 より $S$ は $B/T$ のみの関数だから、$S$ 一定は $B/T$ 一定を意味する。

$$
\frac{B_1}{T_1} = \frac{B_2}{T_2} \;\Longrightarrow\; \boxed{\;T_2 = T_1\frac{B_2}{B_1}\;}
$$

$B_2$ を小さくするほど低温が得られる（**断熱消磁**。等温磁化 → 断熱消磁の 2 段階でミリケルビン領域に到達できる）。

**下限を決めているもの**: 実際のスピン系にはスピン間の双極子相互作用や交換相互作用があり、外部磁場を $0$ にしても各スピンは他のスピンが作る**内部磁場 $B_{\rm int}$** を感じている。したがって実効的な磁場は $B_{\rm int}$ より小さくできず、到達温度は

$$
T_{\min} \sim T_1\frac{B_{\rm int}}{B_1}
$$

程度で頭打ちになる。**$B_{\rm int}$ の小さい（希薄な）常磁性塩を選ぶことが、より低温に到達するための条件である。** また $T$ が $B_{\rm int}$ に対応する温度を下回るとスピン系自身が秩序化し（自発磁化）、エントロピーが失われて冷却能力がなくなる。

---

## 7 ｜ 第 2-6 回　力学（滑り落ちる棒）

**問 1（18 点）** 上端は壁（$x=0$）に、下端は床（$y=0$）に接している。棒と壁のなす角が $\theta$ なので、上端は $(0,\ 2\ell\cos\theta)$、下端は $(2\ell\sin\theta,\ 0)$。重心は中点だから

$$
\boxed{\;\boldsymbol r_G = \left(\ell\sin\theta,\ \ell\cos\theta\right)\;}
$$

$$
\left|\boldsymbol r_G\right|^2 = \ell^2\left(\sin^2\theta+\cos^2\theta\right) = \ell^2 = \text{一定}
$$

**よって重心は原点を中心とする半径 $\ell$ の円周上を動く。** （直角三角形の斜辺の中点は直角の頂点から常に等距離、という初等幾何そのもの。）

**問 2（17 点）** 長さ $2\ell$ の一様な棒の、重心を通り棒に垂直な軸のまわりの慣性モーメントは

$$
I_G = \int_{-\ell}^{\ell}s^2\frac{M}{2\ell}ds = \frac{M}{2\ell}\cdot\frac{2\ell^3}{3} = \boxed{\frac13M\ell^2}
$$

（$M(2\ell)^2/12 = M\ell^2/3$ と同じ。$I_G\le M\ell^2$ を満たす $\checkmark$）

重心速度は $v_G = \ell|\dot\theta|$（半径 $\ell$ の円運動）。棒の向きの角も $\theta$ なので角速度は $\dot\theta$。

$$
K = \frac12Mv_G^2 + \frac12I_G\dot\theta^2
= \frac12M\ell^2\dot\theta^2 + \frac16M\ell^2\dot\theta^2
= \boxed{\;\frac23M\ell^2\dot\theta^2\;}
$$

**問 3（20 点）** 壁も床もなめらかなので摩擦による散逸はなく、力学的エネルギーが保存する。重心の高さは $\ell\cos\theta$、初期状態は $\theta\simeq0$、$\dot\theta=0$。

$$
\frac23M\ell^2\dot\theta^2 + Mg\ell\cos\theta = Mg\ell
$$

$$
\boxed{\;\dot\theta^2 = \frac{3g}{2\ell}\left(1-\cos\theta\right)\;}
$$

（次元: $[g/\ell] = \mathrm{s^{-2}}$ $\checkmark$。$\theta$ が増えるほど $\dot\theta$ が増える。）

**問 4（25 点）** 壁が棒に及ぼす垂直抗力を $N_w$（$+x$ 方向）とすると、重心の $x$ 方向の運動方程式は

$$
N_w = M\ddot x_G,\qquad x_G = \ell\sin\theta
$$

問 3 を $\theta$ で微分して $2\dot\theta\ddot\theta = \dfrac{3g}{2\ell}\sin\theta\,\dot\theta$、すなわち

$$
\ddot\theta = \frac{3g}{4\ell}\sin\theta
$$

$$
\dot x_G = \ell\cos\theta\,\dot\theta,\qquad
\ddot x_G = \ell\left(\cos\theta\,\ddot\theta - \sin\theta\,\dot\theta^2\right)
$$

$$
\ddot x_G = \ell\left[\cos\theta\cdot\frac{3g}{4\ell}\sin\theta - \sin\theta\cdot\frac{3g}{2\ell}\left(1-\cos\theta\right)\right]
= \frac{3g}{4}\sin\theta\left(3\cos\theta-2\right)
$$

棒が壁から離れるのは $N_w=0$、すなわち $\ddot x_G = 0$ になるとき（$\sin\theta\ne0$ より）

$$
\boxed{\;\cos\theta_c = \frac23,\qquad \theta_c = \arccos\frac23 \simeq 48.2^\circ\;}
$$

（$\ell$ にも $g$ にも $M$ にもよらない。**離れる角は棒の長さや重さと無関係**というのがこの問題の見どころ。）

**問 5（20 点）** $\cos\theta_c = 2/3$ を問 3 に入れると

$$
\dot\theta_c^2 = \frac{3g}{2\ell}\left(1-\frac23\right) = \frac{g}{2\ell}
$$

$$
\boxed{\;v_G = \ell\dot\theta_c = \ell\sqrt{\frac{g}{2\ell}} = \sqrt{\frac{g\ell}{2}}\;}
$$

**離れたあとの運動**: 壁からの力がなくなり、床はなめらかなので床からの垂直抗力は鉛直方向のみ。したがって**水平方向には力がはたらかず、重心の水平速度は一定に保たれる**。

$$
\dot x_G\big|_{\theta_c} = \ell\cos\theta_c\,\dot\theta_c = \frac23\ell\sqrt{\frac{g}{2\ell}} = \frac23\sqrt{\frac{g\ell}{2}} = \text{一定}
$$

重心は鉛直方向にだけ加速されながら水平方向には等速で進む（床に着くまでは垂直抗力があるので自由落下ではない）。棒自身は一定の角速度ではなく、回転しながら倒れていく。

---

## 8 ｜ 第 2-6 回　電磁気学（一様帯電球 / 同軸ケーブル / 電磁波）

**問 1（35 点）**

**(1)（18 点）** 電荷密度は $\rho = \dfrac{Q}{\frac43\pi a^3} = \dfrac{3Q}{4\pi a^3}$。球対称なので半径 $r$ の球面をガウス面にとる。

$$
r<a:\;E\cdot4\pi r^2 = \frac{1}{\varepsilon_0}\rho\cdot\frac43\pi r^3 \;\Rightarrow\; \boxed{E = \frac{Qr}{4\pi\varepsilon_0a^3}},\qquad
r>a:\;\boxed{E = \frac{Q}{4\pi\varepsilon_0r^2}}
$$

電位は $V(r) = \displaystyle\int_r^\infty E\,dr'$。

$$
r>a:\;\boxed{V = \frac{Q}{4\pi\varepsilon_0r}}
$$

$$
r<a:\;V = \int_r^a\frac{Qr'}{4\pi\varepsilon_0a^3}dr' + \frac{Q}{4\pi\varepsilon_0a}
= \frac{Q\left(a^2-r^2\right)}{8\pi\varepsilon_0a^3} + \frac{Q}{4\pi\varepsilon_0a}
= \boxed{\frac{Q\left(3a^2-r^2\right)}{8\pi\varepsilon_0a^3}}
$$

検算: $r=a$ で両式とも $Q/(4\pi\varepsilon_0a)$。中心では $\dfrac{3Q}{8\pi\varepsilon_0a} = \dfrac32V(a)$。

**(2)（17 点）**

$$
U = \int\frac{\varepsilon_0E^2}{2}dV = \int_0^\infty\frac{\varepsilon_0E^2}{2}4\pi r^2dr
$$

**外部**（$r>a$）:

$$
U_{\rm out} = \frac{\varepsilon_0}{2}\left(\frac{Q}{4\pi\varepsilon_0}\right)^2 4\pi\int_a^\infty\frac{dr}{r^2}
= \frac{Q^2}{8\pi\varepsilon_0}\cdot\frac1a = \frac{Q^2}{8\pi\varepsilon_0a}
$$

**内部**（$r<a$）:

$$
U_{\rm in} = \frac{\varepsilon_0}{2}\left(\frac{Q}{4\pi\varepsilon_0a^3}\right)^2 4\pi\int_0^a r^4dr
= \frac{Q^2}{8\pi\varepsilon_0a^6}\cdot\frac{a^5}{5} = \frac{Q^2}{40\pi\varepsilon_0a}
$$

（$\int_0^ar^4dr = a^5/5$。**原始関数の次数を落とさないこと。**）

$$
\boxed{\;U = U_{\rm in}+U_{\rm out} = \frac{Q^2}{8\pi\varepsilon_0a}\left(1+\frac15\right) = \frac{3Q^2}{20\pi\varepsilon_0a}\;}
$$

内部の寄与は全体の $1/6$。表面に電荷を集めた球殻の場合は $Q^2/(8\pi\varepsilon_0a)$ で、一様球のほうが $6/5$ 倍だけ大きい（内側に詰め込む分の仕事が余分にかかる）。

**問 2（30 点）**

**(1)（18 点）** アンペールの法則より $a<r<b$ で $B = \dfrac{\mu_0I}{2\pi r}$（外導体の外では内外の電流が打ち消して $B=0$）。

$$
\frac W\ell = \int_a^b\frac{B^2}{2\mu_0}2\pi r\,dr
= \frac{\mu_0I^2}{4\pi}\int_a^b\frac{dr}{r} = \frac{\mu_0I^2}{4\pi}\ln\frac ba
$$

$W = \tfrac12LI^2$ と比べて

$$
\boxed{\;\frac L\ell = \frac{\mu_0}{2\pi}\ln\frac ba\;}
$$

**(2)（12 点）** 第 2-2 回 問 2 と同じ計算で、内導体内部（一様電流）の寄与は

$$
\boxed{\;\frac{\Delta L}{\ell} = \frac{\mu_0}{8\pi}\;}
$$

$a$ にも $b$ にもよらない定数。実用的な同軸ケーブル（$b/a\sim3$）では $\ln(b/a)/2\pi\simeq0.17$、$1/8\pi\simeq0.04$ なので、内部寄与は全体の約 2 割にあたる（無視できない）。

**問 3（35 点）**

**(1)（18 点）** 真空中（$\rho=0$, $\boldsymbol j=0$）のマクスウェル方程式は

$$
\nabla\cdot\boldsymbol E=0,\quad \nabla\cdot\boldsymbol B=0,\quad
\nabla\times\boldsymbol E = -\frac{\partial\boldsymbol B}{\partial t},\quad
\nabla\times\boldsymbol B = \varepsilon_0\mu_0\frac{\partial\boldsymbol E}{\partial t}
$$

第 3 式の回転をとり、ベクトル公式 $\nabla\times(\nabla\times\boldsymbol E) = \nabla(\nabla\cdot\boldsymbol E) - \nabla^2\boldsymbol E$ と第 1 式を使うと

$$
-\nabla^2\boldsymbol E = -\frac{\partial}{\partial t}\left(\nabla\times\boldsymbol B\right)
= -\varepsilon_0\mu_0\frac{\partial^2\boldsymbol E}{\partial t^2}
$$

$$
\boxed{\;\nabla^2\boldsymbol E = \varepsilon_0\mu_0\frac{\partial^2\boldsymbol E}{\partial t^2}\;}
$$

これは位相速度 $v$ の波動方程式 $\nabla^2\boldsymbol E = v^{-2}\partial_t^2\boldsymbol E$ の形だから

$$
\boxed{\;v = \frac{1}{\sqrt{\varepsilon_0\mu_0}} = c \simeq 3.00\times10^8\ \mathrm{m/s}\;}
$$

**(2)（17 点）** $\nabla\times\boldsymbol E = -\partial\boldsymbol B/\partial t$ に $\boldsymbol E = E_0\cos(kz-\omega t)\hat{\boldsymbol x}$ を入れる。

$$
\nabla\times\boldsymbol E = \frac{\partial E_x}{\partial z}\hat{\boldsymbol y} = -kE_0\sin(kz-\omega t)\hat{\boldsymbol y}
$$

$$
\frac{\partial\boldsymbol B}{\partial t} = kE_0\sin(kz-\omega t)\hat{\boldsymbol y}
\;\Longrightarrow\;
\boxed{\;\boldsymbol B = \frac{kE_0}{\omega}\cos(kz-\omega t)\hat{\boldsymbol y} = \frac{E_0}{c}\cos(kz-\omega t)\hat{\boldsymbol y}\;}
$$

$\boldsymbol E \perp \boldsymbol B \perp \hat{\boldsymbol z}$ で、$\boldsymbol E\times\boldsymbol B$ が進行方向 $+z$ を向く（$\hat{\boldsymbol x}\times\hat{\boldsymbol y} = \hat{\boldsymbol z}$ $\checkmark$）。

$$
\boldsymbol S = \frac{\boldsymbol E\times\boldsymbol B}{\mu_0} = \frac{E_0^2}{\mu_0c}\cos^2(kz-\omega t)\hat{\boldsymbol z}
$$

$$
\boxed{\;\left|\langle\boldsymbol S\rangle\right| = \frac{E_0^2}{2\mu_0c} = \frac12\varepsilon_0cE_0^2\;}
$$

（$\langle\cos^2\rangle=1/2$、$1/(\mu_0c) = \varepsilon_0c$ を使った。次元は W/m² $\checkmark$）

---

## 10 ｜ 第 2-6 回　統計力学（光子気体の熱力学）

**問 1（18 点）** 体積 $V$ の箱で、波数の大きさが $k$ 以下のモード数は偏光 2 種を含めて

$$
N(k) = 2\cdot\frac{V\cdot\frac43\pi k^3}{(2\pi)^3} = \frac{Vk^3}{3\pi^2}
$$

$k = \omega/c$ を代入して微分すると

$$
\boxed{\;D(\omega)\,d\omega = \frac{V\omega^2}{\pi^2c^3}\,d\omega\;}
$$

**$\mu=0$ の理由**: 光子は空洞の壁で吸収・放出され、**粒子数が保存しない**。粒子数が自由に変わる系では、平衡条件は自由エネルギーが $N$ について極小、すなわち $\mu = (\partial F/\partial N)_{T,V} = 0$ である。（保存量でないものに対する化学ポテンシャルは意味をもたない。）

**問 2（20 点）** 光子はボース粒子で $\mu=0$ だから、モードあたりの平均光子数は $\langle n\rangle = \dfrac{1}{e^{\beta\hbar\omega}-1}$（プランク分布）。

$$
U = \int_0^\infty \hbar\omega\,D(\omega)\,\frac{d\omega}{e^{\beta\hbar\omega}-1}
= \frac{V\hbar}{\pi^2c^3}\int_0^\infty\frac{\omega^3\,d\omega}{e^{\beta\hbar\omega}-1}
$$

$x = \beta\hbar\omega$ と置換すると $\omega^3d\omega = x^3dx/(\beta\hbar)^4$ だから

$$
U = \frac{V\hbar}{\pi^2c^3}\left(\frac{k_BT}{\hbar}\right)^4\cdot\frac{\pi^4}{15}
= \boxed{\;\frac{\pi^2k_B^4}{15\hbar^3c^3}\,VT^4 \equiv aVT^4\;},\qquad
\boxed{a = \frac{\pi^2k_B^4}{15\hbar^3c^3}}
$$

**シュテファン–ボルツマンの $T^4$ 則。** （放射強度は $\sigma T^4$、$\sigma = ac/4$。）

**問 3（27 点）** ボース系の自由エネルギーは（$\mu=0$）

$$
F = k_BT\int_0^\infty D(\omega)\ln\left(1-e^{-\beta\hbar\omega}\right)d\omega
= \frac{k_BTV}{\pi^2c^3}\int_0^\infty\omega^2\ln\left(1-e^{-\beta\hbar\omega}\right)d\omega
$$

$\int\omega^2d\omega = \omega^3/3$ を使って部分積分する。境界項は $\omega\to0$（$\omega^3\ln\omega\to0$）でも $\omega\to\infty$（指数で落ちる）でも消える。

$$
F = -\frac{k_BTV}{\pi^2c^3}\int_0^\infty\frac{\omega^3}{3}\cdot\frac{\beta\hbar e^{-\beta\hbar\omega}}{1-e^{-\beta\hbar\omega}}d\omega
= -\frac13\cdot\frac{V\hbar}{\pi^2c^3}\int_0^\infty\frac{\omega^3d\omega}{e^{\beta\hbar\omega}-1}
$$

$$
\boxed{\;F = -\frac U3 = -\frac13aVT^4\;}
$$

$$
\boxed{\;P = -\left(\frac{\partial F}{\partial V}\right)_T = \frac13aT^4 = \frac{U}{3V}\;}
$$

$$
\boxed{\;S = -\left(\frac{\partial F}{\partial T}\right)_V = \frac43aVT^3 = \frac{4U}{3T}\;}
$$

**検算**: $F = U-TS = aVT^4 - \tfrac43aVT^4 = -\tfrac13aVT^4$ $\checkmark$
$P = U/3V$ は超相対論的な気体に共通の状態方程式（非相対論的単原子分子気体の $P=2U/3V$ と対比せよ）。

**問 4（20 点）**

$$
\boxed{\;C_V = \left(\frac{\partial U}{\partial T}\right)_V = 4aVT^3 = \frac{4U}{T} = 3S\;}
$$

（$T\to0$ で $C_V\to0$。第 3 法則と整合 $\checkmark$）

断熱・準静的な変化では $S$ が一定だから、$S = \tfrac43aVT^3$ より

$$
\boxed{\;VT^3 = \text{一定}\;}
$$

（$P\propto T^4$ と合わせると $PV^{4/3} = $ 一定。光子気体のポアソンの関係で、比熱比にあたる指数は $4/3$。）
膨張する宇宙で $V\propto R^3$ とすれば $T\propto1/R$ となり、宇宙マイクロ波背景放射の温度が膨張とともに下がることに対応する。

**問 5（15 点）** $d$ 次元では、波数空間の球殻の体積が $\propto k^{d-1}dk$ になる。偏光 1 種として

$$
D(\omega) \propto V_d\,k^{d-1}\frac{dk}{d\omega} \propto V_d\,\omega^{d-1}
$$

$$
U = \int_0^\infty\hbar\omega\,D(\omega)\frac{d\omega}{e^{\beta\hbar\omega}-1}
\propto V_d\int_0^\infty\frac{\omega^{d}\,d\omega}{e^{\beta\hbar\omega}-1}
$$

$x = \beta\hbar\omega$ と置くと $\omega^dd\omega \to x^ddx/(\beta\hbar)^{d+1}$ で、残る積分 $\int_0^\infty x^d/(e^x-1)dx$ は $d>0$ で収束する定数。したがって

$$
\boxed{\;U \propto V_d\,T^{\,d+1}\;}
$$

- $d=3$: $U\propto VT^4$ $\checkmark$（問 2 と一致）
- **$d=2$: $\boxed{U\propto A\,T^3}$**（面積 $A$ の 2 次元空洞では $T$ の 3 乗）
- $d=1$: $U\propto LT^2$

**本質は「状態密度のべき」である。** $D(\omega)\propto\omega^{d-1}$ の指数がそのまま $T$ のべきに 1 を足した形で現れる。低次元ほど高振動数モードが少ないので、温度依存性は緩くなる。
（同じ論法はデバイ模型の低温比熱にも使え、$d$ 次元で $C\propto T^d$ を与える。）

---

## 付録: この 6 回で意図的に仕込んだ「検算が効く箇所」

| 回 | 科目 | 検算 | 見逃すと |
| --- | --- | --- | --- |
| 2-1 | 力学 問 2 | 引力なら $U=-k/r$。$+k/r$ だと $U_{\rm eff}$ に極小がない | 問 2 の $r_0$ と図が矛盾する |
| 2-1 | 電磁気 問 3-2 | $CV_0^2 = \tfrac12CV_0^2+\tfrac12CV_0^2$ | エネルギー保存が破れる |
| 2-1 | 統計 問 4 | $0\le S\le Nk_B\ln(1+g)$ | 上限を超える |
| 2-2 | 力学 問 1 | $I\le Ma^2$、$\int_0^hz^4dz = h^5/5$ | $(5/2)Ma^2$ 型の誤り |
| 2-2 | 電磁気 問 3-2 | $[LV_0^2/R^2]=\mathrm J$ | $V_0$ の 1 乗で書く誤り |
| 2-2 | 統計 問 4 | $(e^x-1)^2 \ne (e^{x/2}-e^{-x/2})^2$ | 低温極限だけ間違える |
| 2-3 | 力学 問 3 | $\cos\theta_0$ は無次元 | 次元の合わない式 |
| 2-3 | 電磁気 問 1-2 | $\varepsilon_r\to1$ で $\sigma_b\to0$ | 分極電荷の誤り |
| 2-3 | 統計 問 2 | $0\le\theta\le1$ | 被覆率が 1 を超える |
| 2-4 | 力学 問 4 | $\gamma\to0$ で $A_{\max}\to\infty$ | 係数の取り違え |
| 2-4 | 統計 問 4 | $S<0$ は $W<1$ を意味しありえない | 第 3 法則の破れを見逃す |
| 2-5 | 力学 問 4 | $M\to\infty$ で $\omega\to\sqrt{g/\ell}$ | 分母分子の取り違え |
| 2-5 | 電磁気 問 1-2 | 束縛電荷の総和が $0$ | $a^2, b^2$ の取り違え |
| 2-5 | 電磁気 問 3-3 | $[R^2]=[L/C]=\Omega^2$ | $\sqrt{L^2R^2+4LC}$ 型の誤り |
| 2-5 | 統計 問 2 | $0\le M_z\le N\mu$、$J=1$ のキュリー定数 | 係数 $2/3$ の誤り |
| 2-6 | 力学 問 4 | $\cos\theta_c$ は $\ell,g,M$ を含まない | 余計な文字が残る |
| 2-6 | 電磁気 問 1-2 | $\int_0^ar^4dr = a^5/5$ | 係数 $3/20$ を外す |
| 2-6 | 統計 問 3 | $F = U-TS$ に代入して $-U/3$ | 符号・係数の誤り |
