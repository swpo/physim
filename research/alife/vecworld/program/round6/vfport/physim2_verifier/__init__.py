"""physim2-verifier -- verifiers' stock isolated grader, plus the one thing it lacks for the PhySim v2 exam:
a run that FAILED is graded too (the coordinator's ruling E1).

    --env.id physim2-verifier          (instead of --env.id isolated-verifier; same config fields)

verifiers skips a task's finalize and its scoring when the solver's rollout failed (rollout.py:490: the harness
exited with an error, was killed, or the model route broke), and the isolated grader grades only a trace that is
`ok` (envs/isolated_verifier/env.py:105-109). Such a run ended without a grade, and the operator settled it by
hand. The exam's rule is now: whatever is in submission/ when the run ends is graded, however it ends.

For a failed run this env asks the task for the last frozen copy of submission/ that its controller took while
the run was alive (Physim2Task.recover: the checkpoint in the worker's own store; never a box, the box is gone)
and then grades exactly as the stock env does: a fresh verifier box, the three validation calls, one box per
item, the null policy for every item without a valid forecast. The trace keeps `ok = false` and its error; it
gains a reward and the record of what was graded (`info.physim2.submission.source = "checkpoint"`).

A run that did not fail takes the stock path, unchanged. Nothing else is overridden.
"""
import logging

from verifiers.v1.envs.isolated_verifier.env import IsolatedVerifierEnv

logger = logging.getLogger(__name__)


class Physim2VerifierEnv(IsolatedVerifierEnv):
    """Run one solver, then its deterministic task scoring in a fresh runtime, also when the solver's run failed."""

    async def finalize(self, task, episode) -> None:
        solution = episode.traces[0]
        if solution.ok or not hasattr(task, "recover"):
            await super().finalize(task, episode)
            return
        try:
            found = task.recover(solution)
        except Exception as e:                               # the store could not be read: the run stays ungraded, and says why
            solution.info.setdefault("physim2", {})["recovery_error"] = type(e).__name__
            return
        if found is None:                                    # the run never opened its instance: there is nothing to grade
            return
        try:
            graded = await self.grade(self.verifier_config(task), task, solution)
            episode.traces[0] = graded[1]
        except Exception as e:                               # grading the copy failed: recorded, never raised into the episode
            logger.warning("grading the checkpoint of a failed run did not finish (%s)", type(e).__name__)
            solution.info.setdefault("physim2", {})["recovery_error"] = type(e).__name__


__all__ = ["Physim2VerifierEnv"]
