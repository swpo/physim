from functools import partial

import numpy as np
import pytest
from blobkit import genome, worlds
from blobkit.soup import sim_cpu, sim_gpu
from test_cpu import canonical

pytestmark = pytest.mark.accelerator


def relative_error(a, b):
    return float(
        np.linalg.norm(np.asarray(a, np.float64) - np.asarray(b, np.float64))
        / max(np.linalg.norm(np.asarray(b, np.float64)), 1e-30)
    )


@pytest.mark.parametrize("name", worlds.GT_SET)
def test_f64_cpu_accelerator_trajectory(accelerator, name):
    g = worlds.load(name)
    kw = dict(L=64, seed=1, dtype="f64", noise=0, kicks=worlds.kicks_for(g))
    cpu = sim_cpu.init_soup(g, workers=1, **kw)
    gpu = sim_gpu.init_soup_gpu(g, **kw)
    np.testing.assert_array_equal(cpu["F"], gpu["F"])
    sim_cpu.advance(cpu, 25)
    sim_gpu.advance_gpu(gpu, 25)
    assert relative_error(cpu["F"], gpu["F"]) < 1e-9


def test_noisy_chunking_is_bitwise(accelerator):
    g = worlds.load("m4")
    a, b = [sim_gpu.init_soup_gpu(g, L=64, seed=3) for _ in range(2)]
    sim_gpu.advance_gpu(a, 100)
    for target in (25, 50, 75, 100):
        sim_gpu.advance_gpu(b, target)
    np.testing.assert_array_equal(a["F"], b["F"])
    assert canonical(sim_gpu.snapshot_rec_gpu(a)) == canonical(sim_gpu.snapshot_rec_gpu(b))


def packed_run(gens, fields, seeds, noise=0.002):
    import jax.numpy as jnp

    params, struct, _ = sim_gpu.pack_genomes(gens, dtype=np.float32)
    initial = sim_gpu.pack_states(gens, fields, struct["na_max"], struct["nc_max"])
    device_params = {key: jnp.asarray(value) for key, value in params.items()}
    device_params["E"] = sim_gpu.diffusion_E(params["D"], 64, 0.5, 0.02, np.float32)
    step = sim_gpu.make_stepper(struct, 64, 0.5, 0.02, noise=noise)
    final = step(jnp.asarray(initial), device_params, sim_gpu.batch_keys(seeds), 0, 200)
    return np.asarray(final), struct


@pytest.mark.parametrize("name", ["bf", "xv", "m4"])
def test_padding_and_noise_are_lane_independent(accelerator, name):
    g, other = worlds.load(name), worlds.load("pred")
    fields = [genome.poke(genome.state_vacuum(x, 64), x, 0, 16, 16, 2, 3, 0.5).astype(np.float32) for x in (g, other)]
    single, s = packed_run([g], fields[:1], [7])
    batch, b = packed_run([g, other], fields, [7, 9])
    ref = sim_gpu.unpack_state(g, single[0], s["na_max"])
    got = sim_gpu.unpack_state(g, batch[0], b["na_max"])
    # cuFFT can choose different plans for different batch shapes.
    assert relative_error(ref, got) <= 1e-5
    na, nc = len(g["acts"]), len(g["chans"])
    assert (batch[0, na : b["na_max"]] == 0).all()
    assert (batch[0, b["na_max"] + nc :] == 0).all()


def test_explicit_initial_fields_are_owned_and_recorded(accelerator):
    g = worlds.load("m0")
    ic = genome.state_vacuum(g, 128).astype(np.float32)
    ic = genome.poke(ic, g, 0, 20, 20, 2, 3, 0.5)
    original = ic.copy()
    batch = sim_gpu.init_soup_gpu_batch([(g, 5)], L=64, ics=[ic])
    ic[:] = 99
    np.testing.assert_array_equal(sim_gpu._pull(batch["_gpu"])[0], original)
    sim_gpu.advance_gpu_batch(batch, 25)
    np.testing.assert_array_equal(batch["worlds"][0]["snaps"][0], original[:1])


@pytest.mark.slow
def test_full_grid_seven_world_batch_matches_cpu(accelerator):
    names = worlds.GT_SET
    batch = sim_gpu.init_soup_gpu_batch(
        [(worlds.load(n), 1) for n in names], L=128, dtype="f64", noise=0, kicks_map=worlds.KICKS
    )
    sim_gpu.advance_gpu_batch(batch, 100)
    for name, lane in zip(names, batch["worlds"]):
        g = worlds.load(name)
        cpu = sim_cpu.init_soup(g, L=128, seed=1, dtype="f64", noise=0, kicks=worlds.kicks_for(g), workers=1)
        sim_cpu.advance(cpu, 100)
        error = relative_error(cpu["F"], lane["F"])
        assert error < 1e-5, (name, error)


@pytest.mark.slow
@pytest.mark.parametrize("padding", [(1, 2), (2,)])
def test_assay_repack_and_ballast_match_singles(accelerator, padding):
    from blobkit.assay_batch import run_assay_batch
    from blobkit.assay_v2b import run_assay_b
    from blobkit.soup import get_backend

    jobs = [
        dict(genome=worlds.load("m0"), seed=7, t0=1250, cap=1250),
        dict(genome=worlds.load("m4"), seed=1, t0=2500, cap=2500),
    ]
    batch = run_assay_batch(jobs, dtype="f64", L=64, t0=1250, cap=2500, battery_procs=2, B_pad=padding, verbose=False)
    backend = get_backend("gpu")
    backend.init_soup = partial(backend.init_soup, dtype="f64")
    for job, actual in zip(jobs, batch):
        expected = run_assay_b(
            job["genome"],
            seed=job["seed"],
            L=64,
            t0=job["t0"],
            cap=job["cap"],
            backend=backend,
            workers=1,
            verbose=False,
            results_path=None,
        )
        assert canonical(actual) == canonical(expected)


@pytest.mark.slow
@pytest.mark.parametrize("mode", ["async", "device"])
def test_accelerated_recording_matches_host(accelerator, mode):
    from blobkit.soup import asyncapply_proto, devrec_proto

    jobs = [(worlds.load(n), i + 1) for i, n in enumerate(["m0", "pred"])]
    host = sim_gpu.init_soup_gpu_batch(jobs, L=64)
    sim_gpu.advance_gpu_batch(host, 500)
    fast = sim_gpu.init_soup_gpu_batch(jobs, L=64)
    if mode == "device":
        devrec_proto.install(async_apply=True)
    else:
        asyncapply_proto.install()
    try:
        sim_gpu.advance_gpu_batch(fast, 500)
    finally:
        if mode == "device":
            devrec_proto.uninstall()
        else:
            asyncapply_proto.uninstall(shutdown=True)
    for a, b in zip(host["worlds"], fast["worlds"]):
        np.testing.assert_array_equal(a["F"], b["F"])
        assert a["ts"] == b["ts"]
        assert canonical(a["patches"]) == canonical(b["patches"])
        for act in a["mass"]:
            np.testing.assert_allclose(a["mass"][act], b["mass"][act], atol=1e-10, rtol=1e-12)
        if mode == "async":
            assert canonical(a["blobs"]) == canonical(b["blobs"])
        else:
            for act in a["blobs"]:
                assert len(a["blobs"][act]) == len(b["blobs"][act])
                for first, second in zip(a["blobs"][act], b["blobs"][act]):
                    np.testing.assert_allclose(first, second, atol=1e-10, rtol=1e-12)
