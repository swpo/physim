#!/bin/bash
# c58 review of c55's chimera-field screen, fresh seed 5: alpha 1.2 R 6 smooth init (T=1500), alpha 1.1 smooth (T=600), alpha 1.45 random (T=600), alpha 1.2 at world dt 0.05 (T=1500)
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1
G=collective/contrib/20261027T1049-c55-chimera-field-negative; R=collective/contrib/20261027T1645-c58-review-chimera
WORLD_P='{"alpha":1.2,"init":1}' python -m labkit.run $G/world.py --out $R/a12 --seeds 5 --frames 300 --spf 50 --no-movie > /dev/null 2>&1 &
WORLD_P='{"alpha":1.1,"init":1}' python -m labkit.run $G/world.py --out $R/a11 --seeds 5 --frames 120 --spf 50 --no-movie > /dev/null 2>&1 &
WORLD_P='{"alpha":1.45,"init":0}' python -m labkit.run $G/world.py --out $R/a145 --seeds 5 --frames 120 --spf 50 --no-movie > /dev/null 2>&1 &
WORLD_P='{"alpha":1.2,"init":1,"dt":0.05}' python -m labkit.run $G/world.py --out $R/a12_dthalf --seeds 5 --frames 300 --spf 100 --no-movie > /dev/null 2>&1 &
wait; echo ALLDONE
