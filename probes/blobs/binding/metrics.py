"""metrics.py — locked measurement conventions for M2 blob-binding certification.
LOCKED before final certification runs; changing anything here invalidates the cert.

Working point P7s ("stable"):
  lam=2.0, k1=-0.7, k3=1.0, k4=1.5, tau=2.5, theta=0.7, Du=1.0, Dv=2.0, Dw=20.0
Reference exploratory point P7 ("saddle"): same but tau=3.0.

Conventions (inherited from day0 + sim.py):
  - integrator: explicit Euler; 5-pt periodic Laplacian / dx^2; dt = min(0.2*dx^2/Dw, 0.02)
  - background: most-negative real root u0 of -u^3 + (lam-k3-k4) u + k1 = 0
  - v, w initialized FLAT at u0; u seeded by blob stamps
  - stamp: single blob relaxed 2000 tu on L=64 dx=1, deviations (du,dv,dw) saved,
    pasted additively at target positions (zoom-interpolated for dx != 1)
  - blob mask: u > u0 + 0.45*(sqrt(lam) - u0); periodic connected components;
    centroid = circular mean weighted by (u - thr)
  - pair separation: min-image distance between the two centroids

Measurements:
  B1: single blob, L=64, T=1e4 tu; PASS if ncomp==1 throughout, area steady
      (tail min/max within 30% of mean), survives noise sigma=2e-3 (>=1e-3 * amp~1.8).
  Bond curve: pair at d0 grid; d* = final separation when |dsep/dt| < 1e-4 px/tu
      sustained over last 500 tu and ncomp==2.
  Unpinning: d*(dx=1) vs d*(dx=0.5) relative shift < 10% => continuum bond.
  Escape (B4): prep pair at d0=15.7 noiseless 300 tu, then noise on;
      escape time = first t with |sep - 15.99| > 3 px (dx=1 convention) or ncomp != 2.
      Bond certified if median escape time >= 10x single-blob relaxation time
      (t_relax = 3.6 tu from 5% peak-kick decay; use 10x = 36 tu) at a noise level
      the SINGLE blob survives (sigma <= 0.045 at tau=3; ceiling re-measured at tau=2.5).
  Multi: chain/triangle at d*; molecule certified if ncomp constant and all
      final pairwise seps within 5% of d* (or documented shell values).
"""
