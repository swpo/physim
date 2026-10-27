#!/bin/bash
# c53 review of 20261026T2119-c46-hunting-ecology-dthalf: fresh seed 4 at the claim's dt 0.2 and at dt 0.1 (the finding's
# world.py), 128^2, t=12000, --lineage-k 5, and a second fresh seed 6 for both
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1
R=collective/contrib/20261027T0918-c53-review-hunting-dthalf
python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out $R/base --seeds 4 6 --frames 120 --lineage-k 5 --no-movie > $R/base.log 2>&1 &
python -m labkit.run collective/contrib/20261026T2119-c46-hunting-ecology-dthalf/world.py --out $R/dthalf --seeds 4 --frames 120 --lineage-k 5 --no-movie > $R/dthalf4.log 2>&1 &
python -m labkit.run collective/contrib/20261026T2119-c46-hunting-ecology-dthalf/world.py --out $R/dthalf6 --seeds 6 --frames 120 --lineage-k 5 --no-movie > $R/dthalf6.log 2>&1 &
wait; echo ALLDONE
