// own brute force: every n < 2^31 descends below itself or hits cycle min 1 or 13; plus random samples < 2^42
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
static int ok(uint64_t n){ unsigned __int128 x=n; long s=0;
  if(n==1||n==13) return 1;
  while(1){ if(x&1) x = ((x&3)==1)? 5*x+1 : x+1; else x>>=1; s++;
    if(x<n) return 1; if(x==1||x==13) return 1; if(s>100000) return 0; if(x==n) return 0; } }
int main(){ uint64_t bad=0;
  #pragma omp parallel for reduction(+:bad) schedule(dynamic,65536)
  for(uint64_t n=1;n<(1ULL<<31);n++) if(!ok(n)) bad++;
  uint64_t s=88172645463325252ULL; uint64_t bad2=0;
  for(int i=0;i<10000000;i++){ s^=s<<13; s^=s>>7; s^=s<<17; uint64_t n=(s%((1ULL<<42)-(1ULL<<31)))+(1ULL<<31); if(!ok(n)) bad2++; }
  printf("brute n<2^31 bad=%llu; random 1e7 in [2^31,2^42) bad=%llu\n",(unsigned long long)bad,(unsigned long long)bad2); return bad||bad2; }
