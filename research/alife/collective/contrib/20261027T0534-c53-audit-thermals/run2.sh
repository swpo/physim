#!/bin/bash
# c53 audit, part 2 (seed 31 died out, so the passive controls run on seed 32): passive thermal (A=0,h=0 from t=300),
# burn-off (A=0 from t=300), 1.5x grid seed 34, and a survival screen of the first 150 t on seeds 35-46
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
D=collective/contrib/20261027T0534-c53-audit-thermals; W=collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py; W2=$D/world.py
WORLD_P='{"fork2_t":300,"fork2":{"A":0,"h":0}}' python -m labkit.run $W2 --out $D/passive --seeds 32 --frames 450 --spf 25 --no-movie > $D/passive.log 2>&1
WORLD_P='{"fork2_t":300,"fork2":{"A":0}}' python -m labkit.run $W2 --out $D/noburn --seeds 32 --frames 450 --spf 25 --no-movie > $D/noburn.log 2>&1 &
WORLD_P='{"nu":0.675,"kT":0.225,"kY":4.5,"hyper":0.0050625,"g":0.75,"L":6.0,"dt":0.025}' python -m labkit.run $W --out $D/res15 --seeds 34 --size 192 192 --frames 600 --spf 40 --dt 0.025 --min-area 14 --no-movie > $D/res15.log 2>&1
wait
python -m labkit.run $W --out $D/screen --seeds 35 36 37 38 39 40 41 42 43 44 45 46 --frames 200 --spf 25 --no-movie > $D/screen.log 2>&1
echo ALLDONE
