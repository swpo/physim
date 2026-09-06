"""Build bounded timeline and E1/E2 comparison from local audited data only.
Never executes trace scripts, models, simulations, or world tools.
"""
from pathlib import Path
import json
import hashlib
from audit_counts import select_trace, parse_rows, utc, ref, TARGET, OUT, WORLD_TOOLS

E1 = OUT.parent / "e1_928_process_audit"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pick(rows, *, node=None, tool=None, tid=None, description=None):
    rr=[r for r in rows if (node is None or r['node']==node) and (tool is None or r['tool']==tool)
        and (tid is None or r['tool_call_id']==tid)
        and (description is None or description in r['args'].get('description',''))]
    assert len(rr)==1, (node,tool,tid,description,len(rr))
    return rr[0]


def build_timeline(trace, rows, summary):
    ready=pick(rows,tool='mcp__probe__ready')
    milestones=[
      (pick(rows,node=3,tool='mcp__probe__status'),'Start: reads status/syllabus before exploration.'),
      (pick(rows,node=37,tool='Agent'),'Delegates serial base capture; later capture batches continue the same advancing base head.'),
      (pick(rows,node=163,tool='mcp__probe__read'),'Base capture reaches2500. The21 successful base reads account for500 grid frames;20 full large-output files are absent here.'),
      (pick(rows,node=222,tool='Agent',description='Post-record continuation r1'),'Eight Agent calls in this sampled response launch fork divergence/continuation work. This row identifies one of them, not eight completed experiments.'),
      (pick(rows,node=231,tool='mcp__probe__fork'),'A requested2500 anchor returns the handle later returned at1000 in node254. Distinct sampled calls, not a copied tool result; see CONCURRENCY.md.'),
      (pick(rows,node=325,tool='Agent'),'Delegates actuator axis-push trials; later work fits an empirical contraction, not a recovered spatial simulator.'),
      (pick(rows,node=961,tool='Agent',description='Global stream capture 600-1080'),'Four Agent calls plan global-only sweeps. Wait replies expose free global statistics; these are observations, not learned forecasts.'),
      (pick(rows,node=1386,tool='Agent',description='Emission port scan ports 0-3'),'Emission scan starts at anchor1200, amp1, dur10. Across workers it covers all13 ports.'),
      (pick(rows,node=1856,tool='Agent',description='L1 emulation sequences 0-19'),'Delegates actuator command sequences; a second sequence batch follows at node2232.'),
      (pick(rows,tid='toolu_01YYUePYZxCJ71Foe7dctYBd'),'Printed amp1 response table shows much larger late residuals for injection port6 than11. This is measured-condition evidence, not hidden-dose truth.'),
      (pick(rows,node=2470,tool='Agent'),'Delegates dose series for ports2/4; later batches add ports6/7, duration variants, and lower-dose off-anchor checks.'),
      (pick(rows,node=3206,tool='Agent'),'Delegates longer divergence/continuation tails; success replies, status clocks and retained saved data must be distinguished.'),
      (pick(rows,node=4013,tool='Agent'),'Fresh anchor2500 global capture:16 waits provide2525..2900 at25tu spacing; device tail later covers2905..3100. This supplies L3S second-window coverage before reveal.'),
      (pick(rows,node=4374,tool='Agent'),'Restarts a measurement batch after the earlier branch has an empty model response and two provider400 content-policy errors (calls1923-1924); no retry-chain count is inferred.'),
      (pick(rows,node=4949,tool='Agent'),'Final tails/global-fill delegation. Remaining trace gaps are not assumed resolved by the task acknowledgment.'),
      (pick(rows,node=5071,tool='mcp__probe__reset'),'Last sampled world-tool request: reset. About196s of node-clock time remain before ready; native/background completion time is not logged.'),
      (ready,'Ready: irreversible reveal. Final metadata gives14,655simtu and1,016persisted turns at this boundary.'),
      (pick(rows,node=5092,tool='Bash'),'Runs the saved predictor locally to construct all six payloads from revealed parameters.'),
      (pick(rows,node=5114,tool='Bash'),'Replaces L2 with a0.7 device-pooled /0.3 global blend, repeated across hidden slots. This override is not predict_L2 in the archived Python file.'),
      (pick(rows,node=5128,tool='Edit'),'Fixes emission sigma broadcasting offline; this is before first L4/L4D submission, not a rejected-submit recovery.'),
      (pick(rows,node=5131,tool='Bash'),'Regenerates L4/L4D and checks mean/sigma shapes.'),
      (pick(rows,node=5135,tool='Bash'),'Rounds L4/L4D payloads to4decimals. Accepted objects later match the archived files exactly.'),
    ]
    lines=['# Annotated timeline — E2 #942','',f'Only trace `{TARGET}`. Node and model-call indices are zero-based. Tool IDs below belong to sampled responses; copied context adds no actions.','',
           '**Clock caution:** UTC values are sampled-node timestamps. A result node may be recorded at the next model response, not at native tool completion. Native GET/PUT and timeout-work completion times are unavailable.','',
           '## Investigation and closed-book preparation','', '| UTC sampled-node time | Call → result | Unique tool ID | Annotation |','|---|---:|---|---|']
    for r, note in milestones:
        lines.append(f"| {utc(r['timestamp'])} | {r['node']}→{r['result_node']} | `{r['tool_call_id']}` | {note} |")
    lines.extend(['','## Six accepted submissions','',
                  'One accepted submission per instance, no rejects or resubmissions. Each object exactly matches its corresponding archived `app/models/sub_*_i1.json` file (line1). JSON-object hashes are in `summary.json#/ready_and_submission/submissions`.','',
                  '| Instance | UTC sampled-node time | Call → result | Unique tool ID | Accepted shape / artifact |','|---|---|---:|---|---|'])
    for s in summary['ready_and_submission']['submissions']:
        shape=json.dumps(s['accepted_shape'],separators=(',',':'))
        path=s['matching_workspace_payloads'][0]
        lines.append(f"| {s['instance']} | {s['timestamp_utc']} | {s['node']}→{s['result_node']} | `{s['tool_call_id']}` | `{shape}`; `{path}:1` |")
    status=summary['ready_and_submission']['final_status']
    lines.extend(['',f"Final status: **{status['timestamp_utc']}**, node**{status['node']}→{status['result_node']}**, `{status['tool_call_id']}`. All six flags are true; phase is revealed; base head is2500; `contexts=[]`.",
                  '',f"Scoring ends **{summary['completion']['scoring_end_utc']}**. Both nested completion flags are true. Resource policyv2r2 has zero cap hits and no truncation.",
                  '', '## Boundary and late-work limits','',
                  '- After ready:9Bash,8Read,1Edit,6submit,1status; no read/wait/fork/adjust/inject/reset world requests. The inspected Bash/import path uses local data/model files, not world transport.',
                  '- No pre-ready tool invocation has a recorded result-node timestamp later than ready. Eleven world invocations have no result;266 timed out. That leaves unknown native completion/commit timing. Do not infer every background request had stopped from silence alone.',
                  '- Last world timeout: node4969→4971, `toolu_01QTXqdimPJPu1mJFbVvcZh3`, at02:47:21.639Z (result node02:48:26.009Z). Last world request: node5071→5072, reset at03:09:52.573Z. These are observed boundary facts, not proof of server quiescence.',
                  '- Ready/final persisted turns1016→1023 equal the six submits plus final status. Live sim meter remains14655tu. Final status itself exposes no resource meters.',
                  '- Post-ready model accounting:26 sampled response calls; one429 error attempt with no usage. Reported prompt88406, cache-read8111024, output43248, reasoning4898 within output.',
                  '', 'The complete strategy and calibration evidence is in [SCIENTIFIC_PROCESS.md](SCIENTIFIC_PROCESS.md). Separate state-integrity evidence is in [CONCURRENCY.md](CONCURRENCY.md).'])
    (OUT/'TIMELINE.md').write_text('\n'.join(lines)+'\n')


def main():
    trace,_=select_trace(); rows,_,_=parse_rows(trace)
    e1=json.loads((E1/'summary.json').read_text()); e2=json.loads((OUT/'summary.json').read_text())
    state=json.loads((OUT/'experiment_summary.json').read_text())
    build_timeline(trace,rows,e2)
    cases={}
    for label,s in [('E1_928',e1),('E2_942',e2)]:
        a=s['accounting']; r=s['resources']; ready=s['ready_and_submission']
        keys=['prompt_tokens','cached_input_tokens','input_tokens','completion_tokens','reasoning_tokens','total_tokens','cache_write_tokens','billed_dollars']
        cases[label]=dict(trace_id=s['scope']['trace_id'],task=s['scope']['task'],world=s['scope']['world'],seed=s['scope']['world_seed'],
          reported_episode_skill=s['scores']['instance_reward']['skill']['score'],elapsed_wall_seconds=s['completion']['elapsed_wall_seconds'],
          completed_model_calls=a['completed_model_calls'],model_error_attempts=a['request_errors'],usage={k:a['total_usage'].get(k) for k in keys},
          unique_tool_invocations=a['unique_tool_calls'],environment_requests=a['environment_tool_requests'],persisted_environment_turns=a['environment_persisted_turns'],
          Agent_invocations=a['delegated_Agent_invocations'],tools={k.removeprefix('mcp__probe__'):v['calls'] for k,v in s['tools'].items()},
          environment_tool_timeouts=sum(v['outcomes'].get('tool_timeout',0) for k,v in s['tools'].items() if k.startswith('mcp__probe__')),
          environment_missing_results=sum(v['outcomes'].get('no_result_recorded',0) for k,v in s['tools'].items() if k.startswith('mcp__probe__')),
          persisted_meters=r['persisted_meters'],resident_cache=r['resident_cache'],time_to_ready=r['time_to_ready'],
          policy=r['policy']['id'],resource_truncated=s['completion']['resource_truncated'],cap_hits=s['completion']['cap_hits'],
          readied=True,all_six_submissions_accepted=len(ready['submissions'])==6 and all(x['accepted'] for x in ready['submissions']),
          submission_order=[x['instance'] for x in ready['submissions']],post_ready_world_tool_requests=len(ready['world_tool_requests_after_ready']),
          final_logical_contexts=ready['final_status_open_contexts'],instance_skills=s['scores']['instance_skills_full_precision'],
          selected_trace_sha256=s['scope']['selected_trace_sha256'])
    cases['E1_928']['request_error_description']='22 HTTP429 +1 connection reset; all23 lack usage; retry chains unknown.'
    cases['E2_942']['request_error_description']='38 HTTP429 +2 HTTP400 content_policy_violation; all40 lack usage; retry chains unknown.'
    cases['E1_928']['fork_reply_summary']={k:e1['resources'][k] for k in ['fork_success_responses','unique_returned_fork_ids','fork_ids_returned_multiple_times','fork_ids_with_multiple_reported_anchors']}
    cases['E2_942']['fork_reply_summary']={
      'fork_success_responses':state['handles']['successful_fork_replies'],
      'unique_returned_fork_ids':state['handles']['unique_returned_ids'],
      'fork_ids_returned_multiple_times':state['handles']['fork_ids_returned_more_than_once'],
      'fork_ids_with_multiple_reported_anchors':state['handles']['fork_ids_with_multiple_anchor_times']}
    cases['E1_928']['reply_minus_persisted_meters']=e1['resources']['observed_reply_minus_persisted_meters']
    cases['E2_942']['reply_minus_persisted_meters']=state['reply_accounting']['reply_minus_persisted']
    cases['E1_928']['ordinary_reply_minus_persisted_turns']=e1['resources']['successful_or_error_reply_minus_persisted_turns']
    cases['E2_942']['ordinary_reply_minus_persisted_turns']=state['reply_accounting']['reply_minus_persisted']['turns']
    cases['E1_928']['method_summary']={
      'L1':'Empirical record-to-global contraction; two drawn commands; post-ready sequential u3 clipping.',
      'L2':'Per-port global nowcast/climatology, repeated hidden-slot marginals.',
      'L3F':'Catmull-Rom/circular recorded-history interpolation; targets794.72,814.72,889.72,1189.72 all inside base2500.',
      'L3E':'Recorded-history upward-crossing counts,1694.78..2494.78, inside base.',
      'L4_L4D':'Drawn ports3/1 use passive recorded means with dose-aware uncertainty. Port2 fitted mean template is unused.',
      'continuation':'Audited continuation through3105 was collected but unnecessary for drawn L3F/L3E.',
      'general_dynamical_simulator_in_submitted_path':False,
      'citations':['../e1_928_process_audit/SCIENTIFIC_PROCESS.md:9-21,24-45','E1 embedded app/probe/predict_final.py:53-227','E1 node2972/toolu_017uK4JgPMqyKmAsFk6SS5SR','../e1_928_process_audit/REPORT.md sections4-5']}
    cases['E2_942']['method_summary']={
      'L1':'Fitted actuator-distance contraction of record toward local mean; one drawn command; target752.6.',
      'L2':'Post-ready0.7 pooled-device mean +0.3 global mean; identical marginal forecast across13 hidden slots.',
      'L3F':'Cubic recorded-history interpolation; targets1814.02,1889.02,2189.02 all inside base2500.',
      'L3S':'Linear saved-global interpolation averaged at41 points per200tu window.2260.72..2460.72 in base;2660.72..2860.72 covered by pre-ready future global samples.',
      'future_global_samples':{'anchor':2500,'count':16,'first_t':2525,'last_t':2900,'step_tu':25,'plan_node':4013,'plan_tool_id':'toolu_01FArZ3E2DiK4KjzcSpJQaCG','fork_node':4016,'fork_tool_id':'toolu_01PzHLUnhsFM9kiRdMdL7cQK','fork_id':'fceee3e6210a425daa3830b8d928cd49a'},
      'device_continuation':'cont_r1:80 retained distinct frames2505..3000 with gap2800->2905; cont_r3b:40frames2905..3100. Not uniform5tu post-base.',
      'L4_L4D':'Empirical RMS-derived decorrelation/shrinkage changes means and sigma. Drawn port6 amp2.7998 uses unvalidated above-apparatus scaling; port11 amp0.8124 has smaller measured training residuals.',
      'general_dynamical_simulator_in_submitted_path':False,
      'citations':['SCIENTIFIC_PROCESS.md','E2 embedded app/models/predictor3.py:13-29,44-76,79-94,105-214','E2 node5114/toolu_01KwioQiU29N3GXNPj1gg4YA','E2 node2364->2365/toolu_01YYUePYZxCJ71Foe7dctYBd']}
    pair=dict(scope='Two completed case audits, not a clean comparative benchmark or aggregate benchmark mean.',
              stop_status_as_supplied_by_operator='All runs stopped. Two reported completions; E1#929 unscored HarnessError; one queued E2#943 operator-canceled after about11min; other queued tasks had no model stage. Excluded from these completed-case totals.',
              cases=cases,
              limitations=['Different worlds/seeds, menus and drawn instances; completion-selected cases are not balanced performance evidence.',
                           'Recorded/allowed-future lookup is permitted, not misconduct; it limits claims about learned dynamics.',
                           'Empirical response/uncertainty models are genuine narrower modeling; no general dynamics rollout is used in either submitted path.',
                           'State-update integrity defects and scientific target discriminating power are different issues.',
                           'No actual billing; cache writes merged into prompt; auxiliary count_tokens and errored-attempt usage unknown.',
                           'Missing bulk predictor inputs and native transaction history prevent full regeneration/state reconstruction.'],
              controls=[dict(name='Native model-free state and phase-gate regression',status='Recommended only; not executed.',
                             recipe='Use deterministic barrier-controlled state handlers through actual native GET/fn/PUT/MCP transport. Assert distinct fork IDs, stable anchors, additive shared-state meters, nondecreasing clocks, durable resets, and ready gating for delayed calls, across same/different contexts. Include shape-only six-submit and large-output persistence checks.',
                             interpretation='Diagnostic wiring/state integrity, not scientific model performance; no pressure/time caps imposed on investigators and no production fix here.'),
                        dict(name='Declared record/continuation and emission controls',status='Recommended only; not executed.',
                             recipe='Compare transparent record(+allowed pre-ready continuation) and no-emission-mean controls with empirical RMS/shrinkage. Separately predeclare targets outside any captured stream and active-response ports/doses, with anchor/protocol holdouts. Do not choose only favorable completed worlds/ports.',
                             interpretation='Scientific evidence control, not another paid rollout or a diagnostic benchmark mean.')],
              numeric_citations={'E1':'../e1_928_process_audit/summary.json#/accounting,/resources,/scores,/ready_and_submission; existing validation.json all_passed=true',
                                 'E2':'summary.json#/accounting,/resources,/scores,/ready_and_submission; experiment_summary.json#/handles,/reply_accounting'},
              audit_input_hashes={str(p.relative_to(OUT.parent)):digest(p) for p in [E1/'summary.json',E1/'REPORT.md',E1/'SCIENTIFIC_PROCESS.md',E1/'validation.json']},
              E2_full_source_sha256=e2['scope']['source_sha256_at_read'])
    (OUT/'paired_summary.json').write_text(json.dumps(pair,indent=2)+'\n')
    print(json.dumps({'timeline':'TIMELINE.md','paired_summary':'paired_summary.json','E1_skill':cases['E1_928']['reported_episode_skill'],'E2_skill':cases['E2_942']['reported_episode_skill']},indent=2))

if __name__=='__main__':
    main()
