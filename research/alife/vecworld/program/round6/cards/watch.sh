#!/bin/bash
# watch.sh <job_id> -- one loop: fetch origin/gpu-jobs every 60 s, print state changes, end on a final state.
JOB=$1
ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
last=""
while true; do
  git -C "$ROOT" fetch -q origin gpu-jobs 2>/dev/null
  st=$(git -C "$ROOT" show "origin/gpu-jobs:jobs/$JOB/status.json" 2>/dev/null | python3 -c 'import json,sys
try:
    d=json.load(sys.stdin); r=d.get("review") or {}
    print(d.get("state"), "|", (d.get("message") or "")[:160].replace("\n"," "), "| review:", (r.get("summary") or "-")[:120])
except Exception as e:
    print("no status yet")')
  if [ "$st" != "$last" ]; then echo "$(date -u +%T) $st"; last="$st"; fi
  case "$st" in done*|failed*|timeout*|cancelled*|rejected*|infra_error*) break;; esac
  sleep 60
done
