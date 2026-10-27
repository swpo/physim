import sys, importlib.util, numpy as np
sys.path.insert(0,'/home/user/physim/research/alife')
spec=importlib.util.spec_from_file_location('w',sys.argv[1]); w=importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
for seed in map(int, sys.argv[2:]):
    s=w.init(seed,(128,128)); n=int(200/w.P['dt']); out=[]
    for i in range(n):
        s=w.step(s)
        if i%int(50/w.P['dt'])==0: out.append(round(float(s['T'].max()),3))
    print(seed, 'Tmax@0,50,100,150:', out, 'Tmax200', round(float(s['T'].max()),3), 'alive' if s['T'].max()>0.25 else 'EXTINCT', flush=True)
