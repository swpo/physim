#!/bin/bash
# pod/bootstrap.sh — set up the blobgpu env on a fresh CUDA pod.
set -e
cd ~
if ! command -v uv >/dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi
cd ~/physim/probes/blobs/gpu
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python "jax[cuda12]==0.4.38" numpy scipy
.venv/bin/python -c "import jax; print(jax.devices())"
