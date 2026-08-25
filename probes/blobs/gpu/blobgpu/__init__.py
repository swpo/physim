"""blobgpu — JAX accelerator port of the L0 blob genome simulator.

Correctness-gated against the locked CPU numerics (see GATES.md):
  * f64 trajectory parity: rel L2 < 1e-5 at T=100tu vs genome.py/soup_sim f64
  * descriptor parity: locked metrics_v1 battery on the 7 ground truths
  * bond anchors: A4s pair d*=15.40 @ dt=0.02; A5 pair d*=15.70 @ dt=0.005

Modules: packing (genomes -> padded tensors), core (jitted stepper),
soup (run_soup_gpu, drop-in for soup_sim_v2), anchors (bond-anchor drivers).
"""
from .core import make_stepper, make_single_step, diffusion_E, k2_grid, enable_x64
from .packing import pack_genomes, pack_states, unpack_state
