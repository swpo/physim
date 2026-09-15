"""Fresh paired interventions and native sensor readings from preserved states.

Investigator diagnostics, not an evaluation suite. Uses current installed source
and sensor operations. Common noise isolates intervention effects; independent
members separately measure ordinary between-realization differences.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path

for variable in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(variable, "1")

import numpy as np
from blobkit.soup import sim_cpu
from characterize import digest, write_json
from physim import devices


def probe(source):
    source = Path(source)
    output = source / "responses"
    output.mkdir(exist_ok=False)
    g = json.loads((source / "genome.json").read_text())
    protocol = json.loads((source / "protocol.json").read_text())
    with np.load(source / "final_state.npz", allow_pickle=False) as data:
        initial = data["F"].copy()
    # A fixed, reproducible investigator placement rule, chosen before responses.
    y, x = np.unravel_index(np.argmax(initial[0]), initial[0].shape)
    center = np.array([(y + 0.5) * 0.5, (x + 0.5) * 0.5])
    emitter = (center + np.array([0.0, 6.0])) % 128.0
    instrument = devices.ProbeDevice(
        dev_id=0,
        lattice="square",
        n_rings=3,
        base_ds=3.0,
        center=center,
        L=128.0,
        secret_rot=0.0,
        reflect=False,
        motion_theta=0.0,
        motion_reflect=False,
        node_perm=np.arange(13),
    )
    times = np.array([0.0, 5.0, 10.0, 25.0, 50.0])
    seeds = [22001, 22002, 22003]
    arms = ["baseline", "pulse_0.05", "pulse_0.3"]
    if protocol["world"] == "bf":
        arms.append("erase_trail")
    samples, finals = [], []
    for arm in arms:
        members = []
        for member, seed in enumerate(seeds):
            state = sim_cpu.init_soup(g, L=128.0, seed=seed, n_soup=0, workers=1, noise=0.002)
            state["F"] = initial.copy()
            if arm == "erase_trail":
                # BFIELD's third channel is its relaxing trail. No equation is changed.
                assert len(g["acts"]) == 1 and len(g["chans"]) == 3
                state["F"][3] = 0
            readings = [instrument.sample(state["F"], 0.5)]
            for previous, target in zip(times[:-1], times[1:]):
                injections = []
                if previous == 0 and arm.startswith("pulse_"):
                    injections = [dict(field=0, y=float(emitter[0]), x=float(emitter[1]), amp=float(arm[6:]))]
                devices.step_chunk(state, int(round((target - previous) / 0.02)), injections=injections)
                if not np.isfinite(state["F"]).all():
                    raise ValueError(f"Nonfinite response: {source.name}, {arm}, {seed}")
                readings.append(instrument.sample(state["F"], 0.5))
            members.append(readings)
            if member == 0:
                finals.append(state["F"].copy())
        samples.append(members)
    samples = np.array(samples)
    np.savez_compressed(
        output / "samples.npz", samples=samples, times=times, seeds=np.array(seeds), arms=np.array(arms)
    )
    np.savez_compressed(output / "final_fields.npz", F=np.stack(finals), arms=np.array(arms))

    # RMS is descriptive, in raw field units. Per-port values remain available.
    def rms(value):
        return np.sqrt(np.mean(np.asarray(value, float) ** 2, axis=(-1, -2)))

    baseline = samples[0]
    between = np.stack([rms(baseline[i] - baseline[j]) for i, j in ((0, 1), (0, 2), (1, 2))])
    effects = {arm: rms(samples[i] - baseline).tolist() for i, arm in enumerate(arms) if i}
    per_port = {
        arm: np.sqrt(np.mean((samples[i] - baseline) ** 2, axis=-1)).tolist() for i, arm in enumerate(arms) if i
    }
    result = dict(
        world=protocol["world"],
        preparation_seed=protocol["seed"],
        times=times,
        noise_seeds=seeds,
        baseline_drift_rms=rms(baseline - baseline[:, :1]),
        independent_pair_difference_rms=between,
        paired_effect_rms=effects,
        paired_effect_rms_per_port=per_port,
        placement=dict(
            rule="Probe centered on initial activator-0 maximum; emitter offset +6px in x.",
            probe_center_yx=center,
            emitter_yx=emitter,
            probe_nodes_yx=instrument.node_positions(),
        ),
        interventions=dict(
            pulses="Activator 0 source, Gaussian sigma=2px, amplitude 0.05 or 0.3, t=[0,5).",
            erase_trail="BF only: set initial trail channel to zero. Privileged diagnostic, not an agent action.",
        ),
        scope="Three independent future noise seeds per preserved start; paired treatment/control within each seed. Raw RMS across all fields and probe nodes, not a prediction score.",
        source_sha256={
            "devices.py": digest(devices.__file__),
            "probe_candidates.py": digest(__file__),
            "initial_fields": hashlib.sha256(initial.tobytes()).hexdigest(),
        },
    )
    write_json(output / "summary.json", result)
    print(
        f"PROBED {source.name}: final drift={np.mean(rms(baseline - baseline[:, :1])[:, -1]):.4g}, "
        f"noise difference={between[:, -1].mean():.4g}, "
        f"pulse 0.3={np.mean(np.array(effects['pulse_0.3'])[:, -1]):.4g}",
        flush=True,
    )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", type=Path)
    args = parser.parse_args()
    for source in args.sources:
        probe(source)
