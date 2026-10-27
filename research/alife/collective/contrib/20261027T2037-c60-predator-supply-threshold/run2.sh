#!/bin/bash
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=2
cd /tmp/claude-0/thr
python kdarms.py /tmp/claude-0/c25/st_$1.npz $1 kdhold hold_f0_r1000_s$1.json --T 3000 --frac 0 --ramp 1000
python kdarms.py /tmp/claude-0/c25/st_$1.npz $1 kdhold hold_f0.05_r1000_s$1.json --T 3000 --frac 0.05 --ramp 1000
python kdarms.py /tmp/claude-0/c25/st_$1.npz $1 kdhold hold_f0.1_r1000_T5000_s$1.json --T 5000 --frac 0.1 --ramp 1000
python kdarms.py /tmp/claude-0/c25/st_$1.npz $1 ctrl ctrl_T5000_s$1.json --T 5000
echo FIN
