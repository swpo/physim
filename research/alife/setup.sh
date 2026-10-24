#!/usr/bin/env bash
# Create the lab environment at research/alife/.labenv (about a minute with uv).
set -euo pipefail
cd "$(dirname "$0")"
uv venv .labenv --python 3.12 -q
uv pip install --python .labenv/bin/python -q -r requirements.txt
.labenv/bin/python -c "import numpy, scipy, gudhi, matplotlib; print('labenv ready')"
