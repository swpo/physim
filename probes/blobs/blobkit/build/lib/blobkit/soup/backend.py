"""blobkit.soup.backend — uniform backend selector for the S1 soup assay.

get_backend("cpu") / get_backend("gpu") -> namespace with the four locked
entry points used by assay_v2 and the deploy workers:

    init_soup(g, L=..., seed=..., workers=..., kicks=...) -> S
    advance(S, T_target) -> status
    snapshot_rec(S) -> record dict
    save_run(rec, path)

"cpu": blobkit.soup.sim_cpu (the LOCKED soup_sim_v2 numerics, verbatim).
"gpu": blobkit.soup.sim_gpu (blobgpu port; requires jax — pip install
       'blobkit[gpu]'). GPU advance/snapshot wrap the *_gpu drivers so the
       calling contract is identical; init_soup builds ICs with the same
       numpy RNG (bit-identical seeded states) and packs to device.
"""
from types import SimpleNamespace


def get_backend(name="cpu"):
    if name == "cpu":
        from . import sim_cpu
        return SimpleNamespace(
            name="cpu",
            init_soup=sim_cpu.init_soup,
            advance=sim_cpu.advance,
            snapshot_rec=sim_cpu.snapshot_rec,
            save_run=sim_cpu.save_run,
        )
    if name == "gpu":
        from . import sim_gpu
        from . import sim_cpu

        def init_soup(g, L=128.0, seed=0, dtype="f32", kicks=None,
                      noise=None, workers=0, n_soup=None, gpu_seed=None):
            kw = {}
            if noise is not None:
                kw["noise"] = noise
            if n_soup is not None:
                kw["n_soup"] = n_soup
            return sim_gpu.init_soup_gpu(g, L=L, seed=seed, dtype=dtype,
                                         kicks=kicks, gpu_seed=gpu_seed, **kw)

        return SimpleNamespace(
            name="gpu",
            init_soup=init_soup,
            advance=sim_gpu.advance_gpu,
            snapshot_rec=sim_gpu.snapshot_rec_gpu,
            save_run=sim_cpu.save_run,
        )
    raise ValueError(f"unknown backend {name!r} (want 'cpu' or 'gpu')")
