#!/bin/bash
# Two long noisy runs (fresh seeds 21, 22), then analysis with curation/analyze.py
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
P=/home/user/physim/.venv/bin/python
S=/home/user/evalwork/vortex_eval/scripts
CUR=/home/user/physim/research/alife/evals/labworlds/runs/curation
cd /home/user/evalwork/vortex_eval/behav
L=${1:-0.003}
for s in 21 22; do
  ( $P $S/behav_noise.py --seed $s --T 3000 --intensity $L --out fv_s${s}_L${L}.npz > fv_s${s}_L${L}.log 2>&1 && \
    cd $CUR && $P analyze.py /home/user/evalwork/vortex_eval/behav/fv_s${s}_L${L}.npz >> /home/user/evalwork/vortex_eval/behav/fv_s${s}_L${L}.log 2>&1 ) &
done
wait
echo BEHAV_DONE $L
