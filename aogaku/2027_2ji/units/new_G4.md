#### ① 板書

**減衰の法則**：厚さ $d$ の物質を通る光子数 $N = N_0e^{-d/\lambda}$（$\lambda$：減衰長＝$1/e$ になる距離。$\mu = 1/\lambda$ は線吸収係数）。逆に解けば厚さの測定：$d = \lambda\ln(N_0/N)$。

**吸収端**：X線のエネルギーが内殻電子（K殻など）の束縛エネルギーを超えた瞬間、その電子を叩き出す光電吸収が新たに可能になり、吸収が急増（減衰長が急落）。Si の K 吸収端は 1839 eV。

**カウントの誤差伝播（最頻の型）**：$N$ カウントの誤差は $\sqrt N$。$d = \lambda(\ln N_0 - \ln N)$ に伝播させると
$$\delta d = \lambda\sqrt{\left(\frac{\delta N_0}{N_0}\right)^2 + \left(\frac{\delta N}{N}\right)^2} = \lambda\sqrt{\frac{1}{N_0} + \frac1N}$$
（$\ln$ の誤差は相対誤差、$\sqrt N/N = 1/\sqrt N$）

**測定時間の最適配分**：合計時間が決まっているとき、誤差の2乗（分散）を $f$ で微分して0。**カウント率が低い方に長く時間を割く**のが常に答え。

#### ② 過去問【立教 2025年夏 大問6・原文】

図1はシリコン中での 1000〜5000 eV のX線の減衰長のグラフ（1800 eV で急激に変化。4000 eV で約 12 μm、5000 eV で約 19 μm）。減衰長とは光子数が $1/e$ になる距離。
(a) 厚さ $d$ の薄膜に単色X線 $N_0$ 個を垂直入射。減衰長 $\lambda$。通り抜ける数 $N$ を推定せよ。
(b) シリコン中の減衰長がおよそ 1800 eV で急激に変化する理由を簡潔に説明せよ。
(c) $N_0$ 個入射して $N$ 個通り過ぎた。厚さ $d$ を推定せよ。
(d) $N_0$ に $\sqrt{N_0}$、$N$ に $\sqrt N$ の統計誤差があるとする。$d$ につく統計誤差 $\delta d$ を誤差伝播で求めよ。
(e) 厚さがほぼ 10 μm のシリコン薄膜を、4.1 keV のX線で $\delta d\le0.1$ μm の精度で測りたい。まず直接検出器に時間 $T$ 当てて $N_0$ を測り、次に薄膜を入れて同じ時間 $T$ で $N$ を測る。$N_0$ として必要な数を定量的に議論せよ（$e = 2.72$）。
(f) 全測定時間が決まっている。透過させた測定の時間と直接当てる測定の時間を $f:(1-f)$ に振り分ける。$\delta d$ を最小にする $f$ を求めよ。

#### ③ 解説

**(a)** $N = N_0e^{-d/\lambda}$。

**(b)** 1800 eV 付近に Si の K 殻電子の束縛エネルギー（1839 eV）がある。これを超えるとK殻電子による光電吸収が起きるようになり吸収が急増、減衰長が急に短くなる（K吸収端）。

**(c)** $d = \lambda\ln\dfrac{N_0}{N}$。

**(d)** $d = \lambda(\ln N_0 - \ln N)$。$\dfrac{\partial d}{\partial N_0} = \dfrac{\lambda}{N_0}$、$\dfrac{\partial d}{\partial N} = -\dfrac\lambda N$。
$$(\delta d)^2 = \frac{\lambda^2}{N_0^2}N_0 + \frac{\lambda^2}{N^2}N = \lambda^2\left(\frac1{N_0} + \frac1N\right),\qquad \delta d = \lambda\sqrt{\frac1{N_0} + \frac1N}$$

**(e)** グラフから 4.1 keV で $\lambda\simeq13$ μm。$d/\lambda = 10/13\simeq0.77$、$e^{0.77}\simeq2.16$ → $N = N_0/2.16$。
$(\delta d)^2 = \lambda^2\left(\dfrac1{N_0} + \dfrac{2.16}{N_0}\right) = \dfrac{3.16\lambda^2}{N_0}$。$\delta d\le0.1$ μm：$\dfrac{3.16\times13^2}{N_0}\le0.01$ → $N_0\ge\dfrac{3.16\times169}{0.01}\simeq5.3\times10^4$。
**$N_0$ は $5\times10^4$ 個以上（$10^5$ のオーダー）必要**。（$\lambda$ の読み取りが ±2 μm ずれても $N_0$ は数万〜十万で変わらない、と一言添えると強い）

**(f)** 直接ビームのカウント率を $R$、全時間 $T_{\rm tot}$ とする。$N_0 = R(1-f)T_{\rm tot}$、$N = Re^{-d/\lambda}fT_{\rm tot}$。$k\equiv e^{d/\lambda}$ とおくと
$$(\delta d)^2 = \frac{\lambda^2}{RT_{\rm tot}}\left[\frac{1}{1-f} + \frac kf\right]$$
$g(f) = \dfrac1{1-f} + \dfrac kf$ を最小化：$g' = \dfrac{1}{(1-f)^2} - \dfrac{k}{f^2} = 0$ → $\dfrac{f}{1-f} = \sqrt k$ →
$$f = \frac{\sqrt k}{1+\sqrt k} = \frac{e^{d/2\lambda}}{1 + e^{d/2\lambda}}$$
$d/\lambda\simeq0.77$ なら $\sqrt k\simeq1.47$、$f\simeq0.60$。**透過側（弱い方）に6割**。検算：$d\to0$（$k\to1$）で $f = 1/2$ ✓ 対称。

> **落とし穴**：①(d)で $\delta N = \sqrt N$ を入れ忘れて $\delta d = \lambda\sqrt{(\delta N_0/N_0)^2 + \cdots}$ のまま止める。②(e)で「$N_0 = 10^4$ で 1% だから十分」と早合点（$d$ の誤差は $\lambda$ 倍される）。③(f)で分散でなく標準偏差を微分する（同じ結果になるが計算が汚い）。

#### ④ 練習問題

**練習G4-A**（立教2022春 大問5 (b)）：計数管で1秒間に144個。計数率を相対精度1%以下で測るには何秒必要か。

**練習G4-B**（立教2018夏 大問6）：線源を10分測って900カウント、バックグラウンドを10分測って100カウント。(a) 正味の計数率と誤差。(b) さらに100分使えるとき、線源とBGに何分ずつ配分すれば正味計数率の誤差が最小か。

**練習G4-C**：減衰長 $\lambda = 20$ μm の物質の厚さを測る。$N_0 = 10^6$、$N = 3.7\times10^5$ のとき $d$ と $\delta d$。

**略解**
G4-A：$1/\sqrt N\le0.01$ → $N\ge10^4$ → $10^4/144\simeq70$ 秒。
G4-B：(a) 正味 $800$ カウント/10分、誤差 $\sqrt{900+100}\simeq32$ → $80\pm3.2$ /分。(b) $t_s/t_b = \sqrt{r_s/r_b} = \sqrt{90/10} = 3$ → 線源75分、BG25分。
G4-C：$d = 20\ln(10^6/3.7\times10^5) = 20\ln2.70\simeq20\times0.994\simeq19.9$ μm。$\delta d = 20\sqrt{10^{-6} + 2.7\times10^{-6}}\simeq20\times1.9\times10^{-3}\simeq0.04$ μm。
