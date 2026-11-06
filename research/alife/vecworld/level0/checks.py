"""Checks for flowlenia.py: (1) agreement with a line-by-line numpy transliteration of the
reference code (erwanplantec/FlowLenia: get_kernels_fft, sobel via convolve2d, the 121-offset
roll-based ReintegrationTracking with border='torus'); (2) mass drift over many steps;
(3) determinism; (4) time per step.  Usage: python checks.py [n_long_steps]"""
import json
import sys
import time
import numpy as np
import scipy.signal as ss
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import flowlenia as fl

OUT = __file__.rsplit("/", 1)[0] + "/checks.json"


def ref_kernels_fft(X, Y, p):  # transliteration of utils.get_kernels_fft (X == Y)
    mid = X // 2
    Ds = [np.linalg.norm(np.mgrid[-mid:mid, -mid:mid], axis=0) / ((p["R"] + 15) * p["r"][k])
          for k in range(p["k"])]
    sigm = lambda x: 0.5 * (np.tanh(x / 2) + 1)
    ker_f = lambda x, a, w, b: (b * np.exp(-(x[..., None] - a) ** 2 / w)).sum(-1)
    K = np.dstack([sigm(-(D - 1) * 10) * ker_f(D, np.array(p["a"][k]), np.array(p["w"][k]),
                                                np.array(p["b"][k])) for k, D in zip(range(p["k"]), Ds)])
    nK = K / np.sum(K, axis=(0, 1), keepdims=True)
    return np.fft.fft2(np.fft.fftshift(nK, axes=(0, 1)), axes=(0, 1))


def ref_sobel(A):  # (x, y, c) -> (x, y, 2, c), zero-padded convolve2d as in the reference
    kx = np.array([[1., 0., -1.], [2., 0., -2.], [1., 0., -1.]])
    ky = kx.T
    sx = np.dstack([ss.convolve2d(A[:, :, c], kx, mode="same") for c in range(A.shape[-1])])
    sy = np.dstack([ss.convolve2d(A[:, :, c], ky, mode="same") for c in range(A.shape[-1])])
    return np.concatenate((sy[:, :, None, :], sx[:, :, None, :]), axis=2)


def ref_rt_torus(A, F, dt, dd, sigma):  # ReintegrationTracking._apply_without_hidden, torus
    SX, SY = A.shape[:2]
    x, y = np.arange(SX), np.arange(SY)
    Xg, Yg = np.meshgrid(x, y)
    pos = np.dstack((Yg, Xg)) + .5
    ma = dd - sigma
    mu = pos[..., None] + np.clip(dt * F, -ma, ma)
    nA = np.zeros_like(A)
    for dx in range(-dd, dd + 1):
        for dy in range(-dd, dd + 1):
            Ar = np.roll(A, (dx, dy), axis=(0, 1))
            mur = np.roll(mu, (dx, dy), axis=(0, 1))
            dpmu = np.min(np.stack([np.absolute(pos[..., None] - (mur + np.array([di, dj])[None, None, :, None]))
                                    for di in (-SX, 0, SX) for dj in (-SY, 0, SY)]), axis=0)
            sz = .5 - dpmu + sigma
            area = np.prod(np.clip(sz, 0, min(1, 2 * sigma)), axis=2) / (4 * sigma ** 2)
            nA += Ar * area
    return nA


def ref_step(A_xyc, p, fK):  # FlowLenia.__call__ with alpha from p["alpha_src"]
    fA = np.fft.fft2(A_xyc, axes=(0, 1))
    fAk = fA[:, :, p["c0"]]
    U = np.real(np.fft.ifft2(fK * fAk, axes=(0, 1)))
    U = (np.exp(-((U - np.array(p["m"])) / np.array(p["s"])) ** 2 / 2) * 2 - 1) * np.array(p["h"])
    c1 = np.array(p["c1"])
    U = np.dstack([U[:, :, c1 == c].sum(axis=-1) for c in range(p["C"])])
    nU = ref_sobel(U)
    nAs = ref_sobel(A_xyc.sum(axis=-1, keepdims=True))
    src = A_xyc.sum(-1, keepdims=True) if p["alpha_src"] == "sum" else A_xyc
    alpha = np.clip((src[:, :, None, :] / p["theta_A"]) ** p["n"], 0., 1.)
    F = nU * (1 - alpha) - nAs * alpha
    return ref_rt_torus(A_xyc, F, p["dt"], p["dd"], p["sigma"]), F


def main():
    res = {}
    rng = np.random.default_rng(7)
    p = fl.sample_params(rng, C=2, k=10)
    H = W = 64
    A = fl.init_patches(3, 2, H, W, n_patches=2, L=20)
    # move matter away from the border so zero-padded reference Sobel == periodic Sobel
    A[:, :6] = 0; A[:, -6:] = 0; A[:, :, :6] = 0; A[:, :, -6:] = 0
    A = A.copy()
    # (1a) kernels
    fK_ref = ref_kernels_fft(H, W, p)
    K_mine = fl.kernels(p, H, W)
    K_ref = np.real(np.fft.ifft2(fK_ref, axes=(0, 1))).transpose(2, 0, 1)
    res["kernel_maxabs_diff"] = float(np.abs(K_mine - K_ref).max())
    # (1b) one full step vs the reference step, interior only for Sobel border effects
    A_ref, F_ref = ref_step(A.transpose(1, 2, 0), p, fK_ref)
    A_mine = fl.step(A, p)
    Fy, Fx = fl.flow(A, p)
    inner = (slice(None), slice(3, -3), slice(3, -3))
    res["flow_maxabs_diff_interior"] = float(max(np.abs(Fy - F_ref[:, :, 0].transpose(2, 0, 1))[inner].max(),
                                                np.abs(Fx - F_ref[:, :, 1].transpose(2, 0, 1))[inner].max()))
    res["flow_scale"] = float(np.abs(F_ref).max())
    res["step_maxabs_diff_vs_reference"] = float(np.abs(A_mine - A_ref.transpose(2, 0, 1)).max())
    # (1c) RT alone on a random large flow on the full torus (wrap-around, clipping at dd - sigma)
    Fr = rng.normal(0, 15, (H, W, 2, 2))
    Ar = rng.uniform(0, 1, (H, W, 2))
    rt_ref = ref_rt_torus(Ar, Fr, 0.2, 5, 0.65)
    rt_mine = fl.reintegrate(Ar.transpose(2, 0, 1), Fr[:, :, 0].transpose(2, 0, 1), Fr[:, :, 1].transpose(2, 0, 1), p)
    res["rt_maxabs_diff_random_flow"] = float(np.abs(rt_mine - rt_ref.transpose(2, 0, 1)).max())
    # (1d) reference alpha_src="channel" variant too
    pc = dict(p, alpha_src="channel")
    A_refc, _ = ref_step(A.transpose(1, 2, 0), pc, fK_ref)
    res["step_maxabs_diff_vs_reference_channel_alpha"] = float(np.abs(fl.step(A, pc) - A_refc.transpose(2, 0, 1)).max())
    print(json.dumps(res, indent=1), flush=True)

    # (2) mass drift over N steps, 128^2, C=2, k=10 and C=1, k=10, with and without flow noise
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    drift = {}
    for C, k, noise in ((2, 10, None), (1, 10, None), (2, 10, {"mode": "flow", "std": 0.5, "seed": 1})):
        q = fl.sample_params(np.random.default_rng(11 + C), C=C, k=k, R_scale=0.5)
        if noise:
            q["noise"] = noise
        A0 = fl.init_patches(5, C, 128, 128, n_patches=5, L=20)
        m0 = A0.sum(axis=(1, 2))
        A1 = A0
        traj = []
        for t in range(N):
            A1 = fl.step(A1, q, t)
            if (t + 1) % (N // 10) == 0:
                traj.append(float(np.abs(A1.sum(axis=(1, 2)) - m0).max() / m0.max()))
        name = f"C{C}_k{k}" + ("_flownoise" if noise else "")
        drift[name] = {"steps": N, "mass0": m0.tolist(), "rel_drift_trajectory": traj,
                       "final_rel_drift": traj[-1], "min_value": float(A1.min())}
        print(name, drift[name]["final_rel_drift"], flush=True)
    res["mass_drift"] = drift
    # (3) determinism: two runs of 300 steps with flow noise are bitwise equal
    q = fl.sample_params(np.random.default_rng(3), C=2, k=10, R_scale=0.5)
    q["noise"] = {"mode": "flow", "std": 0.5, "seed": 9}
    A0 = fl.init_patches(4, 2, 96, 96, n_patches=3, L=20)
    r1 = fl.run(A0, q, 300)
    fl._CACHE.clear()
    r2 = fl.run(A0, q, 300)
    res["determinism_bitwise_equal_300_steps"] = bool(np.array_equal(r1, r2))
    # (4) timing
    timing = {}
    for S in (96, 128):
        for C, k in ((1, 10), (2, 10), (2, 20), (3, 15)):
            q = fl.sample_params(np.random.default_rng(1), C=C, k=k)
            A0 = fl.init_patches(1, C, S, S, n_patches=3, L=20)
            A1 = fl.run(A0, q, 20)
            t0 = time.perf_counter()
            A1 = fl.run(A1, q, 200)
            timing[f"{S}^2_C{C}_k{k}_ms_per_step"] = round((time.perf_counter() - t0) / 200 * 1e3, 3)
    res["timing"] = timing
    print(json.dumps(timing, indent=1))
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)


if __name__ == "__main__":
    main()
