#### ① 板書

**ファラデーの法則**：起電力 $\mathcal E = -\dfrac{d\Phi}{dt}$、$\Phi = \int\boldsymbol B\cdot d\boldsymbol S$。符号（レンツ）は「磁束の変化を妨げる向き」。

**インダクタンス**

- 自己：$\Phi = LI$ → $\mathcal E = -L\dfrac{dI}{dt}$。ソレノイド（長さ $l$、$N$ 巻、断面 $S$）：$B = \mu_0\dfrac Nl I$、$\Phi_{\rm 全} = N\cdot BS$ → $L = \mu_0\dfrac{N^2S}{l}$
- 相互：コイル1の電流 $I_1$ がコイル2に作る磁束 $\Phi_2 = MI_1$。ソレノイドに $N_2$ 巻を巻きつけると $M = \mu_0\dfrac{N_1N_2S}{l}$
- 磁気エネルギー $\frac12LI^2$

**回路の微分方程式**（キルヒホッフ：一周の電圧降下の和＝起電力）

- RC放電：$R\dfrac{dq}{dt} + \dfrac qC = 0$ → $q = q_0e^{-t/RC}$（時定数 $RC$）
- LR：$L\dfrac{dI}{dt} + RI = V$ → $I = \dfrac VR(1 - e^{-Rt/L})$（時定数 $L/R$）
- LRC：$L\ddot q + R\dot q + \dfrac qC = V$。減衰振動と同じ形（$\omega_0^2 = 1/LC$、$2\gamma = R/L$）
- 交流：$V = V_0e^{i\omega t}$ とおくとインピーダンス $Z = R + i\omega L + \dfrac{1}{i\omega C}$、$I_0 = V_0/Z$、位相差 $\tan\phi = \mathrm{Im}Z/\mathrm{Re}Z$

**動く導体の起電力**：$\mathcal E = \int(\boldsymbol v\times\boldsymbol B)\cdot d\boldsymbol l$。長さ $l$ の棒が $v$ で動けば $vBl$。半径 $a$ の円板が角速度 $\omega$ で回れば中心と縁の間に $\int_0^a\omega rB\,dr = \frac12\omega Ba^2$。

#### ② 過去問（立教 2011年春 大問2）

(a) 被覆銅線を $N_1$ 回巻いた断面積 $S$、長さ $L_1$ の円筒形ソレノイド（十分長い）。(i) 直流 $I$ を流したときの内部の磁場 $B$。(ii) 側面に $N_2$ 回巻きつけ、$N_1$ 側に交流 $I_1$ を流す。$N_2$ 側の誘導起電力 $V_2 = L_{21}\dfrac{dI_1}{dt}$ の相互インダクタンス $L_{21}$。
(b) 起電力 $V$ の電池、自己インダクタンス $L$、抵抗 $R$ の閉回路。$L\dfrac{dI}{dt} + RI = V$。(i) $t=0$ でスイッチを閉じたときの $I(t)$。(ii) 電池を交流電源 $V = V_0\exp(i\omega t)$ に替える。$I = I_0\exp(i\omega t)$ とおき、$I_0 = V_0/(\text{ロ})$、$(\text{ロ}) = Z\exp(i\phi)$ のときの $Z$ と $\phi$。

#### ③ 解説

**(a)(i)** アンペール：$B = \mu_0\dfrac{N_1}{L_1}I$。
**(ii)** $N_2$ 巻を貫く磁束 $= N_2\cdot BS = \mu_0\dfrac{N_1N_2S}{L_1}I_1$。よって $L_{21} = \mu_0\dfrac{N_1N_2S}{L_1}$。

**(b)(i)** 特解 $I = V/R$、斉次解 $e^{-Rt/L}$。$I(0) = 0$：$I = \dfrac VR\left(1 - e^{-Rt/L}\right)$。
**(ii)** 代入：$i\omega LI_0 + RI_0 = V_0$ → $I_0 = \dfrac{V_0}{R + i\omega L}$。$R + i\omega L = Ze^{i\phi}$、$Z = \sqrt{R^2 + \omega^2L^2}$、$\tan\phi = \omega L/R$。電流は電圧より位相 $\phi$ 遅れる。

> **落とし穴**：①相互インダクタンスで「$N_2$ 巻分」を掛け忘れる。②LR回路で $I(0)=0$ から定数を決める。③交流で $1/(i\omega C) = -i/(\omega C)$ の符号。

#### ④ 練習問題

**練習E10-A**（RC放電）：$C$ に $q_0$ を蓄えて $R$ につなぐ。$q(t)$ と、抵抗で消費される全エネルギーが $q_0^2/2C$ になることを確認。

**練習E10-B【自作・回転円板】**：半径 $a$ の金属円板を、面に垂直な一様磁場 $B$ 中で角速度 $\omega$ で回す。中心と縁の間の起電力。縁と中心を抵抗 $R$ でつないだときの電流と、円板を回し続けるのに必要な仕事率。

**練習E10-C**：LRC直列回路のインピーダンスの大きさが最小になる $\omega$（共振）と、そのときの位相差。

**略解**
E10-A：$q = q_0e^{-t/RC}$。$\int_0^\infty RI^2dt = \int_0^\infty\frac{q_0^2}{R C^2}e^{-2t/RC}dt = \frac{q_0^2}{2C}$。
E10-B：$\mathcal E = \frac12\omega Ba^2$、$I = \mathcal E/R$、仕事率 $= \mathcal E I = \dfrac{\omega^2B^2a^4}{4R}$。
E10-C：$\omega L = 1/\omega C$ → $\omega = 1/\sqrt{LC}$、位相差0（$Z = R$）。
