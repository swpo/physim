#!/bin/bash
# c63: distribution-memory waste (world.py here, wmode rff: 2M = 24 cos/sin feature channels, orthogonal frequencies, rff_seed 0),
# run with c61's checkpointed trait3c.py (WORLD_DIR = this directory), paired with c61's mean-waste and kind-blind runs on the same seeds:
#   seed 6 standard waste: 20261028T0326-c61-vortex-t30k-saturates/s6_spec.json, s6_blind.json
#   seed 10 long memory:   20261028T0344-c61-vortex-long-memory-4seeds/m10_spec.json, m10_blind.json
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1 WORLD_DIR=$PWD
T=/home/user/physim/research/alife/collective/contrib/20261028T0118-c61-vortex-t30k-interim/trait3c.py
WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50,"mut_seed":6,"wmode":"rff"}' python $T r6_rff 6 10000 &
WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50,"mut_seed":10,"dw":0.0005,"Dw":0.25,"wmode":"rff"}' python $T r10_rff 10 10000 &
wait
C=/home/user/physim/research/alife/collective/contrib
python vcmp.py vcmp_10k.json 1000 10000 0.4 rff6=r6_rff.json mean6=$C/20261028T0326-c61-vortex-t30k-saturates/s6_spec.json blind6=$C/20261028T0326-c61-vortex-t30k-saturates/s6_blind.json rff10=r10_rff.json mean10=$C/20261028T0344-c61-vortex-long-memory-4seeds/m10_spec.json blind10=$C/20261028T0344-c61-vortex-long-memory-4seeds/m10_blind.json
