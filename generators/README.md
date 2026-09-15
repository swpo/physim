# Generators

Synthetic-data generation and validation live in `generators/<environment>/`,
following Prime's residency repository. They are not part of an environment wheel.
See `physim/` for executable recipes, registry import/export, and physical parity
checks. The reusable simulation and search engine is an installed dependency
(`blobkit`); generation recipes use the same physics as evaluation.
