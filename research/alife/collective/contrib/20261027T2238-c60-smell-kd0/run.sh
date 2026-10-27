#!/bin/bash
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=2 WORLD_P='{"chiS": 1.0, "DS": 10.0, "kS": 0.045}'
cd /tmp/claude-0/sk
python spin.py $1 6000 st_$1.npz
for arm in ctrl kdlocal kdlocal_chiF0; do python kdarms.py st_$1.npz $1 $arm ${arm}_s$1.json --T 2000; done; echo FIN
