#!/bin/bash
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261026T1819-c44-cips-chemostat-sighting/world.py; R=collective/contrib/20261027T0313-c49-review-chemostat
WORLD_P='{"wash_T":800,"wash_t0":12000,"noise":0.03}' python -m labkit.run $W --out $R/W800s2 --seeds 2 --frames 300 --no-movie > $R/a.log 2>&1 &
WORLD_P='{"wash_T":-1,"noise":0.03}' python -m labkit.run $W --out $R/nowash_s2 --seeds 2 --frames 300 --no-movie > $R/b.log 2>&1
wait; echo ALLDONE
