#!/bin/bash
# c19: c16's wound.py, unchanged, on fresh seeds; run from the finding's directory.
# args: seed. side-11 loops at t=20000 (default founders m=15, 400^2), 10 loops per run, 300-step window.
R=$1; s=$2
for k in 1 2 4; do python wound.py '{}' $s 400 20000 11 10 300 $R/results/w11_s${s}_k${k}.json core $k > /dev/null; done
python wound.py '{}' $s 400 20000 11 10 300 $R/results/w11_s${s}_outer.json outer > /dev/null
echo seed $s done
