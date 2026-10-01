# HI4PI 水素柱密度マップ（Git管理外、*.fits で除外設定済み）

出典: HI4PI Collaboration (2016), A&A 594, A116
      "HI4PI: a full-sky HI survey based on EBHIS and GASS"

取得元: https://lambda.gsfc.nasa.gov/product/foreground/fg_hi4pi_get.html
ファイル: NHI_HPX.fits (578,924,544 bytes, HEALPix nside=1024, Galactic座標, RING順序)
取得日: 2026-07-13

用途: code/mcmc_fit_bin6_hi_proxy_check.py で「GALPROP gas成分の形状代用品」
      として使う探索的検証用。教授からのISRF+ガスリングデータ提供(2026-07-15予定)
      が実現すれば、この近似アプローチより正式なGALPROP再計算を優先する。

再現手順: 上記URLから同名ファイルをダウンロードし、このディレクトリに配置するだけ。
