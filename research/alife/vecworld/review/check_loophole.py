"""Zero-sum tolerance gap: InputConstraints.check accepts |sum a| <= 1e-9*max(1, l1); the kick
pools (conserves) only if |sum a| <= 1e-9*l1, else it ADDS the positive part (designer-probe branch).
For l1 < 1 an agent can pass the check and create matter every tick."""
import json
import sys

import numpy as np

sys.path.insert(0, "/home/user/evalwork/vecworld/integrate")
import lenia_world as LW   # noqa: E402
vw = LW.vw

specs, parts = LW.make_specs("A_gliders")
l0 = parts["l0"]
w = vw.VectorWorld(specs["objects"], world_seed=0)
inv = LW.inverse_in_map(w)
w.reset(seed=5)
dz = w.designer
S = dz.state()["h0"].reshape(l0.C, -1).sum(0)
order = np.argsort(S)
src_c, snk_c = order[0], order[1]
out = {"S_src": float(S[src_c]), "S_snk": float(S[snk_c]), "n_cells_S_below_1e-6": int((S < 1e-6).sum()),
       "n_cells_exactly_0": int((S == 0).sum())}
cmd = {int(inv[snk_c]): 0.45, int(inv[src_c]): -0.45 + 9e-10}
v = np.array(list(cmd.values()))
out.update({"sum": float(v.sum()), "l1": float(np.abs(v).sum()),
            "check_violations": w.spec.inputs.violations(cmd, 0, None, 0.0)})
m_b = dz.state()["h0"].reshape(l0.C, -1).sum(1)
acc = 0
for _ in range(10):
    w.step(cmd)
    acc += 1
m_a = dz.state()["h0"].reshape(l0.C, -1).sum(1)
out.update({"accepted_ticks": acc, "mass_before": m_b.tolist(), "mass_after": m_a.tolist(),
            "mass_created_total": float((m_a - m_b).sum())})
# the same command with an exactly zero sum, for contrast
w.reset(seed=5)
cmd0 = {int(inv[snk_c]): 0.45, int(inv[src_c]): -0.45}
m_b = dz.state()["h0"].reshape(l0.C, -1).sum(1)
for _ in range(10):
    w.step(cmd0)
out["exact_zero_sum_mass_change"] = float((dz.state()["h0"].reshape(l0.C, -1).sum(1) - m_b).sum())
json.dump(out, open("/home/user/evalwork/vecworld_integrate_review/check_loophole.json", "w"), indent=1)
print(json.dumps(out, indent=1))
