"""Re-seal the fed-vortex lab bundle after a labworld.py change, with the bundle recipe's own code.

    python reseal_fedvortex.py BUNDLE OUT_JSON

1. fedvortex_bundle.write_manifest(BUNDLE) rewrites manifest.json (the recipe's own function; checks.json and
   every data file are left as they are). Only the world identity's implementation hashes change.
2. open_bundle(profile="evaluation") + check_runtime + every truth file; the simulation profile opens too.
3. Results unchanged: member 0 of one truth (c015, the 11-action feed_and_follow case, seed 71014) is
   re-simulated through the re-sealed bundle's make_oracle and compared bit for bit with the frozen truth;
   evaluation.reference_demo reproduces checks.json (initial persistence, 4 members) within 1e-10.
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
import json
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
sys.path.insert(0, "/home/user/swpo/residency-environments/scripts/physim/labworlds")
import numpy as np  # noqa: E402

import fedvortex_bundle as FB  # noqa: E402
from physim import evaluation as EV  # noqa: E402
from physim import labbundle as LB  # noqa: E402


def main(bundle: Path, out: Path):
    t0 = time.process_time()
    before = json.loads((bundle / "manifest.json").read_text())
    try:
        LB.open_bundle(bundle, profile="evaluation").check_runtime()
        refused_before = None
    except Exception as exc:  # expected: implementation identity changed
        refused_before = f"{type(exc).__name__}: {exc}"
    manifest = FB.write_manifest(bundle)
    b = LB.open_bundle(bundle, profile="evaluation")
    b.check_runtime()
    for rec in b.suite["cases"]:
        b.truth(rec)
    sim = LB.open_bundle(bundle, profile="simulation")
    sim.check_runtime()
    changed = {k: [before["objects"][k]["id"], manifest["objects"][k]["id"]] for k in manifest["objects"]
               if before["objects"][k]["id"] != manifest["objects"][k]["id"]}
    impl_changed = {m: [before["objects"]["world"]["implementation"]["source_sha256"].get(m), h]
                    for m, h in manifest["objects"]["world"]["implementation"]["source_sha256"].items()
                    if before["objects"]["world"]["implementation"]["source_sha256"].get(m) != h}
    files_changed = sorted(set((r["path"], r["sha256"]) for r in manifest["files"]) ^
                           set((r["path"], r["sha256"]) for r in before["files"]))
    # one truth member, bit for bit
    i = len(b.suite["cases"]) - 1
    rec = b.suite["cases"][i]
    seed = b.suite["truth_seeds"][i]
    c0 = time.process_time()
    member = b.make_oracle().sample_truth(rec["request"]["actions"], rec["request"]["queries"], 1, truth_seed=seed)["samples"]
    sim_cpu = time.process_time() - c0
    truth = b.truth(rec)["samples"]
    same = [bool(np.array_equal(m[0], t[0])) for m, t in zip(member, truth)]
    maxdiff = [float(np.abs(m[0] - t[0]).max()) for m, t in zip(member, truth)]
    target = out.parent / "fedvortex_reseal_persistence"
    if target.exists():
        shutil.rmtree(target)
    demo = EV.reference_demo(b, target)
    result = dict(
        bundle=str(bundle), refused_before=refused_before,
        bundle_id_before=before["bundle_id"], bundle_id_after=manifest["bundle_id"],
        object_ids_changed=changed, implementation_sources_changed=impl_changed,
        data_files_changed=[p for p, _ in files_changed],
        truth_member_check=dict(case=rec["request"]["id"], family=rec["family"], truth_seed=seed, member=0,
                                bit_identical=all(same), per_query=same, max_abs_diff=maxdiff, cpu_s=sim_cpu),
        persistence_reference=dict(ok=demo["ok"], expected=demo["expected"]["primary_joint_energy"], actual=demo["actual"]),
        cpu_s=time.process_time() - t0,
    )
    out.write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
