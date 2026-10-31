"""Envelope: amp 3 for 50 tu on each actuator at its worst site, at candidate gains (1 noisy member)."""
import json, sys, time
import numpy as np
sys.path.insert(0, "/home/user/evalwork/vortex_eval/scripts")
import common as C
import design as D

s = D.load_state(f"{C.OUT}/prep/state_s31.pkl")
bs = {b["id"]: b for b in json.load(open(f"{C.OUT}/prep/bodies_s31.json"))}
site = lambda i: [bs[i]["cy"], bs[i]["cx"]]
far = [20.0, 20.0]  # high-fuel region without a body
runs = [("sham", None, 0.01, 0.1, site(0)),
        ("om+", "om+", 0.01, 0.1, site(0)), ("om+", "om+", 0.02, 0.1, site(0)),
        ("om-", "om-", 0.01, 0.1, site(1)), ("om-", "om-", 0.02, 0.1, site(1)),
        ("om+ empty", "om+", 0.01, 0.1, far),
        ("Y+ vortex", "Y+", 0.01, 0.03, site(0)), ("Y+ vortex", "Y+", 0.01, 0.1, site(0)), ("Y+ vortex", "Y+", 0.01, 0.3, site(0)),
        ("Y+ empty", "Y+", 0.01, 0.1, far), ("Y+ empty", "Y+", 0.01, 0.3, far),
        ("Y- vortex", "Y-", 0.01, 0.1, site(0)), ("Y- vortex", "Y-", 0.01, 0.03, site(0))]
out = []
for label, act, gom, gy, yx in runs:
    devs = [D.device(0, yx), D.device(1, site(1))]
    o = D.oracle(s, devs, gains={"om": gom, "Y": gy})
    actions = [] if act is None else [dict(t=0, kind="inject", device=0, port=D.ACT[act], amp=3.0, dur=50.0)]
    t0 = time.process_time()
    fr, res = D.capture(o, actions, seed=4100, every=5.0)
    yy, xx = np.indices((128, 128))
    near = np.hypot(D.wrap(yy + 0.5 - yx[0]), D.wrap(xx + 0.5 - yx[1])) < 10
    rows = []
    for t in sorted(fr):
        F = fr[t]
        rows.append(dict(t=t, finite=bool(np.isfinite(F).all()), om=[float(F[0].min()), float(F[0].max())],
                         Y=[float(F[1].min()), float(F[1].max())], om_near=[float(F[0][near].min()), float(F[0][near].max())],
                         Y_near=float(F[1][near].mean()), speed_max=float(F[3].max()), eat_max=float(F[2].max())))
    r = dict(label=label, actuator=act, gains=dict(om=gom, Y=gy), site=yx, cpu=round(time.process_time() - t0, 1), rows=rows)
    out.append(r)
    last = rows[-1]; ext = lambda k, j: max(abs(x[k][j]) for x in rows)
    print(f"{label:10s} g_om {gom} g_Y {gy}: finite {all(x['finite'] for x in rows)} om [{min(x['om'][0] for x in rows):.3f},{max(x['om'][1] for x in rows):.3f}] "
          f"Y [{min(x['Y'][0] for x in rows):.3f},{max(x['Y'][1] for x in rows):.3f}] near om@25 {rows[5]['om_near']} @50 {last['om_near']} Ynear@25 {rows[5]['Y_near']:.3f} @50 {last['Y_near']:.3f} cpu {r['cpu']}", flush=True)
json.dump(out, open(f"{C.OUT}/envelope/envelope.json", "w"), indent=0)
