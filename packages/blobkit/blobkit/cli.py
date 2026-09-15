"""Inspect an installed blobkit distribution without running an assay."""

import argparse
import json
from importlib.metadata import version

import blobkit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accelerator", action="store_true", help="also check JAX devices")
    parser.add_argument("--gpu", action="store_true", help="require a real JAX GPU device")
    commands = parser.add_subparsers(dest="command")
    generate = commands.add_parser("generate", help="execute a local Python recipe defining build_recipe()")
    generate.add_argument("recipe")
    generate.add_argument("--registry", required=True)
    generate.add_argument("--resume", help="resume from this registry checkpoint ID")
    generate.add_argument("--stop-after", type=int)
    generate.add_argument("--workers", type=int, default=1)
    registry = commands.add_parser("registry", help="inspect registry records without executing recipe code")
    actions = registry.add_subparsers(dest="action", required=True)
    verify = actions.add_parser("verify")
    verify.add_argument("root")
    export = actions.add_parser("export-recipe")
    export.add_argument("root")
    export.add_argument("recipe_id")
    export.add_argument("destination")
    args = parser.parse_args()
    if args.command == "generate":
        from .generation import run_recipe_file

        report = run_recipe_file(
            args.recipe, args.registry, resume=args.resume, stop_after=args.stop_after, workers=args.workers
        )
        print(json.dumps(report, indent=2))
        return 0
    if args.command == "registry":
        from .registry import Registry

        registry = Registry(args.root)
        report = (
            registry.verify()
            if args.action == "verify"
            else {"exported": str(registry.export_recipe(args.recipe_id, args.destination))}
        )
        print(json.dumps(report, indent=2))
        return 0
    report = {
        "blobkit": blobkit.__version__,
        "integrity": blobkit.verify_locks(quiet=True),
        "versions": {name: version(name) for name in ("numpy", "scipy")},
    }
    ok = report["integrity"]["ok"]
    if args.accelerator or args.gpu:
        from .soup.sim_gpu import _jax

        jax, _ = _jax()
        report["versions"]["jax"] = jax.__version__
        report["devices"] = [{"platform": d.platform, "kind": d.device_kind} for d in jax.devices()]
        if args.gpu and not any(d["platform"] == "gpu" for d in report["devices"]):
            report["error"] = "No GPU device is available to JAX"
            ok = False
    report["ok"] = ok
    print(json.dumps(report, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
