"""Export what the renderers need (hidden permutations, standardisation, steering pick).
usage: python prep_render.py WORLD [STEER_J STEER_KEY]"""
import glob
import sys

import numpy as np

import lenia_world as LW
vw = LW.vw

name = sys.argv[1]
specs, parts = LW.make_specs(name)
wo, wc = vw.VectorWorld(specs["objects"], 0), vw.VectorWorld(specs["coarse"], 0)
Yo = np.concatenate([np.load(f)["Yo"] for f in sorted(glob.glob(f"data/{name}/base_*.npz"))])
Yc = np.concatenate([np.load(f)["Yc"] for f in sorted(glob.glob(f"data/{name}/base_*.npz"))])
sdo, sdc = Yo.std(0), Yc.std(0)
np.savez(f"data/{name}/render_meta.npz", K=parts["tracker"].K, perm_objects=wo.out_map, perm_coarse=wc.out_map,
         sd_objects=np.where(sdo > 1e-9, sdo, 1.0), sd_coarse=np.where(sdc > 1e-9, sdc, 1.0),
         steer_video_j=int(sys.argv[2]) if len(sys.argv) > 2 else 0,
         steer_video_key=sys.argv[3] if len(sys.argv) > 3 else "lead+")
print("ok")
