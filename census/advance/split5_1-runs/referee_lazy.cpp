// Referee's independent range certificate for split5_1, lazy-split residue tree.
// Class: n = 2^d t + r (t>=0); current iterate = a t + b. T applied only when the
// needed residue of the value is constant on the class; otherwise split t by parity.
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
typedef unsigned __int128 U;
static unsigned BITS;
static inline U T(U x){ if(!(x&1)) return x>>1; if(x>((~(U)0)>>4)){fprintf(stderr,"ovf\n");exit(2);} return (x&3)==1? 5*x+1 : x+1; }
struct Acc{ U cov=0; uint64_t leaves=0, direct=0; };
static bool term(U n, U x){ // iterate until below n or at 1/13
  for(uint64_t s=0;;++s){ if(x<n||x==1||x==13) return true; if(s>5000000) return false; x=T(x);} }
static void go(unsigned d, U r, U a, U b, Acc&A){
  for(;;){
    U M=(U)1<<d;
    if(a<=M && (a<M || b<r)){
      // leaf: t with a t + b < M t + r need nothing more
      A.leaves++; U cnt=(U)1<<(BITS-d); U t0=(r==0)?1:0; A.cov+=cnt-t0;
      if(b<r) return;
      U lim=(b-r)/(M-a)+1; if(lim>cnt) lim=cnt;
      for(U t=t0;t<lim;++t){ A.direct++; if(!term(M*t+r,a*t+b)){fprintf(stderr,"FAIL\n");exit(1);} }
      return;
    }
    if(d==BITS){ A.leaves++; if(r==0) return; A.cov+=1; A.direct++; if(!term(r,b)){fprintf(stderr,"FAIL\n");exit(1);} return; }
    bool can=false;
    if(!(a&1)){ if(!(b&1)){ a>>=1; b>>=1; can=true; }
                else if(!(a&3)){ if((b&3)==1){a*=5;b=5*b+1;} else {b+=1;} can=true; } }
    if(can) continue;
    go(d+1,r,2*a,b,A); go(d+1,r+M,2*a,b+a,A); return;
  }
}
struct Task{unsigned d;U r,a,b;};
static void gen(unsigned d,U r,U a,U b,unsigned S,std::vector<Task>&v,Acc&A){
  for(;;){
    U M=(U)1<<d;
    if((a<=M && (a<M||b<r)) || d==BITS){ go(d,r,a,b,A); return; }
    if(d==S){ v.push_back({d,r,a,b}); return; }
    bool can=false;
    if(!(a&1)){ if(!(b&1)){ a>>=1; b>>=1; can=true; }
                else if(!(a&3)){ if((b&3)==1){a*=5;b=5*b+1;} else {b+=1;} can=true; } }
    if(can) continue;
    gen(d+1,r,2*a,b,S,v,A); gen(d+1,r+M,2*a,b+a,S,v,A); return;
  }
}
int main(int c,char**v){
  BITS=atoi(v[1]);
  // known cycles
  U x=13; int per=0; do{x=T(x);per++;}while(x!=13&&per<1000); if(per!=35){printf("bad per %d\n",per);return 1;}
  std::vector<Task> tasks; Acc A0; gen(0,0,1,0,BITS<18?BITS:18,tasks,A0);
  U cov=A0.cov; uint64_t leaves=A0.leaves, direct=A0.direct;
  #pragma omp parallel for schedule(dynamic,1) reduction(+:leaves,direct)
  for(long i=0;i<(long)tasks.size();++i){ Acc A; go(tasks[i].d,tasks[i].r,tasks[i].a,tasks[i].b,A);
    leaves+=A.leaves; direct+=A.direct;
    #pragma omp critical
    cov+=A.cov; }
  U want=((U)1<<BITS)-1;
  printf("bits=%u leaves=%llu direct=%llu coverage_ok=%d\n",BITS,(unsigned long long)leaves,(unsigned long long)direct,(int)(cov==want));
  return cov==want?0:1;
}
