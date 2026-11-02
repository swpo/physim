# PhySim lab-world adapter: patch series for PrimeIntellect-ai/residency-environments

15 patches against `PrimeIntellect-ai/residency-environments` main at
`1f70c51e9135ef3012d493e04be39739d0da8a6a`. They touch only `environments/physim/`
(`physim/labworld.py`, `physim/labbundle.py`, `physim/taskset.py`, `LABWORLDS.md`);
world-specific suite scripts are not included. Apply with `git am patches_adapter/*.patch`
on a branch from that commit. `tests/test_envs.py`: 12 passed.

sha256 of the concatenated patches (`cat *.patch | sha256sum`):
12c0bcf5f83533804fb8069086fa09d3d90c469038d42e720154bf3ba454d5af
