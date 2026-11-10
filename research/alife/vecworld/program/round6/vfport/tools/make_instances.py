"""make_instances -- fresh hidden instances in the worker's store, and the public index that names them.

For each instance: agentenv's make_instance (a 256-bit secret from os.urandom and a hidden theta from the public
prior, drawn now) and build_exam (frozen items, replicate truths, climatology pool). The index holds pointers
only: instance id, world, config name, the commitment hash of the secret.

usage: python tools/make_instances.py --store DIR --world ring --config smoke_ring --n 4 --prefix ring-smoke
The store is hidden-side data: keep it off the repository and delete it when the pilot is over.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from physim2_env._paths import config_path, use_agentenv  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=True)
    ap.add_argument("--world", required=True)
    ap.add_argument("--config", required=True, help="name of an agentenv config, e.g. smoke_ring")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--prefix", default=None)
    a = ap.parse_args()
    use_agentenv()
    from evaluator import instance as INST
    cfg = json.load(open(config_path(a.config)))
    os.makedirs(a.store, mode=0o700, exist_ok=True)
    f = os.path.join(a.store, "index.json")
    index = json.load(open(f)) if os.path.exists(f) else []
    have = {r["instance_id"] for r in index}
    prefix = a.prefix or f"{a.world}-{a.config}".replace("_", "-")
    made, k = 0, 0
    while made < a.n:
        iid = f"{prefix}-w{k}"
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
