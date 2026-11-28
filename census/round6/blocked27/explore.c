// Blocked mixed-base system: n = 26 mod 27 -> (n+1)/27; else even n -> n/2; else (3n+1)/2.
// Counts, per octave, starts not below themselves after b divisions-by-2 ("halvings"; the /27 step counts 0).
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
#define CAP 300
int main(int argc,char**argv){ int M=atoi(argv[1]); static uint64_t cnt[64][CAP+2]; uint64_t worst=0;
  for(uint64_t n=28;n<((uint64_t)1<<M);n++){ u128 x=n; int b=0,steps=0;
    while(b<CAP && steps<100000){ steps++;
      if(x%27==26){ x=(x+1)/27; } else if(!(x&1)){ x>>=1; b++; } else { x=(3*x+1)>>1; b++; }
      if(x<n) break; }
    int m=63-__builtin_clzll(n); cnt[m][b>CAP?CAP:b]++; if(b>=CAP) worst++; }
  for(int m=5;m<M;m++){ printf("%d",m); uint64_t t=0,c[CAP+2]; for(int b=CAP;b>=0;b--){t+=cnt[m][b];c[b]=t;}
    for(int b=0;b<=CAP;b++) printf(" %llu",(unsigned long long)c[b]); printf("\n"); }
  fprintf(stderr,"never dropped within %d halvings: %llu\n",CAP,(unsigned long long)worst); return 0; }
