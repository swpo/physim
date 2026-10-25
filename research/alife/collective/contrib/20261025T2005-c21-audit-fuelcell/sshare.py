"""(c21) Who makes the surfactant in nematic-fuelcell? From labkit frames (channels phi, |Q|, s, f), every
10th frame after frame 20: the source ks (1+phi)/2 (srcin=0) or ks clip(phi,0,1) (srcin=1) summed inside
bodies (phi > 0) and in the bath (phi <= 0); bath phi median; occupancy. Also the share of the interface
band's s that a bath source could supply is not separable, so the production split is the measure.
usage: sshare.py frames.npz srcin"""
import sys, numpy as np
R = np.load(sys.argv[1])["render"]; srcin = int(sys.argv[2])
ins, bath, ph, occ = 0.0, 0.0, [], []
for i in range(20, len(R), 10):
    phi = R[i, 0]
    src = np.clip(phi, 0, 1) if srcin else 0.5 * (1 + np.clip(phi, -1, 1))
    ins += src[phi > 0].sum(); bath += src[phi <= 0].sum(); ph.append(np.median(phi[phi <= 0])); occ.append((phi > 0).mean())
print(f"{sys.argv[1]}: surfactant production in bodies {ins / (ins + bath):.3f}, in bath {bath / (ins + bath):.3f}; bath phi median {np.median(ph):.3f}; occupancy {np.mean(occ):.3f}")
