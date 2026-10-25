import sys, json, gzip, numpy as np
fn=sys.argv[1]
d=json.load(gzip.open(fn) if fn.endswith('.gz') else open(fn)); S=d['series']
pos={}
for a,x in enumerate(S):
    for i,c in enumerate(x['id']): pos.setdefault(c,[]).append((a,i))
mode={}
for t,ty,p,ch in d['events']:
    if ty in('split','appear','merge'):
        for c in ch: mode[c]=ty
deaths=[(t,p[0]) for t,ty,p,ch in d['events'] if ty=='death' and p[0] in pos and t>1000 and len(pos[p[0]])>=20]
out=[]
for t,c in deaths:
    A=pos[c]; nps=[S[a]['np'][i] for a,i in A]
    med=[np.median(S[a]['np']) for a,i in A]
    life=(S[A[-1][0]]['t']-S[A[0][0]]['t'])
    out.append((mode.get(c,'founder/bud'), life, max(nps), int(np.median(med)), nps[0], nps[-1]))
for m in set(o[0] for o in out):
    sub=[o for o in out if o[0]==m]
    print(fn.split('/')[-1], m, 'n',len(sub),'life med',int(np.median([o[1] for o in sub])),'peak np med',int(np.median([o[2] for o in sub])),'pop median np',int(np.median([o[3] for o in sub])),'np birth med',int(np.median([o[4] for o in sub])), 'peak/popmed', [round(o[2]/o[3],2) for o in sub])
