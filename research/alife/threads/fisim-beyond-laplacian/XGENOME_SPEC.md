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
cap; add a gated waste channel (τ=40, D=2, K=+0.3) for turnover.
