# Lab-bundle tools (from the cloud build session)

Scripts used to build, prove and re-seal the PhySim lab bundles in `../rollout_kit`. They run in the cloud container
that built the bundles: paths are absolute (`/home/user/evalwork/bundles`, `/home/user/swpo/residency-environments`)
and the re-seal needs each bundle's source suite directory (`work/<bundle>/build.json` -> `suite_dir`), which only
exists there.

- `gc_reseal_all.py BUNDLE...`: re-seal grand-challenge bundles with the recipe's own manifest writer
  (`gc_bundle.write_manifest`), then open both profiles, read every truth, and re-simulate member 0 of the last
  case bit for bit. `reseal_all.py` is the same script under its earlier name.
- `reseal_fedvortex.py BUNDLE OUT_JSON`: the same for the fed-vortex bundle (`fedvortex_bundle.write_manifest`,
  truth c015 member 0 re-simulated, `reference_demo` against checks.json).
- `gc_bundle_recipe.py` and `fedvortex_bundle.py`: the recipes as committed in residency-environments
  (`scripts/physim/labworlds/`); `gc_bundle.py` here is the bundles-folder copy used by the build scripts.
- `build_tasks.py`, `make_configs.py`, `prove_bundle.py`, `verify_all.sh`, `run_proofs.sh` and the rest: building and
  proving the kit.
