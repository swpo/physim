"""Compile demonstrated physics into anonymous R6 request programs.

Developer/evaluator material: this module, its source evidence, the manifest,
and load_demonstration must not enter a submitted predictor's filesystem.
Only ``public_cases`` contain agent-facing requests. No native stepping occurs.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROUND6 = HERE.parents[2]
ROOT = ROUND6.parents[3]
STUDY = ROUND6 / "physics/p4g2_044/sensor_study"
NOISE = STUDY / "noise_study"
VERSION = "p4g2_044-prepared1700-v1"
ORIGIN_FIELD_SHA256 = "847754b2bff40693e2f830ea083a97d1b23a513fab50ad11ca7f9d44399cc7ea"
TIMES = [0, 5, 10, 12, 14, 14.5, 15, 17.5, 18, 20, 25, 30, 30.5, 31, 35, 40, 50]
DEFECT_TIMES = [0, 5, 9, 10, 12, 15, 20, 25, 28.5, 30, 35, 40]
ARMS = [
    ("sham", 0.0, 0.0),
    ("pulse1", 1.0, 0.0),
    ("pulse2", 2.0, 0.0),
    ("pulse3", 3.0, 0.0),
    ("pulse1_feedback", 1.0, 0.3),
]
POSES = [(y, x) for y in (60.0, 66.0, 72.0, 78.0, 84.0)
         for x in (98.0, 104.0, 110.0, 116.0)]
# Two peripheral regions, an interior contrast and a selective null. These
# selected poses do not estimate continuum connected-component counts.
COMPACT_PLACEMENTS = [("pulse1", 9), ("pulse3", 9), ("pulse2", 6),
                      ("pulse3", 6), ("pulse3", 13), ("sham", 13)]
HISTORIES = {
    "sham": "No induced positive patch in the studied region through lag50.",
    "pulse1": "One positive patch persists after the source stops.",
    "pulse2": "Initial activity collapses; no positive return through lag50.",
    "pulse3": "Activity collapses then returns; two local patches at lag50.",
    "pulse1_feedback": "The added feedback pulse changes survival into collapse and return.",
}


def _origin():
    rows = json.loads((STUDY / "early_observations.json").read_text())["context"]["poses"]
    return deepcopy(next(row["devices"] for row in rows if row["t"] == 1700))


def _actions(arm_name, pose_id=None):
    _, amp, feedback = next(a for a in ARMS if a[0] == arm_name)
    actions = [dict(t=0, kind="inject", port=4, amp=amp, dur=10)]
    if feedback:
        actions.append(dict(t=10, kind="inject", port=0, amp=feedback, dur=2))
    if pose_id is not None:
        center = _origin()[0]["center"]
        delta = [(target - start + 64) % 128 - 64
                 for start, target in zip(center, POSES[pose_id])]
        steps = math.ceil(max(abs(v) for v in delta) / 1.5)
        # A pose change at0 would conflict with the initial inject action.
        # The first dt later is legal; adjustment and injection lanes may overlap.
        for i in range(steps):
            actions.append(dict(t=round(0.02 + 5 * i, 2), kind="adjust", device=0,
                                u=[delta[1] / steps / 1.5, delta[0] / steps / 1.5, 0.0]))
    return sorted(actions, key=lambda a: a["t"])


def _group(name, query, times, port, slots, query_times, scale=1.0):
    selectors = [dict(query=query, time_index=query_times.index(t), port=port, slot=slot)
                 for t in times for slot in slots]
    return dict(id=name, selectors=selectors, scales=[float(scale)] * len(selectors),
                unit=f"native observable units; fixed scale={scale:g} per coordinate")


def _temporal_groups():
    return [
        _group("early_excitation", 0, [10, 14.5, 18, 20], 4, [5], TIMES),
        _group("feedback_memory", 0, [10, 12, 20], 0, [5], TIMES),
        _group("stripe_evolution", 0, [20, 25, 30, 35], 5, [5], TIMES),
        _group("late_spatial", 1, [30, 40, 50], 4, list(range(19)), TIMES),
    ]


def _case_specs():
    specs = [(f"c{i + 1:03d}", arm, None) for i, (arm, _, _) in enumerate(ARMS)]
    specs.extend((f"c{100 + ai * 20 + pose:03d}", arm, pose)
                 for ai, (arm, _, _) in enumerate(ARMS) for pose in range(20))
    return specs


def _supplemental_cases():
    """Later-admitted ordinary protocols; each has an independent-noise study."""
    rows = []
    for case_id, arm, amp in (("c006", "x5_1", 1), ("c007", "x5_3", 3)):
        q_times = DEFECT_TIMES
        groups = [
            _group("defect_center_history", 0, [5, 10, 15, 20, 30, 40], 7, [5], q_times, 3),
            _group("defect_late_spatial", 0, [30, 40], 7, list(range(13)), q_times, 3),
            _group("asymmetric_partner", 0, [5, 10, 15, 20, 40], 11, [5], q_times, .4),
            _group("shared_feedback_history", 0, [5, 10, 15, 20], 9, [5], q_times, 1.5),
            _group("filtered_response_a", 0, [10, 20, 30, 40], 2, [5], q_times, .03),
            _group("filtered_response_b", 0, [10, 20, 30, 40], 3, [5], q_times, .3),
            _group("selective_quiet_port", 0, [5, 10, 20, 40], 6, [5], q_times, .03),
        ]
        rows.append(dict(
            public=dict(id=case_id,actions=[dict(t=0,kind="inject",port=9,amp=amp,dur=10)],
                        queries=[dict(sensor=s,t=deepcopy(q_times)) for s in ("device0","device1")]),
            groups=groups,
            entry=dict(treatment=arm,family="shared_feedback_defect",pose_id=None,
                       established_outcome=("Center port7 remains positive; modest transient response and boundary movement."
                                            if amp == 1 else
                                            "Center port7 turns negative, then positive by28.5; peripheral negative readings remain at40 while port11 center stays positive."),
                       evidence_status="demonstrated_at_native_noise_in_3_independent_continuations",
                       action_schedule_status="native_treatment_and_pose_validated",noise_replicates=3,
                       evidence_pattern=f"physics/p4g2_044/sensor_study/defect_halo/{arm}_r??.npz",
                       evidence_array="device0/device1",uses_privileged_action=False,
                       interpretation_limit="No center sign switch is a selective null, not absence of response everywhere."),
            paths=[STUDY / "defect_halo" / f"{arm}_r{rep:02d}.npz" for rep in range(3)],
        ))
    for case_id, when in (("c008", 20), ("c009", 30)):
        arm = f"gap{when}_u1_0.3"
        groups = _temporal_groups() + [
            _group("central_excursion", 0, [30, 35, 40], 4, [5], TIMES),
            _group("local_spatial_response", 0, [35, 40, 50], 4, list(range(13)), TIMES),
        ]
        rows.append(dict(
            public=dict(id=case_id,
                        actions=[dict(t=0,kind="inject",port=4,amp=3,dur=10),
                                 dict(t=when,kind="inject",port=5,amp=.3,dur=5)],
                        queries=[dict(sensor=s,t=deepcopy(TIMES)) for s in ("device0","device1")]),
            groups=groups,
            entry=dict(treatment=arm,family="timed_stripe_intervention",pose_id=None,
                       established_outcome=("No positive center port4 samples during25..50; two late local patches still form."
                                            if when == 20 else
                                            "Center port4 has a positive excursion around33..39.5; two late local patches still form."),
                       evidence_status="demonstrated_at_native_noise_in_3_independent_continuations",
                       action_schedule_status="native_treatment_and_pose_validated",noise_replicates=3,
                       evidence_pattern=f"physics/p4g2_044/sensor_study/spatial_selection/trials/{arm}*.npz",
                       evidence_array="device0/device1",uses_privileged_action=False,
                       interpretation_limit="A negative center sample does not rule out an off-center connected positive path."),
            paths=[STUDY / "spatial_selection/trials" / f"{arm}{suffix}.npz"
                   for suffix in ("", "_r1", "_r2")],
        ))
    return rows


def build_suite(family="compact"):
    """Return public requests and separate private evidence/scoring metadata.

    ``core`` includes all admitted temporal programs. ``compact`` adds six
    placement programs. ``full`` includes all20 placement programs for each of
    the original five pulse arms.
    Every request begins at the same prepared, opaque t=0 and includes its entire
    post-origin action history. No model seed or evaluator truth seed is stored.
    """
    if family not in ("core", "compact", "full"):
        raise ValueError("family must be core, compact, or full")
    cases, entries, groups = [], {}, {}
    for case_id, arm, pose_id in _case_specs():
        if pose_id is not None and (family == "core" or
                (family == "compact" and (arm, pose_id) not in COMPACT_PLACEMENTS)):
            continue
        if pose_id is None:
            queries = [dict(sensor=sensor, t=deepcopy(TIMES)) for sensor in ("device0", "device1")]
            score_groups = _temporal_groups()
        else:
            queries = [dict(sensor="device0", t=[50])]
            score_groups = [_group("placed_spatial", 0, [50], 4, list(range(13)), [50])]
        cases.append(dict(id=case_id, actions=_actions(arm, pose_id), queries=queries))
        groups[case_id] = score_groups
        entries[case_id] = dict(
            treatment=arm, family="temporal" if pose_id is None else "placement",
            pose_id=pose_id, pose_center=None if pose_id is None else list(POSES[pose_id]),
            established_outcome=HISTORIES[arm],
            evidence_status="demonstrated_at_native_noise_in_6_independent_continuations",
            action_schedule_status=("native_treatment_and_pose_validated" if pose_id is None else
                                    "legal_placement_schedule; readings_demonstrated_by_passive_native_pose_sampling"),
            noise_replicates=6,
            evidence_pattern=f"physics/p4g2_044/sensor_study/noise_study/trials/noise1_{arm}_r??.npz",
            evidence_array="device0/device1" if pose_id is None else "survey",
            uses_privileged_action=False,
            interpretation_limit=("Selected slot values do not certify the absence of every positive field cell."
                                  if pose_id is None else
                                  "Independent placement experiments sample geometry; no cross-case member pairing or exact topology is claimed."))
    for row in _supplemental_cases():
        case_id = row["public"]["id"]
        cases.append(row["public"])
        entries[case_id] = row["entry"]
        groups[case_id] = row["groups"]
    cases.sort(key=lambda c: c["id"])
    private = dict(
        origin=dict(world="p4g2_044",initialization_seed=928,physical_time=1700,
                    public_time=0,field_sha256=ORIGIN_FIELD_SHA256,devices=_origin(),
                    emitter="original device0 home; remains fixed during every adjustment"),
        entries=entries,score_groups=groups,
        contrasts=[
            dict(id="survival_vs_extinction",cases=["c002","c003"],sensor="device0",t=20,port=4,slot=5),
            dict(id="extinction_vs_delayed_return",cases=["c003","c004"],sensor="device1",t=40,port=4,slot=12),
            dict(id="retained_stripe_response",cases=["c003","c004"],sensor="device0",t=30,port=5,slot=5),
            dict(id="accessible_feedback_changes_fate",cases=["c002","c005"],sensor="device0",t=20,port=4,slot=5),
            dict(id="shared_feedback_selective_sign_switch",cases=["c006","c007"],sensor="device0",t=10,port=7,slot=5),
            dict(id="timed_pulse_changes_central_excursion",cases=["c008","c009"],sensor="device0",t=35,port=4,slot=5),
            dict(id="timed_pulse_changes_peripheral_geometry",cases=["c008","c009"],sensor="device1",t=50,port=4,slot=4),
        ],
        scoring=dict(primary="Full sensor arrays; every query/port/slot is predicted.",
                     focused="Predeclared observable groups retain joint member identity across times and slots.",
                     scales="Pulse-family coordinates use scale1; defect-family response-sized weights are chosen from development evidence and frozen before new native grading. They are not empirical noise floors and are never fitted to grading truth.",
                     aggregation="Average groups equally within each case, then average cases equally; adding groups does not increase a case's total weight.",
                     noise="One or more fresh native-noise trajectories for each experiment, independent across cases and from predictor sampling seeds.",
                     reference="Historical demonstration samples are supporting evidence, not frozen evaluation truth."),
        unadmitted_generalization=[
            "Other source times or prepared initial configurations.",
            "Unmeasured amplitudes, durations, repeated-pulse schedules or port combinations beyond the admitted protocols.",
            "Fresh-noise outcomes beyond public t=50, including the historical lag250 cache.",
            "The causal explanation of the precise two-lobe spatial selection.",
            "New negative-defect or gated-halo protocols beyond the admitted shared-feedback doses.",
        ],
    )
    return dict(version=VERSION,family=family,public_cases=cases,private=private)


def public_requests(family="compact"):
    """The only portion intended for the investigator/predictor boundary."""
    return deepcopy(build_suite(family)["public_cases"])


def load_demonstration(case_id):
    """Load the available *historical evidence* members without native stepping.

    Results follow the R6 samples shape, including query and member ordering.
    Placement values were passively sampled from native trajectories. They are
    not a new run of the placement action scheduler. Do not use as grading truth.
    """
    import numpy as np

    for row in _supplemental_cases():
        if row["public"]["id"] != case_id:
            continue
        by_query = [[] for _ in row["public"]["queries"]]
        for path in row["paths"]:
            with np.load(path, allow_pickle=False) as z:
                meta = json.loads(str(z["meta"]))
                if meta["initial_field_sha256"] != ORIGIN_FIELD_SHA256:
                    raise ValueError("Evidence origin does not match this suite")
                for qi, q in enumerate(row["public"]["queries"]):
                    indices = [int(np.flatnonzero(z["lag"] == t).item()) for t in q["t"]]
                    by_query[qi].append(z[q["sensor"]][indices].copy())
        return {"samples": [np.stack(arrays) for arrays in by_query]}
    matches = [row for row in _case_specs() if row[0] == case_id]
    if not matches:
        raise KeyError(case_id)
    _, arm, pose_id = matches[0]
    by_query = [[], []] if pose_id is None else [[]]
    for rep in range(6):
        with np.load(NOISE / "trials" / f"noise1_{arm}_r{rep:02d}.npz", allow_pickle=False) as z:
            meta = json.loads(str(z["meta"]))
            if meta["initial_field_sha256"] != ORIGIN_FIELD_SHA256:
                raise ValueError("Evidence origin does not match this suite")
            if pose_id is None:
                indices = [int(np.flatnonzero(z["lag"] == t).item()) for t in TIMES]
                for qi, sensor in enumerate(("device0", "device1")):
                    by_query[qi].append(z[sensor][indices].copy())
            else:
                by_query[0].append(z["survey"][pose_id][None].copy())
    return {"samples": [np.stack(arrays) for arrays in by_query]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family",choices=("core","compact","full"),default="compact")
    parser.add_argument("--write",action="store_true",help="Write public/private JSON files beside this source")
    args = parser.parse_args()
    suite = build_suite(args.family)
    if args.write:
        public_path = HERE / f"{args.family}_requests.json"
        text = json.dumps(dict(version="r6-requests-v1",cases=suite["public_cases"]),indent=2) + "\n"
        public_path.write_text(text)
        private = dict(version=VERSION,family=args.family,**suite["private"],
                       public_requests_sha256=hashlib.sha256(text.encode()).hexdigest())
        (HERE / f"{args.family}_private_manifest.json").write_text(json.dumps(private,indent=2)+"\n")
    print(json.dumps(dict(version=VERSION,family=args.family,cases=len(suite["public_cases"]),
                         horizons=sorted({max(q["t"]) for c in suite["public_cases"] for q in c["queries"]}),
                         native_steps=0,written=args.write),indent=2))


if __name__ == "__main__":
    main()
