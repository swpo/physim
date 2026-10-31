"""Credit-free validation of a lab bundle through PhySim's own task code.

    python fedvortex_validate.py --bundle BUNDLE --out OUT [--reference-dir WORK/controls]

1. ``taskset.required_bundle`` opens the bundle (a ``LabBundle``) in both profiles and checks its runtime.
2. ``taskset.public_prompt`` renders the agent contract; the port counts must match the declared roster.
3. ``LaboratoryTools.experiment`` and ``LaboratoryTools.usage`` run directly on an ``R6State`` (the copy of
   each observation into the agent's container, ``_put_observation``, is skipped: there is no runtime here).
   A valid request is admitted and charged; an invalid port is rejected without charge.
4. Trusted predictors are graded with ``evaluation._forecast_suite`` / ``score_frozen`` (frozen forecasts,
   then the retained truths): initial persistence via ``evaluation.reference_demo`` (checks.json), and the
   native oracle's cached 64-member reference ensembles when ``--reference-dir`` is given. Rewards use
   ``rewards.precision_reward`` with the calibrated K.
No Prime sandbox, container or model call is made.
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import asyncio
import json
import shutil
import sys
from pathlib import Path

import numpy as np

ENV = Path(__file__).resolve().parents[3] / "environments" / "physim"
sys.path.insert(0, str(ENV))

from physim import evaluation as EV  # noqa: E402
from physim import labbundle as LB  # noqa: E402
from physim import taskset as TS  # noqa: E402
from physim.rewards import DEFAULT_PRECISION, precision_reward  # noqa: E402


def check_prompt(config, bundle):
    text = TS.public_prompt(config)
    n = bundle.roster.n_ports
    expected = [
        f"`port` is an integer from 0 to {n - 1}.",
        f"Each measurement interface returns {n} channels.",
        f"shape `(1, number_of_requested_times, {n}, slots)`",
        f"(n_samples, number_of_requested_times, {n}, number_of_output_slots)",
        '"port": 2',
    ]
    missing = [e for e in expected if e not in text]
    leftover = [k for k in ("{n_ports}", "{last_port}", "{example_port}") if k in text]
    return dict(ok=not missing and not leftover, missing=missing, unreplaced=leftover, chars=len(text),
                ports_line=next((l for l in text.splitlines() if "`port` is an integer" in l), None)), text


async def tool_calls(config, out: Path):
    import verifiers.v1.mcp.server as S

    TS._put_observation = lambda state, path: None   # no agent runtime in this local check
    tools = TS.LaboratoryTools(config)
    state = TS.R6State(output=str(out), usage=dict(experiments=0, max_experiments=config.max_experiments,
                                                   charged_tu=0, max_total_tu=config.max_total_tu))
    (out / "observations").mkdir(parents=True, exist_ok=True)
    token = S._call_state.set(state)
    try:
        good = json.loads(await tools.experiment(
            [dict(t=0, kind="inject", device=1, port=1, amp=3.0, dur=10.0), dict(t=1, kind="adjust", device=0, u=[0.2, -0.1, 0.0])],
            [dict(sensor="device0", t=[0, 5, 10]), dict(sensor="device1", t=[10, 20]), dict(sensor="global", t=[20])]))
        bad = json.loads(await tools.experiment([dict(t=0, kind="inject", device=0, port=4, amp=1.0, dur=1.0)],
                                                [dict(sensor="global", t=[1])]))
        usage = json.loads(await tools.usage())
    finally:
        S._call_state.reset(token)
    with np.load(out / "observations" / Path(good["path"]).name, allow_pickle=False) as z:
        shapes = {k: list(z[k].shape) for k in z.files if k.startswith("query")}
        finite = all(np.isfinite(z[k]).all() for k in z.files if k.startswith("query"))
    return dict(admitted=good, rejected=bad, usage=usage, saved_shapes=shapes, finite=finite,
                recorded_experiments=len(state.experiments), rejected_requests=state.rejected_requests)


def grade_reference(bundle, ref_dir: Path, out: Path, precision):
    """The native oracle as a trusted predictor: its cached 64-member ensembles, frozen then scored."""
    def predict(case, count, seed):
        path = ref_dir / f"reference_{case['id']}.npz"
        with np.load(path, allow_pickle=False) as z:
            meta = json.loads(str(z["meta"]))
            assert meta["actions"] == case["actions"] and meta["queries"] == case["queries"] and meta["members"] == count
            samples = [z[f"query{i}"].copy() for i in range(len(case["queries"]))]
        return dict(samples=samples), dict(kind="trusted-native-oracle", ensemble=path.name, truth_seed=meta["seed"])

    report = EV._forecast_suite(bundle, out, predict, members=64,
                                predictor=dict(kind="trusted-native-oracle", name="independent_native_reference"))
    return dict(primary_joint_energy=report["primary_joint_energy"], status=report["status"],
                reward=precision_reward(report["primary_joint_energy"], precision), by_family=report["by_family"],
                run_id=report["id"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bundle", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--reference-dir", type=Path)
    ap.add_argument("--precision", type=float, default=DEFAULT_PRECISION)
    a = ap.parse_args()
    if a.out.exists():
        shutil.rmtree(a.out)
    a.out.mkdir(parents=True)
    result = {}
    config = TS.R6ToolsConfig(bundle=a.bundle.resolve(), max_experiments=10, max_total_tu=200)
    bundle = TS.required_bundle(config)
    sim = TS.required_bundle(config, profile="simulation")
    result["required_bundle"] = dict(type=type(bundle).__name__, is_lab=isinstance(bundle, LB.LabBundle),
                                     bundle_id=bundle.manifest["bundle_id"], roster=dict(n_ports=bundle.roster.n_ports,
                                     device_slots=list(bundle.roster.device_slots), protocol=bundle.roster.protocol),
                                     simulation_profile_suite=sim.suite, cases=len(bundle.suite["cases"]),
                                     public_roster_ports=TS.public_roster(config).n_ports)
    result["prompt"], text = check_prompt(config, bundle)
    (a.out / "AGENT_SPEC.md").write_text(text)
    result["tools"] = asyncio.run(tool_calls(config, a.out / "lab"))
    demo = EV.reference_demo(bundle, a.out / "persistence")
    result["initial_persistence"] = dict(ok=demo["ok"], primary_joint_energy=demo["actual"], expected=demo["expected"],
                                         reward=precision_reward(demo["actual"], a.precision))
    if a.reference_dir:
        result["native_reference"] = grade_reference(bundle, a.reference_dir, a.out / "native", a.precision)
    result["reward_precision_K"] = a.precision
    (a.out / "validation.json").write_text(json.dumps(result, indent=1, default=str) + "\n")
    print(json.dumps(result, indent=1, default=str)[:6000])


if __name__ == "__main__":
    main()
