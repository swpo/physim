import json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
z = np.load("/home/user/evalwork/vortex_eval/prep/fields_s31.npz"); bs = json.load(open("/home/user/evalwork/vortex_eval/prep/bodies_s31.json"))
fig, ax = plt.subplots(1, 2, figsize=(16, 8))
ax[0].imshow(z["om"], cmap="RdBu_r", vmin=-0.22, vmax=0.22, origin="lower")
for b in bs:
    ax[0].text(b["cx"] - 0.5, b["cy"] - 0.5, str(b["id"]), fontsize=9, ha="center", va="center")
ax[1].imshow(z["Y"], cmap="viridis", origin="lower"); ax[1].set_title("Y")
ax[0].set_title("om at prep (t=600, seed 31)")
plt.tight_layout(); plt.savefig("/home/user/evalwork/vortex_eval/prep/prep_s31.png", dpi=55)
