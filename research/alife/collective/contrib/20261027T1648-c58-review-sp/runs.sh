#!/bin/bash
# c58 review of c55's Schroedinger-Poisson negative: damped fed arm (eta 0.05, g 0.02, sig 0.002, G 1e-3) on fresh seeds 6 7, the same at world dt 0.1 on seed 6, conservative arm seed 6; T=2000
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1
G=collective/contrib/20261027T0949-c55-schrodinger-poisson-negative; R=collective/contrib/20261027T1648-c58-review-sp
WORLD_P='{"eta":0.05,"g":0.02,"sig":0.002,"G":0.001}' python -m labkit.run $G/world.py --out $R/packC --seeds 6 7 --frames 200 --spf 50 --no-movie > /dev/null 2>&1 &
WORLD_P='{"eta":0.05,"g":0.02,"sig":0.002,"G":0.001,"dt":0.1}' python -m labkit.run $G/world.py --out $R/packC_dthalf --seeds 6 --frames 200 --spf 100 --no-movie > /dev/null 2>&1 &
python -m labkit.run $G/world.py --out $R/pack0 --seeds 6 --frames 200 --spf 50 --no-movie > /dev/null 2>&1 &
wait; echo ALLDONE
