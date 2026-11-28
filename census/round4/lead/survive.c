// Counts, per octave [2^m, 2^{m+1}), the starts n whose orbit has not gone below n after b halvings.
// usage: survive <system 0=split5_3 1=3x+1 2=K7 3=3x-1 4=3x+5> <M>   (n < 2^M).  Exact integer arithmetic (128-bit).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
#define CAP 600
static inline u128 step(int sys, u128 x, int *halved){
  *halved = 0;
  if (sys==0){ if(!(x&1)){*halved=1;return x>>1;} return ((x&3)==1)? 5*x+3 : x+3; }
  if (sys==1){ if(!(x&1)){*halved=1;return x>>1;} return 3*x+1; }
  if (sys==3){ if(!(x&1)){*halved=1;return x>>1;} return 3*x-1; }
  if (sys==4){ if(!(x&1)){*halved=1;return x>>1;} return 3*x+5; }
  /* K7 on z>=0 */ if(!(x&1)){*halved=1;return x>>1;} if((x&3)==3){*halved=1;return (3*x+1)>>1;} *halved=2; return (x-1)>>2;
}
int main(int argc,char**argv){
  int sys=atoi(argv[1]), M=atoi(argv[2]);
  static uint64_t cnt[64][CAP+2];
  for(uint64_t n=64; n<((uint64_t)1<<M); n++){
    u128 x=n; int b=0,h;
    while(b<CAP){ x=step(sys,x,&h); b+=h; if(x<n) break; }
    int m=63-__builtin_clzll(n);
    cnt[m][b>CAP?CAP:b]++;          // b = halvings used when it first went below n (CAP: did not)
  }
  for(int m=6;m<M;m++){ printf("%d",m); uint64_t tail=0; uint64_t c[CAP+2];
    for(int b=CAP;b>=0;b--){ tail+=cnt[m][b]; c[b]=tail; }   // c[b] = #{sigma >= b}
    for(int b=0;b<=CAP;b++) printf(" %llu",(unsigned long long)c[b]); printf("\n"); }
  return 0;
}
