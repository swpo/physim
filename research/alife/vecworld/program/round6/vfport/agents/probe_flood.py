"""probe_flood -- a box that floods: what reaches vf-eval and the laboratory when an agent sends without end.

A scripted test agent for the agent's box (physim2-script harness; tools/check_step3.py, part `flood`, starts it).
Round 4, second pass (code audit K4): it pushes far more bytes than the pilot keeps into each way out of a box,
and writes what came back to /workspace/flood_report.json. The worker side (vf-eval's memory, the laboratory's)
is measured by the tool that started the rollout, from outside the box.

  card        lab.card(): the compute envelope and the per-item limits of THIS run (exam audit X5)
  body        one request of 64 MiB to the laboratory (declared length) and one without a declared length,
              sent as fast as the box can: answered 413 after the guard's cap, the rest never read
  connections 80 connections to the box's proxy at once: it serves 64 and closes the others unread
  validator   lab.validate with a physim2/validate.py of the agent's that prints 256 MiB: the report is cut in the
              box; then one that writes 256 MiB straight into the output of the command that started it
              (/proc/<parent>/fd/1, which root in a box can open): vf-eval keeps at most its bound and the
              check reports a failure. The original validate.py is put back afterwards.
  as graded   lab.validate on three predictors that read a file left in /tmp, one left in /dev/shm, and a module
              added to physim2/: each must fail (exam audit X6)
  interception with --interception (round 5, code audit K9), run by the stock bash harness's own `bash` tool (a
              stand-in model asks for it: tools/check_step3.py, part `flood5`): the rollout's secret and the
              interception server's address are read from the chat program's command line, as a model could
              (/proc/<pid>/cmdline, --api-key= and --base-url=); then one request declaring 1 GiB and one chunked
              1 GiB request, each with the secret, are sent as fast as the box can (answered 413 after the
              server's body limit, the rest never read); PARALLEL requests of 15 MiB of JSON at once, each with the
              secret (the box's proxy lets one at a time through to the server, the others wait); UNAUTHORIZED
              small requests without the secret (vf-eval's log keeps a bounded number of their lines); to the
              laboratory, LAB_BIG requests with an operation name of 3 MiB and LAB_SMALL refused ones (the
              laboratory's log on the host keeps each line short and at most its number of lines). Writes
              /workspace/flood5_report.json.
  harness     with --harness-flood: 256 MiB into the output of the harness's own command, last of all. vf-eval
              keeps at most its bound, the harness command is reported as failed, and the run is graded on its
              last checkpoint (ruling E1). The report is written BEFORE that, in a second file the harness never
              collects (the run fails), so this mode is run on its own, with nothing else.

IT FLOODS PIPES AND SOCKETS. The first statement below refuses to do anything unless this process is inside a
box that the environment prepared: the same gate as agents/probe_caps.py (host-safety audit, change 3).
"""
import os
import stat
import sys


def _in_prepared_box() -> bool:
    try:
        d, f = os.lstat("/etc/physim2"), os.lstat("/etc/physim2/predictor_uid")
    except OSError:
        return False
    return (os.path.exists("/.dockerenv") and stat.S_ISDIR(d.st_mode) and stat.S_ISREG(f.st_mode) and d.st_uid == 0 and f.st_uid == 0
            and not f.st_mode & 0o022)


if not _in_prepared_box():
    sys.exit("refused: probe_flood.py runs only inside a box prepared by the PhySim v2 environment "
             "(/.dockerenv and a root-owned /etc/physim2/predictor_uid); it floods pipes and sockets")

import json  # noqa: E402
import socket  # noqa: E402
import time  # noqa: E402
import urllib.parse  # noqa: E402

MIB = 1 << 20
REPORT = "/workspace/flood_report.json"
FLOOD = 256 * MIB
sys.path.insert(0, "/workspace")
import physim2  # noqa: E402


def write_to(path: str, n: int) -> dict:
    """Write n bytes into an open file of another process (a pipe), as fast as it is read."""
    t0, done = time.time(), 0
    try:
        with open(path, "wb", buffering=0) as f:
            block = b"F" * MIB
            while done < n:
                done += f.write(block)
        return {"written": done, "seconds": round(time.time() - t0, 2)}
    except OSError as e:
        return {"written": done, "error": type(e).__name__, "seconds": round(time.time() - t0, 2)}


def parent_stdout() -> str:
    """The output of the command that started this process: a pipe the parent shell holds. A shell that redirects
    a command's output (`cmd > log`) keeps its own output on a saved descriptor meanwhile (dash: fd 10 and up),
    so the first PIPE among the parent's descriptors 1, 2, then the others is taken."""
    base = f"/proc/{os.getppid()}/fd"
    fds = sorted((int(n) for n in os.listdir(base) if n.isdigit()), key=lambda n: (n not in (1, 2), n))
    for n in fds:
        try:
            if os.readlink(f"{base}/{n}").startswith("pipe:"):
                return f"{base}/{n}"
        except OSError:
            continue
    return f"{base}/1"


PARALLEL, UNAUTHORIZED, LAB_BIG, LAB_SMALL = 8, 3000, 4, 2000


def chat_program() -> dict:
    """The --base-url and --api-key of the chat program of the stock bash harness, read from its command line in
    /proc as any process of the box can (the agent is root here). {} when there is none."""
    for d in os.listdir("/proc"):
        if not d.isdigit():
            continue
        try:
            argv = open(f"/proc/{d}/cmdline", "rb").read().split(b"\0")
        except OSError:
            continue
        got = {a.split(b"=", 1)[0].decode(): a.split(b"=", 1)[1].decode() for a in argv if a.startswith((b"--api-key=", b"--base-url="))}
        if len(got) == 2:
            return {"pid": int(d), "base_url": got["--base-url"], "secret": got["--api-key"]}
    return {}


def raw_post(url: str, headers: dict, declared, n: int, piece: bytes, wait_s: float = 120.0) -> dict:
    """One POST of n body bytes (declared length, or chunked when declared is None) to an http:// URL, sent as
    fast as the peer takes it; stops at the first byte of an answer. Returns the status line, the body bytes sent
    and the seconds."""
    u = urllib.parse.urlsplit(url)
    s = socket.create_connection((u.hostname, u.port or 80), timeout=60)
    head = [f"POST {u.path} HTTP/1.1", f"Host: {u.netloc}", "Content-Type: application/json", "Connection: close"]
    head += [f"{k}: {v}" for k, v in headers.items()]
    head += [f"Content-Length: {declared}"] if declared is not None else ["Transfer-Encoding: chunked"]
    s.sendall(("\r\n".join(head) + "\r\n\r\n").encode())
    sent, status, t0 = 0, None, time.time()
    try:
        while sent < n:
            s.settimeout(0.0)
            try:
                got = s.recv(4096)
                status = got.split(b"\r\n", 1)[0].decode("latin-1")[:60] if got else "closed"
                break
            except BlockingIOError:
                pass
            s.settimeout(wait_s)
            part = piece[:n - sent]
            try:
                s.sendall(part if declared is not None else b"%x\r\n" % len(part) + part + b"\r\n")
            except OSError as e:
                status = f"send failed ({type(e).__name__})"
                break
            sent += len(part)
        if status is None:
            if declared is None:
                s.sendall(b"0\r\n\r\n")
            s.settimeout(wait_s)
            got = s.recv(4096)
            status = got.split(b"\r\n", 1)[0].decode("latin-1")[:60] if got else "closed"
    except OSError as e:
        status = status or f"error {type(e).__name__}"
    finally:
        s.close()
    return {"status": status, "body_bytes_sent": sent, "seconds": round(time.time() - t0, 2), "t": [round(t0, 2), round(time.time(), 2)]}


def interception_flood(rep: dict) -> None:
    import threading
    cp = chat_program()
    rep["chat_program"] = {"found": bool(cp), "pid": cp.get("pid"), "secret_chars": len(cp.get("secret", "")),
                           "base_url_path_parts": len(urllib.parse.urlsplit(cp.get("base_url", "")).path.split("/"))}
    if not cp:
        return
    url, auth = cp["base_url"].rstrip("/") + "/chat/completions", {"Authorization": "Bearer " + cp["secret"]}
    big = b"{" * MIB
    rep["one_gib"] = {"t": round(time.time(), 2), "declared": raw_post(url, auth, 1 << 30, 1 << 30, big),
                      "chunked": raw_post(url, auth, None, 1 << 30, big)}
    one = b"{},"                                             # 15 MiB of a JSON list of empty objects: parsed, then refused
    body = b"[" + one * ((15 * MIB) // len(one)) + b"{}]"
    res = [None] * PARALLEL

    def worker(i):
        res[i] = raw_post(url, auth, len(body), len(body), body)
    ths = [threading.Thread(target=worker, args=(i,)) for i in range(PARALLEL)]
    t0 = time.time()
    for t in ths:
        t.start()
    for t in ths:
        t.join(600)
    rep["parallel"] = {"n": PARALLEL, "body_bytes": len(body), "t": [round(t0, 2), round(time.time(), 2)], "answers": res}
    t0, statuses = time.time(), {}
    for i in range(UNAUTHORIZED):
        r = raw_post(url, {"Authorization": "Bearer not-the-secret"}, 2, 2, b"{}", wait_s=30)
        statuses[r["status"]] = statuses.get(r["status"], 0) + 1
    rep["unauthorized"] = {"n": UNAUTHORIZED, "statuses": statuses, "t": [round(t0, 2), round(time.time(), 2)]}
    lab, t0, out = physim2.Lab(), time.time(), {}
    for i in range(LAB_BIG):                                 # an operation's name, or an argument's name, of 3 MiB
        try:
            lab._send("X" * (3 * MIB) + str(i)) if i % 2 else lab._send("card", **{"k" * (3 * MIB) + str(i): 1})
            out["big_accepted"] = out.get("big_accepted", 0) + 1
        except Exception as e:
            out.setdefault("big_errors", []).append(str(e)[:120])
    for i in range(LAB_SMALL):
        try:
            lab._send("usage", **{"y" * 200: i}) if i % 2 else lab._send("no-such-op")
        except Exception as e:
            k = type(e).__name__ + ": " + str(e)[:60]
            out[k] = out.get(k, 0) + 1
    out["t"] = [round(t0, 2), round(time.time(), 2)]
    rep["lab"] = out


def main():
    harness_flood = "--harness-flood" in sys.argv
    if "--interception" in sys.argv:                        # round 5, K9: alone, from the stock bash harness's tool
        rep = {"time": time.time()}
        interception_flood(rep)
        rep["t_end"] = round(time.time(), 2)
        with open("/workspace/flood5_report.json", "w") as f:
            json.dump(rep, f, indent=1)
        print("interception flood done")
        return
    rep = {"time": time.time()}
    lab = physim2.Lab()
    if harness_flood:                                        # alone, last: see the module text
        target = parent_stdout()
        rep["harness"] = {"target": "the harness command's own output: " + target.rsplit("/", 2)[-2] + " " + target.rsplit("/", 1)[-1], "planned": FLOOD}
        with open(REPORT, "w") as f:
            json.dump(rep, f, indent=1)
        rep["harness"].update(write_to(target, FLOOD))
        with open(REPORT, "w") as f:
            json.dump(rep, f, indent=1)
        print("harness flood done")
        return
    card = lab.card()
    rep["card"] = {"compute_envelope": card.get("compute_envelope"), "predictor_limits": card.get("predictor_limits")}
    url = urllib.parse.urlsplit(lab.address)
    host, port, path = url.hostname, url.port or 80, url.path

    def post(declared: int | None, n: int) -> dict:
        """One POST of up to n bytes to the laboratory through the box's proxy; the status line it got, and how
        many body bytes the box could send before it."""
        s = socket.create_connection((host, port), timeout=60)
        head = [f"POST {path} HTTP/1.1", f"Host: {url.netloc}", "Content-Type: application/json", "Accept: application/json, text/event-stream"]
        head += [f"Content-Length: {declared}"] if declared is not None else ["Transfer-Encoding: chunked"]
        s.sendall(("\r\n".join(head) + "\r\n\r\n").encode())
        sent, status, t0 = 0, None, time.time()
        piece = b"{" * (256 << 10)
        s.settimeout(0.0)
        try:
            while sent < n and status is None:
                try:
                    got = s.recv(4096)
                    status = got.split(b"\r\n", 1)[0].decode("latin-1")[:60] if got else "closed"
                    break
                except BlockingIOError:
                    pass
                s.settimeout(30)
                chunk = piece if declared is not None else b"%x\r\n" % len(piece) + piece + b"\r\n"
                try:
                    s.sendall(chunk)
                except OSError as e:
                    status = f"send failed ({type(e).__name__})"
                    break
                sent += len(piece)
                s.settimeout(0.0)
            if status is None:
                s.settimeout(30)
                got = s.recv(4096)
                status = got.split(b"\r\n", 1)[0].decode("latin-1")[:60] if got else "closed"
        except OSError as e:
            status = status or f"error {type(e).__name__}"
        finally:
            s.close()
        return {"status": status, "body_bytes_sent": sent, "seconds": round(time.time() - t0, 2)}

    t_body = time.time()
    rep["body"] = {"declared_64_mib": post(64 * MIB, 64 * MIB), "chunked_64_mib": post(None, 64 * MIB), "t": [round(t_body, 2), round(time.time(), 2)]}
    rep["body"]["after"] = {"usage_ok": bool(lab.usage())}
    rep["t_floods_start"] = round(t_body, 2)
    conns, closed = [], 0
    for _ in range(80):
        try:
            conns.append(socket.create_connection((host, port), timeout=10))
        except OSError:
            break
    time.sleep(1.0)
    for c in conns:
        c.settimeout(1.0)
        try:
            closed += c.recv(1) == b""
        except (socket.timeout, OSError):
            pass
    for c in conns:
        c.close()
    rep["connections"] = {"opened": len(conns), "closed_unread_by_the_proxy": closed}
    time.sleep(2.0)
    # ---- the validator's output ----
    vpath = os.path.join(os.path.dirname(physim2.__file__), "validate.py")
    original = open(vpath, "rb").read()
    try:
        with open(vpath, "w") as f:
            f.write("import sys\nfor _ in range(%d):\n    sys.stdout.write('x' * 1048575 + '\\n')\n"
                    "def check(path):\n    return {'ok': True}\n" % (FLOOD // MIB))
        t0 = time.time()
        try:                                                 # the tool op itself: Lab.validate would import this file HERE
            r = lab._call("validate", path="submission")
        except Exception as e:
            r = {"raised": f"{type(e).__name__}: {str(e)[:200]}"}
        rep["validator_prints"] = {"report": {k: str(v)[:200] for k, v in r.items()}, "seconds": round(time.time() - t0, 1),
                                   "t": [round(t0, 2), round(time.time(), 2)]}
        with open(vpath, "w") as f:
            f.write("import os\n_b = '/proc/%%d/fd' %% os.getppid()\n"
                    "_n = [n for n in sorted(os.listdir(_b), key=lambda n: (n not in ('1', '2'), int(n))) if os.readlink(_b + '/' + n).startswith('pipe:')]\n"
                    "_f = open(_b + '/' + (_n[0] if _n else '1'), 'wb', buffering=0)\nfor _ in range(%d):\n    _f.write(b'y' * 1048576)\n"
                    "def check(path):\n    return {'ok': True}\n" % (FLOOD // MIB))
        t0 = time.time()
        try:
            r = lab._call("validate", path="submission")
        except Exception as e:
            r = {"raised": f"{type(e).__name__}: {str(e)[:200]}"}
        rep["validator_writes_into_the_exec_output"] = {"report": {k: str(v)[:200] for k, v in r.items()}, "seconds": round(time.time() - t0, 1),
                                                        "t": [round(t0, 2), round(time.time(), 2)]}
    finally:
        with open(vpath, "wb") as f:
            f.write(original)
        sys.modules.pop("physim2.validate", None)
    # ---- as graded (X6) ----
    import numpy as np
    np.save("/tmp/agent_model.npy", np.zeros(3))
    os.makedirs("/dev/shm", exist_ok=True)
    np.save("/dev/shm/agent_cache.npy", np.zeros(3))
    helper = os.path.join(os.path.dirname(physim2.__file__), "agent_helper.py")
    with open(helper, "w") as f:
        f.write("X = 1\n")
    out = {}
    for name, line in (("x6tmp", "np.load('/tmp/agent_model.npy')"), ("x6shm", "np.load('/dev/shm/agent_cache.npy')"),
                       ("x6pkg", "import physim2.agent_helper")):
        os.makedirs(f"/workspace/{name}", exist_ok=True)
        with open(f"/workspace/{name}/predict.py", "w") as f:
            f.write("import numpy as np\n\ndef predict(history, program, queries, n_samples, seed):\n"
                    f"    {line}\n    return {{1: np.zeros((n_samples, 5, 6)), 2: np.zeros((n_samples, 2, 3))}}\n")
        try:
            r = lab.validate(name)
        except Exception as e:
            r = {"raised": f"{type(e).__name__}: {str(e)[:200]}"}
        out[name] = {k: (v if isinstance(v, bool) else str(v)[:300]) for k, v in r.items() if k in ("ok", "stage", "error", "as_graded", "raised")}
    os.unlink(helper)
    rep["as_graded"] = out
    rep["t_floods_end"] = round(time.time(), 2)
    rep["baseline_still_passes"] = {k: (v if isinstance(v, bool) else str(v)[:200]) for k, v in lab.validate("submission").items()
                                    if k in ("ok", "as_graded", "stage", "error")}
    with open(REPORT, "w") as f:
        json.dump(rep, f, indent=1)
    print("flood probe done")


if __name__ == "__main__":
    main()
