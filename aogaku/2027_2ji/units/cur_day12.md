#### ① 板書

**原則**：質量が変わる系では $F = ma$ ではなく**運動量の変化** $\dfrac{d\boldsymbol p}{dt} = \boldsymbol F_{\rm ext}$ を使う。ただし「系」の取り方を固定して、**出入りする質量が持ち去る（持ち込む）運動量を数える。**

**ロケット**：時刻 $t$ に質量 $M(t)$、速度 $V(t)$。$dt$ の間に質量 $dm = \alpha\,dt$ をロケットに対して速さ $v$ で後方へ放出。
- $t$：運動量 $MV$
- $t + dt$：ロケット $(M - dm)(V + dV)$ ＋ 燃料 $dm(V - v)$
- 外力なしで等置し、2次の微小量を落とす：$M\,dV = v\,dm$
$$M\frac{dV}{dt} = \alpha v \quad(\text{推力} = \alpha v), \qquad M(t) = M_0 - \alpha t$$
$$V(t) = V_0 + v\ln\frac{M_0}{M(t)} \quad(\text{ツィオルコフスキーの式})$$

**鎖**：机の端から垂れた長さ $s$、線密度 $\lambda$。垂れた部分だけを系とすると、机上から質量 $\lambda\,ds$ が速度0で流入。
$$\frac{d}{dt}(\lambda sv) = \lambda sg$$
$\dfrac{d}{dt} = v\dfrac{d}{ds}$ に直して $s$ で積分するのが定石。

#### ② 過去問

**(A) 立教 2025年夏 大問1**：重力・抵抗のない宇宙空間で速さ $V_0$ で等速直線運動しているロケットが $t = 0$ から加速。時刻 $t$ の質量 $M(t)$、速さ $V(t)$。燃料はロケットに対して一定の速さ $v$ で逆向きに、1秒あたり一定質量 $\alpha = -dM/dt$ で噴出。
(a) $M(t)$ を求めよ。(b) $V$ の従う微分方程式を導け。(c) $V(t)$ を求めよ。(d) 質量が半分になったときの速さ。

**(B) 上智 2026年春 問3-2**：線密度 $\lambda$ の鎖が机の端に静止。わずかに押すと落下開始。垂れた長さ $s$、速さ $v$。空気抵抗なし。
(1) 垂れた部分の運動方程式を書け。(2) $v$ と $s$ の関係を求めよ。$\dfrac{d}{dt} = \dfrac{ds}{dt}\dfrac{d}{ds}$、$2sv\dfrac{d}{ds}(sv) = \dfrac{d}{ds}(sv)^2$ を使ってよい。(3) 長さ $s$ になるまでに失った力学的エネルギー。

#### ③ 解説

**(A)**
(a) $M(t) = M_0 - \alpha t$。
(b) 板書の導出通り $M\dfrac{dV}{dt} = \alpha v$。
(c) $\dfrac{dV}{dt} = \dfrac{\alpha v}{M_0 - \alpha t}$。積分：$V - V_0 = -v\ln(M_0 - \alpha t) + v\ln M_0 = v\ln\dfrac{M_0}{M_0 - \alpha t}$。
(d) $M = M_0/2$：$V = V_0 + v\ln 2$。

**(B)**
(1) 垂れた部分の運動量 $\lambda sv$、重力 $\lambda sg$：$\dfrac{d}{dt}(\lambda sv) = \lambda sg$、すなわち $\dfrac{d(sv)}{dt} = sg$。
(2) $\dfrac{d(sv)}{dt} = v\dfrac{d(sv)}{ds} = sg$。両辺に $2sv$ をかけると $\dfrac{d}{ds}(sv)^2 = 2gs^2$。積分（$s = 0$ で $v = 0$）：$(sv)^2 = \dfrac{2gs^3}{3}$ → $v^2 = \dfrac{2gs}{3}$。
（自由落下なら $v^2 = 2gs$。鎖は机上の部分を引きずるので遅い）
(3) 運動エネルギー $\frac12\lambda s\cdot v^2 = \frac12\lambda s\cdot\frac{2gs}{3} = \dfrac{\lambda gs^2}{3}$。失った位置エネルギー：垂れた部分の重心が $s/2$ 下がったので $\lambda sg\cdot\frac{s}{2} = \dfrac{\lambda gs^2}{2}$。差 $\dfrac{\lambda gs^2}{2} - \dfrac{\lambda gs^2}{3} = \dfrac{\lambda gs^2}{6}$ が失われた（机の端での非弾性的な引き込み）。

#### ④ 確認問題

**確認3-A**：雨滴が落下しながら霧を取り込み質量が増える。$\dfrac{dm}{dt} = km$（$k$ 定数）、霧は静止。重力のみ。(a) 運動方程式を書け。(b) 終端速度があるか。あれば求めよ。

**確認3-B**：ロケットが地表から鉛直に打ち上がる（重力 $g$ 一定、空気抵抗なし）。$M\dfrac{dV}{dt} = \alpha v - Mg$ を導き、$V(t)$ を求めよ。離陸の条件は何か。

**略解**
3-A：$\dfrac{d(mv)}{dt} = mg$ → $m\dot v + kmv = mg$ → $\dot v = g - kv$。終端速度 $g/k$。
3-B：$V = v\ln\dfrac{M_0}{M_0 - \alpha t} - gt$。離陸には $\alpha v > M_0g$。

---
