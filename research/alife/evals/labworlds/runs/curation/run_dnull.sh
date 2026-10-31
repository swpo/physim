#!/bin/bash
cd /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/curation || exit 1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
P=/home/user/physim/.venv/bin/python
mkdir -p dnull
$P dnull.py run --world phase_membrane --cases c001 c002 c005 c007 c010 c013 >> dnull/run.log 2>&1
$P dnull.py run --world fed_vortices --cases c001 c002 c003 c006 c009 >> dnull/run.log 2>&1
echo DNULL_DONE >> dnull/run.log
# after the nulls: one fed-vortex run at 2x (256^2), seed 11, same protocol as the other behaviour runs
$P behav.py --world fv --seed 11 --N 256 --T 1500 --rot 0 --out runs/fv_s11_N256_dtdef_rot0.npz >> runs/behav.log 2>&1 && $P analyze.py runs/fv_s11_N256_dtdef_rot0.npz >> runs/behav.log 2>&1
echo FV256_DONE >> dnull/run.log
