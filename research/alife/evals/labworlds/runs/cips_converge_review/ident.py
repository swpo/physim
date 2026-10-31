"""Default-path identity: run the CIPS world through LabStepper with white noise (additive, proportional,
conserved), a source injection, 30 ticks from the prepared state, under one physim package copy.
usage: python ident.py PKGDIR OUT.npz [explicit_empty]"""
import os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
import json, sys
import numpy as np
pkg, out = sys.argv[1], sys.argv[2]
explicit = len(sys.argv) > 3
sys.path.insert(0, pkg)
sys.path.insert(1, "/home/user/physim/packages/blobkit")
from physim import labworld as LW  # noqa: E402
assert os.path.realpath(LW.__file__).startswith(os.path.realpath(pkg)), LW.__file__
sys.path.insert(1, "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/cips_runner")
import cips as C  # noqa: E402
assert os.path.realpath(C.LW.__file__) == os.path.realpath(LW.__file__)
st0, info = C.prepared()
res = {}
for kind in ("additive", "proportional", "conserved"):
    kw = {"noise_corr": {}} if explicit else {}
    w = LW.LabWorld(path=C.WORLD, fields=C.FIELDS, steps_per_tick=1, native_dt=0.1,
                    ports={f: LW.Port(gain=0.1, clip=C.CLIPS[f]) for f in C.FIELDS},
                    noise={f: (kind, 0.01) for f in C.FIELDS}, dx=1.0, sys_path=(C.LAB,), carry=("t",), **kw)
    s = LW.LabStepper(w, dict(w.aux(st0), _grid=(192, 192)))
    C.one_worker(s.module)
    sim = LW.template(w, st0, 11)
    s(sim, 10)
    s(sim, 10, injections=[dict(field=2, amp=3.0, y=60.5, x=70.5)])
    s(sim, 10)
    res[kind] = np.asarray(sim["F"])
    res[kind + "_rng"] = np.frombuffer(json.dumps(sim["rng"].bit_generator.state).encode(), dtype=np.uint8)
    res[kind + "_decl"] = np.frombuffer(json.dumps(w.declaration(), sort_keys=True, default=str).encode(), dtype=np.uint8)
np.savez(out, **res)
print(out, {k: float(np.abs(v).sum()) for k, v in res.items() if v.dtype != np.uint8})
