"""bench/roofline.py — arithmetic-intensity model + roofline figure.

Step cost model for one field of size N x N (rfft2 half-spectrum M = N*(N/2+1)):
  FFT flops: 2 real-2D transforms ~ 2 * 2.5 N^2 log2(N^2)  (real transform =
             ~half of complex 5 N^2 log2(N^2) mult-add count, Cooley-Tukey)
  pointwise: reaction (~15 flops/px for cubic+relax mix), E-multiply
             (2 flops/complex px), noise (when on).
Bytes (per field-step, minimum): the step reads and writes the state a few
times; with perfect fusion the floor is ~2 moves of F + 2 moves of the
half-spectrum + 1 read of E. FFTs are not fusable with pointwise in XLA
(cuFFT library calls), so each FFT stage adds its own read+write pass.

The model is used to place measured points on the device roofline; the point
of the figure is WHERE the kernel sits (bandwidth-bound), not 5% accuracy.
"""
import numpy as np

BYTES = dict(f32=4, f64=8)

# A100 40GB SXM4 peaks (NVIDIA datasheet)
A100 = dict(name="A100 40GB SXM4",
            bw_GBs=1555.0,
            fp32_TFLOPS=19.5,      # non-tensor FP32 (we pin HIGHEST precision)
            fp64_TFLOPS=9.7)


def step_flops_per_field(N, reaction_flops=15):
    """Total flops for one field's step at N^2 (fwd+inv rFFT + pointwise)."""
    fft = 2 * 2.5 * N * N * np.log2(N * N)      # fwd + inv real 2D
    M = N * (N // 2 + 1)
    pw = reaction_flops * N * N + 6 * M          # reaction + complex E-mult
    return fft + pw, fft, pw


def step_bytes_per_field(N, dtype="f32", passes=None):
    """Bytes moved per field-step. passes: dict of stage->(reads, writes) in
    units of field-size arrays. Default: measured-XLA-like decomposition:
      reaction+update (fused): read F(all coupled fields ~ amortized 1.5x),
                               write F'         -> 2.5 passes of N^2
      rfft2: read N^2 real, write M complex (2 floats)
      E-mult: read M cplx + E cplx-size real (assume f32 E), write M cplx
      irfft2: read M cplx, write N^2 real
    """
    b = BYTES[dtype]
    M = N * (N // 2 + 1)
    n2 = N * N
    react = 2.5 * n2 * b
    fwd = n2 * b + 2 * M * b
    emul = 2 * M * b * 2 + M * b   # read+write spectrum + read E (real, same dt)
    inv = 2 * M * b + n2 * b
    return react + fwd + emul + inv


def step_bytes_staged(N, dtype="f32"):
    """Staged (as-executed) traffic model: cuFFT runs row and column passes
    (each a full read+write of the array), the E-multiply and reaction are
    separate XLA kernels. This is what the pipeline ACTUALLY moves:
      reaction+update : read F (+coupled fields ~1.5x amortized), write F'
      rfft2 row pass  : r N^2, w 2M ; col pass: r 2M, w 2M
      E-mult          : r 2M, r E (M, f32), w 2M
      irfft2 col pass : r 2M, w 2M ; row pass: r 2M, w N^2
    M = N*(N/2+1) ~ N^2/2 complex numbers (x2 floats).
    """
    b = BYTES[dtype]
    M = N * (N // 2 + 1)
    n2 = N * N
    react = 2.5 * n2 * b
    fwd = (n2 + 2 * M) * b + (4 * M) * b
    emul = (4 * M) * b + M * 4          # E stored f32-per-dtype run; ~M reals
    inv = (4 * M) * b + (2 * M + n2) * b
    return react + fwd + emul + inv


def intensity(N, dtype="f32"):
    fl, fft, pw = step_flops_per_field(N)
    by = step_bytes_per_field(N, dtype)
    return fl / by


def predicted_ms_per_step(N, nfields, dtype="f32", dev=A100, fft_eff=0.5):
    """Bandwidth-bound prediction (ms) with an FFT-efficiency fudge."""
    by = step_bytes_per_field(N, dtype) * nfields
    return by / (dev["bw_GBs"] * 1e9 * fft_eff) * 1e3


if __name__ == "__main__":
    for N in (128, 256, 512, 1024):
        fl, fft, pw = step_flops_per_field(N)
        by = step_bytes_per_field(N)
        print(f"N={N:5d} flops/field-step {fl/1e6:7.2f}M "
              f"(fft {100*fft/fl:.0f}%) bytes {by/1e6:6.2f}MB "
              f"AI={fl/by:5.2f} flop/B "
              f"-> bw-bound floor {by/(A100['bw_GBs']*1e9)*1e6:6.1f} us/field")
