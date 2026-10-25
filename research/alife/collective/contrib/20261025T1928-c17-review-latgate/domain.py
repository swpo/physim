"""c19: A-pattern length scale over the last 100 recorded frames: the mean wavelength 2 pi / <k> of the radially
averaged structure factor S(k) of the A field (mean removed), weighted by S(k) over k in (0, k_max/2], which
discounts single-site noise. usage: domain.py label=run_dir ..."""
import sys, numpy as np
for arg in sys.argv[1:]:
    lab, d = arg.split("="); R = np.load(d + "/frames.npz")["render"].astype(np.float64); out = []
    H = R.shape[-1]; k = 2 * np.pi * np.fft.fftfreq(H); KK = np.hypot(k[:, None], k[None, :]); sel = (KK > 0) & (KK <= np.pi / 2)
    for i in range(len(R) - 100, len(R), 5):
        a = R[i, 0] - R[i, 0].mean(); S = np.abs(np.fft.fft2(a)) ** 2
        out.append(2 * np.pi / ((KK[sel] * S[sel]).sum() / S[sel].sum()))
    print(f"{lab}: A pattern wavelength {np.mean(out):.1f} px (sd over frames {np.std(out):.1f})")
