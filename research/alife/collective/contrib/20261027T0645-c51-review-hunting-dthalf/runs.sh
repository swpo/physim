#!/bin/bash
# c51 review of c46 dt/2 check: the claim's world (dt 0.2) and the finding's dt 0.1 world, fresh seed 17, 128^2, t=12000, --lineage-k 5
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2; R=collective/contrib/20261027T0645-c51-review-hunting-dthalf
python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out $R/base_s17 --seeds 17 --frames 120 --lineage-k 5 --no-movie > $R/base.log 2>&1 &
python -m labkit.run collective/contrib/20261026T2119-c46-hunting-ecology-dthalf/world.py --out $R/dthalf_s17 --seeds 17 --frames 120 --lineage-k 5 --no-movie > $R/dthalf.log 2>&1
wait; echo done > $R/done.txt
