import sys, json, numpy as np
sys.path.insert(0,'threads/lenia-multichannel/tools')
import screen_chan, quick
from PIL import Image
cat=json.load(open(sys.argv[1])); ids=[int(x) for x in sys.argv[3:]]
out=sys.argv[2]
rows=[]
for i in ids:
    e=cat[i]
    try:
        mass,frames,A=screen_chan.run(e,128,1500,nframes=8)
    except Exception as ex:
        print(i,'ERR',ex); continue
    n=quick.ncomp(A.sum(0)); occ=float((A.sum(0)>0.1).mean())
    print(i, repr(e['name']), 'mass %.0f->%.0f'%(mass[0].sum(),mass[-1].sum()), 'ncomp_end',n,'occ %.2f'%occ, flush=True)
    rows.append(np.concatenate([np.pad(f,((1,1),(1,1),(0,0)),constant_values=60) for f in frames],1))
    Image.fromarray(rows[-1]).save(f'{out}/rep_{i}.png')
