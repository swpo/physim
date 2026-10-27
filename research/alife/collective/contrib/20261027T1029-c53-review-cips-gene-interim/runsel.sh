#!/bin/bash
# sel.py arms (rerun with PYTHONPATH set so world.py finds labkit): seed 7, a2 0.5 and a2 0, swap_T 200, wash_T 1000, T=20000
cd "$(dirname "$0")"; export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1 PYTHONPATH=/home/user/physim/research/alife
WORLD_P='{"a2":0.5,"swap_T":200,"wash_T":1000}' python sel.py 7 20000 sel_s7_a0.5 > sel_a05.log 2>&1 &
WORLD_P='{"a2":0.0,"swap_T":200,"wash_T":1000}' python sel.py 7 20000 sel_s7_a0.0 > sel_a0.log 2>&1 &
wait; echo ALLDONE
