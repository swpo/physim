import sys, os
os.environ['WORLD_P']=sys.argv[1]
import numpy as np, crawler as c
s=c.init(0,(256,256)); L=256*0.5
def com(u):
    y,x=np.mgrid[0:256,0:256]*0.5
    return [np.angle((u*np.exp(2j*np.pi*z/L)).sum())*L/2/np.pi for z in (x,y)]
pos=[]
for i in range(int(200/0.05)):
    c.step(s)
    if i%400==0: pos.append(com(s['u']))
pos=np.array(pos); d=np.diff(pos,axis=0); d=(d+L/2)%L-L/2
print(sys.argv[1], 'speeds', np.round(np.hypot(d[:,0],d[:,1])/20,2), 'area', round(float((s['u']>0.5).sum()*0.25)))
