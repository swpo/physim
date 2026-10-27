#!/bin/bash
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=2
K=/home/user/physim/research/alife/collective/contrib/20261027T2013-c60-halftaxis-ecology/controls/kdarms
O=/tmp/claude-0/dth; mkdir -p $O; export WORLD_P='{"dt": 0.1}'
python $K/spin.py 63 6000 $O/st_63.npz
for arm in ctrl kdlocal; do python $K/kdarms.py $O/st_63.npz 63 $arm $O/${arm}_s63.json --T 2000; done
echo FIN
