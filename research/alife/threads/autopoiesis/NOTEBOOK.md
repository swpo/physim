# Autopoiesis notebook

Sprint 1 start: 2026-10-24 14:28 UTC. Tools: `screen.py` (quick strips with dimmed substrate, per-frame
stats), `sweep.py` (lattice SCL membrane-closure screen: fraction of samples where the planted ring
still encloses >= half its area; 2 seeds x 3000 sweeps).

## 1. Lattice SCL reference (`worlds/scl_lattice`)
Numba random-sequential SCL on 64x64: hole/S/K/L, link bonds as 8-bit masks, McMullin-style
rules (bond angle >= 90 deg, no diagonal crossing, bonded links immobile, S permeates bonded L
by jumping over it, K + 2S -> K + L, L -> 2S). Planted 9-px ring around one catalyst.
- v0 (p_ext=0.9: any link adjacent to a chain end bonds): the ring persists 1000 sweeps but
  internal links bond onto gap ends and grow inward spurs; the interior fills with debris
  chains and K eventually escapes (`screens/scl_base.png`). Classic SCL failure mode.
- v1: added **splice** (a free link touching two chain ends bonds to both at once, p=1) and
  made end-to-end joins likely (p_join=0.9) but single-end extension rare (p_ext=0.05).
  Closure fraction 0.59/0.64 (2 seeds) at p_dis=5e-4; 0.00/0.03 at p_dis=2e-3.
- separate decay for free links (p_disf=5e-3, cleans leaked links): no robust gain (0.39-0.78).
- MIN_SEP=3 (bond angle >= 135 deg, stiffer membrane) + p_dis=2e-4: closure 0.67/0.76, the best
  lattice setting. Gaps open and are re-spliced continually; catalysts sometimes escape through
  a gap (`screens/scl_k3.png`, 3 catalysts). Lattice SCL membranes are maintained but leaky:
  consistent with the historical record.

## 2. Gated protocell, continuum SCL on a Gray-Scott replicator (`worlds/gated_protocell`)
Fields S, K, L, M. K + S -> K + L; L polymerizes into M where |grad L| is large (edge of the
link cloud); M gates the diffusion of L (and optionally K) through div(D g(M) grad u) with face
mobility min(g_i, g_j); K autocatalysis S K^2 needs h(L) (Hill), so the catalyst only grows where
the membrane holds links in.
- numerics: explicit Euler blew up (K^2 S consuming more S than present once K was trapped);
  fixed by capping consumption at 0.5 S per step, and clipping. Central-difference |grad L|
  gave dotted (checkerboard) membranes; smoothing L before the gradient fixed it.
- b=0.2, gated K: 4 small cells (ring of M, K inside) form from the 4 GS seeds and then freeze
  in a steady state: no growth, no division (`screens/gp_L0-0.1_b-0.2.png`). L3 morphology but static.
- membrane ablation (cM=0, no polymerization): L diffuses away, h(L) falls, K dies everywhere
  within ~1500 steps (`screens/gp5_*cM-0.0*`). The membrane is necessary for the catalyst.
