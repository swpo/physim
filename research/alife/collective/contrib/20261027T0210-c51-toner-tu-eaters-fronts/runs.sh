#!/bin/bash
# packs: motile (v0 0.25) and v0=0 twin, seeds 0 1, t=3000; then speed-rises-with-density variant (rs 0.5, v0 0.5) seed 0
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
F=collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts; W=$F/world.py
python -m labkit.run $W --out $F/pack --seeds 0 1 --frames 150 --spf 80 --no-movie > $F/pack.log 2>&1 &
WORLD_P='{"v0":0}' python -m labkit.run $W --out $F/pack_v0 --seeds 0 1 --frames 150 --spf 80 --no-movie > $F/pack_v0.log 2>&1
wait
WORLD_P='{"v0":0.5,"rs":0.5,"lam":2.0}' python -m labkit.run $W --out $F/pack_rs --seeds 0 --frames 150 --spf 80 --no-movie > $F/pack_rs.log 2>&1
echo done > $F/done.txt
