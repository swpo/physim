#!/bin/bash
cd "$(dirname "$0")"
JOBS="m0 m4 pred coex mv3 p6g8_033 p3g9_022 p4g2_044 cargo_cell m5_trains m2_dimer m2_dimer_a4 dead frozen noise"
printf '%s\n' $JOBS | xargs -P 4 -I{} sh -c 'python3 run_val_v3.py {} --seed 1 --workers 2 > logs_v3/{}.log 2>&1; echo "done {}"'
echo ALL_DONE
