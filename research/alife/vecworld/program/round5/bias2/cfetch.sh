#!/bin/bash
# cfetch.sh -- copy the small outputs of a finished GPU job from origin/gpu-jobs into results/ (study `bias2`).
# usage: bash cfetch.sh JOB_ID world [world ...]      (run from this folder; needs `git fetch origin gpu-jobs` access)
set -eu
JOB=$1; shift
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO=${REPO:-/home/user/physim}
git -C "$REPO" fetch -q origin gpu-jobs
mkdir -p "$HERE/results"
git -C "$REPO" show "origin/gpu-jobs:jobs/$JOB/status.json" > "$HERE/results/status_$JOB.json"
git -C "$REPO" show "origin/gpu-jobs:jobs/$JOB/out/progress.txt" > "$HERE/results/progress_$JOB.txt" || true
SUF=${B5_SUFFIX:-}          # B5_SUFFIX=_w: the follow-up job's worlds go to results/<world>_w (the grid's stay in results/<world>)
for W in "$@"; do
  mkdir -p "$HERE/results/$W$SUF"
  for f in combined.json table.txt sim_A.json sim_B.json closed_forms.json train_done.json; do
    git -C "$REPO" show "origin/gpu-jobs:jobs/$JOB/out/$W/$f" > "$HERE/results/$W$SUF/$f" || { echo "missing $W/$f"; rm -f "$HERE/results/$W$SUF/$f"; }
  done
  [ -f "$HERE/results/$W$SUF/combined.json" ] && gzip -9 -k -f "$HERE/results/$W$SUF/combined.json"
done
ls -la "$HERE/results" "$HERE"/results/*/ | head -60
