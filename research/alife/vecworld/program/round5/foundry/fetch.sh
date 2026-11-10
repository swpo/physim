#!/bin/bash
# fetch.sh <job_id> [dest] -- unpack a finished GPU job's outputs from origin/gpu-jobs into a scratch folder
# (default work/<job_id>, ignored by git) and copy the small status files into results/jobs/<job_id>/.
set -eu
JOB=${1:?job id}
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST=${2:-$HERE/work/$JOB}
ROOT=$(git -C "$HERE" rev-parse --show-toplevel)
git -C "$ROOT" fetch -q origin gpu-jobs
mkdir -p "$DEST" "$HERE/results/jobs/$JOB"
git -C "$ROOT" archive origin/gpu-jobs "jobs/$JOB" | tar -x -C "$DEST" --strip-components=2
for f in status.json manifest.json review.md request.json; do
  [ -f "$DEST/$f" ] && cp "$DEST/$f" "$HERE/results/jobs/$JOB/$f"
done
for f in progress.txt job_state.json selection.json checks_quick.json; do
  [ -f "$DEST/out/$f" ] && cp "$DEST/out/$f" "$HERE/results/jobs/$JOB/$f"
done
[ -f "$DEST/logs/sysinfo.txt" ] && cp "$DEST/logs/sysinfo.txt" "$HERE/results/jobs/$JOB/sysinfo.txt"
du -sh "$DEST"
