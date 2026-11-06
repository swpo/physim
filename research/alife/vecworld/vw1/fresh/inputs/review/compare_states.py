import json

import numpy as np

a = np.load("/home/user/evalwork/vecworld/vw1/fresh/inputs/results/states.npz")
b = np.load("/home/user/evalwork/vecworld/vw1/fresh/inputs/review/states_rerun.npz")
out = {k: float(np.abs(a[k].astype(float) - b[k].astype(float)).max()) for k in a.files}
out["shape_x"] = list(a["x"].shape)
print(json.dumps(out))
print(open("/home/user/evalwork/vecworld/vw1/fresh/inputs/review/states_rerun.json").read())
