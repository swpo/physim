#!/bin/bash
# (a) refinement and (b) rotation runs, one process at a time; appends to runs/behav.log
cd /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/curation || exit 1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
P=/home/user/physim/.venv/bin/python
run() {  # world seed N dt T rot
  out=runs/$1_s$2_N$3_dt$4_rot$6.npz
  [ -f "${out%.npz}.json" ] && return
  dtarg=""; [ "$4" != "def" ] && dtarg="--dt $4"
  $P behav.py --world $1 --seed $2 --N $3 $dtarg --T $5 --rot $6 --out $out >> runs/behav.log 2>&1 && $P analyze.py $out >> runs/behav.log 2>&1
}
for s in 11 12; do run pm $s 128 def 8000 0; run pm $s 128 0.5 8000 0; run pm $s 192 0.5 8000 0; done
for s in 11 12 13 14; do run pm $s 128 def 8000 45; done
for s in 13 14; do run pm $s 128 def 8000 0; done
for s in 11 12; do run pm $s 192 0.5 8000 45; done
for s in 11 12; do run pm $s 256 0.25 8000 0; done
for s in 11 12; do run fv $s 128 def 1500 0; run fv $s 128 0.01 1500 0; done
for s in 11 12; do run fv $s 128 def 1500 45; done
for s in 11 12; do run fv $s 192 def 1500 0; done
echo QUEUE_DONE >> runs/behav.log
