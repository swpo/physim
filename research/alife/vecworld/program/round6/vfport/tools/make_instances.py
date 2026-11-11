"""make_instances -- fresh hidden instances in the worker's store, and the public index that names them.

For each instance: agentenv's make_instance (a 256-bit secret from os.urandom and a hidden theta from the public
prior, drawn now) and build_exam (frozen items, replicate truths, climatology pool). The index holds pointers
only: instance id, world, config name, the commitment hash of the secret.

usage: python tools/make_instances.py --store DIR --profile ring --id pilot-example-001
       python tools/make_instances.py --store DIR --world ring --config smoke_ring --n 4 --prefix ring-smoke
The first form (round 4) makes ONE instance of an exam profile (physim2_env/profiles.py) under exactly the given
id and refuses an id the store already holds; the second names instances <prefix>-w0, -w1, ...
The store is hidden-side data: keep it off the repository and delete it when the pilot is over.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import vfrun  # noqa: E402

vfrun.require_clean_environment()                          # before the package is imported: see vfrun.ENV_REFUSE
from physim2_env._paths import config_path, use_agentenv  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True)
    ap.add_argument("--profile", default=None, help="an exam profile (physim2_env/profiles.py); gives the world and the exam config")
    ap.add_argument("--id", default=None, help="with --profile: the exact id of the ONE instance to make")
    ap.add_argument("--world", default=None)
    ap.add_argument("--config", default=None, help="name of an exam config, e.g. smoke_ring")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--prefix", default=None)
    a = ap.parse_args()
    if a.profile is not None:
        from physim2_env import profiles as PROFILES
        from physim2_env.store import ID
        if a.world or a.config or a.prefix or a.n != 1 or not a.id:
            raise SystemExit("refused: --profile takes --id and nothing else (one instance, the profile's world and exam config)")
        if not ID.match(a.id):
            raise SystemExit("refused: --id must be lower-case letters, digits, '.', '_' and '-' (at most 64, starting with a letter or digit)")
        prof = PROFILES.get(a.profile)
        a.world, a.config = prof["world"], prof["config_name"]
    elif a.id or not a.world or not a.config:
        raise SystemExit("refused: give --profile NAME --id ID, or --world W --config C [--n N] [--prefix P]")
    use_agentenv()
    from evaluator import instance as INST
    cfg = json.load(open(config_path(a.config)))
    os.makedirs(a.store, mode=0o700, exist_ok=True)
    f = os.path.join(a.store, "index.json")
    index = json.load(open(f)) if os.path.exists(f) else []
    have = {r["instance_id"] for r in index}
    if a.id and (a.id in have or os.path.lexists(os.path.join(a.store, a.id))):
        raise SystemExit(f"refused: the store already holds an instance named {a.id}; an instance is made once and never again")
    prefix = a.prefix or f"{a.world}-{a.config}".replace("_", "-")
    made, k = 0, 0
    while made < a.n:
        iid = a.id or f"{prefix}-w{k}"
        k += 1
        if iid in have:
            continue
        hidden = os.path.join(a.store, iid, "hidden")
        info = INST.make_instance(a.world, cfg, hidden)
        ex = INST.build_exam(hidden, log=lambda *_: None)
        os.unlink(os.path.join(hidden, "examples.npz"))      # public examples are rebuilt from public code (bundle.py)
        index.append({"instance_id": iid, "world": a.world, "config_name": a.config,
                      "secret_commitment": info["secret_commitment"]})
        json.dump(index, open(f, "w"), indent=1)
        print(json.dumps({"instance_id": iid, "secret_commitment": info["secret_commitment"], "n_items": ex["n_items"],
                          "R": ex["R"], "seconds": round(ex["seconds"], 1)}), flush=True)
        made += 1


if __name__ == "__main__":
    main()
