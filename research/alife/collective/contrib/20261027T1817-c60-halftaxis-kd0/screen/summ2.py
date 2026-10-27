import json,glob
for f in sorted(glob.glob('*_6*.json')):
    d=json.load(open(f)); r=d['rows']
    al=[x['alive'] for x in r[-1]['targets']]
    print(f, 'npred', [r[i]['n_pred'] for i in (0,10,20,-1)], 'nprey', r[0]['n_prey'], r[-1]['n_prey'], 'targets alive', sum(al), [ (x.get('area'),round(x.get('max_cb',0),2)) for x in r[-1]['targets']])
