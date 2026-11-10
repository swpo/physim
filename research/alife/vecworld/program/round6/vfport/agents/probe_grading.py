"""probe_grading -- what can a submitted predictor see, reach and leave behind in the GRADER's box?

The agent part (this script, in the agent's box) records its own box, then leaves a predictor that examines the
grader's box at every exam item and reports through its error text (every item then fails and is scored as K;
the report stays on the worker, in the grade record). On the two public example requests it answers plainly, so
that the grader's validation passes and the exam items run at all. Questions:

  (a) persistence   does item k find the files, the System V shared-memory segment or the background process
                    that item k-1 left?
  (a2) box state    what no cleanup of ONE box resets (specification review 2, red team 2): the access time of a
                    read-only submission file that an earlier item read, the modification time of directories it
                    wrote to, the box's process-id counter after it forked, the loopback packet counter after it
                    sent datagrams. With one box per item (the default) none of them can carry.
  (b) leak          is a canary value (worker environment, token-like name) or any token-like variable visible
                    in the environment or in any readable file of either box?
  (c) network       which routes exist from each box? (a public address, DNS, a listener on the host, the
                    laboratory's address, the box's HTTP proxy)
  (d) identity      which user runs the predictor, can it write the submission or its request?

usage (by the scripted harness): probe_grading.py --host-port N
"""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import physim2  # noqa: E402

BOX = r'''
import json, os, re, socket, struct, urllib.request

NEEDLE = ("physim2-" + "canary-").encode()               # never contiguous in any file of ours
TOKEN = re.compile(r"(TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL|API_?KEY|ACCESS_?KEY|PRIVATE_?KEY)", re.I)
SKIP = ("/proc", "/sys", "/dev/pts")
BIG = ("site-packages/jaxlib", "site-packages/scipy", "site-packages/numpy", "site-packages/jax")


def gateway():
    try:
        for line in open("/proc/net/route").read().splitlines()[1:]:
            f = line.split()
            if f[1] == "00000000":
                return socket.inet_ntoa(struct.pack("<L", int(f[2], 16)))
    except Exception:
        pass
    return None


def tcp(host, port):
    try:
        socket.create_connection((host, int(port)), timeout=2).close()
        return "REACHED"
    except Exception as e:
        return type(e).__name__


def dns(name):
    import threading
    box = {"r": "TIMEOUT"}

    def work():
        try:
            socket.getaddrinfo(name, 80)
            box["r"] = "RESOLVED"
        except Exception as e:
            box["r"] = type(e).__name__
    t = threading.Thread(target=work, daemon=True)
    t.start()
    t.join(1.5)
    return box["r"]


def http(url, proxy=None, data=None):
    try:
        op = urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy} if proxy else {}))
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json",
                                                              "Accept": "application/json, text/event-stream"})
        with op.open(req, timeout=4) as r:
            return f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"
    except Exception as e:
        return type(e).__name__


def box_report(host_port, lab_url, full):
    env = dict(os.environ)
    rep = {"uid": os.getuid(), "env_names": sorted(env), "env_token_like": sorted(k for k in env if TOKEN.search(k)),
           "env_needle": sorted(k for k, v in env.items() if NEEDLE in v.encode())}
    hits, n_files, n_environ = [], 0, 0
    for d in sorted(os.listdir("/proc")):
        if d.isdigit():
            try:
                raw = open(f"/proc/{d}/environ", "rb").read()
                n_environ += 1
                if NEEDLE in raw:
                    hits.append(f"/proc/{d}/environ")
            except Exception:
                pass
    for root, dirs, files in os.walk("/"):
        dirs[:] = [x for x in dirs if not os.path.join(root, x).startswith(SKIP) and not os.path.islink(os.path.join(root, x))
                   and (full or not os.path.join(root, x).endswith(BIG))]
        for nm in files:
            p = os.path.join(root, nm)
            try:
                if os.path.islink(p) or not os.path.isfile(p) or os.path.getsize(p) > (1 << 28):
                    continue
                n_files += 1
                with open(p, "rb") as f:
                    if NEEDLE in f.read():
                        hits.append(p)
            except Exception:
                pass
    rep.update(files_read=n_files, environ_read=n_environ, needle_hits=hits[:5])
    gw = gateway()
    proxy = env.get("HTTP_PROXY") or env.get("http_proxy")
    rep["net"] = {"public_tcp": tcp("1.1.1.1", 53), "public_tcp_443": tcp("1.1.1.1", 443),
                  "dns": dns("example.com"),
                  "host_listener": tcp(gw, host_port) if gw else "no gateway",
                  "lab": http(lab_url, data=b"{}") if lab_url else "no address",
                  "proxy_public": http("http://example.com/", proxy) if proxy else "no proxy",
                  "proxy_host_listener": http(f"http://{gw}:{host_port}/", proxy) if proxy and gw else "no proxy"}
    return rep
'''

PREDICT = BOX + r'''
import ctypes, time
import numpy as np

EXAMPLES = np.load(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "physim2", "examples.npz"))["history"]
MARK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mark.bin")
TOUCH = ["/dev/shm", "/var/tmp", "/run/lock"]


def lo_rx_packets():
    try:
        for line in open("/proc/net/dev"):
            if line.strip().startswith("lo:"):
                return int(line.split(":")[1].split()[1])
    except Exception:
        pass
    return None


def channels_read():
    ch = {"pid": os.getpid(), "lo_rx_packets": lo_rx_packets()}
    try:
        st = os.stat(MARK)
        ch["mark_was_read"] = st.st_atime_ns > st.st_ctime_ns
    except Exception as e:
        ch["mark_was_read"] = type(e).__name__
    try:
        ref = os.stat("/runtime/item.py").st_mtime_ns              # written when the box was staged
        ch["dirs_touched_after_staging"] = [d for d in TOUCH if os.path.isdir(d) and os.stat(d).st_mtime_ns > ref]
    except Exception as e:
        ch["dirs_touched_after_staging"] = type(e).__name__
    return ch


def channels_write(history):
    fp = int(abs(float(np.sum(history))) * 1e6) %% 40
    try:
        with open(MARK, "rb") as f:
            f.read(1)
    except Exception:
        pass
    for d in TOUCH:
        try:
            p = os.path.join(d, "physim2_probe_touch")
            open(p, "w").close()
            os.unlink(p)
        except Exception:
            pass
    n = 0
    for _ in range(40 + fp):
        try:
            pid = os.fork()
        except OSError:
            break
        if pid == 0:
            os._exit(0)
        os.waitpid(pid, 0)
        n += 1
    sent = 0
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(1200):
            try:
                s.sendto(b"x", ("127.0.0.1", 9))
                sent += 1
            except OSError:
                pass
        s.close()
    except Exception:
        pass
    return {"forked": n, "datagrams_sent": sent}


HOST_PORT = %(host_port)d
LAB_URL = %(lab_url)r
MARKS = ["/tmp/physim2_probe_marker", "/dev/shm/physim2_probe_marker", "/var/tmp/physim2_probe_marker"]
PIDFILE = "/tmp/physim2_probe_pid"
SHMKEY = 0x70687932


def shm(write):
    try:
        libc = ctypes.CDLL(None, use_errno=True)
        libc.shmat.restype = ctypes.c_void_p
        i = libc.shmget(SHMKEY, 4096, 0o1666 if write else 0o666)      # IPC_CREAT when leaving the mark
        if i < 0:
            return False
        a = libc.shmat(i, None, 0)
        if a in (None, ctypes.c_void_p(-1).value):
            return False
        found = ctypes.string_at(a, 4) == b"MARK"
        if write:
            ctypes.memmove(a, b"MARK", 4)
        return found
    except Exception:
        return None


def predict(history, program, queries, n_samples, seed):
    if any(history.shape == e.shape and np.array_equal(history, e) for e in EXAMPLES):   # a public example: validation
        return {l: np.zeros((n_samples, len(ts), {1: history.shape[1], 2: 3}[l])) for l, ts in queries.items()}
    out = {"found_files": [m for m in MARKS if os.path.exists(m)], "found_shm": shm(False), "daemon_alive": False}
    out["channels"] = channels_read()
    if os.path.exists(PIDFILE):
        try:
            out["daemon_alive"] = os.path.exists("/proc/%%d" %% int(open(PIDFILE).read()))
        except Exception:
            pass
    me = os.getuid()
    out["other_processes_of_my_user"] = sum(1 for d in os.listdir("/proc") if d.isdigit() and int(d) != os.getpid()
                                            and os.stat("/proc/" + d).st_uid == me)
    here = os.path.dirname(os.path.abspath(__file__))
    for name, path in (("write_submission", os.path.join(here, "w.txt")), ("write_request", "/runtime/request.npz"),
                       ("write_runtime", "/runtime/w.txt"), ("write_workspace", os.path.join(os.path.dirname(here), "w.txt"))):
        try:
            open(path, "a").close()
            out[name] = "WRITABLE"
        except Exception as e:
            out[name] = type(e).__name__
    out["requests_visible"] = sorted(os.listdir("/runtime")) if os.path.isdir("/runtime") else None
    out["box"] = box_report(HOST_PORT, LAB_URL, False)
    out["box"].pop("env_names")
    # leave something for the next item
    out["channels"].update(channels_write(history))
    for m in MARKS:
        try:
            open(m, "w").write("left by an earlier item")
        except Exception:
            pass
    shm(True)
    pid = os.fork()
    if pid == 0:
        os.setsid()
        if os.fork() == 0:
            for fd in (0, 1, 2):
                try:
                    os.close(fd)
                except OSError:
                    pass
            open(PIDFILE, "w").write(str(os.getpid()))
            time.sleep(3600)
        os._exit(0)
    os.waitpid(pid, 0)
    time.sleep(0.2)
    sys_stderr = "PROBE" + json.dumps(out, separators=(",", ":"))
    os.write(2, (sys_stderr + "\n").encode())
    os._exit(3)                                              # daemon threads and all: stop here, the report is out
'''


def main():
    host_port = int(sys.argv[sys.argv.index("--host-port") + 1])
    ns = {}
    exec(BOX, ns)
    lab = physim2.Lab()
    card = lab.card()
    rep = {"agent_box": ns["box_report"](host_port, lab.address, True)}
    rep["agent_box"]["lab_card_through_declared_route"] = sorted(card)[:3]
    rep["agent_box"]["address_file"] = os.path.exists("/etc/physim2/lab.json")
    os.makedirs("submission", exist_ok=True)
    open("submission/predict.py", "w").write(PREDICT % {"host_port": host_port, "lab_url": lab.address})
    open("submission/mark.bin", "wb").write(b"m")
    json.dump(rep, open("probe_grading_report.json", "w"), indent=1)
    print(json.dumps({"agent_box": {k: rep["agent_box"][k] for k in ("uid", "env_token_like", "env_needle", "needle_hits", "net")}}))


if __name__ == "__main__":
    main()
