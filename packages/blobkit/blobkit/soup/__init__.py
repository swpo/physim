"""blobkit.soup — S1 soup simulators (locked CPU kernel + JAX GPU port).

  sim_v1   soup_sim.py     (phase-5 single-shot run_soup; sim_cpu depends on it)
  sim_cpu  soup_sim_v2.py  (LOCKED chunked-continuation simulator)
  sim_gpu  blobgpu merge   (lazy-jax; pip install 'blobkit[gpu]')
  backend  get_backend("cpu"|"gpu") -> init_soup/advance/snapshot_rec/save_run
"""
from .backend import get_backend

__all__ = ["get_backend"]
