"""check_request -- a rollout request (schema `rollout-job/v1`) and the state of the pilot folder it would run in.

    python -B tools/check_request.py --fetch --source-commit HEX --job-id ID --pilot DIR
    python -B tools/check_request.py --request FILE --pilot DIR [--prices] [--no-go] [--shared-ledger FILE]
    python -B tools/check_request.py --facts

The first form copies a job's three input files out of one commit of the repository into the pilot folder (see
fetch); the second checks a request; the third prints what a runner can check mechanically (see facts).

A request is a JSON object with EXACTLY these keys:

    schema       "rollout-job/v1"
    job_id       ^[a-z0-9][a-z0-9-]{2,62}$      names the run folder, the run and the ledger row; used once
    purpose      a sentence (at most 500 characters)
    requester    a name (at most 100 characters)
    pin          the 40-character commit the runner checked out and reviewed
    pin_sha256   sha256 of PIN.sha256 at that commit
    config       round6/rollouts/configs/<name>.toml     (tools/check_config.py: the strict schema)
    exam_profile, instance, model, cap_usd               must equal the config's
    caps         {"max_turns", "max_output_tokens", "wall_minutes", "box_memory_gb"}: must equal the config's
                 max_turns, max_output_tokens_per_turn, wall_minutes (at most 180) and box_memory_gb (at most 4)

The request repeats what the config says so that the runner can read the caps without parsing TOML; this tool
makes sure the two agree. Nothing in a request can name code, a path outside the configs folder, or a setting
the config schema does not have.

What is checked, in this order, each failure a `refused:` line and exit status 2:
  1. the request's own shape;            2. the pin: sha256 of this checkout's PIN.sha256, and `git rev-parse HEAD`;
  3. the config (strict schema);         4. request and config agree;
  5. the pilot folder: the job id is new, the instance name is new or was made for this job;
  6. (unless --no-go) the lead's standing go: `<pilot>/LEAD-GO-MODEL-SPEND.json`, see read_go;
  7. (with --prices) the model's listed prices and the bounds on the bill, and the ceiling of the go (with
     --shared-ledger FILE: counting what other machines spent as well).
Steps 1 to 6 read local files only. Step 7 makes ONE request without a credential: GET <inference url>/models.

The functions below are also what tools/vfrun.py uses for the request route; they start nothing and write
nothing except where their text says so (register_instance, ledger_append).
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import check_config as CC  # noqa: E402

SCHEMA = "rollout-job/v1"
KEYS = ("schema", "job_id", "purpose", "requester", "pin", "pin_sha256", "config", "exam_profile", "instance", "model", "caps", "cap_usd")
CAP_KEYS = ("max_turns", "max_output_tokens", "wall_minutes", "box_memory_gb")
JOB = re.compile(r"^[a-z0-9][a-z0-9-]{2,62}$")
INSTANCE = re.compile(r"^pilot-[a-z0-9-]{3,40}$")
HEX40, HEX64 = re.compile(r"^[0-9a-f]{40}$"), re.compile(r"^[0-9a-f]{64}$")
MAX_REQUEST_BYTES = 16 << 10
PRIME_MODELS_URL = "https://api.pinference.ai/api/v1/models"
REQUESTS_PREFIX = "research/alife/vecworld/program/rollouts/requests/"            # where requests are committed (never by this study)
SHARED_LEDGER_PATH = "research/alife/vecworld/program/round6/rollouts/ledger.json"
# Round 5 (runbook audit T22): the publication folder of a job as tools/pack_rollout.py builds it (these files in this
# order, then submission/, key_scan.json and MANIFEST.json), its size limits in bytes, and the clean-up after a crash.
PUBLICATION_FILES = ("status.json", "PILOT_NEVER_REUSE_AS_EXAM.txt", "request.json", "config.toml", "resolved.toml", "model_entry.json",
                     "usage.json", "grades.json", "reference.json", "lab_log.jsonl", "submission.json", "transcript.md", "trace.redacted.jsonl")
PUBLICATION_MAX_FILE_BYTES, PUBLICATION_MAX_TOTAL_BYTES = 20 << 20, 50 << 20
STAGES = ("instance", "reference", "dry-run", "rollout", "close")                 # tools/vfrun.py --stage, in the order of a job
GO_FILE = "LEAD-GO-MODEL-SPEND.json"
GO_SCHEMA = "physim2-lead-go/v1"
GO_MAX_AGE_DAYS = 30
LEDGER = "LEDGER.jsonl"
INSTANCES = "INSTANCES.jsonl"
MTOK = 1_000_000


class Refused(Exception):
    pass


def _num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x == x and abs(x) != float("inf")


# ----------------------------------------------------------------------------- 1. the request
def read_request(path: str) -> dict:
    try:
        st = os.lstat(path)
        if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_REQUEST_BYTES:
            raise Refused("the request is not a regular file of at most 16 KiB")
        with open(path, "rb") as f:
            raw = f.read(MAX_REQUEST_BYTES + 1)
        req = json.loads(raw.decode("utf-8"))
    except OSError:
        raise Refused("the request file cannot be read") from None
    except (UnicodeDecodeError, ValueError):
        raise Refused("the request is not UTF-8 JSON") from None
    bad = validate_request(req)
    if bad:
        raise Refused("the request: " + "; ".join(bad))
    return dict(req, _sha256=hashlib.sha256(raw).hexdigest())


def validate_request(req) -> list[str]:
    if not isinstance(req, dict):
        return ["not an object"]
    bad = [f"unknown key {str(k)[:40]!r}" for k in sorted(req) if k not in KEYS] + [f"{k}: required" for k in KEYS if k not in req]
    if bad:
        return bad
    if req["schema"] != SCHEMA:
        bad.append(f"schema must be {SCHEMA!r}")
    for key, pattern in (("job_id", JOB), ("instance", INSTANCE), ("pin", HEX40), ("pin_sha256", HEX64)):
        if not isinstance(req[key], str) or not pattern.match(req[key]):
            bad.append(f"{key}: does not match {pattern.pattern}")
    for key, n in (("purpose", 500), ("requester", 100), ("config", 300), ("exam_profile", 40), ("model", 160)):
        if not isinstance(req[key], str) or not 0 < len(req[key]) <= n or any(ord(c) < 32 for c in req[key]):
            bad.append(f"{key}: a plain string of at most {n} characters")
    caps = req["caps"]
    if not isinstance(caps, dict) or sorted(caps) != sorted(CAP_KEYS):
        bad.append("caps: exactly " + ", ".join(CAP_KEYS))
    else:
        for k in ("max_turns", "max_output_tokens", "wall_minutes"):
            if isinstance(caps[k], bool) or not isinstance(caps[k], int) or caps[k] < 1:
                bad.append(f"caps.{k}: a positive integer")
        if not bad and caps["wall_minutes"] > 180:
            bad.append("caps.wall_minutes: at most 180")
        if not _num(caps["box_memory_gb"]) or not 1 <= caps["box_memory_gb"] <= 4:
            bad.append("caps.box_memory_gb: from 1 to 4 (the pin's cap, lower only)")
    if not _num(req["cap_usd"]) or req["cap_usd"] <= 0:
        bad.append("cap_usd: a positive number")
    return bad


# ----------------------------------------------------------------------------- 2. the pin
def pin_sha256(root: str = ROOT) -> str:
    with open(os.path.join(root, "PIN.sha256"), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def git_head(root: str = ROOT) -> str | None:
    """`git rev-parse HEAD` of the checkout that holds the study folder, or None. Read-only; a client that does not
    answer in 20 s is killed by Python (its own child)."""
    try:
        r = subprocess.run(["git", "-C", root, "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL,
                           env={k: os.environ[k] for k in ("PATH", "HOME") if k in os.environ})
    except (OSError, subprocess.TimeoutExpired):
        return None
    return r.stdout.strip() if r.returncode == 0 and HEX40.match(r.stdout.strip()) else None


def check_pin(req: dict, root: str = ROOT, head: str | None = None) -> dict:
    have = pin_sha256(root)
    if have != req["pin_sha256"]:
        raise Refused("the request's pin_sha256 is not the sha256 of this checkout's PIN.sha256: it was written for another pin")
    head = git_head(root) if head is None else head
    if head != req["pin"]:
        raise Refused("the request's pin is not the commit this checkout is at (`git rev-parse HEAD`)")
    return {"pin": head, "pin_sha256": have}


# ----------------------------------------------------------------------------- 3, 4. the config
def use_pilot_configs(pilot: str) -> str:
    """From now on a config named `round6/rollouts/configs/<name>.toml` is read from `<pilot>/configs/<name>.toml`:
    the runner's copy of that one file (see fetch). Returns the folder."""
    CC.CONFIG_DIR = os.path.join(os.path.abspath(os.path.expanduser(pilot)), "configs")
    return CC.CONFIG_DIR


def check_config(req: dict) -> dict:
    name = req["config"][len(CC.REPO_PREFIX):] if req["config"].startswith(CC.REPO_PREFIX) else ""
    if not CC.NAME.match(name):
        raise Refused("the request's config is not `" + CC.REPO_PREFIX + "<name>.toml`")
    try:
        got = CC.check(req["config"])
    except CC.Refused as e:
        raise Refused("the config: " + str(e)) from None
    flat = got["flat"]
    pairs = [("exam_profile", req["exam_profile"], flat["exam_profile"]), ("instance", req["instance"], flat["instance"]),
             ("model", req["model"], flat["model"]), ("cap_usd", req["cap_usd"], flat["cap_usd"]),
             ("caps.max_turns", req["caps"]["max_turns"], flat["max_turns"]),
             ("caps.max_output_tokens", req["caps"]["max_output_tokens"], flat["max_output_tokens_per_turn"]),
             ("caps.wall_minutes", req["caps"]["wall_minutes"], flat["wall_minutes"]),
             ("caps.box_memory_gb", req["caps"]["box_memory_gb"], flat["box_memory_gb"])]
    differ = [name for name, a, b in pairs if a != b or isinstance(a, bool) != isinstance(b, bool)]
    if differ:
        raise Refused("request and config disagree on " + ", ".join(differ))
    return got


# ----------------------------------------------------------------------------- 5. the pilot folder
def pilot_paths(pilot: str, job_id: str | None = None) -> dict:
    pilot = os.path.abspath(os.path.expanduser(pilot))
    p = {"pilot": pilot, "store": os.path.join(pilot, "store"), "rollouts": os.path.join(pilot, "rollouts"),
         "publish": os.path.join(pilot, "publish"), "ledger": os.path.join(pilot, LEDGER), "instances": os.path.join(pilot, INSTANCES),
         "go": os.path.join(pilot, GO_FILE), "requests": os.path.join(pilot, "requests"), "configs": os.path.join(pilot, "configs"),
         "shared": os.path.join(pilot, "shared-ledger.json")}
    if job_id:
        job = os.path.join(p["rollouts"], job_id)
        p.update(job=job, out=os.path.join(job, "out"), run_dir=os.path.join(job, "out", job_id), status=os.path.join(job, "status.json"),
                 request=os.path.join(job, "request.json"), config=os.path.join(job, "config.toml"),
                 resolved=os.path.join(job, "resolved.toml"), model_entry=os.path.join(job, "model_entry.json"),
                 spend_log=os.path.join(job, "spend.jsonl"), reference=os.path.join(job, "reference.json"),
                 published=os.path.join(p["publish"], job_id))
    return p


def require_pilot(pilot: str) -> dict:
    p = pilot_paths(pilot)
    try:
        st = os.lstat(p["pilot"])
    except OSError:
        raise Refused("the pilot folder does not exist") from None
    if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.getuid() or st.st_mode & 0o077:
        raise Refused("the pilot folder is not a directory of this user with mode 0700 (or it is a link)")
    return p


def read_jsonl(path: str) -> list[dict]:
    rows = []
    try:
        with open(path) as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))
    except FileNotFoundError:
        return []
    except (OSError, ValueError):
        raise Refused(f"{os.path.basename(path)} cannot be read as JSON lines: stop and report, do not repair it") from None
    return rows


def append_jsonl(path: str, row: dict) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(fd, "a") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())


def instance_state(p: dict, instance: str) -> dict:
    """What the pilot folder knows of an instance name: the job it was registered for, whether the store's index
    or a folder of the store names it."""
    registered = [r for r in read_jsonl(p["instances"]) if r.get("instance") == instance]
    index = []
    try:
        with open(os.path.join(p["store"], "index.json")) as f:
            index = [r.get("instance_id") for r in json.load(f)]
    except FileNotFoundError:
        pass
    except (OSError, ValueError):
        raise Refused("the store's index.json cannot be read") from None
    return {"job": registered[0].get("job_id") if registered else None, "in_index": instance in index,
            "in_store": os.path.lexists(os.path.join(p["store"], instance))}


def check_instance(p: dict, req: dict, *, must_exist: bool) -> dict:
    """An instance name is used ONCE: by the job it was made for. Before it is made (must_exist False) the name
    must be unknown everywhere; afterwards it must be registered for exactly this job."""
    s = instance_state(p, req["instance"])
    if s["job"] not in (None, req["job_id"]):
        raise Refused("the instance name has been used by another job; a name is never used twice")
    if not must_exist:
        if s["job"] or s["in_index"] or s["in_store"]:
            raise Refused("the store has seen this instance name already; a name is never used twice")
    elif not (s["job"] == req["job_id"] and s["in_index"] and s["in_store"]):
        raise Refused("the instance of this job has not been made yet (stage `instance`), or was not made for this job")
    return s


def register_instance(p: dict, req: dict) -> None:
    """WRITES one line to <pilot>/INSTANCES.jsonl: this name now belongs to this job, for ever."""
    append_jsonl(p["instances"], {"instance": req["instance"], "job_id": req["job_id"], "time_unix": round(time.time(), 3)})


def ledger_rows(p: dict) -> list[dict]:
    return read_jsonl(p["ledger"])


def ledger_append(p: dict, row: dict) -> None:
    """WRITES one line to <pilot>/LEDGER.jsonl (append only; the tools never rewrite or delete a line)."""
    append_jsonl(p["ledger"], dict(row, time_unix=round(time.time(), 3)))


def ledger_sum(rows: list[dict]) -> dict:
    """What the pilot folder's ledger says was spent, at most: per job the counted cost once the run has ended,
    else the whole bound that was reserved for it (cap_usd + one worst-case call). Runs against a stand-in
    endpoint (`billed` false) cost nothing and are left out."""
    jobs: dict = {}
    for r in rows:
        j = jobs.setdefault(r.get("job_id"), {})
        if r.get("event") == "reserved":
            j.update(bound=float(r.get("bound_usd") or 0.0), billed=bool(r.get("billed", True)))
        elif r.get("event") == "ended":
            j["counted"] = float(r["counted_usd"]) if _num(r.get("counted_usd")) else None
            j["complete"] = bool(r.get("count_complete"))
    total, open_jobs = 0.0, []
    for job, j in jobs.items():
        if not j.get("billed", True):
            continue
        if j.get("counted") is not None and j.get("complete"):
            total += j["counted"]
        else:                                                # still running, cut without a complete count, or never ended
            total += max(j.get("bound", 0.0), j.get("counted") or 0.0)
            open_jobs.append(job)
    return {"sum_usd": total, "jobs": len(jobs), "counted_at_their_bound": sorted(str(j) for j in open_jobs)}


def open_jobs(rows: list[dict]) -> list[str]:
    """Job ids that the ledger holds as reserved and never ended: a rollout that is running, or one whose tool died
    before it could close its row. One rollout at a time: while there is one, no stage of any job starts."""
    ended = {r.get("job_id") for r in rows if r.get("event") == "ended"}
    return sorted({str(r.get("job_id")) for r in rows if r.get("event") == "reserved" and r.get("job_id") not in ended})


def check_job_is_new(p: dict, req: dict) -> None:
    if any(r.get("job_id") == req["job_id"] for r in ledger_rows(p)):
        raise Refused("the ledger already holds this job id: a job runs once, and a run that was cut is not run again")


# ----------------------------------------------------------------------------- 6. the lead's standing go
def read_go(p: dict, today: datetime.date | None = None) -> dict:
    """The lead's standing go for model spend: the file <pilot>/LEAD-GO-MODEL-SPEND.json,

        {"schema": "physim2-lead-go/v1", "ceiling_usd": 500, "date": "2026-11-11"}

    The session on the lead's machine creates it ONLY on the lead's instruction in that session, with the ceiling
    the lead named and the date of that day; no tool creates or changes it. Refused: no such file, a link, other
    keys, a ceiling that is not a positive number, a date in the future or more than 30 days ago."""
    try:
        st = os.lstat(p["go"])
        if not stat.S_ISREG(st.st_mode) or st.st_size > 4096:
            raise Refused(f"{GO_FILE} is not a small regular file")
        with open(p["go"]) as f:
            go = json.load(f)
    except FileNotFoundError:
        raise Refused(f"no {GO_FILE} in the pilot folder: the lead has not given a go for model spend. Nothing was started.") from None
    except (OSError, ValueError):
        raise Refused(f"{GO_FILE} cannot be read as JSON") from None
    if not isinstance(go, dict) or set(go) - {"schema", "ceiling_usd", "date", "note"} or go.get("schema") != GO_SCHEMA:
        raise Refused(f"{GO_FILE} is not of schema {GO_SCHEMA} with ceiling_usd and date")
    if not _num(go.get("ceiling_usd")) or go["ceiling_usd"] <= 0:
        raise Refused(f"{GO_FILE}: ceiling_usd is not a positive number")
    try:
        day = datetime.date.fromisoformat(str(go.get("date")))
    except ValueError:
        raise Refused(f"{GO_FILE}: date is not YYYY-MM-DD") from None
    today = today or datetime.datetime.now(datetime.timezone.utc).date()
    age = (today - day).days
    if age < -1 or age > GO_MAX_AGE_DAYS:
        raise Refused(f"{GO_FILE}: its date is in the future or more than {GO_MAX_AGE_DAYS} days old; the lead gives a new go")
    return {"ceiling_usd": float(go["ceiling_usd"]), "date": day.isoformat()}


# ----------------------------------------------------------------------------- 7. prices and bounds
def models_url(base_url: str | None) -> str:
    return PRIME_MODELS_URL if not base_url else base_url.rstrip("/") + "/models"


def fetch_model_entry(model: str, base_url: str | None = None, timeout: float = 30.0) -> dict:
    """The model's entry in the provider's public listing, fetched now, WITHOUT a credential (one GET). Returns
    {"fetched_unix", "source", "entry"}. Refused when the listing does not answer or does not hold the model."""
    import urllib.error
    import urllib.request
    url = models_url(base_url)
    if not (url.startswith("https://") or url.startswith("http://127.0.0.1:")):
        raise Refused("the model listing is fetched over https, or from a stand-in on 127.0.0.1, and from nowhere else")
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "physim2-pilot"}),
                                    timeout=timeout) as r:
            raw = r.read(32 << 20)
        listing = json.loads(raw)
    except (urllib.error.URLError, OSError, ValueError) as e:
        raise Refused(f"the model listing did not answer ({type(e).__name__}); without listed prices no model run starts") from None
    rows = listing.get("data") if isinstance(listing, dict) else listing
    found = [r for r in rows or [] if isinstance(r, dict) and r.get("id") == model]
    if len(found) != 1:
        raise Refused("the model is not listed (exactly once) by the provider: check the id")
    return {"fetched_unix": int(time.time()), "source": f"GET {url} (no credential sent)", "entry": found[0]}


def prices_of(entry: dict) -> dict:
    """Listed prices in dollars per million tokens and the context window, from a saved model entry. Refused when
    the input price, the output price or the window is missing: such a run cannot be bounded."""
    e = entry.get("entry") if isinstance(entry.get("entry"), dict) else entry
    pr = e.get("pricing") if isinstance(e.get("pricing"), dict) else {}
    p_in, p_out, p_cache = pr.get("input_usd_per_mtok"), pr.get("output_usd_per_mtok"), pr.get("cache_read_usd_per_mtok")
    window = e.get("context_window") or e.get("context_length")
    if not _num(p_in) or not _num(p_out) or p_in < 0 or p_out < 0 or isinstance(window, bool) or not isinstance(window, int) or window < 1:
        raise Refused("the model's listing lacks an input price, an output price or a context window")
    p_write = pr.get("cache_write_usd_per_mtok")
    p_write = float(p_write) if _num(p_write) and p_write >= 0 else None
    # `input_counted` is the price every prompt token that is not a cache read is COUNTED at: the listed input price,
    # or the listed cache-write price where that is higher (a provider may bill a prompt it stores at that price)
    return {"input": float(p_in), "output": float(p_out), "cache_read": float(p_cache) if _num(p_cache) and p_cache >= 0 else None,
            "cache_write": p_write, "input_counted": max(float(p_in), p_write or 0.0),
            "context_window": window, "max_output_tokens": e.get("max_output_tokens") if isinstance(e.get("max_output_tokens"), int) else None}


def bounds(flat: dict, prices: dict) -> dict:
    """The three numbers of a run's bill, from its caps and the listed prices:
        worst_call_usd   one call: max_context_tokens x input price + max output tokens x output price
                         (input price = the listed one, or the listed cache-write price where that is higher)
        bound_usd        cap_usd + worst_call_usd: what the spend stop guarantees (tools and runbook use this one)
        crude_bound_usd  max_turns x (context window x input price + max output tokens x output price): what the
                         caps alone would allow without the spend stop and the context cap
    Refused when cap_usd is below one worst-case call, when max_context_tokens exceeds the model's window, or
    when the reply cap exceeds what the model lists."""
    ctx, out = int(flat["max_context_tokens"]), int(flat["max_output_tokens_per_turn"])
    if ctx > prices["context_window"]:
        raise Refused(f"max_context_tokens ({ctx}) is above the model's listed context window ({prices['context_window']})")
    if prices.get("max_output_tokens") and out > prices["max_output_tokens"]:
        raise Refused(f"max_output_tokens_per_turn ({out}) is above the model's listed output limit ({prices['max_output_tokens']})")
    p_in = prices.get("input_counted", prices["input"])
    worst = (ctx * p_in + out * prices["output"]) / MTOK
    crude = int(flat["max_turns"]) * (prices["context_window"] * p_in + out * prices["output"]) / MTOK
    b = {"worst_call_usd": worst, "bound_usd": float(flat["cap_usd"]) + worst, "crude_bound_usd": crude, "cap_usd": float(flat["cap_usd"]),
         "max_context_tokens": ctx, "max_output_tokens": out, "max_turns": int(flat["max_turns"]), "prices_usd_per_mtok": prices}
    if flat["cap_usd"] < worst:
        raise Refused(f"cap_usd ({flat['cap_usd']}) is below one worst-case call ({worst:.4f}): raise the cap or lower max_context_tokens")
    return b


SHARED_SCHEMA = "rollout-ledger/v1"
SHARED_STATUS = ("done", "running", "cut")


def shared_ledger(path: str) -> dict:
    """What OTHER machines spent on model rollouts, from a copy of the program's shared ledger (schema
    `rollout-ledger/v1`: research/alife/vecworld/program/round6/rollouts/ledger.json on the lab branch; it lists
    the rollouts that did NOT run from this pilot folder). The lead's ceiling is one total, so this sum is added
    to the pilot folder's own ledger before a model run is admitted. Per row: a finished or cut run counts its
    billed cost (its bound, if no billed cost is given), a running one its bound; the file's own totals count
    when they are higher. Numbers only are read; the file is data and names no code. Refused: anything that is
    not a small regular file of exactly this shape."""
    try:
        st = os.lstat(path)
        if not stat.S_ISREG(st.st_mode) or st.st_size > 256 << 10:
            raise Refused("the shared ledger is not a regular file of at most 256 KiB")
        with open(path, "rb") as f:
            raw = f.read()
        led = json.loads(raw.decode("utf-8"))
    except OSError:
        raise Refused("the shared ledger cannot be read") from None
    except (UnicodeDecodeError, ValueError):
        raise Refused("the shared ledger is not UTF-8 JSON") from None
    if not isinstance(led, dict) or led.get("schema") != SHARED_SCHEMA or not isinstance(led.get("rows"), list):
        raise Refused(f"the shared ledger is not of schema {SHARED_SCHEMA} with rows")
    spent = 0.0
    for r in led["rows"]:
        ok = isinstance(r, dict) and r.get("status") in SHARED_STATUS and _num(r.get("bound_usd")) and r["bound_usd"] >= 0 \
            and (r.get("billed_usd") is None or (_num(r["billed_usd"]) and r["billed_usd"] >= 0))
        if not ok:
            raise Refused("the shared ledger holds a row without a status of done, running or cut and a bound (and billed cost) in dollars")
        spent += float(r["bound_usd"]) if r["status"] == "running" or r.get("billed_usd") is None else float(r["billed_usd"])
    stated = [led.get(k) for k in ("billed_usd_total", "reserved_usd_open")]
    if not all(_num(x) and x >= 0 for x in stated):
        raise Refused("the shared ledger lacks billed_usd_total or reserved_usd_open")
    return {"spent_elsewhere_usd": max(spent, float(stated[0]) + float(stated[1])), "rows": len(led["rows"]),
            "updated_utc": str(led.get("updated_utc"))[:40], "sha256": hashlib.sha256(raw).hexdigest()}


def check_ceiling(p: dict, go: dict, b: dict, elsewhere: dict | None = None) -> dict:
    """The lead's ceiling is ONE total: this pilot folder's ledger, plus what the shared ledger says other
    machines spent (when the caller gives one; a billed model run must), plus this run's bound."""
    s = ledger_sum(ledger_rows(p))
    other = float(elsewhere["spent_elsewhere_usd"]) if elsewhere else 0.0
    if s["sum_usd"] + other + b["bound_usd"] > go["ceiling_usd"] + 1e-9:
        raise Refused(f"the ledger's sum ({s['sum_usd']:.4f}) plus what other machines spent ({other:.4f}) plus this run's bound "
                      f"({b['bound_usd']:.4f}) would exceed the lead's ceiling ({go['ceiling_usd']:.2f})")
    return dict(s, ceiling_usd=go["ceiling_usd"], spent_elsewhere_usd=other, after_this_run_at_most_usd=s["sum_usd"] + other + b["bound_usd"])


# ----------------------------------------------------------------------------- 0. the three input files of a job
def git_show(commit: str, path: str, limit: int, repo: str = ROOT) -> bytes:
    """The bytes of `path` (from the repository root) in `commit`, read from the checkout's own object store.
    Read-only; no network; a client that does not answer in 20 s is killed by Python (its own child)."""
    try:
        r = subprocess.run(["git", "-C", repo, "show", f"{commit}:{path}"], capture_output=True, timeout=20, stdin=subprocess.DEVNULL,
                           env={k: os.environ[k] for k in ("PATH", "HOME") if k in os.environ})
    except (OSError, subprocess.TimeoutExpired):
        raise Refused("git did not answer") from None
    if r.returncode != 0:
        raise Refused(f"commit {commit[:12]} does not hold {path} (or the commit was not fetched)")
    if len(r.stdout) > limit:
        raise Refused(f"{path} is larger than {limit} bytes")
    return r.stdout


def _existing(path: str) -> bytes | None:
    try:
        st = os.lstat(path)
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(st.st_mode) or st.st_size > (1 << 20):
        raise Refused(f"{os.path.basename(path)} in the pilot folder is not a small regular file")
    with open(path, "rb") as f:
        return f.read()


def fetch(pilot: str, commit: str, job_id: str, show=git_show) -> dict:
    """Copy the THREE input files of a job out of ONE commit of the repository into the pilot folder, as data:

        <REQUESTS_PREFIX><job_id>.json          -> <pilot>/requests/<job_id>.json     (created once, never replaced)
        the config the request names            -> <pilot>/configs/<name>.toml        (created once, never replaced)
        <SHARED_LEDGER_PATH>                    -> <pilot>/shared-ledger.json         (the newest copy)

    Nothing else is read from that commit and nothing of it is executed: the code stays the pin's. The request must
    pass its own shape check and carry the job id of its file name; the config's NAME must be a plain file name in
    round6/rollouts/configs/ (its content is checked by the strict schema when the request is checked); the ledger
    must be of schema rollout-ledger/v1. Refused, with nothing written, if any of that fails."""
    if not isinstance(commit, str) or not HEX40.match(commit):
        raise Refused("--source-commit is not 40 hexadecimal digits")
    if not isinstance(job_id, str) or not JOB.match(job_id):
        raise Refused("--job-id is not lower-case letters, digits and hyphens (3 to 63 characters)")
    p = dict(require_pilot(pilot), **pilot_paths(pilot, job_id))
    raw = show(commit, REQUESTS_PREFIX + job_id + ".json", MAX_REQUEST_BYTES)
    try:
        req = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        raise Refused("the request is not UTF-8 JSON") from None
    bad = validate_request(req)
    if bad:
        raise Refused("the request: " + "; ".join(bad))
    if req["job_id"] != job_id:
        raise Refused("the request's job_id is not the name of its file")
    name = req["config"][len(CC.REPO_PREFIX):] if req["config"].startswith(CC.REPO_PREFIX) else ""
    if not CC.NAME.match(name):
        raise Refused("the request's config is not `" + CC.REPO_PREFIX + "<name>.toml`")
    cfg = show(commit, CC.REPO_PREFIX + name, CC.MAX_BYTES)
    led = show(commit, SHARED_LEDGER_PATH, 256 << 10)
    targets = (("request", os.path.join(p["requests"], job_id + ".json"), raw), ("config", os.path.join(p["configs"], name), cfg))
    for key, path, data in targets:                          # look before anything is written
        have = _existing(path)
        if have is not None and have != data:
            raise Refused(f"the pilot folder holds another {key} under this name: a request and a config are never replaced "
                          "(the requester writes a new job id and a new config name)")
    out = {"job_id": job_id, "source_commit": commit}
    for d in (p["requests"], p["configs"]):
        os.makedirs(d, mode=0o700, exist_ok=True)
    for key, path, data in targets:
        if _existing(path) is None:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
            with os.fdopen(fd, "wb") as f:
                f.write(data)
        out[key] = {"file": os.path.relpath(path, p["pilot"]), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    fd = os.open(p["shared"], os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(led)
    s = shared_ledger(p["shared"])                           # a ledger of another shape is refused here, and by every later stage
    out["shared_ledger"] = {"file": "shared-ledger.json", "bytes": len(led), "sha256": s["sha256"], "updated_utc": s["updated_utc"],
                            "spent_elsewhere_usd": s["spent_elsewhere_usd"]}
    out["request_says"] = {k: req[k] for k in ("pin", "pin_sha256", "config", "exam_profile", "instance", "model", "caps", "cap_usd")}
    return out


def facts() -> dict:
    """What a runner needs to check a request and a config mechanically, as data: the request's keys and shapes, the
    strict schema of a rollout config, the exam profiles with their item counts, the scripted policies of the
    reference table, the stages in order, and the files of the pilot folder. RUNBOOK_MAC.md, step 3, prints the
    same object; tools/check_runbook.py compares the two."""
    return {"request": {"schema": SCHEMA, "keys": list(KEYS), "caps_keys": list(CAP_KEYS), "job_id": JOB.pattern, "instance": INSTANCE.pattern,
                        "pin": HEX40.pattern, "pin_sha256": HEX64.pattern, "max_bytes": MAX_REQUEST_BYTES, "file": REQUESTS_PREFIX + "<job_id>.json",
                        "wall_minutes_max": 180, "box_memory_gb_max": 4},
            "config": CC.schema(),
            "reference_table": {"tool": "tools/prove.py", "policies_by_profile": {r["profile"]: r["reference_policies"] for r in CC.schema()["exam_profiles"]},
                                "scale": "K = 0 (climatology) and O = 1 (oracle) come from the frozen exam, not from a rollout"},
            "stages": list(STAGES), "then": "tools/pack_rollout.py",
            "pilot_folder": {"go": GO_FILE, "go_schema": GO_SCHEMA, "go_max_age_days": GO_MAX_AGE_DAYS, "ledger": LEDGER, "instances": INSTANCES,
                             "shared_ledger": "shared-ledger.json", "shared_ledger_schema": SHARED_SCHEMA, "shared_ledger_source": SHARED_LEDGER_PATH},
            "prices_from": PRIME_MODELS_URL,
            "publication": {"folder": "publish/<job_id>/", "files": [*PUBLICATION_FILES, "submission/", "key_scan.json", "MANIFEST.json"],
                            "max_file_bytes": PUBLICATION_MAX_FILE_BYTES, "max_total_bytes": PUBLICATION_MAX_TOTAL_BYTES,
                            "created_once": True, "a_file_with_a_key_scan_hit": "left out and listed by name and count"},
            "after_a_crash": {"stage": "close", "runbook": "If a run was interrupted, point 8", "then": "tools/pack_rollout.py"}}


def facts_text() -> str:
    """facts() as JSON text with one line per key of a config and per exam profile (what the runbook prints)."""
    f = facts()
    d = lambda o: json.dumps(o, separators=(", ", ": "))     # noqa: E731
    lines = ["{"]
    for i, (k, v) in enumerate(f.items()):
        comma = "," if i < len(f) - 1 else ""
        if k != "config":
            lines.append(f" {json.dumps(k)}: {d(v)}{comma}")
            continue
        lines.append(' "config": {')
        items = list(v.items())
        for j, (k2, v2) in enumerate(items):
            c2 = "," if j < len(items) - 1 else ""
            if k2 == "keys":
                ks = list(v2.items())
                lines += ['  "keys": {'] + [f"   {json.dumps(a)}: {d(b)}" + ("," if n < len(ks) - 1 else "") for n, (a, b) in enumerate(ks)] + ["  }" + c2]
            elif k2 == "exam_profiles":
                lines += ['  "exam_profiles": ['] + ["   " + d(r) + ("," if n < len(v2) - 1 else "") for n, r in enumerate(v2)] + ["  ]" + c2]
            else:
                lines.append(f"  {json.dumps(k2)}: {d(v2)}{c2}")
        lines.append(" }" + comma)
    return "\n".join(lines + ["}"])


def spend_log_total(path: str) -> dict:
    """What a run's spend log (physim2_env/spend.py) says was counted: the last line's running sum, plus one
    worst-case call for every attempt that was sent and never settled (the process died with it in flight)."""
    rows = read_jsonl(path)
    meter = next((r for r in rows if r.get("event") == "meter"), None)
    if meter is None:
        return {"present": False, "counted_usd": None, "attempts": 0, "complete": False}
    sent = {r["n"] for r in rows if r.get("event") == "sent"}
    settled = {r["n"]: r for r in rows if r.get("event") == "settled"}
    hanging = len(sent - set(settled))
    counted = sum(float(r["usd"]) for r in settled.values()) + hanging * float(meter["worst_call_usd"])
    stops = [r.get("condition") for r in rows if r.get("event") == "refused"]
    return {"present": True, "counted_usd": counted, "attempts": len(sent), "settled": len(settled), "never_settled": hanging,
            "worst_case_calls": sum(1 for r in settled.values() if str(r.get("basis", "")).startswith("worst case")) + hanging,
            "refused": len(stops), "stopped": stops[0] if stops else None, "complete": hanging == 0,
            "worst_call_usd": float(meter["worst_call_usd"]), "bound_usd": float(meter["bound_on_the_bill_usd"]), "billed": bool(meter.get("billed", True)),
            "within_bound": counted <= float(meter["bound_on_the_bill_usd"]) + 1e-9}


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="check a rollout request against the pin and the pilot folder; starts nothing")
    ap.add_argument("--request")
    ap.add_argument("--pilot")
    ap.add_argument("--fetch", action="store_true", help="copy the job's request, its config and the shared ledger out of --source-commit "
                                                         "into the pilot folder (reads git objects of this checkout; no network)")
    ap.add_argument("--source-commit", help="with --fetch: the 40-character commit that holds the request")
    ap.add_argument("--job-id", help="with --fetch: the job id (the request is <job_id>.json)")
    ap.add_argument("--facts", action="store_true", help="print the request's shape, the config schema, the profiles and the stages as JSON")
    ap.add_argument("--prices", action="store_true", help="also fetch the model's listed prices (one GET, no credential) and print the bounds")
    ap.add_argument("--no-go", action="store_true", help="do not look for the lead's go (for the free stages)")
    ap.add_argument("--shared-ledger", default=None, help="a copy of the program's shared ledger (rollout-ledger/v1): what other machines spent")
    a = ap.parse_args(argv)
    if a.facts:
        print(facts_text())
        return 0
    if not a.pilot or bool(a.request) == bool(a.fetch) or (a.fetch and not (a.source_commit and a.job_id)):
        ap.error("--request FILE --pilot DIR, or --fetch --source-commit HEX --job-id ID --pilot DIR, or --facts")
    if a.fetch:
        try:
            print(json.dumps(fetch(a.pilot, a.source_commit, a.job_id)))
        except (Refused, CC.Refused) as e:
            print("refused: " + str(e))
            return 2
        return 0
    try:
        use_pilot_configs(a.pilot)
        req = read_request(a.request)
        if os.path.basename(a.request) != req["job_id"] + ".json":
            raise Refused("the request file is not named <job_id>.json")
        pin = check_pin(req)
        cfg = check_config(req)
        p = dict(require_pilot(a.pilot), **pilot_paths(a.pilot, req["job_id"]))
        state = instance_state(p, req["instance"])
        if state["job"] not in (None, req["job_id"]) or (state["job"] is None and (state["in_index"] or state["in_store"])):
            raise Refused("the store has seen this instance name already; a name is never used twice")
        out = {"job_id": req["job_id"], "pin": pin, "config": cfg["name"], "config_sha256": cfg["sha256"], "flat": cfg["flat"],
               "instance": state, "ledger": ledger_sum(ledger_rows(p))}
        go = None if a.no_go else read_go(p)
        if go:
            out["go"] = go
        if a.prices:
            b = bounds(cfg["flat"], prices_of(fetch_model_entry(req["model"])))
            out["bounds"] = b
            if go:
                out["ceiling"] = check_ceiling(p, go, b, shared_ledger(a.shared_ledger) if a.shared_ledger else None)
    except (Refused, CC.Refused) as e:
        print("refused: " + str(e))
        return 2
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
