#!/bin/bash
# deepsearch generation driver: runs gens 1..6, synchronous.
cd /Users/spoho/Documents/prime/test/physim/probes/blobs/l0/deepsearch
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
for GEN in 1 2 3 4 5 6; do
  # wait for current gen workers to finish
  while ls jobs/g${GEN}_w*.json >/dev/null 2>&1; do
    RUNNING=$(pgrep -f "worker.py jobs/g${GEN}_" | wc -l | tr -d " ")
    if [ "$RUNNING" -eq 0 ]; then
      # check all jobs done (worker skips done ones; run once more to be sure)
      for W in jobs/g${GEN}_w*.json; do
        nohup $PY worker.py "$W" >> g${GEN}_drain.log 2>&1
      done
      break
    fi
    sleep 60
  done
  $PY gen.py ingest $GEN >> driver.log 2>&1
  NEXT=$((GEN+1))
  if [ $NEXT -le 6 ]; then
    $PY gen.py breed $NEXT >> driver.log 2>&1
    for W in jobs/g${NEXT}_w*.json; do
      nohup $PY worker.py "$W" > w_g${NEXT}_$(basename $W .json).log 2>&1 &
    done
  fi
done
$PY gen.py confirm 12 >> driver.log 2>&1
for W in jobs/confirm_w*.json; do
  [ -f "$W" ] && nohup $PY worker.py "$W" > w_confirm_$(basename $W .json).log 2>&1 &
done
echo DRIVER_DONE >> driver.log
