#!/bin/bash
# c51 review of c44 chemostat: wash_T 800 from t=12000 and the no-washout twin, fresh seed 2, 192^2, t=30000, noise 0.03
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261026T1819-c44-cips-chemostat-sighting/world.py; R=collective/contrib/20261027T0321-c51-review-cips-chemostat
WORLD_P='{"wash_T":800,"wash_t0":12000,"noise":0.03}' python -m labkit.run $W --out $R/W800s2 --seeds 2 --frames 300 --no-movie > $R/W800.log 2>&1 &
WORLD_P='{"noise":0.03}' python -m labkit.run $W --out $R/nowash_s2 --seeds 2 --frames 300 --no-movie > $R/nowash.log 2>&1
wait; echo done > $R/done.txt
