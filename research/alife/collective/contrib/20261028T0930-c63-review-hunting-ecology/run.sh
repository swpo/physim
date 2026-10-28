#!/bin/bash
# c63 review of 20261026T2103-c46-hunting-ecology-claim (claim_world.py = its world.py; ctrl_world.py adds ycut_t)
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1
R=collective/contrib/20261028T0930-c63-review-hunting-ecology
python -m labkit.run $R/claim_world.py --out $R/rerun/seed81 --seeds 81 --frames 120 --lineage-k 5 --no-movie
WORLD_P='{"ycut_t":6000}' python -m labkit.run $R/ctrl_world.py --out $R/ctrl_yoff/seed81 --seeds 81 --frames 120 --lineage-k 5 --no-movie
