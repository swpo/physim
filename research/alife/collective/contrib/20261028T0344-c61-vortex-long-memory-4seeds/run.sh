#!/bin/bash
# c61: long-memory waste (dw 0.0005; Dw 0.25 keeps reach 22 px) on seeds 10 (with twin, T=10000), 13 and 14 (waste arm, T=8000);
# memory-only arm q7 (dw 0.0005, Dw 1: reach 45 px), seed 7, T=10000; labkit pack of the long-memory waste world, seeds 11, 12.
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
T=/home/user/physim/research/alife/collective/contrib/20261028T0118-c61-vortex-t30k-interim/trait3c.py
WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50,"mut_seed":10,"dw":0.0005,"Dw":0.25}' python $T m10_spec 10 10000 &
WORLD_P='{"ew":0.25,"sw":0,"mut_dt":50,"mut_seed":10,"dw":0.0005,"Dw":0.25}' python $T m10_blind 10 10000 &
for s in 13 14; do WORLD_P="{\"ew\":0.25,\"sw\":0.4,\"mut_dt\":50,\"mut_seed\":$s,\"dw\":0.0005,\"Dw\":0.25}" python $T m${s}_spec $s 8000 & done
WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50,"mut_seed":7,"dw":0.0005,"Dw":1.0}' python $T q7_spec 7 10000 &
wait
cd /home/user/physim/research/alife
WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50,"mut_seed":11,"dw":0.0005,"Dw":0.25}' python -m labkit.run collective/contrib/20261027T1401-c58-vortex-trait3d/world.py --out collective/contrib/20261028T0344-c61-vortex-long-memory-4seeds/pack --seeds 11 12 --frames 1000 --spf 150 --no-movie
# vnov.py / vplot.py: 20261028T0105-c61-vortex-long-memory-travels; meanabs.py here
