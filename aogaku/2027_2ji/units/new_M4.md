#### ① 板書

**やりたいこと**：実数の積分 $\displaystyle\int_{-\infty}^\infty f(x)dx$ を、複素平面で「閉じた道」を一周する積分に置き換えて楽に出す。

**道具は3つ**

1. **極**：分母がゼロになる点 $z_0$。$f(z)$ がそこで無限大に飛ぶ。
2. **留数** $\mathrm{Res}(z_0)$：極のまわりでの「爆発の強さ」。分母が1回だけゼロになる**単純極**なら
$$\mathrm{Res}(z_0) = \frac{\text{分子}}{(\text{分母})'}\Big|_{z=z_0}$$

3. **留数定理**：閉じた道 $C$ を反時計回りに一周すると
$$\oint_C f(z)dz = 2\pi i\sum(\text{C の内側の極の留数})$$

**半円の道（最頻）**：実軸 $-R\to R$（$C_1$）＋上半円弧（$C_2$）。$R\to\infty$ で $\int_{C_1}\to$ 求めたい積分、$\int_{C_2}\to0$（分母の次数が分子より2以上大きければ消える。1だけ大きいときはジョルダンの補題：$e^{imz}$（$m>0$）が付いていれば上半面で消える）。よって
$$\int_{-\infty}^\infty f(x)dx = 2\pi i\sum(\text{上半面の留数})$$

**$n$乗根**：$z^n = -1 = e^{i\pi}$ → $z = e^{i(\pi + 2\pi k)/n}$（$k = 0,\ldots,n-1$）。角度を $n$ で割って $360°/n$ ずつ回す。

**三角関数の積分（0〜2π）**：$z = e^{i\theta}$ とおくと $\cos\theta = \dfrac{z + 1/z}{2}$、$d\theta = \dfrac{dz}{iz}$、道は単位円一周。

**$\sin$ や $\cos$ が分子にあるとき**：$e^{imx}$ の虚部・実部として計算し、最後に $\mathrm{Im}$ / $\mathrm{Re}$ を取る。

#### ② 過去問

**(A) 上智 2026年秋 問2**：$f(x) = \dfrac{x^2}{1+x^4}$ に対する積分 $\int_{-\infty}^\infty f(x)dx$ を複素積分で求める。$z = x + iy$。

1. 十分大きな $R$ で、$C_1$（$-R\le x\le R$）と $C_2$（上半面の半径 $R$ の半円弧）からなる積分路 $C$ を考える。$C$ の中にある極の座標をすべて求めよ。
2. 各極における留数を求めよ。
3. $\int_{C_2}f(z)dz$ を極形式で表せ。
4. 3の結果を用いて $\lim_{R\to\infty}\int_{C_2}f(z)dz = 0$ を示せ。
5. 4の結果を用いて $\int_{-\infty}^\infty f(x)dx = \lim_{R\to\infty}\int_Cf(z)dz$ を求めよ。

**(B) 上智 2025年春 問2-2**：留数定理を利用して次の定積分を求めよ。
(1) $\displaystyle\int_0^\infty\frac{x\sin mx}{x^2+a^2}dx$（$a, m > 0$）　(2) $\displaystyle\int_0^\pi\frac{d\theta}{a + b\cos\theta}$（$a > b > 0$、ヒント：$z = e^{i\theta}$）

#### ③ 解説

**(A)**

1. $1 + z^4 = 0$ → $z^4 = -1 = e^{i\pi}$ → $z = e^{i\pi/4}, e^{i3\pi/4}, e^{i5\pi/4}, e^{i7\pi/4}$（45°, 135°, 225°, 315°）。上半面は **$z_1 = e^{i\pi/4} = \dfrac{1+i}{\sqrt2}$、$z_2 = e^{i3\pi/4} = \dfrac{-1+i}{\sqrt2}$**。
2. 単純極：$\mathrm{Res} = \dfrac{z^2}{4z^3} = \dfrac{1}{4z}$。$\mathrm{Res}(z_1) = \frac14e^{-i\pi/4}$、$\mathrm{Res}(z_2) = \frac14e^{-i3\pi/4}$。和：$\frac14\left[\frac{1-i}{\sqrt2} + \frac{-1-i}{\sqrt2}\right] = \frac14\cdot\frac{-2i}{\sqrt2} = -\dfrac{i}{2\sqrt2}$。
3. $z = Re^{i\theta}$（$\theta: 0\to\pi$）、$dz = iRe^{i\theta}d\theta$：$\displaystyle\int_{C_2} = \int_0^\pi\frac{R^2e^{2i\theta}}{1 + R^4e^{4i\theta}}\,iRe^{i\theta}d\theta$。
4. $|1 + R^4e^{4i\theta}| \ge R^4 - 1$ なので $\left|\int_{C_2}\right| \le \pi\cdot\dfrac{R^3}{R^4 - 1}\to0$。分子3次・分母4次だから消える。
5. $\oint_C = 2\pi i\cdot\left(-\dfrac{i}{2\sqrt2}\right) = \dfrac{\pi}{\sqrt2}$。$C_2$ が消えるので **$\displaystyle\int_{-\infty}^\infty\frac{x^2}{1+x^4}dx = \frac{\pi}{\sqrt2}$**。
検算：被積分関数は正 ✓。$\pi/\sqrt2\simeq2.2$、$x^2/(1+x^4)$ は最大値 $1/2$（$x=1$）で幅2くらい → 2前後は妥当 ✓。

**(B)(1)** $\sin mx = \mathrm{Im}\,e^{imx}$。偶関数なので $\displaystyle\int_0^\infty = \frac12\int_{-\infty}^\infty$。$g(z) = \dfrac{ze^{imz}}{z^2+a^2}$ の上半面の極は $z = ia$ だけ。$\mathrm{Res}(ia) = \dfrac{ia\,e^{-ma}}{2ia} = \dfrac{e^{-ma}}{2}$。$m > 0$ なので上半円弧はジョルダンの補題で消える。$\displaystyle\int_{-\infty}^\infty g\,dx = 2\pi i\cdot\frac{e^{-ma}}{2} = \pi ie^{-ma}$。虚部をとって半分：**$\dfrac{\pi}{2}e^{-ma}$**。
検算：$m\to\infty$ で振動が激しくなり積分は 0 に → $e^{-ma}\to0$ ✓。

**(B)(2)** $\cos\theta$ は偶関数なので $\displaystyle\int_0^\pi = \frac12\int_0^{2\pi}$。$z = e^{i\theta}$：$\cos\theta = \dfrac{z+z^{-1}}{2}$、$d\theta = \dfrac{dz}{iz}$。
$$\int_0^{2\pi}\frac{d\theta}{a + b\cos\theta} = \oint_{|z|=1}\frac{1}{a + \frac b2(z + z^{-1})}\frac{dz}{iz} = \oint\frac{2\,dz}{i(bz^2 + 2az + b)}$$
極：$bz^2 + 2az + b = 0$ → $z_\pm = \dfrac{-a\pm\sqrt{a^2-b^2}}{b}$。$|z_+| < 1$、$|z_-| > 1$（積が1で $|z_-| > 1$）。単位円内は $z_+$ だけ。$\mathrm{Res}(z_+) = \dfrac{2}{i\cdot b(z_+ - z_-)} = \dfrac{2}{i\cdot2\sqrt{a^2-b^2}} = \dfrac{1}{i\sqrt{a^2-b^2}}$。
$\oint = 2\pi i\cdot\dfrac{1}{i\sqrt{a^2-b^2}} = \dfrac{2\pi}{\sqrt{a^2-b^2}}$。半分にして **$\dfrac{\pi}{\sqrt{a^2-b^2}}$**。
検算：$b\to0$ で $\int_0^\pi d\theta/a = \pi/a$ ✓。

> **落とし穴**：①「上半面の極だけ」を足す。下半面を足すと符号がおかしくなる。②$n$乗根の角度は $(\pi + 2\pi k)/n$。$k=0$ の $\pi/n$ だけ出して終わらない。③(B)(2)で $|z_-| > 1$ を言わずに両方足すと0になる。

#### ④ 練習問題

**練習M4-A**：$\displaystyle\int_{-\infty}^\infty\frac{dx}{1+x^2}$ を留数定理で求めよ（答えは $\pi$ になるはず）。

**練習M4-B**：$\displaystyle\int_{-\infty}^\infty\frac{dx}{1+x^4}$ を求めよ（(A)と同じ極。留数は $1/(4z^3)$）。

**練習M4-C**：$\displaystyle\int_0^{2\pi}\frac{d\theta}{2 + \sin\theta}$ を $z = e^{i\theta}$、$\sin\theta = \dfrac{z - z^{-1}}{2i}$ で求めよ。

**練習M4-D**：$\displaystyle\int_{-\infty}^\infty\frac{\cos x}{x^2+1}dx$ を求めよ。

**略解**
M4-A：極 $z = i$。$\mathrm{Res} = 1/(2i)$。$2\pi i/(2i) = \pi$。
M4-B：$\mathrm{Res}(z) = 1/(4z^3) = z/(4z^4) = -z/4$（$z^4 = -1$）。和 $= -\frac14(z_1 + z_2) = -\frac14\cdot\frac{2i}{\sqrt2} = -\frac{i}{2\sqrt2}$。答え $\pi/\sqrt2$（偶然(A)と同じ値）。
M4-C：$\oint\dfrac{2\,dz}{z^2 + 4iz - 1}$。極 $z = -2i\pm i\sqrt3$、内側は $z = (-2+\sqrt3)i$。$\mathrm{Res} = \dfrac{2}{2z + 4i}\big|_{z_+} = \dfrac{1}{i\sqrt3}$。答え $\dfrac{2\pi}{\sqrt3}$。
M4-D：$e^{iz}/(z^2+1)$、極 $i$、$\mathrm{Res} = e^{-1}/(2i)$。$2\pi i\cdot e^{-1}/(2i) = \pi/e$。実部をとって $\pi/e$。
