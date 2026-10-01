#### 要点

**第一法則**：$dU = TdS - pdV$（＋$\mu dN$）。これが全ての出発点。

**熱力学ポテンシャルと自然な変数**

| ポテンシャル | 定義 | 全微分 | 自然な変数 |
| --- | --- | --- | --- |
| 内部エネルギー $U$ | — | $dU = TdS - pdV$ | $(S, V)$ |
| ヘルムホルツ $F$ | $F = U - TS$ | $dF = -SdT - pdV$ | $(T, V)$ |
| エンタルピー $H$ | $H = U + pV$ | $dH = TdS + Vdp$ | $(S, p)$ |
| ギブス $G$ | $G = H - TS$ | $dG = -SdT + Vdp$ | $(T, p)$ |

**マクスウェル関係式**：全微分の2階偏微分は順序によらない。例えば $dF = -SdT - pdV$ から
$$\left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial p}{\partial T}\right)_V$$
これが「測れない量 $(\partial S/\partial V)_T$」を「測れる量 $(\partial p/\partial T)_V$」に変換する道具。

**最重要公式**（立教2020春・2011春で出た）
$$\left(\frac{\partial U}{\partial V}\right)_T = -p + T\left(\frac{\partial p}{\partial T}\right)_V$$
導出：$dU = TdS - pdV$ を $T$ 一定で $V$ で割り、マクスウェル関係式を入れる。

**準静的過程**
- 等温：$T$ 一定。理想気体なら $\Delta S = nR\ln(V_2/V_1)$
- 断熱（準静的＝可逆）：$S$ 一定。$dQ = 0$ かつ $dS = 0$


#### 問0-1 ★ 理想気体のエントロピーと等温・断熱変化（青学本番）


単原子理想気体（$n$ mol、$C_V = \frac{3}{2}nR$、$pV = nRT$）について、

(1) $dU = TdS - pdV$ を用いて $S(T, V)$ を求めよ。積分定数を $S_0$ とする。
(2) 準静的等温変化で体積を $V_1 \to V_2$ にした。エントロピーは変化するか。$\Delta S$ を求めよ。
(3) 準静的断熱変化で体積を $V_1 \to V_2$ にした。エントロピーは変化するか。到達温度 $T_2$ を $T_1, V_1, V_2$ で表せ。

**解答**

(1) $dS = \dfrac{dU}{T} + \dfrac{p}{T}dV$。$dU = C_V dT$、$p/T = nR/V$ なので
$$dS = C_V\frac{dT}{T} + nR\frac{dV}{V} \quad\Rightarrow\quad S = C_V \ln T + nR\ln V + S_0 = \frac{3}{2}nR\ln T + nR\ln V + S_0$$

(2) 等温なので第1項は変化しない。**変化する**：
$$\Delta S = nR\ln\frac{V_2}{V_1}$$
膨張なら正（増加）、圧縮なら負。

(3) 準静的断熱は可逆断熱＝等エントロピー。**変化しない**、$\Delta S = 0$。(1) の式で $S$ 一定とすると
$$C_V\ln\frac{T_2}{T_1} = -nR\ln\frac{V_2}{V_1} \quad\Rightarrow\quad T_2 = T_1\left(\frac{V_1}{V_2}\right)^{nR/C_V} = T_1\left(\frac{V_1}{V_2}\right)^{2/3}$$
$\gamma = C_p/C_V = 5/3$ なので $nR/C_V = \gamma - 1 = 2/3$。$TV^{\gamma-1} = $ 一定 と同じ。

> **落とし穴**：等温で「変化しない」、断熱で「変化する」と逆に書きやすい。「断熱・準静的＝$S$ 一定」を先に固定する。


#### 問0-2 ★ $(\partial U/\partial V)_T$ の一般式（立教2020春 大問4）


(1) 状態方程式の形によらず $\left(\dfrac{\partial U}{\partial V}\right)_T = -p + T\left(\dfrac{\partial p}{\partial T}\right)_V$ が成り立つことを示せ。
(2) 状態方程式が $pV = \alpha U(T, V)$（$\alpha$ は定数）で与えられるとき、$U = V^{-\alpha}A(TV^\alpha)$、$S = B(TV^\alpha)$ の形になることを導け（$A, B$ は任意関数）。
(3) 理想気体（$\alpha = 2/3$）、光子気体（$\alpha = 1/3$）でそれぞれ何が言えるか。

**解答**

(1) $dU = TdS - pdV$ の両辺を $T$ 一定で $dV$ で割る：
$$\left(\frac{\partial U}{\partial V}\right)_T = T\left(\frac{\partial S}{\partial V}\right)_T - p$$
マクスウェル関係式 $\left(\dfrac{\partial S}{\partial V}\right)_T = \left(\dfrac{\partial p}{\partial T}\right)_V$（$dF = -SdT - pdV$ から）を代入して完成。

(2) $p = \alpha U/V$ を (1) に代入：
$$\left(\frac{\partial U}{\partial V}\right)_T = -\frac{\alpha U}{V} + \frac{\alpha T}{V}\left(\frac{\partial U}{\partial T}\right)_V$$
整理すると $V\dfrac{\partial U}{\partial V} - \alpha T\dfrac{\partial U}{\partial T} = -\alpha U$。変数 $x = TV^\alpha$ を導入すると、$U = V^{-\alpha}A(x)$ がこの1階偏微分方程式を満たすことが直接代入で確かめられる。
$S$ については $dS = \dfrac{1}{T}dU + \dfrac{p}{T}dV$ に上の $U$ と $p = \alpha U/V$ を入れると $dS = \dfrac{A'(x)}{T}\,dx \cdot V^{-\alpha}$…整理して $S = B(TV^\alpha)$。

(3) $\alpha = 2/3$：断熱で $TV^{2/3} = $ 一定（問0-1と一致）。$\alpha = 1/3$：$TV^{1/3} = $ 一定、$U \propto V^{-1/3}A(TV^{1/3})$ で $U = aVT^4$ の形と整合する。
