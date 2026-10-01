#### ① 板書

**ガウスの法則**：$\displaystyle\oint\boldsymbol E\cdot d\boldsymbol S = \frac{Q_{\rm 内}}{\varepsilon_0}$。球対称なら $E(r)\cdot4\pi r^2 = Q_{\rm 内}(r)/\varepsilon_0$。**「半径 $r$ の球の中にある電荷」だけ数える。**

**電位**：$V(r) = \displaystyle\int_r^\infty E\,dr'$（無限遠を0）。外から内へ、領域ごとに積分をつなぐ。**電位は連続**（境界で値が一致することで検算できる）。

**一様な体積電荷（密度 $\rho$）**：半径 $r$ 内の電荷 $= \rho\cdot\frac43\pi r^3$。球殻 $a<r<b$ なら $\rho\cdot\frac43\pi(r^3 - a^3)$。

**導体の3原則**：①導体内部の電場は0　②導体は全体が等電位　③電荷は表面にだけ乗る。
**導体球殻の中に点電荷 $q_0$ があるとき**：内面に $-q_0$ が誘導される（内部の電場を0にするため）。外面の電荷 $=$（球殻に与えた総電荷）$-(-q_0)$。外側の電場は「全電荷」で決まる。

#### ② 過去問【上智 2026年春 問4-1・原文】

原点 $O$ を中心とする内径 $a$、外径 $b$ の厚みのある球殻が一様な電荷密度 $\rho$ で帯電している。
(1) (i) $r>b$　(ii) $a<r<b$　(iii) $r<a$ における電場の大きさ。
(2) 3つの領域の静電ポテンシャル。
(3) 原点中心・内径 $a$・外径 $b$ の導体球殻がある。原点に電気量 $-q$（$q>0$）の点電荷を固定したあと、導体球殻に電気量 $q$ を与えた。導体球殻内の電荷分布を説明せよ。
(4) (3)のとき、導体球殻の静電ポテンシャルを求めよ。

#### ③ 解説

**(1)** 全電荷 $Q = \dfrac{4\pi}{3}\rho(b^3 - a^3)$。
(i) $r>b$：$E = \dfrac{Q}{4\pi\varepsilon_0r^2} = \dfrac{\rho(b^3-a^3)}{3\varepsilon_0r^2}$。
(ii) $a<r<b$：中の電荷は $\frac43\pi\rho(r^3-a^3)$ → $E = \dfrac{\rho(r^3-a^3)}{3\varepsilon_0r^2}$。
(iii) $r<a$：中に電荷なし → $E = 0$。
検算：(ii)で $r=b$ とすると(i)と一致 ✓、$r=a$ で 0 になり(iii)と一致 ✓。

**(2)** 外から積分。
(i) $V = \dfrac{\rho(b^3-a^3)}{3\varepsilon_0r}$。
(ii) $V(r) = V(b) + \displaystyle\int_r^bE\,dr' = \frac{\rho(b^3-a^3)}{3\varepsilon_0b} + \frac{\rho}{3\varepsilon_0}\int_r^b\left(r' - \frac{a^3}{r'^2}\right)dr'$
$= \dfrac{\rho}{3\varepsilon_0}\left[b^2 - \dfrac{a^3}{b} + \dfrac{b^2-r^2}{2} + a^3\left(\dfrac1b - \dfrac1r\right)\right] = \dfrac{\rho}{3\varepsilon_0}\left[\dfrac{3b^2-r^2}{2} - \dfrac{a^3}{r}\right]$。
(iii) $r<a$：$E=0$ なので一定。$V = V(a) = \dfrac{\rho}{3\varepsilon_0}\left[\dfrac{3b^2-a^2}{2} - a^2\right] = \dfrac{\rho(b^2-a^2)}{2\varepsilon_0}$。
検算：(ii)で $r=b$ → $\frac{\rho}{3\varepsilon_0}(b^2 - a^3/b) = \frac{\rho(b^3-a^3)}{3\varepsilon_0b}$ ✓ (i)と一致。

**(3)** 原点の $-q$ が内面に **$+q$** を誘導する（導体内部の電場を0にするため）。球殻に与えた総電荷は $q$ なので、外面 $= q - (+q) = $ **0**。内面に $+q$ が一様に、外面には電荷なし。

**(4)** $r>b$ の電場は全電荷 $(-q) + q = 0$ で決まるので $E = 0$。よって $V(r\ge b) = 0$、導体は等電位なので導体球殻の電位は **0**。
（別解：$V(b) = \dfrac{(-q) + q}{4\pi\varepsilon_0b} = 0$）

> **落とし穴**：①(ii)の電位で「$r$ から $b$ まで」の積分に $a^3/r'^2$ の項を忘れる。②(3)で「外面に $q$」と書いてしまう（内面の $+q$ で使い切っている）。③導体の電位は外面の電荷だけで決まると思い込む——外面0でも内面と点電荷の寄与は互いに打ち消して0、が正しい説明。

#### ④ 練習問題

**練習E1-A**：半径 $R$ の一様帯電球（全電荷 $Q$）の内外の $E$ と $V$。$V(0)$ は $V(R)$ の何倍か。

**練習E1-B**：半径 $a$ の導体球（電荷 $Q$）を、内径 $b$・外径 $c$ の接地された導体球殻で囲む。各面の電荷と、$r<a$、$a<r<b$、$r>c$ の電位。

**練習E1-C**（球形コンデンサー）：内径 $a$・外径 $b$ の同心導体球殻に $\pm Q$。電位差と容量 $C$。

**略解**
E1-A：内 $E = \dfrac{Qr}{4\pi\varepsilon_0R^3}$、外 $\dfrac{Q}{4\pi\varepsilon_0r^2}$。$V(r<R) = \dfrac{Q}{8\pi\varepsilon_0R}\left(3 - \dfrac{r^2}{R^2}\right)$。$V(0) = \frac32V(R)$。
E1-B：内球 $+Q$、球殻内面 $-Q$、外面 0（接地）。$r>c$：$V=0$。$a<r<b$：$V = \dfrac{Q}{4\pi\varepsilon_0}\left(\dfrac1r - \dfrac1b\right)$。$r<a$：$V = \dfrac{Q}{4\pi\varepsilon_0}\left(\dfrac1a - \dfrac1b\right)$。
E1-C：$V = \dfrac{Q}{4\pi\varepsilon_0}\left(\dfrac1a - \dfrac1b\right)$、$C = \dfrac{4\pi\varepsilon_0ab}{b-a}$。
