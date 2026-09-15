"""Fresh prepared-pair test of XV rotation and a cross-coupling control."""

import argparse
import copy
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from blobkit import genome as G
from blobkit import worlds
from blobkit.soup import sim_cpu
from characterize import digest, write_json


def run(seed, coupled, output):
    label = f"xv_pair_{'coupled' if coupled else 'decoupled'}_s{seed}"
    output = Path(output) / label
    output.mkdir(parents=True, exist_ok=False)
    g = copy.deepcopy(worlds.load("xv"))
    if not coupled:
        g["W"][0][1] = 0.0
        g["W"][1][0] = 0.0
        g["id"] += "_cross_drive_removed"
    state = sim_cpu.init_soup(g, L=128.0, seed=seed, n_soup=0, workers=1, noise=0.002)
    stamp = G.load_stamp_A4()
    # Private M4 inhibitor shadows; coupling drives evolve from time zero.
    for mapping, x in ((dict(du=0, dv=2, dw=4), 60.0), (dict(du=1, dv=3, dw=5), 68.0)):
        G.paste_stamp(state["F"], stamp, mapping, x=x, y=64.0, dx=0.5)
    write_json(output / "genome.json", g)
    write_json(
        output / "protocol.json",
        dict(
            world="xv",
            seed=seed,
            coupled=coupled,
            horizon_tu=2500,
            dtype="f32",
            initialization="Installed A4 deviation stamp; act0 at (x=60,y=64), act1 at (68,64); no kick.",
            noise=0.002,
            L=128.0,
            dx=0.5,
            dt=0.02,
            control="Only W[0,1] and W[1,0] set to zero in the decoupled run.",
            sources={
                "rotor_check.py": digest(__file__),
                "genome.py": digest(G.__file__),
                "sim_cpu.py": digest(sim_cpu.__file__),
            },
        ),
    )
    fields, times = [state["F"].copy()], [0.0]
    started = time.monotonic()
    for t in range(250, 2501, 250):
        if sim_cpu.advance(state, t) != "ok":
            raise ValueError(f"{label} failed at {t}: {state['status']}")
        fields.append(state["F"].copy())
        times.append(float(t))
        if t % 500 == 0:
            print(f"{label}: T={t}, {time.monotonic() - started:.0f}s", flush=True)
    record = sim_cpu.snapshot_rec(state)
    np.savez_compressed(output / "fields.npz", F=np.stack(fields), t=np.array(times))
    np.savez_compressed(output / "final_state.npz", F=state["F"])
    write_json(output / "record.json", record)
    ts, separations, angles = [], [], []
    for k, t in enumerate(record["t"]):
        first, second = record["blobs"][0][k], record["blobs"][1][k]
        if len(first) == len(second) == 1:
            dy, dx = G.min_image(np.array(first[0][:2]) - np.array(second[0][:2]), 128)
            ts.append(float(t))
            separations.append(float(np.hypot(dy, dx)))
            angles.append(float(np.arctan2(dy, dx)))
    ts, angle = np.array(ts), np.unwrap(angles)
    late = ts >= 1500
    if late.sum() < 10:
        raise ValueError("Insufficient intact-pair evidence")
    slope, offset = np.polyfit(ts[late], angle[late], 1)
    result = dict(
        coupled=coupled,
        seed=seed,
        intact_pair_frames=len(ts),
        total_frames=len(record["t"]),
        angular_velocity_rad_per_tu=float(slope),
        late_turns=float((angle[late][-1] - angle[late][0]) / (2 * np.pi)),
        late_separation_mean=float(np.mean(np.array(separations)[late])),
        late_separation_std=float(np.std(np.array(separations)[late])),
        angle_fit_rms_rad=float(np.sqrt(np.mean((angle[late] - (slope * ts[late] + offset)) ** 2))),
        t=ts,
        angle_unwrapped=angle,
        separation=separations,
        wall_seconds=time.monotonic() - started,
    )
    write_json(output / "rotation.json", result)
    print(f"ROTATION {label}: omega={slope:.6g}, turns={result['late_turns']:.3g}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    with ProcessPoolExecutor(max_workers=2) as pool:
        jobs = [
            pool.submit(run, seed, coupled, args.output)
            for seed, coupled in ((12001, True), (12002, True), (12001, False))
        ]
        for job in jobs:
            job.result()
