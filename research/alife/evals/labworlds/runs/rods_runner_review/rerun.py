"""Reviewer re-run: (1) parity of the repo's own labworld.oracle (LabStepper/LabOracleRunner at HEAD) against
world.py imported directly, zero noise, no actions, 5 tu; (2) reproduce saved members (sham pred native m0 3 tu,
surf pred dthalf m0 6 tu) with the rods_runner code against HEAD labworld."""
import copy, importlib.util, json, os, sys, time
import numpy as np
sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
sys.path.insert(0, "/home/user/physim/research/alife")
from physim import labworld as LW
from physim.devices import ProbeDevice

RR = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/rods_runner"
W = "/home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py"
PREP = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/out"
res = {}
# ---- (1) independent parity through the repo's oracle() ----
os.environ.pop("WORLD_P", None)
spec = importlib.util.spec_from_file_location("c34_direct", W); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
z = np.load(f"{PREP}/prep_s0.npz"); info = json.load(open(f"{PREP}/prep_s0.json"))
F5 = ("phi", "q1", "q2", "s", "c")
s0 = m.init(0, (128, 128))
for f in F5: s0[f] = z[f].astype(np.float64).copy()
def devs():
    c0 = np.array(info["sites"]["centre"], float) + 0.5; c1 = np.array(info["sites"]["other"], float) + 0.5
    return [ProbeDevice(dev_id=0, lattice="square", n_rings=3, base_ds=3.0, center=c0, L=128.0, secret_rot=0.3, reflect=False,
                        motion_theta=0.0, motion_reflect=False, node_perm=np.arange(13)),
            ProbeDevice(dev_id=1, lattice="hex", n_rings=3, base_ds=6.0, center=c1, L=128.0, secret_rot=1.1, reflect=False,
                        motion_theta=0.0, motion_reflect=False, node_perm=np.arange(19))]
w = LW.LabWorld(path=W, fields=F5, steps_per_tick=1, native_dt=0.05, ports={f: LW.Port(0.01) for f in F5},
                noise={f: ("additive", 0.0) for f in F5}, sys_path=("/home/user/physim/research/alife",), carry=())
t0 = time.process_time()
o = LW.oracle(w, s0, devs())
out = o.sample_truth([], [{"sensor": g, "t": [1.0, 3.0, 5.0]} for g in ("device0", "device1", "global")], 1, truth_seed=11)["samples"]
st = copy.deepcopy(s0); D = devs(); ref = {}
for k in range(1, 251):
    st = m.step(st)
    if k in (50, 150, 250):
        Fr = np.stack([st[f] for f in F5])
        ref[k] = [D[0].sample(Fr, 1.0), D[1].sample(Fr, 1.0), np.stack((Fr.mean(axis=(1, 2)), Fr.var(axis=(1, 2))), 1)]
res["parity_repo_oracle_5tu_maxabs"] = {g: max(float(np.abs(out[gi][0, ti] - ref[k][gi]).max()) for ti, k in enumerate((50, 150, 250)))
                                        for gi, g in enumerate(("device0", "device1", "global"))}
res["parity_cpu_s"] = round(time.process_time() - t0, 1)
# ---- (2) reproduce saved members with the rods_runner code ----
sys.path.insert(0, RR)
import rods_runner as RRm
s, inf = RRm.prepared(); d = RRm.devices(inf)
gains = json.load(open(f"{RR}/out/gains.json"))
t0 = time.process_time()
o, _ = RRm.oracle(RRm.arm_world("native", gains), s, d)
a = o.sample_truth([], RRm.q(RRm.GROUPS, [1.0, 2.0, 3.0]), 1, truth_seed=RRm.PRED_SEED)["samples"]
sv = np.load(f"{RR}/out/sham_pred_native.npz")
res["sham_pred_native_m0_3tu_maxabs_vs_saved"] = {g: float(np.abs(a[i][0] - sv[g][0, :3]).max()) for i, g in enumerate(RRm.GROUPS)}
o, _ = RRm.oracle(RRm.arm_world("dthalf", gains), s, d)
b = o.sample_truth(RRm.PROGRAMS["surf"], RRm.q(RRm.GROUPS, [float(t) for t in range(1, 7)]), 1, truth_seed=RRm.PRED_SEED)["samples"]
sv = np.load(f"{RR}/out/surf_pred_dthalf.npz")
res["surf_pred_dthalf_m0_6tu_maxabs_vs_saved"] = {g: float(np.abs(b[i][0] - sv[g][0, :6]).max()) for i, g in enumerate(RRm.GROUPS)}
res["repro_cpu_s"] = round(time.process_time() - t0, 1)
print(json.dumps(res, indent=1))
json.dump(res, open("/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/rods_runner_review/rerun.json", "w"), indent=1)
