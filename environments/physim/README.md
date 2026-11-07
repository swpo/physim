# Physim environment source

The environment is maintained in the [residency repository](https://github.com/swpo/residency-environments/tree/3687ecbd9abbe3283e27691d0a5d1fb1b30d3c15/environments/physim). Ongoing development is tracked in [residency PR #22](https://github.com/PrimeIntellect-ai/residency-environments/pull/22). This directory contains documentation links only; it is not a Python package.

Run `uv sync --locked` from the repository root to install the revision pinned in `pyproject.toml` and `uv.lock`, together with the editable local Blobkit package.

See [the upstream environment instructions](https://github.com/swpo/residency-environments/blob/3687ecbd9abbe3283e27691d0a5d1fb1b30d3c15/environments/physim/README.md) for runtime setup and evaluation, and [the development guide](../../DEVELOPMENT.md) for changing dependencies or testing both packages together.
