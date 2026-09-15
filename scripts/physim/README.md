# Physim support scripts

Run from the repository root through `uv run python scripts/physim/<script>.py`.

- `docker/`: predictor sandbox and stock-harness agent images; build commands are
  in `environments/physim/README.md`.
- `examples/`: a zero predictor and a short native experiment request.
- `check_clean_install.py`: build both wheels, install outside the checkout, and
  reproduce the persistence score plus a short native experiment without a model.
- `check_published_install.py`: install the public wheel and its public dependency,
  fetch the three explicit world configs, and verify native/offline operation from
  a fresh directory. Requires an HTTPS wheel URL with a SHA-256 fragment.
- `prepare_world_release.py`: stage approved data/license metadata for HF; never uploads.
- `validation/`: existing scientific and integration checks kept for local research
  reproducibility. These are not new per-environment tests for upstream submission.

Reference export and parity migration live in `generators/physim/`.

`check_harness_image.py` verifies the installed stock bash harness can resolve its
dependencies and start in the agent image with Docker networking disabled. Run
it after building the image and whenever changing the pinned Verifiers version.
