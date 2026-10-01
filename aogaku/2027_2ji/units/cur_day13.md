#### 要点

固定するもの：$T, V, \mu$。出発点：**大分配関数**
$$\Xi = \sum_{N=0}^\infty e^{\beta\mu N}Z_N = \sum_{\text{全状態}}e^{-\beta(E - \mu N)}$$
ポテンシャル：$\Omega = -k_BT\ln\Xi = F - \mu N = -pV$。
$$\langle N\rangle = -\left(\frac{\partial\Omega}{\partial\mu}\right)_{T,V} = k_BT\frac{\partial\ln\Xi}{\partial\mu}, \qquad S = -\left(\frac{\partial\Omega}{\partial T}\right)_{V,\mu}, \qquad p = -\frac{\Omega}{V}$$

**独立粒子系での分解**：1粒子状態 $r$（エネルギー $\epsilon_r$）ごとに独立なので
$$\Xi = \prod_r\xi_r, \qquad \xi_r = \sum_{n_r}e^{-\beta(\epsilon_r - \mu)n_r}$$
- フェルミ（$n_r = 0, 1$）：$\xi_r = 1 + e^{-\beta(\epsilon_r-\mu)}$
- ボース（$n_r = 0, 1, 2, \ldots$）：$\xi_r = \dfrac{1}{1 - e^{-\beta(\epsilon_r-\mu)}}$

**占有数** $\langle n_r\rangle = -\dfrac{\partial\ln\xi_r}{\partial(\beta\epsilon_r)} = \dfrac{1}{e^{\beta(\epsilon_r-\mu)} \pm 1}$（＋フェルミ、−ボース）


#### 問3-1 ★ フェルミ分布・ボース分布の導出（立教2023春 大問4）


理想量子気体。分配関数 $Z(\beta, V, N) = \sum_{\{n_i\}}\exp(-\beta\sum_i n_i\epsilon_i)$、$\sum n_i = N$。

(1) 大分配関数 $\Xi(\beta, V, \mu) = \sum_N Z(\beta,V,N)e^{\beta\mu N}$ がフェルミ粒子で $\Xi = \prod_i[1 + e^{-\beta(\epsilon_i - \mu)}]$ となることを示せ。
(2) 1粒子状態 $i$ の粒子数の期待値 $\langle n_i\rangle$ を求め、十分低温での $\epsilon_i$ 依存性を図示せよ。
(3) 1粒子のエネルギーが $\epsilon = c|\boldsymbol p|$（光速 $c$）で与えられる相対論的粒子について、状態密度 $D(\epsilon)$ とフェルミエネルギー $\epsilon_F$ を求めよ（スピン縮退なし）。
(4) ボース粒子について $\Xi$ を求め、$\mu$ の上限を答えよ。$\langle n_i\rangle$ も求めよ。

**解答**

(1) $\sum_N e^{\beta\mu N}\sum_{\{n_i\},\sum n_i=N} = \sum_{\{n_i\}}$（$N$ の制約が外れる）。よって
$$\Xi = \sum_{\{n_i\}}\prod_i e^{-\beta(\epsilon_i-\mu)n_i} = \prod_i\sum_{n_i=0}^{1}e^{-\beta(\epsilon_i-\mu)n_i} = \prod_i\left[1 + e^{-\beta(\epsilon_i-\mu)}\right]$$

(2) $\langle n_i\rangle = \dfrac{1}{\Xi}\sum n_ie^{\cdots} = -\dfrac{1}{\beta}\dfrac{\partial\ln\Xi}{\partial\epsilon_i} = \dfrac{e^{-\beta(\epsilon_i-\mu)}}{1 + e^{-\beta(\epsilon_i-\mu)}} = \dfrac{1}{e^{\beta(\epsilon_i-\mu)} + 1}$。
低温：$\epsilon < \mu$ で 1、$\epsilon > \mu$ で 0 の階段。幅 $\sim k_BT$ でなまる。

(3) 状態数 $= \dfrac{V}{h^3}4\pi p^2dp$、$p = \epsilon/c$：$D(\epsilon) = \dfrac{4\pi V\epsilon^2}{h^3c^3}$。$T = 0$ で $N = \int_0^{\epsilon_F}D\,d\epsilon = \dfrac{4\pi V\epsilon_F^3}{3h^3c^3}$ より
$$\epsilon_F = hc\left(\frac{3n}{4\pi}\right)^{1/3}, \quad n = N/V$$

(4) $\xi_i = \sum_{n=0}^\infty e^{-\beta(\epsilon_i-\mu)n} = \dfrac{1}{1 - e^{-\beta(\epsilon_i-\mu)}}$。収束条件 $\epsilon_i - \mu > 0$ が全 $i$ で必要 → **$\mu < \epsilon_0$（最低準位）**。$\Xi = \prod_i[1 - e^{-\beta(\epsilon_i-\mu)}]^{-1}$、$\langle n_i\rangle = \dfrac{1}{e^{\beta(\epsilon_i-\mu)} - 1}$。


#### 問3-2 ☆ 表面吸着（立教2019夏 大問4）


理想気体（問2-5）が吸着面に接する。吸着サイトが $M$ 個あり、各サイトは粒子0個か1個（吸着エネルギー $-\epsilon_0$）。気体と吸着面で $\mu$ が等しい。

(1) 吸着面の大分配関数 $\Xi_{\rm ads}$ を求めよ。
(2) 吸着粒子数 $N_{\rm ads}$ を $\mu$ で表せ。
(3) 気体の $\mu = k_BT\ln(n\lambda^3)$ を使い、被覆率 $\theta = N_{\rm ads}/M$ を気体の圧力 $p$ で表せ（ラングミュアの吸着等温式）。

**解答**

(1) 各サイトは独立な2状態：$\xi = 1 + e^{\beta(\epsilon_0 + \mu)}$、$\Xi_{\rm ads} = \xi^M$。

(2) $N_{\rm ads} = k_BT\dfrac{\partial\ln\Xi}{\partial\mu} = M\dfrac{e^{\beta(\epsilon_0+\mu)}}{1 + e^{\beta(\epsilon_0+\mu)}}$。

(3) $e^{\beta\mu} = n\lambda^3 = \dfrac{p\lambda^3}{k_BT}$（$p = nk_BT$）。$\theta = \dfrac{p\lambda^3e^{\beta\epsilon_0}/k_BT}{1 + p\lambda^3e^{\beta\epsilon_0}/k_BT} = \dfrac{p}{p + p_0(T)}$、$p_0 = \dfrac{k_BT}{\lambda^3}e^{-\beta\epsilon_0}$。

---
