"""Fraction of catalyst K lying in bilayers (u+1 > THR) and the bilayer area fraction, from labkit frames.npz render
(channels: u+1, P, K), at the last frames; also total amphiphile (sum u+1)."""
import sys, numpy as np
THR = float(sys.argv[2]) if len(sys.argv) > 2 else 0.6
z = np.load(sys.argv[1]); R = z['render'].astype(float); tf = z['render_f']
for i in (len(R) // 2, len(R) - 1):
    u, K = R[i, 0], R[i, 2]; bil = u > THR
    print(f"{sys.argv[1]} frame {int(tf[i])}: K total {K.sum():.0f}, K in bilayer {K[bil].sum() / max(K.sum(), 1e-9):.2f}, bilayer area {bil.mean():.3f}, amphiphile {u.sum():.0f}")
