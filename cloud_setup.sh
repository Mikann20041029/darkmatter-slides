#!/bin/bash
# クラウドセッションで計算する前に 1 回だけ実行する。
#   1. 日本語フォントを本人の PC と同じ絶対パスに置く
#      (code/ の 40 本以上が /home/arsei/.local/share/fonts/NotoSansCJKjp-Regular.otf を直接読むため)
#   2. 本人の PC と同じバージョンのパッケージを入れる
#   3. data_bundle/ から大きいデータを復元し SHA256 で検証する
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE"

FONT_DIR=/home/arsei/.local/share/fonts
if [ ! -f "$FONT_DIR/NotoSansCJKjp-Regular.otf" ]; then
  if mkdir -p "$FONT_DIR" 2>/dev/null; then
    cp cloud_setup/NotoSansCJKjp-Regular.otf "$FONT_DIR/"
  else
    sudo mkdir -p "$FONT_DIR" && sudo cp cloud_setup/NotoSansCJKjp-Regular.otf "$FONT_DIR/"
  fi
fi
echo "font: OK"

python3 -m pip install -q -r cloud_setup/requirements.txt \
  || { echo "pinned install failed; installing unpinned"; \
       python3 -m pip install -q numpy scipy pandas astropy emcee healpy matplotlib pymupdf; }
python3 -c "import numpy, scipy, pandas, astropy, emcee, healpy, matplotlib; print('packages: OK', 'numpy', numpy.__version__)"

bash restore_data.sh
echo "setup done. 例: MCMC_ULTRACLEAN=1 MCMC_PIXEL_DEG=0.125 MCMC_DISK_BUBBLE=1 MCMC_CELL_LIKELIHOOD=1 MCMC_SIGNFREE_HALO=1 MCMC_SKIP_MCMC=1 MCMC_BINS=6 MCMC_ALLBINS_OUTDIR=/tmp/test python3 code/mcmc_fit_all_bins.py"
