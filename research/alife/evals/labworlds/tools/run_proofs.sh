#!/bin/sh
# Local proofs (validation cases, one experiment, naive grading) for every bundle, then the native oracle graded at
# M=2 members, cheapest world first. One process at a time; each step resumes from its outputs.
B=/home/user/evalwork/bundles
PY=/home/user/physim/.venv/bin/python
export OMP_NUM_THREADS=1
path() { [ "$1" = fedvortex ] && echo /home/user/evalwork/vortex_eval/suite/bundle || echo $B/$1; }
for k in vortex_main vortex_formation pm_main pm_formation cips_main cips_formation rods_main rods_formation; do
  [ -f $B/work/prove/$k/local.json ] || $PY $B/scripts/prove_bundle.py local --bundle $(path $k) --out $B/work/prove/$k || echo "FAIL local $k"
done
for k in fedvortex pm_formation vortex_formation pm_main vortex_main cips_formation rods_formation cips_main rods_main; do
  [ -f $B/work/prove/$k/debias_m2.json ] || $PY $B/scripts/prove_bundle.py oracle --members 2 --bundle $(path $k) --out $B/work/prove/$k || echo "FAIL oracle $k"
done
echo ALL DONE
