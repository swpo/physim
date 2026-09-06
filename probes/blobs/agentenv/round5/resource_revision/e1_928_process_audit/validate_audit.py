"""Static consistency checks only: one trace and the generated audit documents."""
from pathlib import Path
import hashlib
import json
import math
import re

root=Path.cwd()
out=root/'probes/blobs/agentenv/round5/resource_revision/e1_928_process_audit'
s=json.loads((out/'summary.json').read_text())
sc=json.loads((out/'scientific_summary.json').read_text())
checks={}
def check(name,value):
    assert value, name
    checks[name]=True
found=[]
with Path(s['scope']['source']).open() as f:
    for line in f:
        if s['scope']['trace_id'] not in line: continue
        row=json.loads(line)
        found.extend(t for t in row['traces'] if t['id']==s['scope']['trace_id'])
check('one_exact_trace',len(found)==1)
t=found[0]
sha=hashlib.sha256(json.dumps(t,sort_keys=True,separators=(',',':')).encode()).hexdigest()
check('selected_trace_content_unchanged',sha==s['scope']['selected_trace_sha256'])
check('exact_task',t['task']['data']['name']=='physim-BLOB2v2r2-E1#928')
completed=[c for c in t['calls'] if 'node'in c]
ids=[tc['id'] for c in completed for tc in t['nodes'][c['node']]['message'].get('tool_calls',[])]
check('sampled_tool_ids_unique',len(ids)==len(set(ids))==1484)
check('completed_model_count',len(completed)==s['accounting']['completed_model_calls']==1216)
check('model_requests_errors',len(t['calls'])==1239 and sum('error'in c for c in t['calls'])==23)
check('total_tool_count',sum(x['calls'] for x in s['tools'].values())==1484)
check('environment_tool_count',sum(x['calls'] for k,x in s['tools'].items() if k.startswith('mcp__probe__'))==1065)
u=s['accounting']['total_usage']
check('usage_input',u['input_tokens']==u['prompt_tokens']+u['cached_input_tokens']==121819324)
check('usage_total',u['total_tokens']==u['input_tokens']+u['completion_tokens']==123019175)
check('reasoning_is_not_added_again',u['reasoning_tokens']==153020 and u['reasoning_tokens']<u['completion_tokens'])
check('unknown_cost_and_cache_write_preserved',u['cache_write_tokens'] is None and u['billed_dollars'] is None)
check('science_same_trace',sc['trace_id']==t['id'])
check('mean_instance_skill',math.isclose(sum(s['scores']['instance_skills_full_precision'].values())/6,t['rewards']['skill']['score'],abs_tol=1e-12))
check('resource_policy_v2r2',s['resources']['policy']['id']=='v2r2')
check('no_resource_stop',not t['info']['physim']['resource_truncated'] and not t['info']['physim']['resource_stop'] and all(v==0 for v in t['info']['physim']['cap_hits'].values()))
r=s['ready_and_submission']
check('six_accepted_matching_submissions',len(r['submissions'])==6 and all(x['accepted'] and x['exact_match_to_workspace_payload'] for x in r['submissions']))
check('all_final_submission_flags',len(r['all_submitted_flags'])==6 and all(r['all_submitted_flags'].values()))
check('no_world_tool_requests_after_ready',r['world_tool_requests_after_ready']==[])
check('post_ready_env_turn_delta',s['resources']['persisted_meters']['turns']-s['resources']['time_to_ready']['turns']==7)
check('post_ready_sim_unchanged',s['resources']['persisted_meters']['sim_tu']==s['resources']['time_to_ready']['sim_tu']==11495)
check('closed_final_contexts',r['final_status_open_contexts']==[])
check('science_no_custom_simulator',all(not x['custom_dynamical_simulator_used'] for x in sc['instances'].values()))
check('L3F_within_base',sc['instances']['L3F']['last_target_time']==1189.72)
check('L3E_within_base',sc['instances']['L3E']['last_target_time']==2494.78)
check('dose_means_do_not_use_port2_template',all(not sc['instances'][k]['port2_template_used'] for k in ['L4','L4D']))
for p in out.glob('*.json'): json.loads(p.read_text())
check('all_output_json_parses',True)
md={p.name:p.read_text() for p in out.glob('*.md')}
refs={x for text in md.values() for x in re.findall(r'toolu_[A-Za-z0-9]+',text)}
check('markdown_tool_id_evidence_matches_trace',refs <= set(ids))
links=[link for text in md.values() for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text)]
check('local_markdown_links_exist',all((out/link).exists() for link in links if not link.startswith(('http://','https://','#'))))
patterns=[r'(?i)authorization\s*[:=]',r'(?i)bearer\s+[A-Za-z0-9+/=._-]{12,}',r'(?i)(?:api[_-]?key|access[_-]?token)\s*[:=]',r'\bsk-[A-Za-z0-9_-]{16,}',r'\bAKIA[0-9A-Z]{16}\b']
report_texts=[p.read_text() for p in out.iterdir() if p.suffix in ['.md','.json']]
check('no_credential_pattern_in_reports',not any(re.search(pattern,text) for text in report_texts for pattern in patterns))
result=dict(trace_id=t['id'],checks=checks,check_count=len(checks),all_passed=True,
            scope='Static read-only audit checks. No environment tests, episode code, simulations, or model calls were executed.',
            audited_tool_reference_count=len(refs))
(out/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
