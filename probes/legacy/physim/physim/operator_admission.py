"""Host-only operator admission control; never a task/scoring/resource policy.

A fence targets an exact evaluator PID + birth time + command hash. It is
checked only at a NEW tool-server process entry point. Existing imported
servers/active rollouts are unaffected. Missing or stale fences do nothing.
"""
from __future__ import annotations
import datetime, hashlib, json, os, pathlib, subprocess, sys

SCHEMA = "physim-operator-admission-v1"

class OperatorAdmissionClosed(RuntimeError):
    pass

def fence_directory():
    return pathlib.Path(os.environ.get("PHYSIM_OPERATOR_ADMISSION_DIR", str(pathlib.Path.home()/".config/physim/admission_fences")))

def process_identity(pid):
    env=dict(os.environ, LC_ALL="C")
    cp=subprocess.run(["ps","-p",str(int(pid)),"-o","lstart=","-o","command="], capture_output=True,text=True,timeout=3,env=env)
    if cp.returncode or not cp.stdout.strip(): return None
    parts=cp.stdout.strip().split(None,5)
    if len(parts)!=6: return None
    return {"pid":int(pid),"birth":" ".join(parts[:5]),"command_sha256":hashlib.sha256(parts[5].encode()).hexdigest(),"command":parts[5]}

def write_fence(identity, *, directory=None, reason="operator stop after current rollout", output_dir=None):
    directory=pathlib.Path(directory) if directory else fence_directory()
    directory.mkdir(parents=True,exist_ok=True)
    doc={"schema":SCHEMA,"parent_pid":identity["pid"],"parent_birth":identity["birth"],"parent_command_sha256":identity["command_sha256"],"created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"reason":reason,"output_dir":output_dir}
    path=directory/(str(identity["pid"])+".json"); tmp=path.with_suffix(".tmp")
    tmp.write_text(json.dumps(doc,indent=2)); tmp.chmod(0o600); tmp.replace(path)
    return path

def check_new_server_admission(*, parent_pid=None, directory=None, identity_reader=process_identity):
    pid=os.getppid() if parent_pid is None else int(parent_pid)
    directory=pathlib.Path(directory) if directory else fence_directory()
    path=directory/(str(pid)+".json")
    if not path.is_file(): return
    doc=json.loads(path.read_text())
    if doc.get("schema")!=SCHEMA: raise RuntimeError("unrecognized operator admission fence")
    actual=identity_reader(pid)
    if actual is None: return
    if (doc.get("parent_pid"),doc.get("parent_birth"),doc.get("parent_command_sha256")) != (actual["pid"],actual["birth"],actual["command_sha256"]):
        return  # PID reuse or different evaluator: do not affect unrelated work
    event={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"server_pid":os.getpid(),"parent_pid":pid,"classification":"not_admitted_by_operator","reason":doc.get("reason"),"output_dir":doc.get("output_dir")}
    fd=os.open(str(directory/"events.jsonl"),os.O_WRONLY|os.O_APPEND|os.O_CREAT,0o600)
    try: os.write(fd,(json.dumps(event)+"\n").encode())
    finally: os.close(fd)
    raise OperatorAdmissionClosed("operator requested no new rollouts for this evaluator")

def main_guard():
    try: check_new_server_admission()
    except OperatorAdmissionClosed as exc:
        print("PHYSIM_OPERATOR_ADMISSION_CLOSED: "+str(exc),file=sys.stderr,flush=True)
        raise SystemExit(78)
