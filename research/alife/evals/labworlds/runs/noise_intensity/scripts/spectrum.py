"""Low-wavenumber spectrum of LabStepper's dynamics noise on synthetic fields (no dynamics).

Box 128 world units, grids 96/128/192/256 (dx 4/3, 1, 2/3, 1/2), ell in {white, 1, 2, 4} world
units; additive (a), proportional on a field of ones (p) and conserved (c). One native step of
h = 1 from zero fields gives the noise increment itself. Continuum-normalised spectrum
S(k) = |FFT|^2 dx^2 / (N0 N1), averaged over draws and over |k| shells. Expected for the intensity
form: sd^2 exp(-ell^2 k^2) (a, p) and 0.25 sd^2 k_d^2 exp(-ell^2 k^2) (c), k_d^2 the discrete
divergence's symbol. Low band: 0 < |k| <= 2 * 2 pi / 128 (wavelengths >= 64 world units).
"""
import json, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import labworld as LW  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out"
SYN = str(HERE / "synthetic_world.py")
L = 128.0
SD = 0.01
DRAWS = int(sys.argv[1]) if len(sys.argv) > 1 else 300


def stepper(N, ell, intensity):
    dx = L / N
    corr = {} if ell is None else {"a": ell, "c": ell, "p": ell}
    w = LW.LabWorld(path=SYN, fields=("a", "c", "p"), steps_per_tick=1, native_dt=1.0,
                    noise={"a": ("additive", SD), "c": ("conserved", SD), "p": ("proportional", SD)},
                    noise_corr=corr, noise_intensity=("a", "c", "p") if intensity else (), dx=dx)
    return LW.LabStepper(w, {}), dx


def spectra(N, ell, intensity, seed=0):
    st, dx = stepper(N, ell, intensity)
    rng = np.random.default_rng(seed)
    acc = {f: np.zeros((N, N)) for f in "acp"}
    var = {f: 0.0 for f in "acp"}
    for _ in range(DRAWS):
        s = {"a": np.zeros((N, N)), "c": np.zeros((N, N)), "p": np.ones((N, N))}
        s = st.add_noise(s, rng, 1.0)
        s["p"] = s["p"] - 1.0
        for f in "acp":
            acc[f] += np.abs(np.fft.fft2(s[f])) ** 2 * dx**2 / (N * N)
            var[f] += float(s[f].var())
    ky = 2 * np.pi * np.fft.fftfreq(N, d=dx)[:, None]
    kx = 2 * np.pi * np.fft.fftfreq(N, d=dx)[None, :]
    k = np.hypot(ky, kx)
    kd2 = (2 * (1 - np.cos(ky * dx)) + 2 * (1 - np.cos(kx * dx))) / dx**2
    return {f: acc[f] / DRAWS for f in "acp"}, {f: np.sqrt(var[f] / DRAWS) for f in "acp"}, k, kd2


def main():
    k1 = 2 * np.pi / L
    rows, curves = [], {}
    for intensity in (True, False):
        for N in (96, 128, 192, 256):
            for ell in (None, 1.0, 2.0, 4.0):
                S, sdpt, k, kd2 = spectra(N, ell, intensity)
                g = np.exp(-((ell or 0.0) ** 2) * k**2)
                low = (k > 0) & (k <= 2 * k1 + 1e-9)
                mid = (k > 0) & (k * (ell or 1.0) <= 1.0)     # where exp(-ell^2 k^2) >= 0.37
                r = dict(form="intensity" if intensity else "per-point (legacy)", N=N, dx=round(L / N, 4),
                         ell=ell, modes_low=int(low.sum()))
                for f in "ap":
                    r[f"{f}_low_over_sd2"] = float(S[f][low].mean() / SD**2)
                    r[f"{f}_comp_over_sd2"] = float((S[f][mid] / g[mid]).mean() / SD**2)
                    r[f"{f}_pointwise_sd_over_sd"] = float(sdpt[f] / SD)
                r["c_low_over_0.25sd2k2"] = float((S["c"][low] / (0.25 * SD**2 * k[low] ** 2)).mean())
                r["c_comp_over_expected"] = float((S["c"][mid] / (0.25 * SD**2 * kd2[mid] * g[mid])).mean())
                r["c_pointwise_sd_over_sd"] = float(sdpt["c"] / SD)
                rows.append(r)
                print(json.dumps({k_: (round(v, 4) if isinstance(v, float) else v) for k_, v in r.items()}), flush=True)
                # radial curve for the figure
                kb = np.arange(0.5, N // 2) * k1
                idx = np.digitize(k.ravel(), np.concatenate([[0], kb]))
                prof = np.bincount(idx, S["a"].ravel(), minlength=len(kb) + 2) / np.maximum(
                    np.bincount(idx, minlength=len(kb) + 2), 1)
                curves[f"{r['form']}|{N}|{ell}"] = dict(k=(np.arange(1, len(kb)) * k1).tolist(),
                                                        S=(prof[2:len(kb) + 1] / SD**2).tolist())
    (OUT / "spectrum.json").write_text(json.dumps(dict(draws=DRAWS, sd=SD, box=L, rows=rows, curves=curves), indent=1))


if __name__ == "__main__":
    main()
