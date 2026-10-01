#### ① 板書

**ビオ・サバールの法則**：電流素片 $Id\boldsymbol l$ が点 $P$（素片からの位置ベクトル $\boldsymbol r$）に作る磁場
$$d\boldsymbol B = \frac{\mu_0}{4\pi}\frac{Id\boldsymbol l\times\hat{\boldsymbol r}}{r^2}$$
**使うのは対称性で成分が生き残る場合だけ**。それ以外はアンペール。

**円電流（半径 $R$、電流 $I$）の軸上、中心から $z$**：各素片の $dB$ のうち軸方向成分だけ生き残る。
$$B(z) = \frac{\mu_0IR^2}{2(R^2+z^2)^{3/2}},\qquad B(0) = \frac{\mu_0I}{2R}$$
（$dB = \frac{\mu_0}{4\pi}\frac{I\,dl}{R^2+z^2}$、軸成分は $\times\frac{R}{\sqrt{R^2+z^2}}$、一周で $dl\to2\pi R$）

**直線電流**（無限長）：$B = \dfrac{\mu_0I}{2\pi r}$（アンペールで一発。ビオ・サバールなら $\int_{-\infty}^\infty$ で同じ）。
**有限長の直線電流**：$B = \dfrac{\mu_0I}{4\pi r}(\sin\theta_2 - \sin\theta_1)$（両端を見込む角）。

**ソレノイド**（単位長あたり $n$ 巻）：内部 $B = \mu_0nI$（アンペール）。有限長は円電流の重ね合わせ。

**回転する帯電球殻**（半径 $R$、面電荷 $\sigma$、角速度 $\omega$）の中心磁場：緯度 $\theta$ の帯が円電流 $dI = \sigma\omega R^2\sin\theta\,d\theta$、半径 $R\sin\theta$、中心からの距離 $R\cos\theta$。積分して $B = \frac23\mu_0\sigma\omega R$。

#### ② 過去問【再構成：立教2013春 大問2・2025夏 大問2 の型を私が書き直したもの。原文は `kakomon/rikkyo/` で確認】

半径 $R$ の円形コイルに電流 $I$ が流れている。
(a) コイルの中心軸上、中心から距離 $z$ の点の磁場の大きさ $B(z)$ をビオ・サバールの法則から導け。
(b) 同じコイルを2つ、軸を共有して距離 $d$ だけ離して置き、同じ向きに電流を流す（ヘルムホルツコイル）。2つの中点での磁場。
(c) $d = R$ のとき、中点で $dB/dz = 0$ かつ $d^2B/dz^2 = 0$ となることを示せ。
(d) 半径 $R$、全電荷 $Q$ が一様に分布した薄い円板を角速度 $\omega$ で回すとき、中心の磁場。

#### ③ 解説

**(a)** 素片 $Id\boldsymbol l$ と、素片から軸上の点への $\boldsymbol r$ は直交。$|d\boldsymbol B| = \dfrac{\mu_0}{4\pi}\dfrac{I\,dl}{R^2+z^2}$。この $d\boldsymbol B$ は軸から角 $\phi$ 傾いており、$\cos\phi = R/\sqrt{R^2+z^2}$。軸に垂直な成分は一周で打ち消し、軸成分は
$$B = \oint\frac{\mu_0}{4\pi}\frac{I\,dl}{R^2+z^2}\cdot\frac{R}{\sqrt{R^2+z^2}} = \frac{\mu_0I}{4\pi}\frac{R\cdot2\pi R}{(R^2+z^2)^{3/2}} = \frac{\mu_0IR^2}{2(R^2+z^2)^{3/2}}$$

**(b)** 中点は各コイルから $d/2$：$B = 2\cdot\dfrac{\mu_0IR^2}{2(R^2+d^2/4)^{3/2}} = \dfrac{\mu_0IR^2}{(R^2+d^2/4)^{3/2}}$。

**(c)** コイル1を $z=0$、コイル2を $z=d$。$B(z) = \dfrac{\mu_0IR^2}{2}\left[(R^2+z^2)^{-3/2} + (R^2+(z-d)^2)^{-3/2}\right]$。$z = d/2$ で1階微分は対称性から0。2階微分：$f(z) = (R^2+z^2)^{-3/2}$ の $f'' = -3(R^2+z^2)^{-5/2} + 15z^2(R^2+z^2)^{-7/2} = (R^2+z^2)^{-7/2}(12z^2 - 3R^2)$。$z = d/2 = R/2$ で $12\cdot R^2/4 - 3R^2 = 0$ ✓。（中点付近で磁場が一様になる＝ヘルムホルツコイルの設計条件）

**(d)** 半径 $r$、幅 $dr$ の円環：電荷 $dq = \dfrac{Q}{\pi R^2}2\pi r\,dr$、周期 $2\pi/\omega$ なので電流 $dI = \dfrac{\omega}{2\pi}dq = \dfrac{Q\omega r\,dr}{\pi R^2}$。中心磁場 $dB = \dfrac{\mu_0dI}{2r} = \dfrac{\mu_0Q\omega}{2\pi R^2}dr$。積分：$B = \dfrac{\mu_0Q\omega}{2\pi R}$。

> **落とし穴**：①円電流の軸上で「軸成分だけ残す」を忘れて $\frac{\mu_0I}{2\sqrt{R^2+z^2}}$ と書く。②回転電荷の電流は「電荷÷周期」。$dI = \omega\,dq/2\pi$。

#### ④ 練習問題

**練習E9-A**：無限長直線電流 $I$ の磁場をビオ・サバールで計算し $\mu_0I/2\pi r$ を出せ（$\int_{-\infty}^\infty\frac{r\,dz}{(r^2+z^2)^{3/2}} = 2/r$ を使う）。

**練習E9-B**：半径 $R$ の半円形の導線（両端は直線で無限遠へ）に電流 $I$。円の中心の磁場。

**練習E9-C**：長さ $L$、$N$ 巻の有限ソレノイドの中心軸上の磁場を、円電流の重ね合わせで求めよ。$L\to\infty$ で $\mu_0nI$ になることを確認。

**略解**
E9-A：$dB = \frac{\mu_0I}{4\pi}\frac{r\,dz}{(r^2+z^2)^{3/2}}$ → $\frac{\mu_0I}{4\pi}\cdot\frac2r = \frac{\mu_0I}{2\pi r}$。
E9-B：半円部分 $\frac12\cdot\frac{\mu_0I}{2R} = \frac{\mu_0I}{4R}$、直線部分は中心を通る延長上なので寄与0。
E9-C：$B = \frac{\mu_0nI}{2}\left[\frac{L/2}{\sqrt{R^2+L^2/4}}\cdot2\right] = \mu_0nI\frac{L/2}{\sqrt{R^2+L^2/4}}\to\mu_0nI$。
