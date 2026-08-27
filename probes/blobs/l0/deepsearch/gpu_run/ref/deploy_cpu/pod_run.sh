#!/bin/bash
# pod_run.sh — island main loop. Usage: ./pod_run.sh <first_gen> <last_gen>
# Requires island_config.json beside this script. Idempotent per gen.
set -u
cd "$(dirname "$0")"
PY=${PY:-python3}
OUT=$($PY -c "import json;c=json.load(open('island_config.json'));print(c.get('out_dir') or 'out')")
mkdir -p "$OUT"
FIRST=${1:-1}; LAST=${2:-25}
run_shards () {  # tag
  local TAG=$1
  ls "$OUT"/jobs/${TAG}_w*.json >/dev/null 2>&1 || return 0
  for W in "$OUT"/jobs/${TAG}_w*.json; do
    nohup $PY pod_worker.py "$W" > "$OUT"/w_${TAG}_$(basename $W .json).log 2>&1 &
  done
  while pgrep -f "pod_worker.py $OUT/jobs/${TAG}_" >/dev/null; do sleep 60; done
  for W in "$OUT"/jobs/${TAG}_w*.json; do   # drain (idempotent)
    $PY pod_worker.py "$W" >> "$OUT"/drain_${TAG}.log 2>&1
  done
}
if [ "$FIRST" -eq 0 ]; then
  $PY pod_gen.py init >> "$OUT"/driver.log 2>&1
  run_shards g0
  $PY pod_gen.py ingest 0 >> "$OUT"/driver.log 2>&1
  run_shards s2g0
  $PY pod_gen.py ingest2 0 >> "$OUT"/driver.log 2>&1
  run_shards s3g0
  $PY pod_gen.py ingest3 0 >> "$OUT"/driver.log 2>&1
  run_shards laneg0
  FIRST=1
fi
for GEN in $(seq $FIRST $LAST); do
  $PY pod_gen.py breed $GEN >> "$OUT"/driver.log 2>&1
  run_shards g${GEN}
  $PY pod_gen.py ingest $GEN >> "$OUT"/driver.log 2>&1
  run_shards s2g${GEN}
  $PY pod_gen.py ingest2 $GEN >> "$OUT"/driver.log 2>&1
  run_shards s3g${GEN}
  $PY pod_gen.py ingest3 $GEN >> "$OUT"/driver.log 2>&1
  run_shards laneg${GEN}
  echo "GEN_${GEN}_DONE $(date)" >> "$OUT"/driver.log
done
echo "POD_RUN_DONE $FIRST-$LAST $(date)" >> "$OUT"/driver.log
