# Review of r6-dialsa-002 / r6-dialsa-003 (study `dialsA`, gliders calibration)

Reviewed by the runner Mac before 002 started. The code is the ten request paths at f38f88ac. 003 is 002 with XLA_PYTHON_CLIENT_ALLOCATOR=platform removed from env; nothing else changed.

Method:
- two reviewers: one checked the run risk on the A100 40GB, the other the correctness against DECLARED.md;
- each minor-or-worse finding re-checked by independent skeptics: two for a major, one for a minor;
- the job's code was not executed on the Mac.

**Verdict for 002: held. 1 major.** The runner did not start it, and the requester replaced it with 003.

**Verdict for 003: fine to run. 0 blocker, 0 major, 1 minor.** The major is resolved by 003's env.

## The major (002), resolved in 003

**Every net trained one jitted step per Python iteration under the platform allocator.**
- Both trainers dispatch one step per Python iteration: a_nets.py:158-160 (ft_lockstep) and round 5's ladder_net.py:388-392 (train_nets, used for the base and D nets at run_a.py:372 and 524).
- The per-step basis (3.9 ms per block net, 17.7 ms per 8-net group) is r5-ladder-002's, which ran with the default allocator. r6-foundryexam-002 ran about 3.5x slower on this card in exactly the 002 setup.
- Modelled, the required stages would still finish (families, worlds, base nets at 6,000 steps, N=8, D(32)). The clock would cut N=32, N=2, the control, D(8), D(2), and likely the 24,000-step rung. The speed guard stops the job only at about 7x.
- 003 drops the platform allocator. Its peak is about 2.2 GB of device data plus 3-4 GB of temporaries, against the default allocator's 30 GiB cap.
- Modelled, everything then finishes in about 1.55 h on run_a.py's clock, nothing cut, about $3.4.
- Next code revision: run 25-50 steps per dispatch (a lax.scan inside vstep) in both trainers, as r6-foundryexam-003 did.

## Checked

- **Memory.** Base-net data is 2.22 GB for 6 nets; the stacked X has 2.34e8 elements (0.109 of 2^31). Step arrays are 8.5e7 to 1.13e8 elements against check_elems' 2^30. Temporaries are about 3-4 GB, and the peak about 6-8 GB of 40. The simulation shapes are round 5's, and the presmoke runs every shape at full size.
- **Zero-point check.** It cannot abort spuriously. float64 is on, and at xw = 0 every extra term in dlaw.tick is exactly 0 or 1. CPU equality is bitwise, and the GPU floor of 1e-8 is about 1e7 times larger than reordering noise. The xw = 4 difference (1.87) and the mass conservation (1.1e-16) hold by wide margins.
- **Deadlines and writes.** run_a.py stops itself 1.9 h after it starts, and the runner kills at 2.2 h, about 17 min later. scores.npz, info.json and train_info.json are rewritten atomically after every stage.
- **Outputs.** About 22 files, 10-15 MB; the largest is nets.npz at about 3.5 MB.
- **Exit codes:** a presmoke failure gives 1, the speed guard 4, a failed part 2.
- **Correctness against DECLARED.md.**
  - The law switch, the public family (gworld.tick, no stress conversion) and the true-form family (eta = 0 or 4) are as declared.
  - The 8 truths are round 5's, with eta nested on the same secret children.
  - Base nets are retrained from scratch per rung. "Met" requires every best step at or below 80% with nothing stopped early, and the criteria read only the last rung's copies, so no rung is picked after the fact.
  - The repairs do not see test items or hidden values.
  - The secret is os.urandom and is never written.

## Minor

1. **D(N)'s training rule counts a group stopped by the deadline as converged.** Read the stopped_early fields before quoting D(N). The study has been told.

## Notes

- The zero point can miss for reasons that are not harness faults: final-rung nets against round 5's 6,000-step sigma, and RES(8) fitting noise at eta 0.
- make_summary defaults to the job id r6-dialsA-001, which never ran; pass the real id.
- job.sh runs under set -e, so after a non-zero exit from run_a.py the rc, du and find lines never run. The exit code still reaches the runner.
- The base-net doublings reserve time only for N=8, D(32) and the final writes, so a 24,000-step rung can take the time N=32 and N=2 would need. The skeptic judged this the declared priority, not a defect.
