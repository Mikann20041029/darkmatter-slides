#### ① 板書

**導体の境界条件**：静電場中の導体は
- 内部で $\boldsymbol E = 0$、電荷は表面のみ
- 表面で電位 $\phi$ 一定、$\boldsymbol E$ は表面に垂直
- 表面電荷密度 $\sigma = \varepsilon_0E_n = -\varepsilon_0\dfrac{\partial\phi}{\partial n}$（$n$ は外向き法線）

**鏡像法の考え方**：導体を取り除き、代わりに仮想の電荷（鏡像電荷）を**導体の内側**に置いて、導体表面での境界条件（電位一定）を再現する。**一意性定理**（境界条件を満たすラプラス方程式の解は唯一）により、それが導体外側の正しい電場。

**2つの基本型**

| 型 | 鏡像電荷 | 位置 |
| --- | --- | --- |
| 無限平面導体（接地）＋点電荷 $q$（距離 $d$） | $-q$ | 面の裏側、距離 $d$ |
| 導体球（半径 $a$、接地）＋点電荷 $Q$（中心から $b > a$） | $q' = -\dfrac{a}{b}Q$ | 中心から $\dfrac{a^2}{b}$（球の内側） |

**導体球のバリエーション**
- 接地：上の $q'$ のみ。球の電位 0
- 絶縁・電荷 0：$q'$ に加えて中心に $-q' = +\dfrac{a}{b}Q$。球の電位 $= \dfrac{aQ/b}{4\pi\varepsilon_0a} = \dfrac{Q}{4\pi\varepsilon_0b}$
- 絶縁・電荷 $Q_0$：中心に $Q_0 - q'$

**鏡像電荷の位置の導出**（相似三角形）：球面上の任意の点 $L$、中心 $O$、点電荷 $K$、鏡像 $M$。$\triangle OLM \sim \triangle OKL$ となるように $M$ を取ると $\dfrac{OM}{OL} = \dfrac{OL}{OK}$ → $OM = \dfrac{a^2}{b}$。このとき $\dfrac{LM}{LK} = \dfrac{a}{b}$（球面上のどこでも）なので、$\dfrac{q'}{LM} + \dfrac{Q}{LK} = 0$ が全 $L$ で成り立つ。

**鏡像法で求まるもの**：外側の電位・電場、表面電荷分布、点電荷に働く力（鏡像電荷からの力）、点電荷を無限遠へ運ぶ仕事。**鏡像電荷は導体内部の場を表さない**（内部は $E = 0$）。

#### ② 過去問（立教 2010年春 大問II）

真空中に絶縁された半径 $a$ の導体球（帯電していない）。中心 $O$ から $b$（$b > a$）の距離の点 $K$ に電荷 $Q$ の点電荷を置く。

1. 球面上の任意の点を $L$。$OK$ 上に点 $M$ をとり、$\triangle OLM$ と $\triangle OKL$ が相似形のとき、$OM$ の距離 $c$ を $a, b$ で表せ。
2. 鏡像法で解くため、導体球の代わりに点 $M$ に電荷 $q$ を置く。球面上の電位がどこでも同じになるように $q$ を求めよ。
3. 導体球は絶縁されているので電荷の総量は 0。総量が 0 になるように中心 $O$ にも鏡像電荷を置き、導体球の電位を求めよ。
4. 導体球と点電荷の間に働く力の大きさと向きを求めよ。

#### ③ 解説

**1.** 相似より $\dfrac{OM}{OL} = \dfrac{OL}{OK}$ → $\dfrac{c}{a} = \dfrac{a}{b}$ → $c = \dfrac{a^2}{b}$。

**2.** 相似より $\dfrac{LM}{LK} = \dfrac{OL}{OK} = \dfrac{a}{b}$（$L$ によらない）。球面上の電位
$$\phi(L) = \frac{1}{4\pi\varepsilon_0}\left(\frac{Q}{LK} + \frac{q}{LM}\right) = \frac{1}{4\pi\varepsilon_0\,LK}\left(Q + q\frac{LK}{LM}\right) = \frac{1}{4\pi\varepsilon_0\,LK}\left(Q + q\frac{b}{a}\right)$$
これが $L$ によらず一定（実は 0）になるには $q = -\dfrac{a}{b}Q$。

**3.** 電荷総量 0 のため中心に $+\dfrac{a}{b}Q$。球面上の電位は、$M$ の $q$ と $K$ の $Q$ の寄与が打ち消し合うので中心電荷の分だけ：
$$\phi_{\text{球}} = \frac{1}{4\pi\varepsilon_0}\cdot\frac{aQ/b}{a} = \frac{Q}{4\pi\varepsilon_0b}$$

**4.** $K$ の $Q$ に働く力 ＝ $M$ の $q$ からの力 ＋ 中心の $+aQ/b$ からの力。$K$ から $M$ までの距離 $b - a^2/b = \dfrac{b^2 - a^2}{b}$。
$$F = \frac{Q}{4\pi\varepsilon_0}\left[\frac{-aQ/b}{\left(\frac{b^2-a^2}{b}\right)^2} + \frac{aQ/b}{b^2}\right] = \frac{aQ^2}{4\pi\varepsilon_0}\left[-\frac{b}{(b^2-a^2)^2} + \frac{1}{b^3}\right]$$
通分：$\dfrac{-b^4 + (b^2-a^2)^2}{b^3(b^2-a^2)^2} = \dfrac{a^2(a^2 - 2b^2)}{b^3(b^2-a^2)^2} < 0$（$b > a$）。
$$F = -\frac{a^3Q^2(2b^2 - a^2)}{4\pi\varepsilon_0b^3(b^2-a^2)^2} \quad(\text{引力})$$
中性の導体球でも引力になる（$q'$ の方が近いので勝つ）。

#### ④ 確認問題

**確認1-A**（立教2012春 大問2 / 都立2025冬）：$x = a$（$a > 0$）に点電荷 $q$、$x < 0$ の領域全体に接地導体。
(i) $x > 0$ の電位 $\phi(x, y, z)$。(ii) 導体表面 $x = 0$ の誘導電荷密度 $\sigma(y, z)$ と総電荷。(iii) 点電荷に働く力。(iv) 点電荷を無限遠まで運ぶ仕事。

**確認1-B**：半径 $a$ の**接地**導体球と距離 $b$ の点電荷 $Q$。(i) 球面上の誘導電荷の総量。(ii) $Q$ に働く力。(iii) 絶縁・中性の場合（過去問の答え）との違いを述べよ。

**略解**
1-A：(i) $\phi = \dfrac{q}{4\pi\varepsilon_0}\left[\dfrac{1}{\sqrt{(x-a)^2+y^2+z^2}} - \dfrac{1}{\sqrt{(x+a)^2+y^2+z^2}}\right]$。(ii) $\sigma = -\varepsilon_0\dfrac{\partial\phi}{\partial x}\Big|_{x=0} = -\dfrac{qa}{2\pi(a^2+y^2+z^2)^{3/2}}$。総電荷 $-q$。(iii) $F = -\dfrac{q^2}{4\pi\varepsilon_0(2a)^2}$（引力）。(iv) $W = \int_a^\infty\dfrac{q^2}{16\pi\varepsilon_0x^2}dx = \dfrac{q^2}{16\pi\varepsilon_0a}$。
1-B：(i) $-\dfrac{a}{b}Q$。(ii) $F = -\dfrac{abQ^2}{4\pi\varepsilon_0(b^2-a^2)^2}$。(iii) 中性球は中心に $+aQ/b$ が加わる分、引力が弱まる。

---
