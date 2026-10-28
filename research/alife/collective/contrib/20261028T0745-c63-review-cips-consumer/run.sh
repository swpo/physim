#!/bin/bash
# c63 review of 20261026T1700-c43-cips-consumer (claim_world.py = its world.py unchanged; ctrl_world.py adds y2cut_t)
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1
R=collective/contrib/20261028T0745-c63-review-cips-consumer
python -m labkit.run $R/claim_world.py --out $R/rerun/seed71 --seeds 71 --frames 120 --lineage-k 5 --no-movie   # non-finite at frame 1 (run71_nonfinite.log), deleted
python -m labkit.run $R/claim_world.py --out $R/rerun/seed72 --seeds 72 --frames 120 --lineage-k 5 --no-movie
WORLD_P='{"y2cut_t":3000}' python -m labkit.run $R/ctrl_world.py --out $R/ctrl_y2off/seed72 --seeds 72 --frames 120 --lineage-k 5 --no-movie
python collective/contrib/20261027T1146-c55-pairtest-tool/pairtest.py $R/rerun/seed72 $R/claim_world.py $R/analysis/pairtest_s72.json --host 0 --guest 1 --K 5 --dtf 100 --L 20
