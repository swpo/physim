// Lattice May-Leonard (Reichenbach, Mobilia & Frey 2007). States 0 empty, 1..3 species.
// sigma: i kills i+1 (cyclic); mu: i reproduces into empty; eps: exchange.
// usage: ml L M tmax seed snapfile(optional)  -> prints "ext t_ext" (ext=1 if any species died by tmax)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
static uint64_t s[2];
static inline uint64_t nx(void){uint64_t a=s[0],b=s[1];s[0]=b;a^=a<<23;s[1]=a^b^(a>>17)^(b>>26);return s[1]+b;}
static inline double ur(void){return (nx()>>11)*(1.0/9007199254740992.0);}
int main(int c,char**v){int L=atoi(v[1]);double M=atof(v[2]),tmax=atof(v[3]);uint64_t seed=atoll(v[4]);
 int trans = c>6? atoi(v[6]) : 0; // 1: transitive A>B, A>C, B>C
 const char*snap=c>5?v[5]:0; long N=(long)L*L; double eps=M*N/2, sig=1, mu=1, R=sig+mu+eps;
 s[0]=seed*0x9E3779B97F4A7C15ULL+1;s[1]=seed^0xDEADBEEF12345ULL;for(int i=0;i<20;i++)nx();
 unsigned char*g=malloc(N); long cnt[4]={0};
 for(long i=0;i<N;i++){g[i]=nx()%4;cnt[g[i]]++;}
 double t=0,dt=1.0/(N*R); double next=0; long steps=0;
 FILE*fs=snap&&snap[0]!='-'?fopen(snap,"wb"):0;
 while(t<tmax){
  for(long k=0;k<N;k++){
   long i=nx()%N; int x=i%L,y=i/L,d=nx()&3; int xx=x,yy=y;
   if(d==0)xx=(x+1)%L;else if(d==1)xx=(x+L-1)%L;else if(d==2)yy=(y+1)%L;else yy=(y+L-1)%L;
   long j=(long)yy*L+xx; int a=g[i],b=g[j]; double r=ur()*R;
   if(r<sig){ if(a&&b){ int kill=0;
      if(!trans){ if(b==a%3+1) kill=2; else if(a==b%3+1) kill=1; }
      else { if(a<b) kill=2; else if(b<a) kill=1; }
      if(kill==2){g[j]=0;cnt[b]--;cnt[0]++;} else if(kill==1){g[i]=0;cnt[a]--;cnt[0]++;} } }
   else if(r<sig+mu){ if(a&&!b){g[j]=a;cnt[a]++;cnt[0]--;} else if(b&&!a){g[i]=b;cnt[b]++;cnt[0]--;} }
   else { g[i]=b; g[j]=a; }
  }
  t+=N*dt;
  if(fs && t>=next){fwrite(&t,8,1,fs);fwrite(g,1,N,fs);next+=tmax/20;}
  if(!cnt[1]||!cnt[2]||!cnt[3]){printf("1 %.1f %ld %ld %ld\n",t,cnt[1],cnt[2],cnt[3]);if(fs){fwrite(&t,8,1,fs);fwrite(g,1,N,fs);fclose(fs);}return 0;}
 }
 printf("0 %.1f %ld %ld %ld\n",t,cnt[1],cnt[2],cnt[3]); if(fs){fwrite(&t,8,1,fs);fwrite(g,1,N,fs);fclose(fs);} return 0;}
