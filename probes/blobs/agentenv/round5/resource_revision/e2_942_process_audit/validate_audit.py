"""Static consistency checks for the E2 audit, not environment tests.
Runs only local parsing, hashes, schema aggregation, and array-shape arithmetic.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import math
import re
from verifiers.v1.types import Usage
from audit_counts import select_trace, parse_rows, canonical, TARGET, TASK, OUT, SOURCE, WORLD_TOOLS


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shape(x):
    if not isinstance(x, list):
        assert isinstance(x, (int, float)) and math.isfinite(x)
        return []
    assert x
    child = shape(x[0])
    assert all(shape(v) == child for v in x)
    return [len(x)] + child


def leaves(x):
    if isinstance(x, list):
        for v in x:
            yield from leaves(v)
    else:
        yield x


def main():
    trace,scope = select_trace()
    rows,results,completed = parse_rows(trace)
    s=json.loads((OUT/'summary.json').read_text())
    state=json.loads((OUT/'experiment_summary.json').read_text())
    science=json.loads((OUT/'scientific_summary.json').read_text())
    pair=json.loads((OUT/'paired_summary.json').read_text())
    phy=trace['info']['physim']; nodes=trace['nodes']; calls=trace['calls']
    ready=next(r for r in rows if r['tool']=='mcp__probe__ready')
    final=next(r for r in reversed(rows) if r['tool']=='mcp__probe__status' and isinstance(r['result'],dict))
    probe=[r for r in rows if r['tool'].startswith('mcp__probe__')]
    errors=[c for c in calls if 'error' in c]
    u=Usage.aggregate(Usage.model_validate(c['usage']) for _,c in completed)
    bytool=Counter(r['tool'] for r in rows)
    known_ids={r['tool_call_id'] for r in rows}
    checks={}
    checks['one_exact_nested_trace']=scope['selected_trace_sha256']==s['scope']['selected_trace_sha256']
    checks['exact_task']=trace['task']['data']['name']==TASK
    checks['whole_source_hash_unchanged']=digest(SOURCE)==s['scope']['source_sha256_at_read']==s['scope']['source_sha256_after_counting']
    checks['source_bytes_unchanged']=SOURCE.stat().st_size==s['scope']['source_bytes_at_read']==11116033
    checks['nested_and_outer_ok']=trace['is_completed'] and trace['ok'] and scope['outer_ok'] is True
    checks['scored_and_readied']=phy['score_status']=='scored' and trace['metrics']['readied']==1 and trace['stop_condition']=='agent_completed'
    checks['v2r2_policy_and_resident_limit']=phy['resource_policy']['id']=='v2r2' and phy['resource_policy']['resident_forks']==8
    checks['zero_caps_no_resource_stop']=not any(phy['cap_hits'].values()) and not phy['resource_truncated'] and not phy['resource_stop'] and not trace['errors']
    checks['sampled_call_node_bijection']=len(completed)==2218==sum(bool(n.get('sampled')) for n in nodes)
    checks['request_records_and_errors']=len(calls)==2258 and len(errors)==40 and len(completed)+len(errors)==len(calls)
    checks['error_status_counts']=Counter(c['error'].get('status_code') for c in errors)=={429:38,400:2}
    checks['error_usage_unavailable']=all('usage' not in c or c['usage'] is None for c in errors)
    checks['sampled_tool_ids_unique']=len(known_ids)==len(rows)==2336
    checks['unique_vs_copied_tool_results']=len(results)==2319 and sum(n['message']['role']=='tool' for n in nodes)==2357 and sum(max(0,len(r['result_node_occurrences'])-1) for r in rows)==38
    checks['duplicated_result_content_validated']=s['accounting']['repeated_result_contents_identical'] is True
    checks['separate_calls_and_environment_turns']=len(probe)==1300 and phy['meters']['turns']==1023
    checks['tool_outcomes_match_independent_state_counts']=all(bytool['mcp__probe__'+k]==v['issued'] for k,v in state['tools'].items())
    checks['timeouts_and_missing_counts']=sum(r['outcome']=='tool_timeout' for r in probe)==266 and sum(r['result_node'] is None for r in probe)==11 and sum(r['result_node'] is None for r in rows)==17
    checks['usage_aggregate_matches_schema']=all(s['accounting']['total_usage'][k]==v for k,v in u.model_dump(exclude_none=True).items())
    checks['usage_input_and_total']=u.input_tokens==219917684 and u.total_tokens==222182761
    checks['reasoning_not_added_again']=u.total_tokens==u.prompt_tokens+u.cached_input_tokens+u.completion_tokens and u.reasoning_tokens==97241
    checks['unknown_billing_and_cache_writes_preserved']=u.cost is None and s['accounting']['total_usage']['billed_dollars'] is None and s['accounting']['total_usage']['cache_write_tokens'] is None
    checks['auxiliary_count_unknown']=trace['extra_usage']==[] and s['accounting']['auxiliary_requests']['count_tokens_requests'] is None
    checks['two_missing_finish_reasons_kept']=[i for i,c in completed if c.get('finish_reason') is None]==[1919,1922]
    checks['no_world_requests_on_or_after_ready_response']=not any(r['tool'] in WORLD_TOOLS and r['timestamp']>=ready['timestamp'] for r in rows)
    checks['no_recorded_late_pre_ready_results']=not any(r['timestamp']<ready['timestamp'] and r['result_timestamp'] is not None and r['result_timestamp']>ready['timestamp'] for r in rows)
    submissions=[r for r in rows if r['tool']=='mcp__probe__submit']
    payload_checks=[]
    for r in submissions:
        p=json.loads(r['args']['payload']) if isinstance(r['args']['payload'],str) else r['args']['payload']
        fn='app/models/sub_'+r['args']['instance'].replace('@','_')+'.json'
        saved=json.loads(phy['workspace'][fn])
        shp=r['result']['shape']
        payload_checks.append(p==saved and r['result'].get('ok') is True and shape(p['mean'])==shp and shape(p['sigma'])==shp and all(v>0 for v in leaves(p['sigma'])))
    checks['six_accepted_matching_finite_shape_valid_payloads']=len(submissions)==6 and all(payload_checks)
    checks['accepted_order']=[r['args']['instance'] for r in submissions]==['L3S@i1','L1@i1','L2@i1','L3F@i1','L4D@i1','L4@i1']
    checks['final_phase_flags_contexts']=final['result']['phase']=='revealed' and len(final['result']['submitted'])==6 and all(final['result']['submitted'].values()) and final['result']['contexts']==[]
    checks['post_ready_turns_simulation_metadata']=phy['meters']['turns']-phy['time_to_ready']['turns']==7 and phy['meters']['sim_tu']==phy['time_to_ready']['sim_tu']==14655
    checks['episode_skill_is_six_instance_mean']=abs(sum(v for k,v in trace['metrics'].items() if k.startswith('skill_'))/6-trace['rewards']['skill']['score'])<1e-14
    checks['independent_state_same_trace_hash']=state['scope']['trace_id']==TARGET and state['scope']['selected_trace_sha256']==scope['selected_trace_sha256']
    science_trace=science.get('trace_id',science.get('scope',{}).get('trace_id'))
    checks['scientific_analysis_same_trace']=science_trace==TARGET
    checks['paired_only_two_completed_cases']=set(pair['cases'])=={'E1_928','E2_942'} and pair['cases']['E2_942']['trace_id']==TARGET
    checks['E1_audit_inputs_unchanged']=all(digest(OUT.parent/path)==value for path,value in pair['audit_input_hashes'].items())
    inst=phy['detail']['instances']
    checks['L3F_targets_in_base']=all(inst['L3F']['t_a']+h<2500 for h in inst['L3F']['horizons'])
    windows=[[inst['L3S']['t_a']+e-inst['L3S']['window_tu'],inst['L3S']['t_a']+e] for e in inst['L3S']['epochs']]
    checks['L3S_second_window_outside_base_within_saved_global_span']=windows[0][1]<2500 and windows[1][0]>2500 and 2525<windows[1][0]<windows[1][1]<2900
    json_outputs=list(OUT.glob('*.json'))
    checks['all_output_json_parses']=all(isinstance(json.loads(p.read_text()),dict) for p in json_outputs)
    markdown_names=['REPORT.md','TIMELINE.md','SCIENTIFIC_PROCESS.md','EXPERIMENTS.md','CONCURRENCY.md']
    md={name:(OUT/name).read_text() for name in markdown_names}
    cited_ids=set(re.findall(r'toolu_[A-Za-z0-9]+','\n'.join(md.values())))
    missing_ids=sorted(cited_ids-known_ids)
    checks['E2_markdown_tool_ids_exist_in_sampled_calls']=not missing_ids
    reference_errors=[]
    for match in re.finditer(r'\|\s*(\d+)→(\d+)\s*\|\s*`(toolu_[A-Za-z0-9]+)`',md['TIMELINE.md']):
        node,result,tid=match.groups(); r=next(x for x in rows if x['tool_call_id']==tid)
        if r['node']!=int(node) or r['result_node']!=int(result): reference_errors.append((node,result,tid))
    checks['timeline_node_tool_result_joins_match']=not reference_errors
    all_md='\n'.join(md.values())+'\n'+(OUT/'POST11_PAIR_NOTES.md').read_text()
    secret_patterns=[r'(?i)bearer\s+[A-Za-z0-9._~-]{20,}',r'(?i)(?:api[_-]?key|access[_-]?token|auth[_-]?token)\s*[:=]\s*[\"\']?[A-Za-z0-9._~-]{20,}',r'\bsk-[A-Za-z0-9_-]{20,}']
    checks['no_credential_value_patterns_in_reports']=not any(re.search(p,all_md) for p in secret_patterns)
    missing_links=[]
    for name,text in {**md,'POST11_PAIR_NOTES.md':(OUT/'POST11_PAIR_NOTES.md').read_text()}.items():
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if not target.startswith(('http:','https:','#')) and not (OUT/target.split('#')[0]).exists(): missing_links.append((name,target))
    checks['local_markdown_links_exist']=not missing_links
    checks['source_unchanged_after_validation']=digest(SOURCE)==s['scope']['source_sha256_at_read']
    validation=dict(trace_id=TARGET,task=TASK,checks=checks,check_count=len(checks),all_passed=all(checks.values()),
                    E2_full_source_sha256=digest(SOURCE),E2_selected_trace_sha256=scope['selected_trace_sha256'],source_bytes=SOURCE.stat().st_size,
                    audited_E2_tool_reference_count=len(cited_ids),missing_tool_ids=missing_ids,reference_errors=reference_errors,missing_links=missing_links,
                    scope='Static read-only audit consistency checks. No environment tests, episode code, predictor generation, simulation, model/evaluation calls or production changes.',
                    limitations='Checks establish archived evidence consistency, not simulator/state exactness, full payload regeneration, auxiliary billing completeness, or benchmark comparability.')
    (OUT/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    print(json.dumps(validation,indent=2))
    assert validation['all_passed'],[k for k,v in checks.items() if not v]


if __name__=='__main__':
    main()
