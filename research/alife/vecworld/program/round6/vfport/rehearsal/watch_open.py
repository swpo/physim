"""watch_open -- write down every open of the files in ONE folder, by any process, for as long as a rehearsal runs.

Round 3, finding M3: the rehearsal's home folder holds a made-up `.prime/config.json`. This watcher asks the
kernel (inotify, Linux only) for every open, read and close of the files in that `.prime` folder and appends
one JSON line per event to --log. It is the rehearsal's proof that no process of the scripted route opens the
file, whatever language it is written in; a control at the end (the stock import of verifiers with the same
HOME) must produce events, or the watcher proved nothing.

It starts nothing, signals nothing, and removes nothing. It ends by itself when the file --stop-file appears
(the operator creates it), after writing a last line with its counts.

usage: python3 -B rehearsal/watch_open.py --folder SCRATCH/home/.prime --log SCRATCH/opens.jsonl --stop-file SCRATCH/watch.stop &
"""
import argparse
import ctypes
import json
import os
import select
import struct
import sys
import time

IN_ACCESS, IN_OPEN, IN_CLOSE_NOWRITE, IN_CLOSE_WRITE, IN_MODIFY = 0x1, 0x20, 0x10, 0x8, 0x2
NAMES = {IN_ACCESS: "read", IN_OPEN: "open", IN_CLOSE_NOWRITE: "close", IN_CLOSE_WRITE: "close after write", IN_MODIFY: "write"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--stop-file", required=True)
    a = ap.parse_args()
    if sys.platform != "linux":
        raise SystemExit("inotify is Linux only")
    libc = ctypes.CDLL(None, use_errno=True)
    fd = libc.inotify_init1(0o4000)                          # IN_NONBLOCK
    if fd < 0 or libc.inotify_add_watch(fd, os.fsencode(a.folder), IN_ACCESS | IN_OPEN | IN_CLOSE_NOWRITE | IN_CLOSE_WRITE | IN_MODIFY) < 0:
        raise SystemExit("inotify failed: " + os.strerror(ctypes.get_errno()))
    counts = {}
    with open(a.log, "a") as log:
        log.write(json.dumps({"watching": a.folder, "since_unix": time.time(), "pid": os.getpid()}) + "\n")
        log.flush()
        while not os.path.exists(a.stop_file):
            if not select.select([fd], [], [], 0.5)[0]:
                continue
            raw, i = os.read(fd, 65536), 0
            while i + 16 <= len(raw):
                _, mask, _, n = struct.unpack_from("iIII", raw, i)
                name = raw[i + 16:i + 16 + n].split(b"\0", 1)[0].decode(errors="replace")
                i += 16 + n
                for bit, word in NAMES.items():
                    if mask & bit:
                        counts[f"{word} {name or '(the folder)'}"] = counts.get(f"{word} {name or '(the folder)'}", 0) + 1
                        log.write(json.dumps({"t_unix": round(time.time(), 3), "event": word, "file": name or "(the folder)"}) + "\n")
                log.flush()
        log.write(json.dumps({"stopped_unix": time.time(), "counts": counts}) + "\n")


if __name__ == "__main__":
    main()
