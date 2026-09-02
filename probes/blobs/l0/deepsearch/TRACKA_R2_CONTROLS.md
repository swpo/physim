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