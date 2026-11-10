#!/bin/bash
# watch.sh <job_id> -- poll origin/gpu-jobs every 60 s; exit when the job reaches a final state.
JOB=${1:?job id}
ROOT=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)
while true; do
  git -C "$ROOT" fetch -q origin gpu-jobs 2>/dev/null
  ST=$(git -C "$ROOT" show "origin/gpu-jobs:jobs/$JOB/status.json" 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin).get("state",""))' 2>/dev/null)
  case "$ST" in done|failed|timeout|cancelled|rejected|infra_error) echo "$JOB $ST $(date -u +%T)"; exit 0;; esac
  sleep 60
done
