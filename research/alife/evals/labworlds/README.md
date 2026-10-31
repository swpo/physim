# Lab worlds as PhySim evaluations: working record

This folder preserves the work of 28-30 Oct 2026 on turning the ALife collective's worlds into
PhySim evaluations. The code lives on a local branch (`feat/labkit-worlds`) of
`swpo/residency-environments` that could not be pushed from the working session, so it is kept
here until its home is decided.

- `src/LABWORLDS.md`: the draft world contract, acceptance and curation checks, and every result
  so far (start here).
- `src/labworld.py`: the adapter (`LabWorld`, `LabStepper`, `LabOracleRunner`) that runs a labkit
  world through PhySim's `OracleRunner`; `src/labeval.py`: frozen suite, truths, controls and
  scoring with PhySim's `score_case`; `src/ports_check.py`: proofs for the port roster;
  `src/runner_demo.py`, `src/vortex_demo.py`: worked examples.
- `patches/`: the branch as a patch series against residency-environments commit `844b58a`
  (`git am patches/*.patch` on a checkout of that commit's branch `codex/physim`).
- `runs/`: scripts and small results of every pilot run (`suite`, `rods_runner`, `cips_runner`,
  `rods_converge`, `cips_converge`, `noise_intensity`, `curation`, `cips_rotation`, the battery
  folders). Large arrays were not kept; they regenerate from the scripts.
- `reports/`: the agents' reports and their independent checks for each round, the Blobkit gap
  analysis (`gap_final.md`) and the fact-checked collective summary (`summary_final.md`).

Operator tooling (dashboard generator, librarian restart script, session notes) is in
`handoff/alife_operator/`.
