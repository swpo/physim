"""Shared setup for the pm_cips_eval scripts: pinned physim, pmcips declarations."""
import os
import sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
OUT = "/home/user/evalwork/pm_cips_eval"
os.environ.setdefault("PHYSIM_PIN", f"{OUT}/pkg")
sys.path.insert(0, "/home/user/swpo/residency-environments/scripts/physim/labworlds")
import pmcips as PC  # noqa: E402,F401
from pmcips import E, LW  # noqa: E402,F401
EVALPILOT = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot"
