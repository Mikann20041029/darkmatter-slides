（要点は Day 1 を参照）


#### 問0-3 ★ ファンデルワールス気体（立教2011春 大問3）


$p = \dfrac{RT}{V - b} - \dfrac{a}{V^2}$（1 mol）について

(1) 膨張率 $\alpha_p = \dfrac{1}{V}\left(\dfrac{\partial V}{\partial T}\right)_p$ を求めよ。
(2) $\left(\dfrac{\partial U}{\partial V}\right)_T$ を求めよ。
(3) $C_V$ が $T$ のみの関数であることを示せ。
(4) $C_p - C_V$ を求めよ。

**解答**

(1) $p$ 一定で全微分：$0 = \dfrac{R}{V-b}dT - \left[\dfrac{RT}{(V-b)^2} - \dfrac{2a}{V^3}\right]dV$ より
$$\alpha_p = \frac{1}{V}\cdot\frac{R/(V-b)}{RT/(V-b)^2 - 2a/V^3} = \frac{R(V-b)V^2}{V\left[RTV^3 - 2a(V-b)^2\right]}$$

(2) 問0-2(1) の式に $\left(\dfrac{\partial p}{\partial T}\right)_V = \dfrac{R}{V-b}$ を入れる：
$$\left(\frac{\partial U}{\partial V}\right)_T = -\frac{RT}{V-b} + \frac{a}{V^2} + \frac{RT}{V-b} = \frac{a}{V^2}$$
理想気体（$a = 0$）ではゼロ。分子間引力 $a$ があると膨張で $U$ が増える。

(3) $\dfrac{\partial C_V}{\partial V} = \dfrac{\partial}{\partial V}\left(\dfrac{\partial U}{\partial T}\right)_V = \dfrac{\partial}{\partial T}\left(\dfrac{\partial U}{\partial V}\right)_T = \dfrac{\partial}{\partial T}\dfrac{a}{V^2} = 0$。よって $C_V = C_V(T)$。

(4) 一般式 $C_p - C_V = T\left(\dfrac{\partial p}{\partial T}\right)_V\left(\dfrac{\partial V}{\partial T}\right)_p = TV\alpha_p\dfrac{R}{V-b}$。(1) を代入して
$$C_p - C_V = \frac{R}{1 - \dfrac{2a(V-b)^2}{RTV^3}}$$
$a \to 0$ で $R$ に戻る。


#### 問0-4 ★ ゴム糸の熱力学（都立2024冬 物理学II[2]）


張力 $X$ のゴム糸を長さ $L \to L + \Delta L$ 断熱的に伸ばすと $\Delta U = X\Delta L$。長さ一定での張力は $X = AT$（$A > 0$）。

(1) $F = U - TS$ の全微分が $dF = XdL - SdT$ となることを示せ。
(2) マクスウェル関係式 $\left(\dfrac{\partial S}{\partial L}\right)_T = -\left(\dfrac{\partial X}{\partial T}\right)_L$ を導け。
(3) $\left(\dfrac{\partial S}{\partial L}\right)_T < 0$ を示せ（等温で伸ばすとエントロピーが減る）。
(4) $\left(\dfrac{\partial U}{\partial L}\right)_T = 0$ を示せ。
(5) $\left(\dfrac{\partial T}{\partial L}\right)_S > 0$ を示せ（断熱で伸ばすと温度が上がる）。

**解答**

(1) $dU = TdS + XdL$（気体の $-pdV$ が $+XdL$ に対応。伸ばすと仕事をされる）。$dF = dU - TdS - SdT = XdL - SdT$。

(2) $dF$ の2階偏微分：$\dfrac{\partial^2 F}{\partial T\partial L} = \left(\dfrac{\partial X}{\partial T}\right)_L = -\left(\dfrac{\partial S}{\partial L}\right)_T$。

(3) $X = AT$ より $\left(\dfrac{\partial X}{\partial T}\right)_L = A > 0$。よって $\left(\dfrac{\partial S}{\partial L}\right)_T = -A < 0$。

(4) $U = F + TS$ より $\left(\dfrac{\partial U}{\partial L}\right)_T = \left(\dfrac{\partial F}{\partial L}\right)_T + T\left(\dfrac{\partial S}{\partial L}\right)_T = X - TA = AT - TA = 0$。

(5) $dS = \left(\dfrac{\partial S}{\partial T}\right)_L dT + \left(\dfrac{\partial S}{\partial L}\right)_T dL = 0$ より
$$\left(\frac{\partial T}{\partial L}\right)_S = -\frac{(\partial S/\partial L)_T}{(\partial S/\partial T)_L} = \frac{A}{C_L/T} = \frac{AT}{C_L} > 0$$
（$C_L = T(\partial S/\partial T)_L > 0$）。ゴムを急に伸ばすと熱くなる。


#### 問0-5 ☆ エンタルピーとジュール・トムソン係数（上智2025秋 問6）


(1) $H = U + pV$ を定義し、$C_p = \left(\dfrac{\partial H}{\partial T}\right)_p$ を示せ。
(2) ジュール・トムソン係数 $\mu_{JT} = \left(\dfrac{\partial T}{\partial p}\right)_H$ を $C_p$、$V$、膨張率 $\alpha_p$ で表せ。
(3) 理想気体で $\mu_{JT} = 0$ を示せ。

**解答**

(1) $dH = TdS + Vdp$。$p$ 一定で $dH = TdS = dQ$。よって $C_p = (dQ/dT)_p = (\partial H/\partial T)_p$。

(2) $dH = 0$ で $dT/dp$ を求める。$dH = C_p dT + \left[T\left(\dfrac{\partial S}{\partial p}\right)_T + V\right]dp$。マクスウェル関係式（$dG = -SdT + Vdp$ から）$\left(\dfrac{\partial S}{\partial p}\right)_T = -\left(\dfrac{\partial V}{\partial T}\right)_p = -V\alpha_p$。よって
$$\mu_{JT} = \frac{TV\alpha_p - V}{C_p} = \frac{V}{C_p}(T\alpha_p - 1)$$

(3) 理想気体 $V = nRT/p$ で $\alpha_p = 1/T$。$T\alpha_p - 1 = 0$。

---
