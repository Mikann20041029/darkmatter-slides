#### ① 板書

**静磁場の2法則（微分形）**

- $\nabla\cdot\boldsymbol B = 0$：磁力線は途中で生まれも消えもしない（磁気単極子は存在しない）。
- $\nabla\times\boldsymbol B = \mu_0\boldsymbol i$：電流のまわりに磁場が渦を巻く。

**アンペールの法則（積分形）**：$\displaystyle\oint\boldsymbol B\cdot d\boldsymbol l = \mu_0I_{\rm 内}$。軸対称なら $B(r)\cdot2\pi r = \mu_0I_{\rm 内}(r)$。**「半径 $r$ の円を貫く電流」だけ数える。**

**電流密度が $r$ に依るとき**：$I_{\rm 内}(r) = \displaystyle\int_0^ri(r')\,2\pi r'dr'$（細い円環 $2\pi r'dr'$ に分けて足す）。

**ローレンツ力**：$\boldsymbol F = q\boldsymbol v\times\boldsymbol B$。向きは右手（$\boldsymbol v$ から $\boldsymbol B$ へ回して親指）。**平行電流は引き合い、反平行は反発**——向きの検算に使える。

円筒座標の単位ベクトル：$\hat z\times\hat\phi = -\hat r$、$\hat r\times\hat\phi = \hat z$。

#### ② 過去問【上智 2026年春 問4-2・原文】

半径 $a$ の無限に長い円柱導体内に、$z$ 軸正方向へ定常電流が流れている。電流密度は
$$i(r) = \begin{cases}i_0\exp(-\beta r^2) & (0\le r\le a)\\ 0 & (r>a)\end{cases}$$
$r$ は $z$ 軸からの距離、$i_0,\beta>0$。透磁率は内外とも $\mu_0$。
(1) 静磁場に関するガウスの法則の微分形、アンペールの法則の微分形を書き、物理的意味を簡潔に説明せよ。
(2) 円柱の内部・外部での磁束密度 $\boldsymbol B(r)$ を求めよ。$\dfrac{d}{dr}[\exp(-\beta r^2)] = -2\beta r\exp(-\beta r^2)$ を使ってよい。
(3) 電気量 $q>0$ の荷電粒子が $z$ 軸から $r_0>a$ の所を $z$ 軸の負の向きに速さ $v_0$ で動いている。磁場から受ける力の向きと大きさ。

#### ③ 解説

**(1)** 板書のとおり。$\nabla\cdot\boldsymbol B = 0$（磁気単極子なし・磁力線は閉じる）、$\nabla\times\boldsymbol B = \mu_0\boldsymbol i$（電流が磁場の渦の源）。

**(2)** 半径 $r$ の円を貫く電流：
$$I_{\rm 内}(r) = \int_0^ri_0e^{-\beta r'^2}\,2\pi r'dr' = 2\pi i_0\left[-\frac{e^{-\beta r'^2}}{2\beta}\right]_0^r = \frac{\pi i_0}{\beta}\left(1 - e^{-\beta r^2}\right)$$
（与えられた微分の式を逆に使った）
内部 $r\le a$：$B\cdot2\pi r = \mu_0I_{\rm 内}(r)$ → $B = \dfrac{\mu_0i_0}{2\beta r}\left(1 - e^{-\beta r^2}\right)$、向きは $\hat\phi$（$z$ 軸正向きの電流に右ねじ）。
外部 $r>a$：全電流 $I = \dfrac{\pi i_0}{\beta}(1 - e^{-\beta a^2})$ → $B = \dfrac{\mu_0i_0}{2\beta r}\left(1 - e^{-\beta a^2}\right)$。
検算：$r\to0$ で $1 - e^{-\beta r^2}\simeq\beta r^2$ → $B\simeq\mu_0i_0r/2$（一様電流の中心付近の式）✓。$r=a$ で内外が一致 ✓。

**(3)** $\boldsymbol v = -v_0\hat z$、$\boldsymbol B = B\hat\phi$。$\boldsymbol F = q\boldsymbol v\times\boldsymbol B = -qv_0B(\hat z\times\hat\phi) = -qv_0B(-\hat r) = qv_0B\,\hat r$。
**向き：$z$ 軸から遠ざかる向き（動径外向き）**。大きさ $F = \dfrac{\mu_0qv_0i_0}{2\beta r_0}\left(1 - e^{-\beta a^2}\right)$。
検算：$+z$ 向きの電流に対して、$q>0$ が $-z$ に動く＝反平行の電流 → 反発 → 外向き ✓。

> **落とし穴**：①$I_{\rm 内}$ を $i(r)\cdot\pi r^2$ と書く（密度が一様でないので積分が要る）。②外側でも $e^{-\beta r^2}$ を残す（外側は $a$ で止まる）。③外積の向き。$\hat z\times\hat\phi = -\hat r$ を紙に書いてから答える。

#### ④ 練習問題

**練習E3-A**：一様な電流密度 $i_0$（$r\le a$）の円柱。内外の $B(r)$ と、$B$ が最大になる $r$。

**練習E3-B**（同軸ケーブル）：半径 $a$ の内導体に $+I$、内径 $b$・外径 $c$ の外導体に $-I$（どちらも一様）。$r<a$、$a<r<b$、$b<r<c$、$r>c$ の $B$。

**練習E3-C**：(3)で粒子が $+z$ 向きに動いたら力の向きは？　$r_0<a$（内部）にいたら大きさは？

**略解**
E3-A：内 $B = \mu_0i_0r/2$、外 $B = \mu_0i_0a^2/(2r)$。最大は $r=a$。
E3-B：$r<a$：$\mu_0Ir/(2\pi a^2)$。$a<r<b$：$\mu_0I/(2\pi r)$。$b<r<c$：$\dfrac{\mu_0I}{2\pi r}\cdot\dfrac{c^2-r^2}{c^2-b^2}$。$r>c$：0。
E3-C：内向き（平行電流は引き合う）。内部なら $F = \dfrac{\mu_0qv_0i_0}{2\beta r_0}(1 - e^{-\beta r_0^2})$。
