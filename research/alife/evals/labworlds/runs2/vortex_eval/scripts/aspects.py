import json, sys, numpy as np
sys.path.insert(0, "/home/user/evalwork/vortex_eval/scripts")
import common as C, design as D
s = D.load_state(f"{C.OUT}/prep/state_s31.pkl")
bs = json.load(open(f"{C.OUT}/prep/bodies_s31.json"))
lab, raw = D.bodies(s["om"])
yy, xx = np.indices((128, 128))
for b in bs:
    r = min(raw, key=lambda q: np.hypot(D.wrap(q["cy"] - b["cy"]), D.wrap(q["cx"] - b["cx"])))
    m = lab == r["label"]
    dy = D.wrap(yy[m] + 0.5 - b["cy"]); dx = D.wrap(xx[m] + 0.5 - b["cx"])
    w = np.abs(s["om"][m])
    Cm = np.cov(np.stack([dy, dx]), aweights=w)
    ev, evec = np.linalg.eigh(Cm)
    b["aspect"] = float(np.sqrt(ev[1] / ev[0])); b["axis"] = evec[:, 1].tolist(); b["length"] = float(4 * np.sqrt(ev[1]))
json.dump(bs, open(f"{C.OUT}/prep/bodies_s31.json", "w"), indent=0)
for b in sorted(bs, key=lambda b: -b["aspect"])[:12]:
    print(b["id"], b["sign"], b["area"], round(b["cy"], 1), round(b["cx"], 1), "aspect", round(b["aspect"], 2), "axis", np.round(b["axis"], 2), "len", round(b["length"], 1))
