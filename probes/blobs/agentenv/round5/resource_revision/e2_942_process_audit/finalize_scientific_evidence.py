"""Complete E2 static science evidence from archived text/literals; execute no agent code."""
from pathlib import Path
import json,hashlib,re
from audit_counts import select_trace,parse_rows,TARGET,TASK,SOURCE,OUT,canonical
from science_counts import saved_json_data
tr,scope=select_trace(); rows,results,completed=parse_rows(tr); phy=tr['info']['physim']; ws=phy['workspace']
code=ws['app/models/predictor3.py']; lines=code.splitlines(); inst=phy['detail']['instances']
ready=next(r for r in rows if r['tool']=='mcp__probe__ready'); ready_t=ready['timestamp']
by_node={r['node']:r for r in rows}
saved,hist=saved_json_data(tr)
global_records=saved['app/data/globals/g2500.jsonl']
global_times=sorted({v['t'] for v,ref in global_records})
assert global_times==list(range(2525,2901,25))
assert all(tr['nodes'][ref['node_index']]['timestamp']<ready_t for v,ref in global_records)
def projection(d): return {k:d[k] for k in ('ctx','t','global_stats') if k in d}
matched_global=[]
for val,ref in global_records:
    matches=[]
    for r in rows:
        rv=r.get('result')
        if r['tool'].startswith('mcp__probe__') and isinstance(rv,dict) and all(rv.get(k)==val.get(k) for k in ('t','global_stats')) and ('ctx' not in val or rv.get('ctx')==val['ctx']):
            matches.append({'node':r['node'],'result_node':r['result_node'],'tool_call_id':r['tool_call_id']})
    matched_global.append({'t':val['t'],'save_ref':ref,'matching_world_replies':matches})
assert all(x['matching_world_replies'] for x in matched_global),'literal global saves lack exact returned measurement matches'
def device_times(prefix):
    times=[]; refs=[]
    for path,vals in saved.items():
        if path.startswith('app/data/forks/'+prefix+'_c'):
            for value,ref in vals:
                times.extend(float(s['t']) for s in value.get('steps',[]) if 't' in s); refs.append(ref)
    return sorted(set(times)),refs
cont1,refs1=device_times('cont_r1'); cont3,refs3=device_times('cont_r3b')
assert len(cont1)==80 and cont1[0]==2505 and cont1[-1]==3000
assert [b-a for a,b in zip(cont1,cont1[1:])].count(105)==1
assert len(cont3)==40 and cont3[0]==2905 and cont3[-1]==3100
horizons=[inst['L3F']['t_a']+h for h in inst['L3F']['horizons']]
windows=[[inst['L3S']['t_a']+e-200,inst['L3S']['t_a']+e] for e in inst['L3S']['epochs']]
assert max(horizons)<2500 and 2525<windows[1][0]<windows[1][1]<2900
required_code=['CubicSpline(ets, E[dev]', 'def glob_window_avg(t_end, width=200.0, n=41)', 'glob_window_avg(te)', 'alpha = np.clip(1 - (M**2)/(2*v), 0.0, 1.0)', 'mean = alpha[:,None]*rec + (1-alpha)[:,None]*m_loc[:,None]']
assert all(s in code for s in required_code)
l2=by_node[5114]
assert l2['tool']=='Bash' and 'mean = 0.7*dev_mean + 0.3*g_mean' in l2['args']['command']
assert 'Traceback' not in str(l2['result']) and 'Exit code 1' not in str(l2['result'])
submitted=[r for r in rows if r['tool']=='mcp__probe__submit']
assert len(submitted)==6
payload_checks=[]
for r in submitted:
    args=r['args']; p=json.loads(args['payload']) if isinstance(args['payload'],str) else args['payload']
    name='app/models/sub_'+args['instance'].replace('@','_')+'.json'
    payload_checks.append({'instance':args['instance'],'node':r['node'],'tool_call_id':r['tool_call_id'],'artifact':name,'exact_object_match':p==json.loads(ws[name]),'ok':r['result'].get('ok')})
assert all(p['exact_object_match'] and p['ok'] for p in payload_checks)
post=[r for r in rows if r['timestamp']>ready_t]
world_names={'mcp__probe__read','mcp__probe__wait','mcp__probe__adjust','mcp__probe__fork','mcp__probe__reset','mcp__probe__inject'}
assert not any(r['tool'] in world_names for r in post)
# Keep limited exact artifact excerpts, not bulk model data or credentials.
ranges={'record_interpolation':(13,29),'global_interpolation':(44,75),'L1':(79,94),'L3F':(105,116),'L3S':(118,128),'emission':(168,214)}
excerpts={k:{'artifact':'app/models/predictor3.py','sha256':hashlib.sha256(code.encode()).hexdigest(),'lines':[lo,hi],'text':'\n'.join(lines[lo-1:hi])} for k,(lo,hi) in ranges.items()}
summary={'trace_id':TARGET,'task':TASK,'scope':scope,'recovery':'Root completed missing scientific handoff after inactive child; static read-only verification only','checks':{'global_times_16':True,'global_saves_exactly_match_world_replies':True,'global_saves_pre_ready':True,'L3S_second_window_bracketed_by_measured_global_continuation':True,'L3F_all_targets_in_base':True,'device_continuation_gap_preserved':True,'emission_mean_shrinkage_in_final_code':True,'L2_local_override_in_accepted_path':True,'six_payloads_exactly_match_archived_objects':True,'no_post_ready_sampled_world_requests':True},'instances':inst,'L3F_targets':horizons,'L3S_windows':windows,'global_continuation':{'times':global_times,'matches':matched_global},'device_continuation':{'cont_r1':{'n':len(cont1),'times':cont1,'source_refs':refs1},'cont_r3b':{'n':len(cont3),'times':cont3,'source_refs':refs3},'gap':[2800,2905]},'artifact_excerpts':excerpts,'L2_override':{'node':5114,'tool_call_id':l2['tool_call_id'],'command':l2['args']['command']},'payloads':payload_checks,'methods':{'L1':'empirical actuator-distance contraction','L2':'0.7device pooled mean+0.3global mean, repeated across hidden slots','L3F':'cubic observed-record interpolation','L3S':'global observed-record/continuation interpolation and window averaging','L4':'RMS-conditioned decorrelation/shrinkage of mean and uncertainty','L4D':'same empirical RMS/shrinkage path; smaller observed training residual at drawn port11'},'limitations':['No embedded predictor or episode code executed','Not a general learned dynamics simulator','Bulk generator input arrays absent; no full payload regeneration','Global/device continuation sampling are different','State transaction and timeout-commit history incomplete','Experimental methods can be legitimate without establishing general theory']}
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==scope['source_sha256_at_read']
(OUT/'scientific_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
report=(OUT/'REPORT.md').read_text()
section=report.split('## 5. Scientific workflow and submitted methods',1)[1].split('## 7. Cheaper controls',1)[0]
md='# E2 #942 — scientific process and bounded evidence\n\nRoot recovered the missing scientific handoff from the immutable trace. This is static evidence checking, not a simulation, model evaluation, or independent regeneration of all predictor inputs. `scientific_summary.json` contains exact artifact excerpts, input hashes, tool IDs, and sixteen literal global saves matched back to actual returned world measurements.\n\n## Scientific workflow and submitted methods'+section+'\n## Static evidence check\n\nRun `.venv/bin/python '+str(OUT.relative_to(Path.cwd()))+'/finalize_scientific_evidence.py` from the repository root. It executes only audit code, never `predictor3.py` or any embedded command. It verifies coverage, selected final code paths, the L2 local override, all six accepted payload objects, and no sampled post-ready world request. It does not certify simulator transactions, causal response validation, complete generator inputs, or a general theory.\n'
(OUT/'SCIENTIFIC_PROCESS.md').write_text(md)
print(json.dumps({'trace_id':TARGET,'checks':summary['checks'],'global_measurements_matched':len(matched_global),'artifacts_written':['scientific_summary.json','SCIENTIFIC_PROCESS.md']},indent=2))
