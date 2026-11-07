"""KL (nats) of one PhySim-v1-style injection on the fed-vortex omega field, read as a mean shift before the
LabWorld's smoothed additive noise (intensity 0.003, ell 2, dx 1, native dt 0.02, 128^2).
Noise per step: a * IFFT(H * FFT(xi)), a = sd sqrt(dt), H = exp(-ell^2 k^2 / 2). Shift: g u bump(width w), u = 1.
KL = 1/2 sum_k |S(k)|^2 / (N a^2 |H(k)|^2) (unnormalised FFT, N pixels); spread over n steps: KL / n."""
import json
import numpy as np
n0 = 128; ell = 2.0; sd = 0.003; dt = 0.02; g = 0.01
a = sd * np.sqrt(dt)
k = 2 * np.pi * np.fft.fftfreq(n0)
K2 = k[:, None] ** 2 + k[None, :] ** 2
H2 = np.exp(-ell ** 2 * K2)
c = (np.arange(n0) + 0.5)
d = (c - 64 + 64) % 128 - 64
out = {}
for w in (2.0, 3.0, 4.0, 8.0):
    bump = np.exp(-(d[:, None] ** 2 + d[None, :] ** 2) / (2 * w * w))
    S = np.fft.fft2(g * bump)
    kl1 = 0.5 * float((np.abs(S) ** 2 / (n0 * n0 * a * a * H2)).sum())
    out[f"w={w}"] = {"one_step": kl1, "spread_over_50_steps": kl1 / 50, "bump_peak_shift": g}
print(json.dumps(out, indent=1))
json.dump(out, open("/home/user/evalwork/vecworld/program/inventory/kl_inject.json", "w"), indent=1)
