#!/bin/bash
# c53 review of 20261026T2102-c48-cips-fuel-powered-division: fresh seed 7, fuel-powered world (defaults) and the matched
# fuel-independent reactivation control (react_const 1), 192^2, t=12000 (labkit, as the finding)
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
R=collective/contrib/20261027T0903-c53-review-cips-fuel-division; W=collective/contrib/20261026T2102-c48-cips-fuel-powered-division/world.py
python -m labkit.run $W --out $R/pack --seeds 7 --frames 120 --no-movie > $R/pack.log 2>&1 &
WORLD_P='{"react_const":1}' python -m labkit.run $W --out $R/pack_const --seeds 7 --frames 120 --no-movie > $R/pack_const.log 2>&1
wait; echo ALLDONE
