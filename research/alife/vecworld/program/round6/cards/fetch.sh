#!/bin/bash
# fetch.sh <job_id> [dest] -- copy a finished job's outputs from origin/gpu-jobs into dest (default: the study's
# work/<job_id>, not committed). Only reads git objects.
set -eu
JOB=$1
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST=${2:-$HERE/work/$JOB}
ROOT="$(git -C "$HERE" rev-parse --show-toplevel)"
git -C "$ROOT" fetch -q origin gpu-jobs
mkdir -p "$DEST"
git -C "$ROOT" archive origin/gpu-jobs "jobs/$JOB" | tar -x -C "$DEST" --strip-components=2
ls "$DEST"
