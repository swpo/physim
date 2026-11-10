"""tests_tcp -- the Lab protocol over TCP with a token (the transport for a host <-> container setup), ring world.
usage: python tests_tcp.py SCRATCH_DIR   (prints a JSON line; exit code 0 on success)"""
import json
import os
import socket
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_rollout as RR  # noqa: E402
from evaluator.lab_service import LabService, serve  # noqa: E402
from physim2.labclient import Lab, LabError  # noqa: E402


def main():
    run = os.path.join(sys.argv[1], "tcp")
    RR.prepare("ring", json.load(open(os.path.join(HERE, "configs", "probe_ring.json"))), run)
    ws, _, _ = RR.workspace(run, "tcp")
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    svc = LabService(os.path.join(run, "hidden"), os.path.join(run, "public"), ws, "tcp")
    threading.Thread(target=serve, args=(svc, f"tcp://127.0.0.1:{port}", "s3cret"), daemon=True).start()
    time.sleep(0.5)
    res = {}
    try:
        Lab(f"tcp://127.0.0.1:{port}", token="wrong").card()
        res["bad_token_rejected"] = False
    except LabError as e:
        res["bad_token_rejected"] = "bad token" in str(e)
    lab = Lab(f"tcp://127.0.0.1:{port}", token="s3cret")
    res["card_world"] = lab.card()["world"]
    res["experiment_shape"] = list(lab.experiment("a", 5).shape)
    res["ticks_used"] = lab.usage()["ticks_used"]
    ok = res["bad_token_rejected"] and res["card_world"] == "ring" and res["experiment_shape"] == [6, 6] and res["ticks_used"] == 6
    json.dump(dict(res, ok=ok), open(os.path.join(HERE, "results", "tcp_test.json"), "w"), indent=1)
    print(json.dumps(dict(res, ok=ok)))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
