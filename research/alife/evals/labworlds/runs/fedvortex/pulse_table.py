import json, sys
D = '/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex/out/'
for f in ['om', 'Y']:
    J = json.load(open(D + f'pulse_s0_dur20_{f}.json'))
    if f == 'om': print('twin target tracks:', {k: v[::10] for k, v in J['twin_track'].items()})
    for r in J['rows']:
        tag = 'p' if r['site'].endswith('_p') else ('n' if r['site'].endswith('_n') else None)
        out = [r['field'], r['site'], r['amp'], 'blow@%s' % r['blowup_at'] if r['blowup_at'] else 'finite']
        for mk in (20, 50, 100, 200):
            d = r.get(f't{mk}')
            if not d or not d.get('finite'): continue
            s = f"t{mk}: n{d['bodies']}/{d['bodies_twin']} chg{d['changed_px']}@{d['max_changed_dist']:.0f} tb{d['twin_bodies_touched']} dL2 {d['diff_l2_om']:.2g} wmax{d['om_max']:.2f} umax{d['u_max']:.2f} site{d['om_site']:+.2f}/{d['om_site_twin']:+.2f} Ys{d['Y_site']:.2f}"
            if tag: s += f" tgt{d[f'target_{tag}_n']}/{d[f'target_{tag}_n_twin']}"
            if 'new_body_n' in d: s += f" new{d['new_body_n']}"
            out.append(s)
        if tag: out.append(f"died {r['target_died_at'][tag]} (twin {r['target_died_at_twin'][tag]}) maxparts {r['target_max_parts'][tag]}/{r['target_max_parts_twin'][tag]}")
        if 'new_body_died_at' in r: out.append(f"newbody died {r['new_body_died_at']} hist {r['new_body_hist'][:12]}")
        print(' | '.join(map(str, out)))
