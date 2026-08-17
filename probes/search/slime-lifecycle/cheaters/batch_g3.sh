#!/bin/bash
cd /Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle/cheaters
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
M2='"chi_d":6.0,"Dv_germ":0.14,"T_wake":300,"Dv_fed":0.04,"N_f":1.5,"V_found":0.3,"K":9,"_T":100000'
run() { MPLBACKEND=Agg $PY probe_long.py "$1" "$2" > "long_$1.log" 2>&1; }
# wave 2: lam extremes
for s in 0 1 2; do
  run Glc0005_s$s "{$M2,\"mu\":0.01,\"lam_c\":0.0005,\"_seed\":$s}" &
  run Glc008_s$s "{$M2,\"mu\":0.01,\"lam_c\":0.008,\"_seed\":$s}" &
done
wait
# wave 3: mu curve at lam=0.002
for s in 0 1 2; do
  run Gmu003_s$s "{$M2,\"lam_c\":0.002,\"mu\":0.003,\"_seed\":$s}" &
  run Gmu03_s$s  "{$M2,\"lam_c\":0.002,\"mu\":0.03,\"_seed\":$s}" &
done
wait
# wave 4: mu extremes
for s in 0 1 2; do
  run Gmu001_s$s "{$M2,\"lam_c\":0.002,\"mu\":0.001,\"_seed\":$s}" &
  run Gmu10_s$s  "{$M2,\"lam_c\":0.002,\"mu\":0.1,\"_seed\":$s}" &
done
wait
echo ALL_DONE
