#!/bin/bash
# checks.json + final manifest, then the control/reference ensembles on two workers
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
P=/home/user/physim/.venv/bin/python
cd /home/user/swpo/residency-environments/scripts/physim/labworlds
B=/home/user/evalwork/vortex_eval/suite/bundle; W=/home/user/evalwork/vortex_eval/suite/work
$P fedvortex_bundle.py checks --out $B --work $W > $W/checks.log 2>&1 || { echo CHECKS_FAILED; exit 1; }
for k in 0 1; do $P fedvortex_bundle.py controls --out $B --work $W --worker $k --workers 2 > $W/controls_$k.log 2>&1 & done
wait
echo CONTROLS_DONE
