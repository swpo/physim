from pathlib import Path
import json,hashlib
from science_counts import selected_trace, model_tools, saved_json_data, decode
line,index,t=selected_trace(); ws=t['info']['physim']['workspace']; out=Path(__file__).parent
source=Path.home()/"v3work/ops/recovery_20260905/eval_fable_r2/E2/traces.jsonl"
source_sha=hashlib.sha256(source.read_bytes()).hexdigest()
code=ws['app/models/predictor3.py']; codelines=code.splitlines()
print('PREDICTOR3')
for n,s in enumerate(codelines,1): print(f'{n}: {s}')
print('SAFE WORKSPACE FILES', [p for p in ws if p.startswith(('app/models/','app/notes/')) and not p.endswith('.sh')])
saved,hist=saved_json_data(t)
print('LITERAL DATA FILES')
for p,values in saved.items():
    if any(k in p.lower() for k in ('global','cont','emission','rms')):
        times=[]
        for v,ref in values:
            if 't' in v: times.append(v['t'])
            for st in v.get('steps',[]):
                if isinstance(st,dict) and 't' in st: times.append(st['t'])
        print(p,'records',len(values),'times',sorted(set(times))[:100])
print('INSTANCE DETAILS', json.dumps(t['info']['physim']['detail']['instances']))
for ni in (4013,5092,5114,5128,5131,5135):
    node=t['nodes'][ni]
    if node['message']['role']!='assistant': continue
    for tc in node['message'].get('tool_calls',[]):
        args=json.loads(tc['arguments'])
        print('EVIDENCE NODE',ni,'TOOL',tc['id'],tc['name'])
        if tc['name'] in ('Bash','Edit'):
            print(json.dumps(args,ensure_ascii=False)[:20000])
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_sha
