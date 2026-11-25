#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int c,char**v){ int B=atoi(v[1]); uint64_t N=1ULL<<B; long bad=0;
#pragma omp parallel for schedule(static,1<<16) reduction(+:bad)
 for(uint64_t n=1;n<N;n++){ unsigned __int128 x=n; long s=0;
   while(!(x<n||x==1||x==13)){ x = (x&1)? (((x&3)==1)?5*x+1:x+1) : x>>1; if(++s>10000000){bad++;break;} } }
 printf("brute bits=%d unresolved=%ld\n",B,bad); return bad!=0; }
