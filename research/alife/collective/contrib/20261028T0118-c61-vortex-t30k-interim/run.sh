#!/bin/bash
# c61: T=30000 pair of c58's trait3d world, seed 6 / mut_seed 6 (standard waste: dw 0.002, Dw 1), 1 thread each, checkpointed by trait3c.py.
# This interim reads the checkpoints at t=15750 (waste) and 16250 (twin): copy state.pkl and link the chunks into p6_<arm>_ck,
# then run trait3c.py with T equal to the checkpoint time (the resume loop is empty and only the analysis runs).
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50,"mut_seed":6}' python trait3c.py s6_spec 6 30000 > s6_spec.log 2>&1 &
WORLD_P='{"ew":0.25,"sw":0,"mut_dt":50,"mut_seed":6}' python trait3c.py s6_blind 6 30000 > s6_blind.log 2>&1 &
# interim: WORLD_P=... python trait3c.py p6_spec 6 15750 ; WORLD_P=... python trait3c.py p6_blind 6 16250
# python vnov.py vnov_p6.json W=2000 s6=p6_spec.json:p6_blind.json   (vnov.py, vplot.py: 20261028T0105-c61-vortex-long-memory-travels)
