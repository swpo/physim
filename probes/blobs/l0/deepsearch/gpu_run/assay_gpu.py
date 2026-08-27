"""assay_gpu.py — assay_v2 with the sim backend swapped to blobgpu.

Loads the LOCKED assay_v2.py source into a separate module instance and
rebinds ONLY its SS2 (simulation module) to backend_gpu. Decision logic,
metrics, thresholds: the locked bytes themselves — never copied or edited.

run_assay(genome, seed=..., ...) -> same return dict as assay_v2.run_assay.
horizon_criteria is re-exported for the batched engine (gpu_eval).
"""
import importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BLOBS = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
CPLX = os.path.join(BLOBS, "l0", "complexity")
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import backend_gpu                                            # noqa: E402

_ASSAY = os.path.join(CPLX, "assay_v2.py")
_spec = importlib.util.spec_from_file_location("assay_v2_gpu_inst", _ASSAY)
_A = importlib.util.module_from_spec(_spec)
sys.modules["assay_v2_gpu_inst"] = _A
_spec.loader.exec_module(_A)
_A.SS2 = backend_gpu          # THE swap: sim call path only

run_assay = _A.run_assay
horizon_criteria = _A.horizon_criteria
T0_DEFAULT, T_CAP = _A.T0_DEFAULT, _A.T_CAP
MV2 = _A.MV2                  # locked metrics module (shared instance)
