from pathlib import Path
import argparse, json, re
from collections import Counter
TRACE_ID = "ae982494a72144c186f58a687a99cd33"
TASK = "physim-BLOB2v2r2-E2#942"
TRACE_PATH = Path.home()/"v3work/ops/recovery_20260905/eval_fable_r2/E2/traces.jsonl"
OUTDIR = Path(__file__).resolve().parent

def selected_trace():
    for line_num, raw in enumerate(TRACE_PATH.open(), 1):
        if TRACE_ID not in raw: continue
        record=json.loads(raw)
        for index,trace in enumerate(record.get("traces",[])):
            if trace.get("id")==TRACE_ID:
                assert trace.get("is_completed") is True
                assert trace["task"]["data"]["name"]==TASK
                return line_num,index,trace
    raise RuntimeError("Exact completed trace not found")

def model_tools(trace):
    seen_nodes=set(); seen_tools=set()
    for call in trace["calls"]:
        if "node" not in call: continue
        ni=call["node"]
        if ni in seen_nodes: continue
        seen_nodes.add(ni)
        node=trace["nodes"][ni]
        if not node.get("sampled"): continue
        for tool in node["message"].get("tool_calls",[]):
            tid=tool["id"]
            if tid in seen_tools: continue
            seen_tools.add(tid)
            try: args=json.loads(tool["arguments"])
            except (ValueError,TypeError): args=tool["arguments"]
            yield ni,node,tool,args

def safe_name(name):
    return name.startswith(("app/models/","app/notes/")) and not name.endswith(".sh") and not re.search(r"(?:secret|credential|token|password|\.env|private.?key|launch\.sh)",name,re.I)

def safe_text(text):
    return not re.search(r"(?:launch\.sh|api[_ -]?key|password|secret|credential|BEGIN.*PRIVATE KEY)",text,re.I)

def response_for(trace, tid):
    for ri,node in enumerate(trace["nodes"]):
        m=node["message"]
        if m.get("role")=="tool" and m.get("tool_call_id")==tid:
            return ri,node,m.get("content")
    raise AssertionError("Missing result for "+tid)

def decode(content):
    for _ in range(5):
        if isinstance(content,str):
            try: content=json.loads(content)
            except (ValueError,TypeError): return None
        elif isinstance(content,dict) and isinstance(content.get("result"),str) and content["result"].lstrip().startswith(("{","[")):
            content=content["result"]
        else: return content
    return content

def saved_json_data(trace):
    """Parse recorded literal data saves only. Never execute stored code."""
    saved={}; histories={}
    for ni,n,to,args in model_tools(trace):
        chunks=[]
        if to["name"]=="Write" and args.get("file_path", "").startswith("/app/data/"):
            chunks=[(args["file_path"].lstrip("/"),args["content"],False,"content",1)]
        elif to["name"]=="Bash":
            c=args.get("command","")
            pattern=r"cat\s*(>>|>)\s*['\"]?(/app/data/[^\s'\";]+)['\"]?\s*<<\s*['\"]?(\w+)['\"]?\n"
            for m in re.finditer(pattern,c):
                end=re.search(r"(?m)^"+re.escape(m.group(3))+r"\s*$",c[m.end():])
                if not end: continue
                body=c[m.end():m.end()+end.start()]
                chunks.append((m.group(2).lstrip("/"),body,m.group(1)==">>","command",c[:m.end()].count("\n")+1))
        for path,content,append,field,lineno in chunks:
            if not path.endswith((".json",".jsonl")): continue
            raw_items=content.splitlines() if path.endswith(".jsonl") else [content]
            rows=[]
            for j,raw in enumerate(raw_items):
                obj=decode(raw)
                if not isinstance(obj,dict): continue
                rows.append((obj,dict(path=path,node_index=ni,tool_call_id=to["id"],argument_field=field,line_start=lineno+j,line_end=lineno+j)))
            if not rows: continue
            histories.setdefault(path,[]).extend(rows)
            if append: saved.setdefault(path,[]).extend(rows)
            else: saved[path]=rows
    return saved,histories

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("mode",choices=["inventory","tools","artifact","node","search","result","tool","digest","delegates","data_inventory"])
    ap.add_argument("query",nargs="?",default="")
    ap.add_argument("--lo",type=int,default=1); ap.add_argument("--hi",type=int,default=300)
    a=ap.parse_args(); line,index,t=selected_trace(); ws=t["info"]["physim"]["workspace"]
    if a.mode=="inventory":
        print(json.dumps(dict(trace_id=TRACE_ID,task=TASK,line=line,index=index,node_count=len(t["nodes"]),call_count=len(t["calls"]),keys=list(t),metrics=t["metrics"],workspace=[dict(path=p,chars=len(v),lines=len(v.splitlines())) for p,v in ws.items() if safe_name(p)],tool_counts=Counter(x[2]["name"] for x in model_tools(t))),indent=2))
    elif a.mode=="data_inventory":
        counts=Counter(); ranges={}; fails=[]; writes=[]
        for ni,n,to,args in model_tools(t):
            if to["name"].endswith("__read"):
                typ="base" if args.get("ctx")=="base" else "fork"
                try: ri,rn,c=response_for(t,to["id"])
                except AssertionError:
                    counts[(typ,"missing_response")]+=1; continue
                d=decode(c)
                counts[(typ,"calls")]+=1
                if isinstance(d,dict) and d.get("steps"):
                    counts[(typ,"parseable_step_calls")]+=1
                    counts[(typ,"steps")]+=len(d["steps"])
                    ranges.setdefault(typ,set()).update(st["t"] for st in d["steps"])
                elif len(fails)<4: fails.append(dict(node=ri,chars=len(c),prefix=c[:180]))
            if to["name"]=="Write" and args.get("file_path","").startswith("/app/data/"):
                d=decode(args["content"]); st=d.get("steps",[]) if isinstance(d,dict) else []
                writes.append(dict(node=ni,tid=to["id"],path=args["file_path"],n=len(st),time_range=[st[0]["t"],st[-1]["t"]] if st else None))
        print(json.dumps(dict(counts={str(k):v for k,v in counts.items()},ranges={k:dict(n=len(v),first=min(v),last=max(v)) for k,v in ranges.items()},unparsed_examples=fails,writes=writes),indent=2))
    elif a.mode=="artifact":
        path="app/models/"+a.query
        assert safe_name(path)
        content=ws[path]
        if not safe_text(content): raise ValueError("Sensitive text excluded")
        lines=content.splitlines()
        for i in range(a.lo-1,min(a.hi,len(lines))): print(f"{path}:{i+1}: {lines[i]}")
    elif a.mode=="tools":
        for ni,n,to,args in model_tools(t):
            if not a.lo<=ni<=a.hi: continue
            if a.query and not re.search(a.query,to["name"]+json.dumps(args),re.I): continue
            text=json.dumps(args)
            if not safe_text(text):
                text="[sensitive command omitted]"
            if to["name"]=="Bash" and ("global_stats" in text and "EOF" in text and "cat >>" in text): text=args.get("description", "")+" [saved global data omitted]"
            if to["name"].endswith("__submit"): text=json.dumps({k:v for k,v in args.items() if k!="payload"})+" [payload omitted]"
            if to["name"]=="Write" and ("/data/" in args.get("file_path","") or "/sub_" in args.get("file_path","")): text=json.dumps({k:v for k,v in args.items() if k!="content"})+" [data omitted]"
            print(ni,to["id"],to["name"],text[:1200])
    elif a.mode=="node":
        for ni in map(int,a.query.split(",")):
            node=t["nodes"][ni]; m=node["message"]
            print("NODE",ni,"sampled",node.get("sampled"),"timestamp",node.get("timestamp"),"role",m.get("role"),"tid",m.get("tool_call_id"))
            content=m.get("content")
            if not isinstance(content,str): content=json.dumps(content)
            if not safe_text(content): content="[sensitive text excluded]"
            if any(x in content for x in ['"fields":','"readings":','"frame":']):
                print("[sensor-bearing content omitted; inspect summary]")
            else:
                lines=content.splitlines()
                for i in range(a.lo-1,min(a.hi,len(lines))): print(f"{i+1}: {lines[i]}")
    elif a.mode in ("result","tool"):
        matches=[row for row in model_tools(t) if row[2]["id"]==a.query]
        ni,n,to,args=matches[0]
        if a.mode=="result":
            ri,rn,content=response_for(t,to["id"])
            print("NODE",ri,"TOOL",to["id"],"RESPONSE TO NODE",ni)
        else:
            print("NODE",ni,"TOOL",to["id"],to["name"])
            content=args.get("command",args.get("content",json.dumps(args)))
        if not isinstance(content,str): content=json.dumps(content)
        assert safe_text(content)
        for i,line in enumerate(content.splitlines(),1):
            if a.lo<=i<=a.hi: print(f"{i}: {line}")
    elif a.mode in ("digest","delegates"):
        for ni,n,to,args in model_tools(t):
            if not a.lo<=ni<=a.hi: continue
            if a.mode=="delegates":
                if to["name"]!="Agent": continue
                ri,rn,content=response_for(t,to["id"])
                print(ni,to["id"],args.get("description"),"background",args.get("run_in_background"),"result_node",ri)
                print("  ",args.get("prompt","")[:550].replace("\n"," "))
            elif to["name"]=="Bash":
                text=args.get("description","")
                if a.query and not re.search(a.query,text+args.get("command",""),re.I): continue
                print(ni,to["id"],text)
            elif to["name"] in ("Write","Edit"):
                p=args.get("file_path","")
                if "/models/" not in p and "/notes/" not in p: continue
                print(ni,to["id"],to["name"],p)
    elif a.mode=="search":
        p=re.compile(a.query,re.I)
        for ni,node in enumerate(t["nodes"]):
            if not a.lo<=ni<=a.hi: continue
            m=node["message"]
            content=m.get("content")
            if not isinstance(content,str): continue
            if not safe_text(content): continue
            matched=[(i,line[:180]) for i,line in enumerate(content.splitlines(),1) if p.search(line)]
            if matched: print(ni,m.get("role"),m.get("tool_call_id"),matched[:15])

if __name__=="__main__": main()
