# Next native test: deterministic whole-state lost updates

**Recipe only. Not executed in this audit.** It starts no models, evaluates no task, and needs no simulator. Run it later in a disposable local test process, after the active cohort is quiet. Do not point it at a rollout's state URL, reuse live credentials, import a live world, or change production code.

## Goal and scope

Exercise the installed `verifiers.v1.mcp.server.ServerBase._with_state` and its real `_pull_state` / `_push_state` HTTP calls. Show whether two distinct invocations can read one state, return success, and overwrite each other's updates. This is a transport/state test, not a test of learned physics or of the exact historical interleaving.

Use `.venv/bin/python` from the project root. Record the installed verifiers version and source hashes. The relevant source is `v1/mcp/server.py:175–206,227–249`; the current wrapper explicitly documents last-write-wins updates.

## Disposable fixture

1. Create a minimal State subclass with `fork_seq=0`, `turns=0`, `forks={}`, `base_index=0`, and a fixed test-only nonce. Bind it to a minimal ServerBase subclass. Do not replace `_with_state`, `_pull_state`, or `_push_state`.
2. Give that instance a **loopback-only temporary state endpoint**. Implement GET/PUT in a small local HTTP fixture with an in-memory JSON document. Use the installed channel's ordinary request format, but no live secrets, state, or service endpoint. For the fixture, the state-channel accessor may return its isolated local URL.
3. The wrapped `fork(anchor)` body contains no physics. It increments the state-local `turns` and `fork_seq`, derives an ID from the fixed nonce plus counter, inserts `{id: anchor}`, and returns `{fork, anchor_t}`. This mirrors the counter/handle mechanism at `physim/servers/blob.py:243–258` without constructing a world.
4. Label requests A/B in the test harness. Log only sequence number, GET/PUT, label, fork counter, turns, returned handle/anchor, and a state-body hash. Do not log headers or credentials.

## Forced race schedule—events/barriers, no sleeps

The critical detail is to **copy the GET body before waiting**, not to reread shared state after release.

- GET handler: take an immutable copy of current JSON; place `(label, copy)` in an `asyncio.Queue`; wait on `release_get`; return that saved copy.
- PUT handler: copy the submitted JSON into a second queue; wait on a label-specific commit event; replace the in-memory state with that copied body; signal `put_done[label]`; acknowledge.
- Controller: create A=`wrapped_fork(200)` and B=`wrapped_fork(600)` concurrently. Wait for both saved GET snapshots. Assert both have counter0 and no forks, then set `release_get`.
- Wait for both proposed PUT bodies. Assert each independently has counter1 and one fork. Release A's PUT; await its done event. Then release B's PUT and await its done event. Gather both tool results.
- Reverse the PUT order in a second fresh fixture. Use events/queues for every transition. Use a bounded `asyncio.timeout` only to fail a hung fixture and ensure cleanup; do not use time-based sleeps to produce the race.

**Expected observation for the currently inspected last-write-wins wrapper, to be tested:** two distinct success results have the same counter-derived handle but different anchors; final counter/turns are1, and only the last PUT's anchor remains. A correct compositional contract would retain two distinct handles, counter2, turns2, and both anchors. Keep the request/result count2 separate from persisted operation count1.

This is deliberately a negative mechanism fixture. If a later fix serializes whole transactions, do not deadlock its correctness test by demanding two simultaneous GETs: adapt the controller to allow the first transaction to complete while the second waits. The green contract remains two retained operations, regardless of serialization or conflict/retry strategy.

## Controls and follow-ups

- **Serial positive control:** reset fixture; await A fully before B. Expect unique handles, counter2, turns2, both anchors.
- **Advancing-read fixture:** a no-physics body increments `base_index` and `turns`. The forced race should distinguish two returned acknowledgments from the retained advance. This directly matches the kind of t165 repetition in node93.
- **Independent-context fixture:** mutate two different fork records that live in the same whole-state document. This checks that “different contexts” does not falsely imply independent state writes.
- **Lifecycle fixture:** in later scripted controls, cover reset versus stale mutation and ready versus an in-flight mutation. The gate must not be undone by an older state write. Check actual native tool/state dispatch after the small mechanism fixture, not only a mocked direct function call.

Close the fixture clients/server and cancel only its owned tasks in `finally`. Save the small event log under a new diagnostic artifact directory. Do not repair or restart active cohort services. Passing these controls does not repair this trace's missing commit history or turn its instance scores into evidence of clean theory learning.
