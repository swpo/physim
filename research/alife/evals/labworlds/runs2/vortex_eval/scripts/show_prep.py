import json, pickle, sys
import numpy as np
sys.path.insert(0, "/home/user/evalwork/vortex_eval/scripts")
import design as D
s = D.load_state("/home/user/evalwork/vortex_eval/prep/state_s31.pkl")
lab, bs = D.bodies(s["om"])
bs = sorted(bs, key=lambda b: -abs(b["circ"]))
for i, b in enumerate(bs):
    b["id"] = i
json.dump(bs, open("/home/user/evalwork/vortex_eval/prep/bodies_s31.json", "w"), indent=0)
np.savez_compressed("/home/user/evalwork/vortex_eval/prep/fields_s31.npz", om=s["om"].astype(np.float32), Y=s["Y"].astype(np.float32))
for b in bs:
    print(b["id"], b["sign"], b["area"], round(b["cy"], 1), round(b["cx"], 1), round(b["peak"], 3), round(b["circ"], 2))
