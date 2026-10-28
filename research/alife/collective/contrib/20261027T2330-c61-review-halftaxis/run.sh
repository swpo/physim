#!/bin/bash
# c61 review of 20261027T2013-c60-halftaxis-ecology (from research/alife)
export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
R=collective/contrib/20261027T2013-c60-halftaxis-ecology; O=collective/contrib/20261027T2330-c61-review-halftaxis
python -m labkit.run $R/world.py --seeds 31 --size 256 256 --frames 120 --no-movie --lineage-k 20 --out $O/rerun/seed31
python $R/tools/indiv.py $O/rerun/seed31 $O/rerun/indiv_s31.json
(cd $R && python tools/predlineage.py ../20261027T2330-c61-review-halftaxis/rerun/seed31 1 ../20261027T2330-c61-review-halftaxis/rerun/pred_ancestry_s31.png)
python $R/controls/kdarms/spin.py 71 6000 st_71.npz          # fresh 128^2 state at t=6000
cd $O/controls; for a in ctrl kdlocal k2local; do python kdarms.py ../../../../st_71.npz 71 $a ${a}_s71.json --T 3000; done; python fig.py 71
