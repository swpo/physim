"""The p4 feedback ablation respects channel/activator matrix dimensions."""

from pathlib import Path

import numpy as np


def test_shared_feedback_ablation_preserves_single_driver_channels(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "generators/physim"))
    from build_evaluation_bundle import disable_shared_feedback

    drive = np.array([[1.0, 0], [1, 0.5], [0, 1], [0.2, 0.2]])
    feedback = np.arange(8, dtype=float).reshape(2, 4)
    fields = np.ones((6, 2, 2))
    state = dict(Wf=drive, Wid=drive.copy(), Kf=feedback, F=fields)
    disable_shared_feedback(state)
    np.testing.assert_array_equal(state["Kf"][:, [1, 3]], 0)
    np.testing.assert_array_equal(state["Kf"][:, [0, 2]], feedback[:, [0, 2]])
    np.testing.assert_array_equal(feedback, np.arange(8).reshape(2, 4))
    assert state["Wf"] is drive and state["F"] is fields
    np.testing.assert_array_equal(state["Wid"], drive)
