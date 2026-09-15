# Blobkit release checks

`check_install.py` creates a fresh environment outside the checkout, installs a
built wheel with its test extra, verifies source integrity, and runs the CPU and
packaging checks against that installation. `--plot` also tests the optional PNG
helper. It does not provision compute or publish a release.

```sh
uv build --package blobkit --out-dir dist/blobkit-polished
uv run python scripts/blobkit/check_install.py \
  --wheel dist/blobkit-polished/blobkit-0.3.5-py3-none-any.whl \
  --workdir /tmp/blobkit-clean-check --python 3.12 --plot
```

Use a fresh work directory. For CUDA checks, install the same wheel with `[gpu,test]`
on a Linux NVIDIA host, copy `packages/blobkit/tests/` outside the checkout, and
run `python -m pytest tests --require-gpu`. The flag fails if JAX only sees CPUs.
Start with `-m 'accelerator and not slow'`, then include the `slow` cases for
full-grid trajectories, repacking, and accelerated recording. Shut down any rented
instance after collecting logs and its wheel hash.
