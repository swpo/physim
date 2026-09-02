INTERFACE REVISION R2 (user, 2026-09-01): the control surface leaks geometry.
probe_move(a1,a2) + probe_dilate(gain) DISCLOSE that the pose space factorizes
into 2 translation channels + 1 scale channel => the 2D-ness and the existence
of a zoom are given away in the API shape.
REPLACE with ONE opaque actuator:
  probe_adjust(device, u1, u2, u3, steps=1, read=True)
  - u in [-1,1]^3; effect = secret per-WORLD fixed linear map M (invertible,
    random rotation+scale mix over (dx, dy, dlog_spacing)); the CHANNELS MIX
    translation and dilation so even the motion/zoom split must be discovered
    by experiment (the lattice structure of the device makes this learnable:
    dilation changes inter-slot correlation scale, translation shifts phase).
  - cost: sum|u_i| per step from a SINGLE 'adjust' budget (no cost-structure
    leak between translation and dilation).
  - status: report n_actuator_channels=3 (count only), drop 'motion'/'dilate'
    budget names, drop the basis-disclosure note ('meaning undisclosed' stays).
Injection stays as-is (emitter disclosure retained round-1: flagged for a
future round decision). probe_status text audit: remove any wording implying
translation/scaling/spacing semantics.
R2 AMENDMENT (user):
A. REMOVE the emitter co-location disclosure entirely. probe_status must contain
   ZERO location language: no 'co-located', no 'device 0's initial position',
   no 'originate there'. Injection docs say only: emissions enter through a
   fixed emission channel; where/what it couples to is undisclosed. (Agents
   can rediscover the emitter location experimentally — Fable already proved
   this is doable via decaying transients. That is now intended science.)
   Add to the barrier regex: 'co-locat', 'position', 'located', 'center',
   'origin' (agent-visible strings only).
B. ADJUST COST SEMANTICS (dilation symmetry): cost = sum|u_i| of the COMMANDED
   control, charged in full even when the effect clamps at (undisclosed)
   spacing bounds. Rationale: (i) log-symmetric — scale-down and scale-up of
   equal |dlog| cost the same (halving == doubling effort); (ii) charging
   commanded-not-actual is leak-free (cost-vs-effect analysis cannot localize
   the bounds; bounds are discoverable only through the STREAMS: correlation
   scale stops changing); (iii) physical: pushing against a wall still costs.
   Unit test: verify cost identical for +u3-dominant and -u3-dominant commands
   of equal magnitude, including at both clamp walls.
C. While auditing: ALSO strip any residual layout language anywhere in agent-
   visible text ('slots' is fine as a count word; 'ring', 'grid', 'lattice',
   'adjacent', 'spacing' are not).
R2 AMENDMENT 2 (user decision on bound behavior): REPLACE silent-clamp with
EXPLICIT GENERIC REJECTION:
- If a probe_adjust step would push spacing past an (undisclosed) bound, that
  step does NOT apply. Response includes result:"adjust_rejected" for that
  step — NO reason, NO which-channel, NO bound value (generic string, add to
  barrier list that it stays generic).
- Charging: completed steps charge normally; the rejected step ALSO charges
  its commanded sum|u_i| ("strain": the actuator refused but effort was
  spent). This kills the free binary-search oracle while avoiding silent
  world-model corruption (agent KNOWS nothing changed, doesn't know why).
- Multi-step calls: apply steps until first rejection, reject the remainder
  (single rejection charge, not per remaining step), return poses' streams
  for the applied steps as usual.
- Translation stays unbounded on the torus (no rejection path for pure
  translation; only the spacing component can strike bounds — NOTE: since
  channels MIX translation+dilation, a rejected step also blocks its
  translation component; that entanglement is intended and undisclosed).
- Unit tests: rejection at both walls, strain charge equality, multi-step
  partial application, and rejected-step stream absence.
R3 CONTROL REVISION (user: mixing = difficulty without depth, like the sensor-
shuffle we already rejected — revert it):
probe_adjust keeps its 3 anonymous channels BUT effects are PURE:
  effect = P @ diag(s1,s2,s3) @ u  where P = secret per-world PERMUTATION
  (which channel is which) x secret SIGNS; s_i = secret per-channel scales
  (translation channels in the old MAX_STEP range, dilation channel in the
  old gain range). NO cross-mixing: each channel does exactly one of
  {translate-axis-A, translate-axis-B, dilate}, agent discovers WHICH by
  trial and error (the user's original intent).
Rejection semantics simplify back: only the (secret) dilation channel can
strike bounds -> adjust_rejected only when the commanded step's dilation
component would cross a wall; pure-translation commands never refused.
(Strain charge + generic rejection + all Amendment A/2 language rules stay.)
Keep cost = sum|u_i| commanded. Tag: BLOB-E1r3; gate E1r2 as superseded
('mixed-control variant, retired before any scored rollouts were kept').
Regate: unit test rewritten for P/diag (both walls, strain equality, pure-
translation-never-refused), barrier audit rerun (text unchanged should pass),
scripted-actor smoke NOT needed again (actor never adjusts; interface change
is adjust-only) — note that exemption in the scorecard.
I killed the in-flight E1r2 eval runs; nothing scored is kept from r2.
R3 SIMPLIFICATION (user; final): drop the permutation/sign/scale secrecy too.
probe_adjust(device, u1, u2, u3): FIXED GLOBAL convention across all worlds —
u1 -> dx, u2 -> dy, u3 -> dlog_spacing, fixed scales (old MAX_STEP for u1/u2,
old gain range for u3). NOTHING about this is documented to the agent (doc
stays: "3 control channels; effects undisclosed") — undocumented IS the
mechanism, same principle as the output channels (fixed retinotopy, no
shuffle). Channel knowledge transfers across worlds, which is desirable
(instrument mastery transfers; the WORLD is what varies).
Everything else stands (generic adjust_rejected on the dilation wall + strain
charge + zero location language + commanded-cost).
Tag stays BLOB-E1r3. Unit tests simplify to the fixed map. Then reply DONE
and I relaunch the eval round.