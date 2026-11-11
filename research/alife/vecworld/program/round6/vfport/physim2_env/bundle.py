"""The agent's workspace as one tar archive, built from PUBLIC inputs only (world name, config name).

agentenv's evaluator.build_workspace.build() makes the public bundle (physim2 with the world module,
predict_runner.py and verbatim copies of the simulator sources, MANIFEST.json); this module then swaps the
transport for the verifiers route: wire.py and the socket labclient.py leave, physim2_env/public/* enter
(HTTP laboratory client, in-box validator, one-request driver, freeze rules), plus the two public example
requests and the public card (exam.json). No file of the hidden directory is read here.

Round 4 of the port adds, still from public inputs only:

  TASK.md       the task statement of THIS route (physim2_env/TASK.md.tmpl): round 5's text with the limits of
                the run, how a run ends and what is graded, where the predictor runs, and the fallback rule.
                `statement(world, config_name, run)` renders it; the taskset renders it once more at setup from
                the run's resolved config and from what it measures in the box, so the text an agent reads is
                the truth about its run.
  submission/   no longer empty: predict.py (physim2_env/public/baseline_predict.py) and pool.npz, the NULL
                policy. `null_pool` simulates the pool with the public law at prior draws by round 5's recipe
                (agents/reference_agent.py, policy "null", seed 0, profiles.BASELINE_EPISODES episodes). The
                same arrays give the grader its fallback forecast (grading.null_scores).
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import tarfile
import tempfile
import types
import zipfile

import numpy as np

from . import profiles as PROFILES
from ._paths import HERE, PUBLIC, config_path, use_agentenv

DROPPED = ["wire.py"]
ADDED = ["labclient.py", "validate.py", "_item.py", "_rules.py"]
# Ruling E15: of the vendored vw library a box gets only what the public world module imports. For the ring that
# is everything but two files: the designers' closed-form linear-Gaussian family (the exact filter and its
# certificates) and the toy worlds. Neither is imported by physim2.world_ring, by vw/__init__ or by the
# reference agents (checked by tests/exam_units.py: the public simulator runs without them). The scoring code
# (vw/scoring.py) stays on purpose: the rule you are scored by is public, and the statement says so.
VENDOR_DROPPED = {"ring": ["_vendor/vw1/vw/lingauss.py", "_vendor/vw1/vw/toys.py"]}
# Every file a box holds at start belongs to one of these groups (first match); tools and results quote them.
FILE_GROUPS = [
    ("TASK.md", "the task statement"),
    ("submission/", "the baseline: the null policy (predict.py and its pool of prior-predictive episodes); replaced by the agent"),
    ("physim2/_vendor/vw1/vw/scoring.py", "the scoring rule (fair energy score), shipped on purpose: how you are scored is public"),
    ("physim2/_vendor/", "the public simulator's own sources (verbatim copies): what physim2.world_<name> imports to simulate the law"),
    ("physim2/world_", "the public world: law, coarse-grainings, prior, test-program generator, simulator"),
    ("physim2/world.json", "which world this exam is"),
    ("physim2/labclient.py", "the client of the laboratory (and its log of every reply)"),
    ("physim2/validate.py", "the check of a submission, as the grader will run it"),
    ("physim2/_item.py", "the grader's one-request driver (unprivileged user, limits, cleanup): public and trusted"),
    ("physim2/_rules.py", "the grader's freeze rules and reply format"),
    ("physim2/predict_runner.py", "how a predictor is called"),
    ("physim2/examples.npz", "two public example requests (prior mean, public noise) for validation"),
    ("physim2/exam.json", "the public card of the exam (sizes, budgets, limits)"),
    ("physim2/MANIFEST.json", "sha256 of every file of the bundle"),
    ("physim2/", "package plumbing (__init__, import path of the vendored sources)"),
]


def file_groups(names) -> list[dict]:
    """The files of a bundle by group: [{"group", "why", "files": [...]}] in the order of FILE_GROUPS."""
    out = [{"group": g, "why": why, "files": []} for g, why in FILE_GROUPS]
    for nm in sorted(names):
        for row in out:
            if nm == row["group"] or nm.startswith(row["group"]):
                row["files"].append(nm)
                break
        else:
            raise ValueError(f"a file of the bundle belongs to no group: {nm}")
    return [r for r in out if r["files"]]
BASELINE = "baseline_predict.py"                             # shipped as submission/predict.py
TOOL_OUTPUT_MAX_BYTES = 20_000                               # verifiers harnesses/utils/compaction.py:18 (the stock bash harness)
_CACHE: dict = {}
_POOLS: dict = {}


def load_config(config_name: str) -> dict:
    use_agentenv()
    from evaluator import instance as INST
    return INST.merge_cfg(json.load(open(config_path(config_name))))


def public_card(world: str, cfg: dict) -> dict:
    """LabService.card() without a laboratory: every field is public (world constants and the config)."""
    use_agentenv()
    from evaluator import instance as INST
    from evaluator.lab_service import LabService
    W = INST.world_module(world)
    return LabService.card(types.SimpleNamespace(W=W, decl=INST.exam_decl(W, cfg), cfg=cfg))


def task_text(world: str, config_name: str) -> str:
    return public_bundle(world, config_name)[1]["task_md"]


def public_examples(world: str, config_name: str) -> dict:
    """The two public example requests (history, prefix, test), as the bundle ships them in physim2/examples.npz."""
    return public_bundle(world, config_name)[1]["examples"]


# ----------------------------------------------------------------------------- the null policy (ruling E2)
def null_pool(world: str, config_name: str) -> dict:
    """{level: float32 array (episodes, len(times), d_level)}: the queried levels at the queried times in
    episodes simulated with the PUBLIC law at draws from the PUBLIC prior. Round 5's recipe, line for line
    (agentenv/agents/reference_agent.py:82, 97-105 with --seed 0, n_train = BASELINE_EPISODES, chunk = 64).
    Deterministic on one machine; cached per process."""
    key = (world, config_name)
    if key not in _POOLS:
        use_agentenv()
        from evaluator import instance as INST
        cfg = load_config(config_name)
        W = INST.world_module(world)
        d = INST.exam_decl(W, cfg)
        P, H, n, chunk, seed = d["P"], d["H"], PROFILES.BASELINE_EPISODES, 64, 0
        rng = np.random.default_rng([seed, 1])
        th = W.prior_sample(rng, n)
        sim = W.Simulator(chunk=chunk)
        obs = np.concatenate([sim.episodes(th[s:s + chunk], seed + s, P=P, H=H, classes=np.array(["a"] * len(th[s:s + chunk])))["obs"]
                              for s in range(0, len(th), chunk)])
        _POOLS[key] = {int(l): np.ascontiguousarray(np.asarray(W.level(l, obs[:, [P + t for t in ts]]), np.float32))
                       for l, ts in d["queries"].items()}
    return _POOLS[key]


def pool_sha256(pool: dict) -> str:
    """One hash over the pool's arrays (shape and bytes, levels in order): names the baseline in every record."""
    h = hashlib.sha256()
    for l in sorted(pool):
        a = np.ascontiguousarray(pool[l], "<f4")
        h.update(f"level{l}:{a.shape}\n".encode())
        h.update(a.tobytes())
    return h.hexdigest()


def npz_bytes(arrays: dict) -> bytes:
    """An .npz with fixed timestamps: the same arrays give the same bytes (numpy's savez stamps the clock)."""
    from numpy.lib import format as npf
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in sorted(arrays):
            b = io.BytesIO()
            npf.write_array(b, np.asanyarray(arrays[name]), allow_pickle=False)
            zi = zipfile.ZipInfo(name + ".npy", date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type, zi.external_attr = zipfile.ZIP_DEFLATED, 0o644 << 16
            zf.writestr(zi, b.getvalue())
    return buf.getvalue()


def baseline_files(world: str, config_name: str) -> dict:
    """{file name in submission/: bytes} of the baseline every box starts with."""
    pool = null_pool(world, config_name)
    with open(os.path.join(PUBLIC, BASELINE), "rb") as f:
        return {"predict.py": f.read(), "pool.npz": npz_bytes({f"level{l}": pool[l] for l in pool})}


# ----------------------------------------------------------------------------- the task statement (E1, E4, E7, E8)
def default_run(world: str, config_name: str, limits: dict | None = None) -> dict:
    """The limits a statement is rendered with before a run exists: the profile's defaults (or the exam config's
    own envelope) and what the task config declares. The taskset replaces them at setup with the run's own."""
    cfg = load_config(config_name)
    p = PROFILES.for_exam(world, config_name) or {}
    lim = {k: v for k, v in (limits or {}).items() if v is not None}
    run = {"max_turns": p.get("max_turns"), "wall_minutes": p.get("wall_minutes") or 60.0 * cfg["envelope"]["wall_hours"],
           "max_output_tokens_per_turn": p.get("max_output_tokens_per_turn"),
           "max_context_tokens": lim.get("max_context_tokens"), "cap_usd": lim.get("cap_usd"),
           "cpus": lim.get("box_cpus") or p.get("box_cpus") or PROFILES.FALLBACK_BOX["box_cpus"],
           "memory_gib": lim.get("box_memory_gb") or p.get("box_memory_gb") or PROFILES.FALLBACK_BOX["box_memory_gb"],
           "pids": None, "workspace_mib": None, "tmp_mib": None, "read_only_root": None, "lab_counts_turns": True, "measured": False}
    try:                                                     # the caps the runtime of this package sets on every box (boxcaps.py)
        from . import boxcaps as BOXCAPS
        caps = BOXCAPS.box_caps(memory_gb=lim.get("box_memory_gb"))
        run.update(cpus=caps.get("cpus", run["cpus"]), memory_gib=caps.get("memory_gb", run["memory_gib"]), pids=caps.get("pids"),
                   workspace_mib=caps.get("workspace_mib"), tmp_mib=caps.get("scratch_mib"), read_only_root=caps.get("read_only_root"))
    except Exception:
        pass
    return run


def _g(v) -> str:
    return f"{float(v):g}"


def limits_block(run: dict) -> str:
    """Section 4 of the statement: every limit that can end THIS run, and the box. `run` holds what the run's
    resolved config says and, once the box exists, what was measured in it."""
    L = []
    t = run.get("max_turns")
    if t:
        L.append(f"- **Turns: at most {int(t)}.** A turn is one reply of yours: one call of the model, however many tool calls that "
                 f"reply contains. Your run ends after reply number {int(t)}. The tool calls of that last reply are still executed, "
                 "but you never see their results: do not leave a step you depend on for the last turn.")
    else:
        L.append("- **Turns:** this run has no limit on the number of turns.")
    L.append(f"- **Wall-clock time: {_g(run['wall_minutes'])} minutes** for the whole run, counted from the start of your first turn: "
             "your own thinking, every tool call, all simulation and training. When the time is up the run ends at once, in the "
             "middle of whatever is running.")
    if run.get("max_output_tokens_per_turn"):
        L.append(f"- **One reply: at most {int(run['max_output_tokens_per_turn'])} tokens**, your reasoning included. A reply that is "
                 "cut at this length loses the tool call it was writing.")
    c = run.get("max_context_tokens")
    tail = f"a tool result longer than {TOOL_OUTPUT_MAX_BYTES:,} bytes is cut"
    if c:
        L.append(f"- **Context: {int(c):,} tokens.** Every turn sends the whole conversation again; nothing shortens or summarises "
                 f"it for you, and {tail}. If your next turn could exceed {int(c):,} tokens, the run ends before that turn. "
                 "Keep tool output short: write data to files and print summaries.")
    else:
        L.append(f"- **Context:** every turn sends the whole conversation again and nothing shortens or summarises it; it must fit "
                 f"your model's context window, and {tail}.")
    if run.get("cap_usd"):
        L.append(f"- **Spend: {_g(run['cap_usd'])} US dollars** at your model's listed prices, counted by the operator over all your "
                 "turns. Each turn is billed for the whole conversation so far, so a long conversation makes every further turn "
                 "more expensive. If the limit is reached, the run ends.")
    if run.get("lab_counts_turns", True):
        L.append("- `lab.usage()` reports, next to the laboratory's budgets, `seconds_elapsed` and `seconds_left` of this run and "
                 "`turns_used` and `turns_left` (the turn that makes the call is already counted).")
    else:
        L.append("- `lab.usage()` reports `seconds_elapsed` and `seconds_left` of this run. The laboratory does not count turns: "
                 "count your own replies.")
    if run.get("max_context_tokens"):
        L.append("- `lab.usage()` also reports `context_tokens_used` (your last turn, as the provider counted it) and "
                 "`context_tokens_left`.")
    cpus = "no cap on CPU cores" if not run.get("cpus") else f"{_g(run['cpus'])} CPU cores"
    mem = "no cap on memory" if not run.get("memory_gib") else f"{_g(run['memory_gib'])} GiB of memory (a process that takes more is killed)"
    pids = "no limit of its own on the number of processes" if not run.get("pids") else f"at most {int(run['pids'])} processes and threads"
    ws, tmp = run.get("workspace_mib"), run.get("tmp_mib")
    if ws or tmp:
        disk = "you can write to " + " and ".join(x for x in ((f"`/workspace` ({_g(ws)} MiB)" if ws else ""), (f"`/tmp` ({_g(tmp)} MiB)" if tmp else "")) if x)
        disk += (" and nowhere else (the rest of the file system is read-only, your home directory included)" if run.get("read_only_root")
                 else "")
        disk += "; both are kept in memory, so what you write there also counts against the box's memory, and a full one answers `No space left on device`"
    else:
        disk = "no disk quota of its own (it shares the operator's disk: keep what you write under about 2 GiB)"
    L.append(f"- **This box:** {cpus}, {mem}, no GPU, {pids}; {disk}. No network except the laboratory."
             + (" (Measured in this box when it started.)" if run.get("measured") else ""))
    return "\n".join(L)


def statement(world: str, config_name: str, run: dict | None = None) -> str:
    """TASK.md for (world, exam config) and the limits `run` (default: default_run)."""
    use_agentenv()
    from evaluator import instance as INST
    cfg = load_config(config_name)
    W = INST.world_module(world)
    d = INST.exam_decl(W, cfg)
    run = dict(default_run(world, config_name), **(run or {}))
    tn = cfg["lab"]["total_nats"]
    rows = "\n".join(f"    {n:8s} in [{lo:g}, {hi:g}]" for n, lo, hi in zip(W.THETA_NAMES, W.PRIOR_LO, W.PRIOR_HI))
    vals = dict(                                             # the values of agentenv's build_workspace.task_text (lines 56-70)
        n_theta=len(W.THETA_NAMES), theta_names=", ".join(W.THETA_NAMES), P=d["P"], H=d["H"],
        queries="{" + ", ".join(f"{l}: {v}" for l, v in d["queries"].items()) + "}",
        level_dims="{" + ", ".join(f"{l}: {v}" for l, v in W.LEVEL_DIMS.items()) + "}",
        n_samples=cfg["predictor"]["n_samples"], world_doc=(W.__doc__ or "").strip(), n_obs=W.N_OBS, n_in=W.N_IN,
        in_lo=f"{W.IN_LO:g}", in_hi=f"{W.IN_HI:g}", prior_table=rows,
        viability_note=getattr(W, "VIABILITY_NOTE", "No further selection was applied."),
        reset_cost=cfg["lab"]["reset_cost"], max_ticks=cfg["lab"]["max_ticks"], sigma_in=f"{W.SIGMA_IN:g}",
        reset_note=(f", as much as the {d['P'] + 1} observations of one item's history: an episode is not a cheap way to draw one "
                    "more observation" if int(cfg["lab"]["reset_cost"]) > 1 else ""),
        tick_cap=f"{W.TICK_CAP:g}", episode_cap=f"{W.EPISODE_CAP:g}",
        total_nats_note="" if tn is None else f", {tn:g} over the whole investigation",
        cpu_s_tick=f"{W.CPU_S_PER_MEMBER_TICK:g}", n_items=cfg["exam"]["n_items"], R=cfg["exam"]["R"],
        program_classes=", ".join(W.program_mix().names), pred_cpu=cfg["predictor"]["cpu_seconds"],
        pred_wall=cfg["predictor"]["wall_seconds"], pred_mem=cfg["predictor"]["memory_gib"],
        artifact_mib=cfg["predictor"]["artifact_mib"], max_attempts=cfg["validation"]["max_attempts"],
        baseline_episodes=PROFILES.BASELINE_EPISODES, limits_block=limits_block(run))
    with open(os.path.join(HERE, "TASK.md.tmpl")) as f:
        return f.read().format(**vals)


def public_bundle(world: str, config_name: str):
    """(tar bytes with members TASK.md, physim2/..., submission/predict.py, submission/pool.npz; info).
    Cached per (world, config). TASK.md here carries the default limits; the taskset writes the run's own
    statement over it at setup."""
    key = (world, config_name)
    if key in _CACHE:
        return _CACHE[key]
    use_agentenv()
    from evaluator import build_workspace as BW
    from evaluator import instance as INST
    cfg = load_config(config_name)
    W = INST.world_module(world)
    d = INST.exam_decl(W, cfg)
    base = baseline_files(world, config_name)
    with tempfile.TemporaryDirectory(prefix="physim2-bundle-") as out:
        BW.build(world, cfg, out)
        pub = os.path.join(out, "public")
        for root, dirs, files in os.walk(pub):
            for nm in files:
                os.chmod(os.path.join(root, nm), 0o644)
        pkg = os.path.join(pub, "physim2")
        for nm in DROPPED + VENDOR_DROPPED.get(world, []):
            os.unlink(os.path.join(pkg, nm))
        for nm in ADDED:
            shutil.copyfile(os.path.join(PUBLIC, nm), os.path.join(pkg, nm))
        # two public example requests: verbatim recipe of evaluator/instance.py:122-126 (prior mean, public noise)
        sim = W.Simulator(chunk=2)
        e = sim.episodes(np.tile(W.PRIOR_MEAN, (2, 1)), seed=12345, P=d["P"], H=d["H"])
        examples = {"history": np.asarray(e["obs"][:, :d["P"] + 1]), "prefix": np.zeros((2, d["P"], W.N_IN)),
                    "test": np.asarray(e["U"][:, d["P"]:])}
        np.savez_compressed(os.path.join(pkg, "examples.npz"), **examples)
        json.dump(public_card(world, cfg), open(os.path.join(pkg, "exam.json"), "w"), indent=1)
        task_md = statement(world, config_name)
        open(os.path.join(pub, "TASK.md"), "w").write(task_md)
        man = {}
        for root, dirs, files in os.walk(pub):
            for nm in sorted(files):
                if nm == "MANIFEST.json":
                    continue
                p = os.path.join(root, nm)
                man[os.path.relpath(p, pub)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
        for nm, data in base.items():                        # the baseline is part of what a box starts with
            man[f"submission/{nm}"] = hashlib.sha256(data).hexdigest()
        json.dump(man, open(os.path.join(pkg, "MANIFEST.json"), "w"), indent=1, sort_keys=True)
        buf = io.BytesIO()

        def norm(ti):
            ti.uid = ti.gid = 0
            ti.uname = ti.gname = "root"
            ti.mode = 0o755 if ti.isdir() else 0o644
            return ti
        with tarfile.open(fileobj=buf, mode="w") as tar:
            for nm in sorted(os.listdir(pub)):
                tar.add(os.path.join(pub, nm), arcname=nm, filter=norm)
            sub = tarfile.TarInfo("submission")
            sub.type, sub.mode = tarfile.DIRTYPE, 0o755
            tar.addfile(sub)
            for nm in sorted(base):
                ti = tarfile.TarInfo(f"submission/{nm}")
                ti.size, ti.mode, ti.uname, ti.gname = len(base[nm]), 0o644, "root", "root"
                tar.addfile(ti, io.BytesIO(base[nm]))
        info = {"files": len(man), "bytes": sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(pub) for f in fs)
                + sum(len(v) for v in base.values()),
                "manifest_sha256": hashlib.sha256(json.dumps(man, sort_keys=True).encode()).hexdigest(), "task_md": task_md,
                "examples": examples, "file_groups": file_groups(man),
                "baseline": {"policy": "null", "episodes": PROFILES.BASELINE_EPISODES,
                                                   "pool_sha256": pool_sha256(null_pool(world, config_name)),
                                                   "files": {nm: hashlib.sha256(v).hexdigest() for nm, v in base.items()}}}
    _CACHE[key] = (buf.getvalue(), info)
    return _CACHE[key]
