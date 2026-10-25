import sys, json, gzip, numpy as np
fn=sys.argv[1]
d=json.load(gzip.open(fn)); S=d['series']
pos={}
for a,x in enumerate(S):
    for i,c in enumerate(x['id']): pos.setdefault(c,[]).append((a,i))
mode={}
for t,ty,p,ch in d['events']:
    if ty in('split','appear','merge'):
        for c in ch: mode[c]=ty
deaths=[(t,p[0]) for t,ty,p,ch in d['events'] if ty=='death' and p[0] in pos]
def last(c,k): a,i=pos[c][-1]; return S[a][k][i], S[a]['t'], S[a]['np'][i]
def first(c,k): a,i=pos[c][0]; return S[a][k][i], S[a]['t'], S[a]['np'][i]
# mature deaths (>=20 snaps, t>1000) that are followed within 300 steps by an appear with matching ym,zm
md=[(t,c) for t,c in deaths if t>1000 and len(pos[c])>=20]
apps=[c for c in pos if mode.get(c)=='appear']
nfollow=0; rows=[]
for t,c in md:
    y,_,n=last(c,'ym'); z=last(c,'zm')[0]
    best=None
    for a in apps:
        ya,ta,na=first(a,'ym'); za=first(a,'zm')[0]
        if 0<=ta-t<=2000:
            dd=max(abs(ya-y),abs(za-z))
            if best is None or dd<best[0]: best=(dd,ta-t,na,len(pos[a]),a)
    if best and best[0]<0.01: nfollow+=1
    rows.append((t,c,n,mode.get(c,'?'),best))
print(fn.split('/')[-1],'mature deaths',len(md),'followed by matching appear (<0.01, 2000 steps):',nfollow)
# chains: how many mature deaths are of cells whose mode is appear
print(' mature deaths by birth mode:', {m: sum(1 for r in rows if r[3]==m) for m in set(r[3] for r in rows)})
for r in rows[:30]: print('  ',r[:4], None if r[4] is None else tuple(round(v,4) if isinstance(v,float) else v for v in r[4]))
