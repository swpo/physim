#!/bin/bash
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=2
cd /tmp/claude-0/thr
for f in 0.5 0.25 0.1; do for r in 0 1000; do
python kdarms.py /tmp/claude-0/c25/st_$1.npz $1 kdhold hold_f${f}_r${r}_s$1.json --T 3000 --frac $f --ramp $r
done; done; echo FIN
