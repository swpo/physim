"""Spatial response model inferred from controlled laboratory observations."""
from pathlib import Path
from functools import lru_cache
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.fft import rfft2, irfft2
from scipy.spatial.distance import cdist

ROOT=Path(__file__).parent
P0=np.array([[0,3],[3,0],[-6,0],[-3,3],[-3,0],[-3,-3],[0,0],[3,3],[0,6],[6,0],[0,-3],[0,-6],[3,-3]],float)
P1=np.load(ROOT/'dev1_points.npy')
POINTS=(P0,P1)
VREF=-0.703539938228
_DAMP_RATE=.15
_DAMP_RADIUS=17.25

@lru_cache(None)
def _model():
 with np.load(ROOT/'baseline_model.npz') as f:
  data={k:f[k].copy() for k in f.files}
 data['output_spline']=CubicSpline(data['times'],data['fields'])
 nn=data['fields'].shape[-1];lo=nn//2-64;data['crop']=slice(lo,lo+128)
 data['fields']=data['fields'][...,lo:lo+128,lo:lo+128]
 data['spline']=CubicSpline(data['times'],data['fields'])
 data['global_spline']=CubicSpline(data['times'],data['global_values'])
 data['weight_spline']=CubicSpline(data['times'],data['weights'].transpose(2,0,1))
 n=data['fields'].shape[-1];dx=float(data['dx']);ax=(np.arange(n)-n/2)*dx
 data['xx'],data['yy']=np.meshgrid(ax,ax)
 kx=2*np.pi*np.fft.rfftfreq(n,dx);ky=2*np.pi*np.fft.fftfreq(n,dx)
 k2=ky[:,None]**2+kx[None,:]**2
 data['heat']=np.exp(-.02*np.array([20.,1.,.7])[:,None,None]*k2)
 return data

def _bilinear(a,p,dx=.5):
 n=a.shape[-1];z=p/dx+n/2;i=np.floor(z).astype(np.int64);f=z-i
 x=i[:,0]%n;y=i[:,1]%n
 return (a[...,y,x]*(1-f[:,0])*(1-f[:,1])+a[...,y,(x+1)%n]*f[:,0]*(1-f[:,1])+a[...,(y+1)%n,x]*(1-f[:,0])*f[:,1]+a[...,(y+1)%n,(x+1)%n]*f[:,0]*f[:,1])

def _field(m,t):
 b=m['spline'](t)
 # Smooth priors in regions far from the reference measurements.
 b[0]=np.clip(b[0],-.01,.6)
 b[1]=np.clip(b[1],-1.02,1.16)
 b[2]=np.clip(b[2],0,.06)
 b[3]=np.clip(b[3],-.13,1.12)
 return b

def _baseline_at(m,t,p,b=None):
 p=(np.asarray(p)+64)%128-64
 if b is None:b=m['output_spline'](t)
 result=_bilinear(b,p)
 far=np.any(np.abs(p)>(b.shape[-1]/4-.5),axis=1)
 if np.any(far):
  pf=p[far];xy=pf/.5;ij=np.floor(xy);ff=xy-ij;res=np.zeros((4,len(pf)))
  wts=m['weight_spline'](t)
  for a in [0,1]:
   for c in [0,1]:
    pp=(ij+[a,c])*.5;d=cdist(pp,m['points'],'sqeuclidean');fac=(ff[:,0] if a else 1-ff[:,0])*(ff[:,1] if c else 1-ff[:,1])
    for ch in range(4):
     val=np.exp(-d/(2*m['lengths'][ch]**2))@wts[:,ch]
     if ch==1:val+=VREF
     res[ch]+=fac*val
  result[:,far]=res
 return result

def _firing(v):
 return .99981555*np.tanh(2.50000444*np.maximum(v-.249464394,0))

_MAX_PATHS=16
_NOISE=.00225
_BASE_UNCERTAINTY=.0005

def predict(actions,queries,n_samples=64,seed=0):
 m=_model();ns=int(n_samples)
 outs=[np.empty((ns,len(q['t']),4,13 if q['sensor']=='device0' else 19 if q['sensor']=='device1' else 2),float) for q in queries]
 schedule={}
 for qi,q in enumerate(queries):
  for ti,t in enumerate(q['t']):schedule.setdefault(int(round(t/.02)),[]).append((qi,ti,q['sensor']))
 if not schedule or ns==0:return {'samples':outs}
 ends=max(schedule);act={}
 for a in actions:act.setdefault(int(round(a['t']/.02)),[]).append(a)
 paths=min(ns,_MAX_PATHS);sample_ids=np.arange(ns)%paths
 rng=np.random.default_rng(int(seed) % (1 << 64))
 def normals(shape):
  half=(paths+1)//2
  x=rng.standard_normal((half,)+shape)
  return np.concatenate([x,-x],axis=0)[:paths]
 radii=np.clip(_DAMP_RADIUS+1.25*normals(()),15.,18.5)
 pos=np.zeros((2,3));delta=np.zeros((paths,)+m['fields'][0].shape,dtype=float);background=np.zeros_like(delta);active=[];has_input=False
 heat=m['heat'];dx=float(m['dx']);weight=dx*dx/(128*128)
 rr=np.sqrt(m['xx']**2+m['yy']**2)
 static_damping=np.exp(-.02*.15*np.maximum(rr-20,0)**2)
 damping=static_damping.copy();mindist=np.full_like(rr,np.inf)
 # A smooth, small uncertainty in the reconstructed unobserved field.
 # It changes responses but leaves the common prepared measurement intact.
 from scipy.ndimage import gaussian_filter
 perturb=gaussian_filter(normals(rr.shape),sigma=(0,2,2),mode='wrap')
 perturb*=(_BASE_UNCERTAINTY/np.maximum(perturb.std(axis=(-2,-1),keepdims=True),1e-12))
 for step in range(ends+1):
  t=step*.02
  for a in act.get(step,()):
   dev=a['device']
   if a['kind']=='adjust':
    pos[dev]+=a['u'];pos[dev,2]=np.clip(pos[dev,2],-np.log(2),np.log(3))
   elif a['amp']:
    has_input=True
    kernel=a['amp']*np.exp(-((m['xx']-pos[dev,0])**2+(m['yy']-pos[dev,1])**2)/8)
    active.append((step+int(round(a['dur']/.02)),a['port'],kernel))
    mindist=np.minimum(mindist,np.sqrt((m['xx']-pos[dev,0])**2+(m['yy']-pos[dev,1])**2))
    damping=np.exp(-.02*_DAMP_RATE*np.maximum(mindist[None]-radii[:,None,None],0)**2)*static_damping
  b=_field(m,t)
  if step in schedule:
   bout=m['output_spline'](t)
   for qi,ti,sensor in schedule[step]:
    if sensor=='global':
     val=np.broadcast_to(m['global_spline'](t),(paths,4,2)).copy();dmean=delta.sum(axis=(-2,-1))*weight
     dsecond=((2*(bout[...,m['crop'],m['crop']]+background)+delta)*delta).sum(axis=(-2,-1))*weight
     val[:,:,1]+=dsecond-2*val[:,:,0]*dmean-dmean*dmean
     val[:,:,0]+=dmean;val[:,:,1]=np.maximum(val[:,:,1],0)
    else:
     dev=int(sensor[-1]);p=pos[dev,:2]+POINTS[dev]*np.exp(pos[dev,2]);p=(p+64)%128-64
     dp=_bilinear(delta+background,p);dp[:,:,np.any(np.abs(p)>31,axis=1)]=0
     val=_baseline_at(m,t,p,bout)[None]+dp
     val[:,2]=np.maximum(val[:,2],0)
    outs[qi][:,ti]=val[sample_ids]
  if step==ends:break
  active=[a for a in active if a[0]>step]
  for end,port,kernel in active:delta[:,port]+=.02*kernel
  nu,nv,nz,nw=[background[:,c] for c in range(4)]
  bu,bv,bz,bw=b
  n_u=(1-.02/.7)*nu+.02/.7*nv
  n_v=nv+.02*((2-3*bv*bv)*nv-(1.5+bz)*nu-bu*nz-nw)
  phi_prime=np.where(bv>.249464394,.99981555*2.50000444*(1-np.tanh(2.50000444*np.maximum(bv-.249464394,0))**2),0)
  n_z=.9999*nz+.02*.00025*phi_prime*nv
  n_w=(1-.02/5.7)*nw+.02/5.7*nv
  n_v+=(_NOISE*np.sqrt(.02))*normals(rr.shape)
  if has_input:
   du,dv,dz,dw=[delta[:,c] for c in range(4)]
   cv=bv[None]+nv+perturb;cu=bu[None]+nu;cz=bz[None]+nz
   u=(1-.02/.7)*du+.02/.7*dv
   v=dv+.02*(2*dv-(np.clip(cv+dv,-10,10)**3-cv**3)-1.5*du-(cz*du+dz*cu+dz*du)-dw)
   z=.9999*dz+.02*.00025*(_firing(cv+dv)-_firing(cv))
   w=(1-.02/5.7)*dw+.02/5.7*dv
   both=np.stack([u,v,w,n_u,n_v,n_w],axis=1)
   diff=irfft2(rfft2(both)*np.concatenate([heat,heat]),s=rr.shape)
   delta[:,0]=diff[:,0];delta[:,1]=np.clip(diff[:,1]*damping,-10,10);delta[:,2]=z;delta[:,3]=diff[:,2]
   noise_diff=diff[:,3:]
  else:
   noise_diff=irfft2(rfft2(np.stack([n_u,n_v,n_w],axis=1))*heat,s=rr.shape)
  background[:,0]=noise_diff[:,0];background[:,1]=noise_diff[:,1]*static_damping;background[:,2]=n_z;background[:,3]=noise_diff[:,2]
  # Reference trajectories condition uncertainty where the reconstruction is sparse.
  gy,gx=np.gradient(b,.5,axis=(-2,-1));grad=np.sqrt(gx*gx+gy*gy)
  phase=.0003*np.sqrt(t+.02)+.00004*(t+.02)**1.5
  envelope=3*phase*grad+np.array([.0003,.001,.000003,.0004])[:,None,None]
  np.clip(background,-envelope,envelope,out=background)
 return {'samples':outs}
