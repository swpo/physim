#!/usr/bin/env bash
# Sync rollout outputs to/from the HF dataset (seanpohorence/physim-rollouts).
# Usage: ./sync_outputs.sh push   # upload local outputs/ (after eval runs)
#        ./sync_outputs.sh pull   # download outputs/ (to regenerate galleries)
set -euo pipefail
cd "$(dirname "$0")"
REPO=seanpohorence/physim-rollouts
case "${1:-}" in
  push)
    .venv/bin/python - <<'EOF'
from huggingface_hub import HfApi
HfApi().upload_folder(folder_path="outputs", path_in_repo="outputs",
                      repo_id="seanpohorence/physim-rollouts", repo_type="dataset",
                      commit_message="sync rollout outputs")
print("pushed outputs/ to HF")
EOF
    ;;
  pull)
    .venv/bin/python - <<'EOF'
from huggingface_hub import snapshot_download
p = snapshot_download(repo_id="seanpohorence/physim-rollouts", repo_type="dataset",
                      allow_patterns="outputs/**", local_dir=".")
print("pulled to", p)
EOF
    ;;
  *) echo "usage: $0 push|pull"; exit 1;;
esac
