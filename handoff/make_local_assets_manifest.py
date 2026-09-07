"""Inventory migration inputs without simulations, archives extraction, or launcher reads.
Default is metadata-only. --hash-inputs streams the four development caches and
small truth/trace files. Multi-GB campaign archives are NEVER rehashed here.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, platform, shutil, time
ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "LOCAL_ASSETS.json"
HOME = Path.home()
CACHE = ROOT / "probes/blobs/agentenv/cache"

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024), b""):
            h.update(b)
    return h.hexdigest()

def entry(path, role, hash_it=False, expected=None, **more):
    p = Path(path)
    portable = str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p).replace(str(HOME), "~", 1)
    row = {"path": portable, "role": role, "exists":p.exists(), **more}
    if p.exists():
        row["kind"] = "directory" if p.is_dir() else "file"
        row["bytes"] = p.stat().st_size if p.is_file() else None
        row["mtime_utc"] = datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()
        if hash_it and p.is_file(): row["sha256_now"] = digest(p)
    if expected:
        row["recorded_sha256"] = expected
        row["sha256_matches_record"] = row.get("sha256_now") == expected if "sha256_now" in row else None
    return row

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hash-inputs",action="store_true")
    args=ap.parse_args(); start=time.perf_counter()
    rows=[]
    e2e=json.loads((ROOT/"probes/blobs/agentenv/round6/physics/p6g8_033/evidence.json").read_text())
    known={r["path"]:r["sha256"] for r in e2e["provenance"]}
    for world,seed in (("p4g2_044",928),("p6g8_033",942)):
        for suffix,role in ((".npz","base full-field record; required to reproduce physics analysis"),("_branches.npz","existing common-state/RNG control and source branches")):
            p=CACHE/f"{world}_s{seed}{suffix}"
            rows.append(entry(p,role,args.hash_inputs,known.get(str(p.relative_to(ROOT))),copy_for="same-machine session: already present; new machine: copy securely if analysis is needed"))
        p=CACHE/"round5"/f"r5_{world}_s{seed}_truth.npz"
        rows.append(entry(p,"frozen R5 sensor truth; needed for absolute-score reproduction",args.hash_inputs,known.get(str(p.relative_to(ROOT)))))
    trace_specs=(("E1","0bdd699154ee4e1d96aac4e0961bc11d","29392ad517806a7743c592b0f527241e23a7128d189c70b050b54c0792756b81"),("E2","ae982494a72144c186f58a687a99cd33","a9e4fb4c1c610eba8dd233061a9f76a11f3cd64cccb62b7c7192acd5990588f9"))
    for menu,tid,thash in trace_specs:
        p=HOME/"v3work/ops/recovery_20260905/eval_fable_r2"/menu/"traces.jsonl"
        rows.append(entry(p,"raw local rollout archive incl submitted payloads; not committed",args.hash_inputs,audited_completed_trace_id=tid,selected_trace_sha256_from_audit=thash,warning="select exact nested trace ID; whole-file hash includes later unscored/canceled records; do not mix cohorts"))
    for island,size,sha in ((1,7526611213,"7ef7e373677750b16cef373623e1b6bbecd400cea312ba359a940fd5fe3f40c3"),(2,7667929517,"cb00bc78b38c7edf28cbb0a6128b721eec5a345810b26460f390992f72a68a81")):
        p=HOME/f"v3work/isl{island}_final2.tgz"
        r=entry(p,"terminated v3 campaign final archive; use selected-member reads ONLY",False,sha,recorded_bytes=size,hash_provenance="previous full integrity verification; not rehashed by this migration inventory")
        r["bytes_match_record"]=r.get("bytes")==size
        rows.append(r)
        rows.append(entry(HOME/f"v3work/harvest2/v3cont-{island}/isl{island}/out","selected harvested metadata/films; no full archive extraction needed"))
    for relative,role in (("v3work/ops/recovery_20260905/state.json","historical operator state; current scientific decisions copied into repo handoff; contents not exported"),("v3work/round6/publish_receipt.log","R6 c06b2fb publication receipt"),(".venvs/bk3/bin/python","existing blobkit/matplotlib science interpreter; not portable as a copied binary")):
        rows.append(entry(HOME/relative,role))
    rows.append(entry(ROOT/".venv/bin/python","project interpreter used for runner/tests/audits"))
    cached_names=[]
    if CACHE.exists():
        cached_names=[{"path":str(p.relative_to(ROOT)),"bytes":p.stat().st_size} for p in sorted(CACHE.glob("*.npz"))]
    truth_names=[{"path":str(p.relative_to(ROOT)),"bytes":p.stat().st_size} for p in sorted((CACHE/"round5").glob("*_truth.npz"))]
    report={"schema":"physim-session-local-assets-v1","created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"repo_root_at_snapshot":str(ROOT),"hash_mode":"stream selected cache/truth/trace inputs" if args.hash_inputs else "metadata only", "assets":rows,"other_base_and_branch_caches":cached_names,"all_assembled_round5_truth_files":truth_names,"disk_free_bytes":shutil.disk_usage(ROOT).free,"seconds":time.perf_counter()-start,"scope":["No file in an old launch .sh is opened or copied.","No API config, secrets, raw operator state, or full trace contents exported.","No model, simulator, truth generation, pod, archive extraction, or environment install.","Directories are presence-checked, not recursively copied.","A new-machine clone lacks these local inputs; missing inputs are not permission to rebuild worlds or run evals."]}
    OUT.write_text(json.dumps(report,indent=2)+"\n")
    mismatches=[r["path"] for r in rows if r.get("sha256_matches_record") is False or r.get("bytes_match_record") is False]
    print(json.dumps({"path":str(OUT),"assets":len(rows),"hashes_computed":sum("sha256_now" in r for r in rows),"mismatches":mismatches,"seconds":report["seconds"]},indent=2))
    raise SystemExit(1 if mismatches else 0)
if __name__=="__main__":main()
