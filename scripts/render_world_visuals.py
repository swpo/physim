"""Render website field snapshots from recorded simulation data; never simulate."""

import argparse
import hashlib
import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/physim-world-figures-mpl")
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs_source/data/world-visuals.npz"
META = DATA.with_suffix(".json")
PANELS = (
    ("bf-sham", "bf/science/sham/fields.npz", 50),
    ("bf-trail-pulse", "bf/science/trail_high/fields.npz", 50),
    ("xv-0", "xv/causal_extended/coupled.npz", 0),
    ("xv-125", "xv/causal_extended/coupled.npz", 125),
    ("xv-250", "xv/causal_extended/coupled.npz", 250),
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def capture(source):
    """Keep small, exact spatial crops so figure rendering needs no research tree."""
    arrays, panels = {}, []
    for key, relative, time in PANELS:
        name = key.split("-")[0]
        apparatus = json.loads((source / name / "preparation/apparatus.json").read_text())
        with np.load(source / relative, allow_pickle=False) as data:
            index = np.flatnonzero(data["t"] == time)
            if len(index) != 1:
                raise ValueError(f"Missing or repeated time {time} in {relative}")
            fields = data["F"]
            center = np.array(apparatus["devices"][0]["parameters"]["center"])
            if name == "xv":
                center = data["centers"][0].mean(axis=0)
            origin = np.floor(center / 0.5) * 0.5
            half_cells = 40 if name == "xv" else 32
            radius = half_cells * 0.5
            indices = [(np.arange(-half_cells, half_cells) + int(value / 0.5)) % 256 for value in origin]
            arrays[key] = fields[index[0], : 2 if name == "xv" else 1][:, indices[0]][:, :, indices[1]]
            arrays[key + "-initial"] = fields[0, 0][np.ix_(*indices)]
        panels.append(
            dict(
                key=key,
                time=time,
                source=str((source / relative).relative_to(ROOT)),
                source_sha256=digest(source / relative),
                crop_origin_yx=origin.tolist(),
                emitter_relative_yx=(np.array(apparatus["emitter_yx"]) - origin).tolist(),
                extent=[-radius, radius, radius, -radius],
                dx=0.5,
                realization="First recorded realization",
            )
        )
    np.savez_compressed(DATA, **arrays)
    META.write_text(
        json.dumps(
            dict(
                description="Exact field-array crops for the Worlds page; no temporal or spatial interpolation.",
                data_sha256=digest(DATA),
                scale=dict(field="activator 0", vmin=-1, vmax=1.6, cmap="viridis"),
                panels=panels,
            ),
            indent=2,
        )
        + "\n"
    )


def render(output):
    output.mkdir(exist_ok=True, parents=True)
    metadata = json.loads(META.read_text())
    assert digest(DATA) == metadata["data_sha256"]
    scale = metadata["scale"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "text.color": "#17242f"})
    with np.load(DATA, allow_pickle=False) as data:
        for panel in metadata["panels"]:
            key = panel["key"]
            fields = data[key]
            assert np.isfinite(fields).all()
            assert scale["vmin"] <= fields[0].min() and fields[0].max() <= scale["vmax"]
            fig = plt.figure(figsize=(3.2, 3.2))
            ax = fig.add_axes([0, 0, 1, 1])
            ax.imshow(
                fields[0],
                cmap=scale["cmap"],
                vmin=scale["vmin"],
                vmax=scale["vmax"],
                extent=panel["extent"],
                interpolation="nearest",
            )
            left, right, bottom, top = panel["extent"]
            coordinates = np.arange(left, right, 0.5) + 0.25
            if key.startswith("bf"):
                ax.contour(
                    coordinates,
                    coordinates,
                    data[key + "-initial"],
                    levels=[0.5],
                    colors="#ffffff",
                    linewidths=1.1,
                    linestyles="dashed",
                )
                y, x = panel["emitter_relative_yx"]
                ax.plot(x, y, "+", color="#ffb7d0", ms=12, mew=1.8)
            else:
                ax.contour(coordinates, coordinates, fields[1], levels=[0.5], colors="white", linewidths=1.4)
            ax.plot([left + 3, left + 8], [bottom - 3.5] * 2, color="white", lw=2.4)
            ax.text(left + 5.5, bottom - 4.6, "5 units", color="white", ha="center", va="bottom", fontsize=11)
            ax.set_axis_off()
            fig.savefig(output / f"{key}.png", dpi=160)
            plt.close(fig)
            print(f"{key}: t={panel['time']}, activator range {fields[0].min():.4f} to {fields[0].max():.4f}")
    fig = plt.figure(figsize=(3.5, 0.65))
    bar = fig.add_axes([0.13, 0.5, 0.73, 0.28])
    fig.colorbar(
        matplotlib.cm.ScalarMappable(norm=Normalize(scale["vmin"], scale["vmax"]), cmap=scale["cmap"]),
        cax=bar,
        orientation="horizontal",
        ticks=[-1, 0, 1, 1.6],
    )
    fig.savefig(output / "activator-scale.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture-from", type=Path, help="Optional original preparation-study directory")
    parser.add_argument("--output", type=Path, default=ROOT / "docs/assets/worlds")
    args = parser.parse_args()
    if args.capture_from:
        capture(args.capture_from.resolve())
    render(args.output)
