#!/bin/bash
# ds2 local validation driver: gens 1..N synchronous, seed2 after each ingest.
# Usage: driver2.sh <first_gen> <last_gen>
cd /Users/spoho/Documents/prime/test/physim/probes/blobs/l0/deepsearch
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
FIRST=${1:-1}; LAST=${2:-2}
for GEN in $(seq $FIRST $LAST); do
  $PY ds2_gen.py breed $GEN >> driver2.log 2>&1
  for W in jobs2/g${GEN}_w*.json; do
    [ -f "$W" ] && nohup $PY ds2_worker.py "$W" > w2_g${GEN}_$(basename $W .json).log 2>&1 &
  done
  # wait for all workers of this gen
  while pgrep -f "ds2_worker.py jobs2/g${GEN}_" >/dev/null; do sleep 60; done
  # drain pass (idempotent)
  for W in jobs2/g${GEN}_w*.json; do
    [ -f "$W" ] && $PY ds2_worker.py "$W" >> d2_g${GEN}_drain.log 2>&1
  done
  $PY ds2_gen.py ingest $GEN >> driver2.log 2>&1
  # seed2 screens for this gen's new/improved holders
  if ls jobs2/s2g${GEN}_w*.json >/dev/null 2>&1; then
    for W in jobs2/s2g${GEN}_w*.json; do
      nohup $PY ds2_worker.py "$W" > w2_s2g${GEN}_$(basename $W .json).log 2>&1 &
    done
    while pgrep -f "ds2_worker.py jobs2/s2g${GEN}_" >/dev/null; do sleep 60; done
    $PY ds2_gen.py ingest2 $GEN >> driver2.log 2>&1
  fi
done
echo DRIVER2_DONE_$FIRST-$LAST >> driver2.log
