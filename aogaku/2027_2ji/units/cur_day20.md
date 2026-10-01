#### 問5-1 ★ エネルギー揺らぎと熱容量


カノニカル分布で $\langle(\Delta E)^2\rangle = \langle E^2\rangle - \langle E\rangle^2 = k_BT^2C_V$ を示せ。

**解答**

$\langle E\rangle = -\dfrac{\partial\ln Z}{\partial\beta}$。$\dfrac{\partial\langle E\rangle}{\partial\beta} = -\dfrac{\partial^2\ln Z}{\partial\beta^2} = -\left[\dfrac{1}{Z}\dfrac{\partial^2Z}{\partial\beta^2} - \left(\dfrac{1}{Z}\dfrac{\partial Z}{\partial\beta}\right)^2\right] = -(\langle E^2\rangle - \langle E\rangle^2)$。
一方 $\dfrac{\partial\langle E\rangle}{\partial\beta} = \dfrac{\partial\langle E\rangle}{\partial T}\dfrac{dT}{d\beta} = -k_BT^2C_V$。よって $\langle(\Delta E)^2\rangle = k_BT^2C_V$。
相対揺らぎ $\sqrt{\langle(\Delta E)^2\rangle}/\langle E\rangle \propto 1/\sqrt N$。


#### 問5-2 ★ ギブス・デュエムと圧縮率（都立2026冬 物理学II[2] 問2）


ギブス・デュエムの関係 $-SdT + Vdp - Nd\mu = 0$ を用いて
$$\left(\frac{\partial\mu}{\partial N}\right)_{T,V} = \frac{V}{N^2}\frac{1}{\kappa}, \qquad \kappa = -\frac{1}{V}\left(\frac{\partial V}{\partial p}\right)_{T,N}$$
を示せ。$p$ の $N, V$ 依存性は密度 $n = N/V$ を通してのみ。

**解答**

$T$ 一定：$Vdp = Nd\mu$ → $\left(\dfrac{\partial\mu}{\partial p}\right)_T = \dfrac{V}{N} = \dfrac{1}{n}$。
$p = p(n)$ なので $\left(\dfrac{\partial p}{\partial N}\right)_{T,V} = \dfrac{dp}{dn}\cdot\dfrac{1}{V}$。
圧縮率：$V = N/n$ より $\left(\dfrac{\partial V}{\partial p}\right)_{T,N} = -\dfrac{N}{n^2}\dfrac{dn}{dp}$、$\kappa = \dfrac{N}{Vn^2}\dfrac{dn}{dp} = \dfrac{1}{n}\dfrac{dn}{dp}$。よって $\dfrac{dp}{dn} = \dfrac{1}{n\kappa}$。
$$\left(\frac{\partial\mu}{\partial N}\right)_{T,V} = \left(\frac{\partial\mu}{\partial p}\right)_T\left(\frac{\partial p}{\partial N}\right)_{T,V} = \frac{1}{n}\cdot\frac{1}{V}\cdot\frac{1}{n\kappa} = \frac{1}{Nn\kappa} = \frac{V}{N^2\kappa}$$


#### 問5-3 ☆ イジング模型の平均場近似（立教2018夏 大問4）


$i$ 番目のスピン（$\sigma_i = \pm1$）のハミルトニアン $\hat H_i = -Jz\langle\sigma\rangle\sigma_i - \mu H\sigma_i$。$z$ は隣接数、$\langle\sigma\rangle$ は自己無撞着に決める平均場。

(1) 1スピンの分配関数と $\langle\sigma\rangle$ の自己無撞着方程式を書け。
(2) $H = 0$ で $\langle\sigma\rangle \ne 0$ の解が存在する温度 $T_c$ を求めよ。
(3) $T > T_c$、$H \to 0$ での磁化率 $\chi = \partial\langle\sigma\rangle/\partial H$ を求めよ（キュリー・ワイス）。

**解答**

(1) 有効磁場 $h = Jz\langle\sigma\rangle + \mu H$。$z_1 = 2\cosh(\beta h)$、$\langle\sigma\rangle = \tanh\left[\beta(Jz\langle\sigma\rangle + \mu H)\right]$。

(2) $H = 0$：$m = \tanh(\beta Jzm)$。$m \ne 0$ の解は $\tanh$ の原点での傾き $\beta Jz > 1$ のとき存在。$T_c = Jz/k_B$。

(3) $m$ 小で $\tanh x \simeq x$：$m \simeq \beta(Jzm + \mu H)$ → $m(1 - \beta Jz) = \beta\mu H$ → $\chi = \dfrac{\mu}{k_B(T - T_c)}$。$T_c$ で発散。


#### 問5-4 ☆ 1次元リング格子と転送行列（立教2025春 大問4）


$L$ 個の格子点が環状。区別できない粒子、各格子に高々1個、隣接不可。$N$ 個の配置数を $Z_{L,N}$、$\Xi_L(x) = \sum_N Z_{L,N}x^N$。

(1) $Z_{4,2}$ を求めよ。
(2) $\Xi_4(x)$ を求めよ。
(3) $L \ge 3$ で $Z_{L,2}$ を $L$ で表せ。
(4) $t_{n,n'} = x^{(n+n')/2}(1 - nn')$ を成分とする転送行列 $T$ で $\Xi_L = \mathrm{Tr}\,T^L$ と書けることを用い、$\Xi_L$ を $x, L$ で表せ。
(5) $F(x) = \lim_{L\to\infty}\dfrac{1}{L}\ln\Xi_L$ の $F(1)$ を求めよ。

**解答**

(1) 4点の環で隣接しない2点：$\{1,3\}, \{2,4\}$ の2通り。$Z_{4,2} = 2$。

(2) $Z_{4,0} = 1$、$Z_{4,1} = 4$、$Z_{4,2} = 2$、$Z_{4,3} = Z_{4,4} = 0$。$\Xi_4 = 1 + 4x + 2x^2$。

(3) 全ペア $\binom L2$ から隣接ペア $L$ 個を引く：$Z_{L,2} = \dfrac{L(L-1)}{2} - L = \dfrac{L(L-3)}{2}$。

(4) $T = \begin{pmatrix}1 & \sqrt x\\ \sqrt x & 0\end{pmatrix}$（$n, n' \in \{0, 1\}$）。固有値 $\lambda_\pm = \dfrac{1 \pm\sqrt{1+4x}}{2}$。$\Xi_L = \lambda_+^L + \lambda_-^L$。
検算：$L = 4$ で $\lambda_+^4 + \lambda_-^4 = (\lambda_+^2+\lambda_-^2)^2 - 2(\lambda_+\lambda_-)^2$、$\lambda_+ + \lambda_- = 1$、$\lambda_+\lambda_- = -x$ より $\lambda_+^2 + \lambda_-^2 = 1 + 2x$、$\Xi_4 = (1+2x)^2 - 2x^2 = 1 + 4x + 2x^2$ ✓

(5) $|\lambda_+| > |\lambda_-|$ なので $\Xi_L \simeq \lambda_+^L$、$F(x) = \ln\lambda_+(x)$。$F(1) = \ln\dfrac{1+\sqrt5}{2} \simeq 0.481$（黄金比の対数）。
