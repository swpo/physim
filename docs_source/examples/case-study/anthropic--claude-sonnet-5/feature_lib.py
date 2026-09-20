
import numpy as np

TAUS2 = np.array([0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0])

def parse_actions(actions):
    inj = {0: {0:[],1:[],2:[],3:[]}, 1: {0:[],1:[],2:[],3:[]}}
    adj = {0: [], 1: []}
    for a in actions:
        if a['kind'] == 'inject':
            d = a['device']; p = a['port']
            t0 = a['t']; t1 = a['t']+a['dur']
            inj[d][p].append((t0,t1,a['amp']))
        else:
            d = a['device']
            t0 = a['t']; t1 = a['t']+5.0
            adj[d].append((t0,t1,a['u']))
    return inj, adj

def leaky_features_for_pulses(pulses, T, taus=TAUS2):
    raw = 0.0
    integrals = np.zeros(len(taus))
    for (t0,t1,amp) in pulses:
        if t0 > T:
            continue
        if amp == 0:
            continue
        b = min(t1, T)
        if b <= t0:
            continue
        if t0 <= T < t1:
            raw += amp
        for i,tau in enumerate(taus):
            contrib = amp*tau*(np.exp(-(T-b)/tau) - np.exp(-(T-t0)/tau))
            integrals[i] += contrib
    return raw, integrals

def leaky_features_for_adjust(pulses, T, taus=TAUS2):
    raw = np.zeros(3)
    integrals = np.zeros((3, len(taus)))
    for (t0,t1,u) in pulses:
        if t0 > T:
            continue
        b = min(t1, T)
        if b <= t0:
            continue
        active = (t0 <= T < t1)
        for k in range(3):
            uk = u[k]
            if uk == 0:
                continue
            if active:
                raw[k] += uk
            for i,tau in enumerate(taus):
                contrib = uk*tau*(np.exp(-(T-b)/tau) - np.exp(-(T-t0)/tau))
                integrals[k,i] += contrib
    return raw, integrals

def featurize2(actions, T, taus=TAUS2):
    inj, adj = parse_actions(actions)
    feats = []
    raws = []
    integs_all = []
    for d in [0,1]:
        for p in [0,1,2,3]:
            raw, integ = leaky_features_for_pulses(inj[d][p], T, taus=taus)
            raws.append(raw)
            integs_all.append(integ)
            feats.append(raw)
            feats.extend(integ.tolist())
    adj_raws = []
    for d in [0,1]:
        raw, integ = leaky_features_for_adjust(adj[d], T, taus=taus)
        for k in range(3):
            adj_raws.append(raw[k])
            feats.append(raw[k])
            feats.extend(integ[k].tolist())
            integs_all.append(integ[k])
    feats.append(T)
    feats.append(np.sqrt(T))
    base = np.array(feats, dtype=np.float64)
    raws_arr = np.array(raws + adj_raws)
    integs_arr = np.concatenate(integs_all)
    extra = np.concatenate([raws_arr**2, integs_arr**2])
    return np.concatenate([base, extra])
