#!/bin/bash
# monitor for g10 v2-epoch bootstrap: when workers are done, drain + ingest.
cd /Users/spoho/Documents/prime/test/physim/probes/blobs/l0/deepsearch
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
while pgrep -f "ds2_worker.py jobs2/g10_" >/dev/null; do sleep 120; done
for W in jobs2/g10_w*.json; do
  $PY ds2_worker.py "$W" >> d2_g10_drain.log 2>&1
done
$PY ds2_gen.py ingest 10 >> driver2.log 2>&1
# seed2 shards were written by ingest if new/improved holders exist
if ls jobs2/s2g10_w*.json >/dev/null 2>&1; then
  for W in jobs2/s2g10_w*.json; do
    nohup $PY ds2_worker.py "$W" > w2_s2g10_$(basename $W .json).log 2>&1 &
  done
  while pgrep -f "ds2_worker.py jobs2/s2g10_" >/dev/null; do sleep 120; done
  $PY ds2_gen.py ingest2 10 >> driver2.log 2>&1
fi
echo G10_INGESTED >> driver2.log
