#!/bin/bash
# fetch.sh JOB_ID DEST: unpack origin/gpu-jobs:jobs/JOB_ID into DEST (scratch) and copy the small records into
# results/job/ (status, review, request, progress, info, gate, meta). The arrays stay on origin/gpu-jobs.
set -eu
JOB=$1; DEST=$2
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO=${REPO:-/home/user/physim}
mkdir -p "$DEST" "$HERE/results/job"
( cd "$REPO" && timeout 120 git fetch -q origin gpu-jobs || true; git archive origin/gpu-jobs "jobs/$JOB" | tar -x -C "$DEST" )
J="$DEST/jobs/$JOB"
cp "$J/status.json" "$HERE/results/job/status_$JOB.json"
[ -f "$J/review.md" ] && cp "$J/review.md" "$HERE/results/job/review_$JOB.md"
[ -f "$J/request.json" ] && cp "$J/request.json" "$HERE/results/job/request_$JOB.json"
[ -f "$J/logs/sysinfo.txt" ] && cp "$J/logs/sysinfo.txt" "$HERE/results/job/sysinfo_$JOB.txt"
for f in progress.txt full/progress.txt presmoke/progress.txt full/info.json full/gate.json full/code_norm.json; do
  [ -f "$J/out/$f" ] && cp "$J/out/$f" "$HERE/results/job/${JOB}_$(echo $f | tr / _)"
done
for arm in P N30 N10; do
  [ -f "$J/out/full/$arm/meta.json" ] && cp "$J/out/full/$arm/meta.json" "$HERE/results/job/${JOB}_${arm}_meta.json"
done
du -sh "$J" || true
ls "$HERE/results/job"
