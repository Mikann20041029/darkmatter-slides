#### ① 板書

**マクスウェル方程式（微分形）と積分形・意味**

| 微分形 | 積分形（積分定理で変換） | 意味 |
| --- | --- | --- |
| $\nabla\cdot\boldsymbol D = \rho$ | $\oint_S\boldsymbol D\cdot d\boldsymbol S = Q_{\rm 内}$（ガウスの定理） | 閉曲面を貫く電束＝中の全電荷 |
| $\nabla\cdot\boldsymbol B = 0$ | $\oint_S\boldsymbol B\cdot d\boldsymbol S = 0$ | 磁束は閉曲面から出入りゼロ。磁気単極子なし |
| $\nabla\times\boldsymbol E = -\dfrac{\partial\boldsymbol B}{\partial t}$ | $\oint_C\boldsymbol E\cdot d\boldsymbol l = -\dfrac{d\Phi}{dt}$（ストークス） | 磁束の変化が起電力を作る（ファラデー） |
| $\nabla\times\boldsymbol H - \dfrac{\partial\boldsymbol D}{\partial t} = \boldsymbol i$ | $\oint_C\boldsymbol H\cdot d\boldsymbol l = I + \dfrac{d\Phi_D}{dt}$ | 電流と電束の変化（変位電流）が磁場を作る（アンペール・マクスウェル） |

**変換の道具**：ガウスの定理 $\int_V\nabla\cdot\boldsymbol A\,dV = \oint_S\boldsymbol A\cdot d\boldsymbol S$、ストークスの定理 $\int_S(\nabla\times\boldsymbol A)\cdot d\boldsymbol S = \oint_C\boldsymbol A\cdot d\boldsymbol l$。「説明せよ」問題は**微分形→積分定理→積分形→日本語**の順に書けば満点。

**静電場の条件**：$\nabla\times\boldsymbol E = 0$ ⟺ $\boldsymbol E = -\nabla\phi$ と書ける ⟺ 一周の仕事 $\oint\boldsymbol E\cdot d\boldsymbol l = 0$。
**$\phi$ の求め方**：$E_x = -\partial\phi/\partial x$ を $x$ で積分し、$E_y, E_z$ で係数を確定。「$\phi$ を推定して $-\nabla\phi$ が $\boldsymbol E$ に戻るか確かめる」が実戦では速い。

**恒等式**：$\nabla\cdot(\nabla\times\boldsymbol A) = 0$、$\nabla\times(\nabla f) = 0$（どちらも偏微分の順序交換で証明）。

**変位電流の必要性**：$\nabla\times\boldsymbol B = \mu_0\boldsymbol J$ の両辺の発散をとると $0 = \mu_0\nabla\cdot\boldsymbol J$。しかし電荷保存 $\partial\rho/\partial t + \nabla\cdot\boldsymbol J = 0$ より、$\rho$ が時間変化するときは $\nabla\cdot\boldsymbol J\ne0$。矛盾を直すのが $\varepsilon_0\partial\boldsymbol E/\partial t$。

#### ② 過去問

**(A) 上智 2025年春 問4**

1. $\boldsymbol E(\boldsymbol r) = (2yz - 12xy^2z^2,\ 2xz - 12x^2yz^2,\ 2xy - 12x^2y^2z)$。(1) $\nabla\times\boldsymbol E = 0$ を具体的に計算して確かめよ。(2) 対応する静電ポテンシャル $\phi(\boldsymbol r)$。
2. マクスウェル方程式 (a) $\nabla\cdot\boldsymbol D = \rho$、(b) $\nabla\cdot\boldsymbol B = 0$、(c) $\nabla\times\boldsymbol H - \partial\boldsymbol D/\partial t = \boldsymbol i$、(d) $\nabla\times\boldsymbol E + \partial\boldsymbol B/\partial t = 0$ に基づいて説明せよ。(1) 閉曲面 $S$ 内の全電荷がその面を貫く電束に等しいこと。(2) 静電場中で閉曲線に沿って電荷を一周させた仕事が0であること。(3) 閉曲面を貫く磁束は常に0であること。(4) 閉回路を貫く磁束の時間変化が誘導起電力を発生させること。(5) 真空中で磁場が存在しないとき、時間変動する電場が存在しうるか。

**(B) 上智 2025年秋 問4**

1. $\boldsymbol A = (xy, x^2, yz)$ の $\nabla\cdot\boldsymbol A$ と $\nabla\times\boldsymbol A$。
2. 任意の $\boldsymbol A$ で $\nabla\cdot(\nabla\times\boldsymbol A) = 0$ を示せ。
3. (a) $\nabla\cdot\boldsymbol E = \rho/\varepsilon_0$、(b) $\partial\rho/\partial t + \nabla\cdot\boldsymbol J = 0$、(c) $\nabla\times\boldsymbol B = \mu_0\boldsymbol J$ の意味を、ア〜クから選べ（ア 電荷保存則・連続の方程式／イ 電磁場のエネルギー保存／ウ ローレンツ力／エ ガウスの法則／オ ファラデー／カ アンペール／キ オーム／ク ポインティング）。
4. (c)の両辺の発散をとると $\nabla\cdot\boldsymbol J = 0$ になり定常電流でしか成り立たない。(a)(b)を使って $\nabla\times\boldsymbol B = \mu_0\boldsymbol J + \dfrac{1}{c^2}\dfrac{\partial\boldsymbol E}{\partial t}$ に拡張されることを示せ（$c = 1/\sqrt{\varepsilon_0\mu_0}$）。

#### ③ 解説

**(A)1.(1)** $x$ 成分：$\partial_yE_z - \partial_zE_y = (2x - 24x^2yz) - (2x - 24x^2yz) = 0$。$y$ 成分：$\partial_zE_x - \partial_xE_z = (2y - 24xy^2z) - (2y - 24xy^2z) = 0$。$z$ 成分：$\partial_xE_y - \partial_yE_x = (2z - 24xyz^2) - (2z - 24xyz^2) = 0$。✓
**(2)** $\phi = -2xyz + 6x^2y^2z^2 + C$。検算：$-\partial_x\phi = 2yz - 12xy^2z^2 = E_x$ ✓（他も同様）。
（見つけ方：$E_x$ を $x$ で積分 → $-\phi = 2xyz - 6x^2y^2z^2 + g(y,z)$。$-\partial_y$ が $E_y$ と一致するので $g$ は $z$ だけの関数、$-\partial_z$ でも一致するので $g$ は定数）

**(A)2.**
(1) (a) を体積 $V$ で積分し、ガウスの定理：$\oint_S\boldsymbol D\cdot d\boldsymbol S = \int_V\rho\,dV = Q$。
(2) 静電場では $\partial\boldsymbol B/\partial t = 0$ なので (d) は $\nabla\times\boldsymbol E = 0$。ストークスの定理で $\oint_C\boldsymbol E\cdot d\boldsymbol l = 0$。電荷 $q$ の受ける力は $q\boldsymbol E$ なので一周の仕事 $q\oint\boldsymbol E\cdot d\boldsymbol l = 0$。
(3) (b) をガウスの定理で $\oint_S\boldsymbol B\cdot d\boldsymbol S = 0$。磁力線は閉曲面に入った分だけ出る。
(4) (d) をストークスの定理で $\oint_C\boldsymbol E\cdot d\boldsymbol l = -\dfrac{d}{dt}\int_S\boldsymbol B\cdot d\boldsymbol S = -\dfrac{d\Phi}{dt}$。左辺が回路一周の起電力。
(5) 真空で $\boldsymbol B = 0$（したがって $\boldsymbol H = 0$）、$\boldsymbol i = 0$ なら (c) は $\partial\boldsymbol D/\partial t = 0$、つまり $\varepsilon_0\partial\boldsymbol E/\partial t = 0$。**時間変動する電場は存在しえない**。（変動する電場は必ず磁場を伴う）

**(B)1.** $\nabla\cdot\boldsymbol A = y + 0 + y = 2y$。$\nabla\times\boldsymbol A = (\partial_y(yz) - \partial_z(x^2),\ \partial_z(xy) - \partial_x(yz),\ \partial_x(x^2) - \partial_y(xy)) = (z,\ 0,\ x)$。
**2.** $\nabla\cdot(\nabla\times\boldsymbol A) = \partial_x(\partial_yA_z - \partial_zA_y) + \partial_y(\partial_zA_x - \partial_xA_z) + \partial_z(\partial_xA_y - \partial_yA_x)$。$\partial_x\partial_yA_z$ と $-\partial_y\partial_xA_z$ のように、6項が2つずつ打ち消す（偏微分の順序交換）。
**3.** (a) エ、(b) ア、(c) カ。
**4.** (a) より $\rho = \varepsilon_0\nabla\cdot\boldsymbol E$。(b) に入れて $\nabla\cdot\boldsymbol J = -\dfrac{\partial\rho}{\partial t} = -\varepsilon_0\nabla\cdot\dfrac{\partial\boldsymbol E}{\partial t}$、つまり $\nabla\cdot\left(\boldsymbol J + \varepsilon_0\dfrac{\partial\boldsymbol E}{\partial t}\right) = 0$。発散が常に0になるこの組み合わせを (c) の右辺に置けば矛盾が消える：$\nabla\times\boldsymbol B = \mu_0\left(\boldsymbol J + \varepsilon_0\dfrac{\partial\boldsymbol E}{\partial t}\right) = \mu_0\boldsymbol J + \dfrac{1}{c^2}\dfrac{\partial\boldsymbol E}{\partial t}$。

> **落とし穴**：①「説明せよ」で式だけ書いて日本語を書かない。②(A)2(5)を「存在しうる」と答える——$\boldsymbol B=0$ を (c) に入れる一手で決まる。③$\nabla\times$ の成分の順番（$x$ 成分は $\partial_yA_z - \partial_zA_y$）。

#### ④ 練習問題

**練習E4-A**：$\boldsymbol E = (y, x, 0)$ は静電場か。静電場なら $\phi$ を求めよ。$\boldsymbol E = (y, -x, 0)$ はどうか。

**練習E4-B**：$\nabla\times(\nabla f) = 0$ を成分で示せ。

**練習E4-C**：平行板コンデンサー（面積 $S$、間隔 $d$）に電流 $I$ で充電中。極板間に電流は流れていないのに、極板間を囲む閉曲線でアンペールの法則が成り立つ理由を、変位電流 $\varepsilon_0\partial E/\partial t$ を計算して示せ。

**略解**
E4-A：前者は $\nabla\times\boldsymbol E = (0,0,1-1) = 0$ → 静電場、$\phi = -xy$。後者は $z$ 成分 $-1-1 = -2\ne0$ → 静電場ではない。
E4-B：$x$ 成分 $= \partial_y\partial_zf - \partial_z\partial_yf = 0$。他も同様。
E4-C：$E = Q/(\varepsilon_0S)$、$\varepsilon_0\dfrac{\partial E}{\partial t}S = \dfrac{dQ}{dt} = I$。変位電流が導線の電流 $I$ と同じ値になるので、閉曲線を貫く「電流」は極板間でも $I$。
