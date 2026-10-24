# x-genome v0: minimal extensions to the blobkit deviation-form genome

Reference implementation: `xgenome.py` (≈150 lines; parity with blobkit `run_genome` on m4:
max |Δ| = 3.8e-14 after 1000 steps). Every new key is optional; a genome without them is a
plain blobkit genome. Every new term vanishes identically at the designated vacuum
(u = u0, x = 0) for any coefficient, so the iso-background property is preserved.

| key | term added | role found in sprint 1 |
|---|---|---|
| `chan.g = "band"` | drive g(z) = 4s(1−s), s = tanh(max(z−thr,0)/sc) | deposits a channel at the activator *front* only → membrane ring |
| `chan.ch = {M,k,h}` | +M ∇²[x(x−h)(x−1)] − M k ∇⁴x on that channel (k∇⁴ in the exact Fourier factor) | caps the membrane at the x=1 well and sets its width; improves sealing |
| `perm = [[f, c, β]]` | diffusion of state field f becomes ∇·(D_f e^{−β max(x_c,0)} ∇f) | membrane gates transport: containment of fast-diffusing species, the key operator |
| `kern = {R,w}` on a channel | drive replaced by ring-kernel convolution of g(z) | (screened; gave Turing tilings) |
| `taxis = [[i,c,χ]]` | −χ ∇·(max(z_i,0) ∇x_c) | (screened; χ>0 collapse, χ<0 worms) |
| `porous = [[i,Dm,p]]` | +∇·(Dm max(z_i,0)^p ∇u_i) | (screened; tiling) |
| `adv = [c, α]` | all deviations advected by v = −α∇x_c (upwind) | (screened; α>0 spot proliferation) |

Numerics: unchanged blobkit convention (dx = 0.5, dt = 0.02, explicit reaction with old
fields, exact Fourier diffusion). Explicit-stability notes: the CH explicit part needs
dt·M·h·8/dx² < 1 (fine at dx=0.5; at dx=0.33 use dt=0.01); the perm correction is
explicit anti-diffusion bounded by D_f and is stable together with the exact step.

Minimal "cell" recipe (worlds/xcell-*): m4 + one band/CH membrane channel (W=2, τ=2,
D=0) + one cargo channel (W=1, τ=5, D=4) gated by the membrane (β=5). Add
K[u,cargo] = −0.25 and a global channel (τ=10, D=100, K=1) for division with a population
cap. (Sprint 1 also listed "a gated waste channel for turnover". That is RETRACTED: the
xcell-turn waste was gated by the cargo channel, not by m, and was planted in the founders.)

## v0.1 (sprint 2): named channels, and the xcell-evo genome

`perm` and `taxis` entries may name their fields: `["c", "m", 5.0]` = gate the diffusion of
channel `c` by channel `m`. Acts and channels carry an optional `"name"`; numeric indices still
work (parity with blobkit unchanged, 3.8e-14). World inits plant only the body (u poke) and its
fast/slow inhibitors (v, w dress); every other channel starts at the vacuum (0).

**xcell-evo** (`evo.py`; arms S/N/L), acts `u` (body, m4 cubic) and `h` (marker:
−h³ + h − 0.2, vacuum = low root −1.088, Du 0.3; arm L: 0.05, ungated):

| channel | τ | D | g | drive W[·,(u,h)] | K[u,·] | K[h,·] | role |
|---|---|---|---|---|---|---|---|
| v | 6 | 0.667 | id | (1, 0) | 1.0 | 0 | m4 slow inhibitor |
| w | 0.7 | 20 | id | (1, 0) | 1.5 | 0 | m4 fast inhibitor |
| m | 2 | 0 | band, CH(M=1,k=1,h=0.5) | (2, 0) | 0 | 0 | membrane at the body front |
| glob | 10 | 100 | id | (1, 0) | 1.0 | 0 | global cap on body mass |
| bdep | 1 | 0.5 | id | (1, 0) | 0 | −0.25 | tilts h toward on inside bodies |
| c | 5 | 4 | id | (1, wch) | −0.25 | 0 | cargo: activates the body; S: marker adds production |
| q | 40 | 2 | id | (1, 0) | 0.15 | 0 | waste (in practice inert at this K: no deaths) |

perm: `[c, m, 5]`, `[q, m, 5]`, `[h, m, 5]` (the last is absent in arm L).
World-level additions (in world.py, not the genome): Poisson h kicks (σ 1.5, amp 2.5) and,
in `xcell-evo2-*`, imposed dilution (disk erasure, radius 5, rate 0.1 per time unit).
