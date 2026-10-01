
#### ⑤ 追加（上智 2025年春 問2-1・2025年秋 問2-2：レビ・チビタで示す恒等式）

**道具**：$\epsilon_{ijk}$（$123, 231, 312$ で $+1$、入れ替えで $-1$、同じ添え字があれば0）。$(\boldsymbol a\times\boldsymbol b)_i = \epsilon_{ijk}a_jb_k$、$(\nabla\times\boldsymbol A)_i = \epsilon_{ijk}\partial_jA_k$。**縮約公式** $\epsilon_{ijk}\epsilon_{ilm} = \delta_{jl}\delta_{km} - \delta_{jm}\delta_{kl}$（共通の添え字が1つのとき）。同じ添え字は和をとる。

**(A) 上智 2025年春 問2-1(1)**：$\nabla\cdot(\boldsymbol v\times\boldsymbol w) = \boldsymbol w\cdot(\nabla\times\boldsymbol v) - \boldsymbol v\cdot(\nabla\times\boldsymbol w)$ を示せ。
$\partial_i(\epsilon_{ijk}v_jw_k) = \epsilon_{ijk}(\partial_iv_j)w_k + \epsilon_{ijk}v_j(\partial_iw_k)$。第1項 $= w_k\,\epsilon_{kij}\partial_iv_j = \boldsymbol w\cdot(\nabla\times\boldsymbol v)$（$\epsilon_{ijk} = \epsilon_{kij}$、巡回）。第2項 $= v_j\,\epsilon_{ijk}\partial_iw_k = -v_j\,\epsilon_{jik}\partial_iw_k = -\boldsymbol v\cdot(\nabla\times\boldsymbol w)$（$i,j$ を入れ替えて符号反転）。∎

**(B) 上智 2025年春 問2-1(2)**：$\boldsymbol L = -i\boldsymbol r\times\nabla$、すなわち $L_i = -i\epsilon_{iab}x_a\partial_b$ のとき $(L_iL_j - L_jL_i)f = i\sum_k\epsilon_{ijk}L_kf$ を示せ。
$L_iL_jf = -\epsilon_{iab}\epsilon_{jcd}\,x_a\partial_b(x_c\partial_df) = -\epsilon_{iab}\epsilon_{jcd}\left(\delta_{bc}x_a\partial_df + x_ax_c\partial_b\partial_df\right)$。
第2項は $i\leftrightarrow j$（同時に $a\leftrightarrow c$、$b\leftrightarrow d$）で不変なので交換子では消える。第1項：$-\epsilon_{iab}\epsilon_{jbd}x_a\partial_df$。$\epsilon_{iab}\epsilon_{jbd} = \epsilon_{bia}\epsilon_{bdj} = \delta_{id}\delta_{aj} - \delta_{ij}\delta_{ad}$ より $= -x_j\partial_if + \delta_{ij}(x_a\partial_af)$。
よって $[L_i,L_j]f = (-x_j\partial_if + \delta_{ij}\boldsymbol r\cdot\nabla f) - (-x_i\partial_jf + \delta_{ij}\boldsymbol r\cdot\nabla f) = x_i\partial_jf - x_j\partial_if$。
一方 $i\epsilon_{ijk}L_kf = i\epsilon_{ijk}(-i)\epsilon_{kab}x_a\partial_bf = \epsilon_{kij}\epsilon_{kab}x_a\partial_bf = (\delta_{ia}\delta_{jb} - \delta_{ib}\delta_{ja})x_a\partial_bf = x_i\partial_jf - x_j\partial_if$。一致。∎
（これは量子力学の角運動量の交換関係 $[L_x,L_y] = iL_z$ そのものだが、問われているのは添え字の計算だけ）

**(C) 上智 2025年秋 問2-2**：$f = x^2\exp(yz)$。$\nabla f = (2xe^{yz},\ x^2ze^{yz},\ x^2ye^{yz})$。$\nabla\times\nabla f$：$x$ 成分 $= \partial_y(x^2ye^{yz}) - \partial_z(x^2ze^{yz}) = x^2e^{yz}(1 + yz) - x^2e^{yz}(1 + yz) = 0$。他も同様に0。$\nabla\times\nabla f = \boldsymbol 0$（勾配の回転は常に0。具体計算で確認させる問題）。

**練習M8-D**：$\epsilon_{ijk}\epsilon_{ijk} = 6$ を縮約公式から示せ。
**練習M8-E**：$(\boldsymbol a\times\boldsymbol b)\cdot(\boldsymbol c\times\boldsymbol d) = (\boldsymbol a\cdot\boldsymbol c)(\boldsymbol b\cdot\boldsymbol d) - (\boldsymbol a\cdot\boldsymbol d)(\boldsymbol b\cdot\boldsymbol c)$ を縮約公式で示せ。
略解：M8-D：$\epsilon_{ijk}\epsilon_{ijk} = \delta_{jj}\delta_{kk} - \delta_{jk}\delta_{kj} = 9 - 3 = 6$。M8-E：$\epsilon_{ijk}a_jb_k\epsilon_{ilm}c_ld_m = (\delta_{jl}\delta_{km} - \delta_{jm}\delta_{kl})a_jb_kc_ld_m$。
