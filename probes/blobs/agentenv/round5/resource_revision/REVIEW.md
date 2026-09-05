# Focused resource/cache review

Independent read-only review used the project `.venv/bin/python`.
No inference, truth build, real integration, GPU/SSH action, or commit ran.

Resolved before final validation:
- Old 32-bit fork IDs had a real collision below the new 100,000-spawn
  guard: nonce `resource-collision-audit`, counters 5,931 and 67,233 both
  produced `f39ff6e0a`. The r2 cohort now uses 128-bit opaque IDs and rejects
  overwrites. Legacy spelling/behavior stays unchanged. Fork RNG salts
  still use the same rollout nonce and cumulative counter.
- `probe_read` formerly allocated `list(range(...))` before resource checks.
  It now sizes the response with integer arithmetic and uses lazy indexing.
- r2 `probe_adjust(read=True)` now uses the existing 60,000-number response
  envelope, before simulation or state mutation. `read=False` has no such
  output-buffer limit. No per-fork duration guard was added.

No additional RNG/pose/emission reconstruction defect was found. The r2
path follows historical parent-step references iteratively, copies only
anchor fields into each fresh child, keeps child salt and captured poses,
and retains reset-ancestor logs. Temporary historical states do not scale
with ancestry depth. The final gate checks a 1,101-deep chain.

Follow-up disposition:
- The parent approved a seventh r2-only `log_entries=1,000,000` guard.
  It counts operation and emission entries before growth, including
  zero-charge/zero-substep injections. Those entries remain stored; no
  no-op elision or physics change was made. Tiny-fixture and real native
  tool-transport regressions exercise its terminal resource-stop path.
- Closed leaves remain in history as well as ancestors. The cumulative
  spawn guard bounds record count, but full-state transport and admission
  scans grow with that count. The normal workflow gates do not benchmark
  10,000 logical-open / 100,000-spawn worst-case throughput.
