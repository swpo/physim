"""Where is the surfactant made? source = ks (1 + clip(phi)) / 2 (world.py line 108). Split it between
rod pixels (phi > 0), the interface band (-0.5 < phi <= 0) and the bath (phi <= -0.5), per render frame.
usage: source.py frames.npz"""
import sys, numpy as np
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); rf = list(F["render_f"])
print("frame  bath_phi(median)  inside_phi(median)  area_in  src_in  src_band  src_bath  | s mass in rods+band / total")
for k in range(0, len(rf), 12):
    phi, s = R[k, 0], R[k, 2]
    src = 0.5 * (1 + np.clip(phi, -1, 1))
    ins, band, bath = phi > 0, (phi > -0.5) & (phi <= 0), phi <= -0.5
    tot = src.sum()
    print(f"{rf[k]:5d}  {np.median(phi[bath]) if bath.any() else np.nan:+.3f}  {np.median(phi[ins]) if ins.any() else np.nan:+.3f}  {ins.mean():.3f}  "
          f"{src[ins].sum()/tot:.2f}  {src[band].sum()/tot:.2f}  {src[bath].sum()/tot:.2f}  | {(s[ins|band].sum()/max(s.sum(),1e-9)):.2f}")
