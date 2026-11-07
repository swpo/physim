"""example_api -- the harness v0 API end to end on the toy (about 20 CPU-seconds)."""
import sys

sys.path.insert(0, "/home/user/evalwork/vecworld/program/track2/harness")
import toy as T                                                   # noqa: E402
from vw.harness import HistoryExam, Lab                           # noqa: E402
from vw.nats import NatsBudget                                    # noqa: E402
from vw.secret import Secret                                      # noqa: E402

secret = Secret()                                                 # 256 bits; held with theta, never published
world = T.world(T.draw_theta(secret.rng("theta")))                # the hidden world (vw.World)
nb = NatsBudget.isotropic(24, 0.3, tick=2.0, episode=8.0, total=64.0)

# the agent's real world: secret keys, nats caps, tick budget (resets cost 1 tick)
lab = Lab(world, secret, nats=nb, max_ticks=600)
try:
    lab.run([(0, {0: 0.5, 1: 0.5})], range(65), label="first")  # 2.78 nats > tick cap: rejected, nothing ran
except Exception as e:
    print(type(e).__name__, e, lab.usage()["ticks_used"])
o = lab.run([(0, {0: 0.4, 1: 0.4})], range(65), label="first")  # 1.78 nats: whole program checked, then run
print(lab.usage())                                                # ticks, resets, nats used and left

# the exam: history items from a secret namespace, R replicate truths, climatology pool
exam = HistoryExam(world, secret, T.program_mix(), n_items=32, prefix=16, queries={1: [1, 2, 4, 8, 16], 2: [16, 32]},
                   R=8, derived={2: T.stat2}, scales=T.public_scales(64), nats=nb)
item = exam.public()[0]                    # {'id', 'history' (17, 6), 'prefix_program', 'program', 'queries'}


def predict(item, n_samples, seed):        # any frozen predictor: {level: (n_samples, len(times), d)}
    return T.filter_predictor(T.PRIOR_MEAN)(item, n_samples, seed)


scores = exam.score(exam.collect(predict, n_samples=64))       # fair ES, v1 ES, fair VS per item and cell
rep = exam.report({"agent": scores})                             # oracle LOO, climatology, OES, bootstrap SE
print(rep["valid"], rep["aggregate_pooled"]["agent"], rep["se_pooled"]["agent"], rep["by_group"])
