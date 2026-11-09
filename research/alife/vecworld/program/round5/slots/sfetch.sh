#!/bin/bash
# sfetch.sh JOB_ID SCRATCH_DIR -- copy a finished job's small outputs from origin/gpu-jobs (local analysis helper).
#   SCRATCH_DIR/<job>/            everything the runner put into git for the job (out/, logs/, status.json)
#   results/<job>/                the files the summary cites: status.json, combined.json, table.txt, sim_*.json,
#                                 train_done.json, progress.txt, train/*.json (training histories)
set -eu
JOB=$1; SCR=$2
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO=${REPO:-/home/user/physim}
git -C "$REPO" fetch -q origin gpu-jobs
rm -rf "$SCR/$JOB"; mkdir -p "$SCR/$JOB"
git -C "$REPO" archive origin/gpu-jobs "jobs/$JOB" | tar -x -C "$SCR/$JOB" --strip-components=2
R="$HERE/results/$JOB"
mkdir -p "$R/train"
cp "$SCR/$JOB/status.json" "$R/"
for f in combined.json table.txt sim_A.json sim_B.json train_done.json progress.txt; do
  [ -f "$SCR/$JOB/out/$f" ] && cp "$SCR/$JOB/out/$f" "$R/" || echo "missing out/$f"
done
cp "$SCR/$JOB"/out/train/*.json "$R/train/" 2>/dev/null || echo "no training histories"
du -sh "$SCR/$JOB" "$R"
