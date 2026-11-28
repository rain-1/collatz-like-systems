// Exact survivor sets R_b (slope definition) and the local functions g_sigma for three base-2 table maps.
// Systems: 0 = split5_3, 1 = 3x+1, 2 = K7.  A map is a table on x mod Q = 2^kQ: x -> (u x + v)/2^e.
// Node rule (round3/density/theory.md, Lemma 1): with s known low bits of the current value x, a step is
// applied iff every residue mod Q congruent to x mod 2^min(s,kQ) uses the same row; it consumes e bits.
// Survival: the slope U/2^h (U = product of multipliers, h = halvings) is >= 1 after every step.
//
// usage:
//   rb bitmap SYS b FILE        write one byte per residue r < 2^b: 1 iff r in R_b
//   rb count  SYS b m           print |R_b| and the histogram of the top m digits of r over R_b
//   rb gfun   SYS L s c0 FILE   for the node state (s known bits, value = c0 mod 2^s) and z < 2^L,
//                               process the L further digits; write per z the pair (U,h) at the minimum
//                               prefix slope (uint64 U, int32 h), the minimum taken over prefixes incl. start (1,0)
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned __int128 u128;
typedef __int128 i128;
static int kQ; static int nrow; static long U_[4], V_[4]; static int E_[4]; static int row_of[16];
static int dec[8][16];  // dec[k][x mod 2^k] = row or -1
static void setup(int sys){
  if(sys==0){ kQ=2; nrow=3; U_[0]=1;V_[0]=0;E_[0]=1; U_[1]=5;V_[1]=3;E_[1]=0; U_[2]=1;V_[2]=3;E_[2]=0;
    row_of[0]=0;row_of[2]=0;row_of[1]=1;row_of[3]=2; }
  else if(sys==1){ kQ=1; nrow=2; U_[0]=1;V_[0]=0;E_[0]=1; U_[1]=3;V_[1]=1;E_[1]=0; row_of[0]=0;row_of[1]=1; }
  else { kQ=2; nrow=3; U_[0]=1;V_[0]=0;E_[0]=1; U_[1]=3;V_[1]=1;E_[1]=1; U_[2]=1;V_[2]=-1;E_[2]=2;
    row_of[0]=0;row_of[2]=0;row_of[3]=1;row_of[1]=2; }
  int Q=1<<kQ;
  for(int k=0;k<=kQ;k++) for(int c=0;c<(1<<k);c++){ int rw=-2;
    for(int r=0;r<Q;r++) if((r&((1<<k)-1))==c){ if(rw==-2) rw=row_of[r]; else if(rw!=row_of[r]) rw=-1; }
    dec[k][c]=rw; }
}
// run from value x with s known bits, slope (U,h) relative; returns 1 if survives all determined steps.
// tracks minimum prefix slope (mU,mh) if track != 0.  Slope compare: U >= 2^h  <=> survive.
static inline int run(i128 x, int s, int track, uint64_t *mU, int *mh){
  u128 U=1; int h=0; u128 bU=1; int bh=0;   // best (minimum) ratio so far
  for(;;){
    int k = s<kQ? s : kQ; int rw = dec[k][(int)(x & ((1<<k)-1))];
    if(rw<0) break;
    x = (U_[rw]*x + V_[rw]); x >>= E_[rw];  // exact: divisibility guaranteed by the table
    U *= (u128)U_[rw]; h += E_[rw]; s -= E_[rw];
    if(track){ // compare U/2^h < bU/2^bh  <=> U*2^bh < bU*2^h
      if( (U<<bh) < (bU<<h) ){ bU=U; bh=h; } }
    else if( U < ((u128)1<<h) ) return 0;
    if(U > ((u128)1<<100)) { U >>= 1; } // unreachable for the sizes used (guard)
  }
  if(track){ *mU=(uint64_t)bU; *mh=bh; }
  return 1;
}
int main(int argc,char**argv){
  if(argc<4){fprintf(stderr,"usage\n");return 2;}
  int sys=atoi(argv[2]); setup(sys);
  if(!strcmp(argv[1],"bitmap")){
    int b=atoi(argv[3]); uint64_t N=1ULL<<b; uint8_t *bm=malloc(N);
    for(uint64_t r=0;r<N;r++) bm[r]=(uint8_t)run((i128)r,b,0,0,0);
    FILE*f=fopen(argv[4],"wb"); fwrite(bm,1,N,f); fclose(f); return 0; }
  if(!strcmp(argv[1],"count")){
    int b=atoi(argv[3]), m=atoi(argv[4]); uint64_t N=1ULL<<b; uint64_t *hist=calloc(1u<<m,8); uint64_t tot=0;
    for(uint64_t r=0;r<N;r++) if(run((i128)r,b,0,0,0)){ tot++; hist[r>>(b-m)]++; }
    printf("%llu",(unsigned long long)tot); for(int k=0;k<(1<<m);k++) printf(" %llu",(unsigned long long)hist[k]);
    printf("\n"); return 0; }
  if(!strcmp(argv[1],"gfun")){
    int L=atoi(argv[3]), s=atoi(argv[4]); long c0=atol(argv[5]); uint64_t N=1ULL<<L;
    uint64_t *Us=malloc(8*N); int32_t *hs=malloc(4*N);
    for(uint64_t z=0;z<N;z++){ uint64_t mU; int mh; run((i128)c0 + ((i128)z<<s), s+L, 1, &mU, &mh); Us[z]=mU; hs[z]=mh; }
    FILE*f=fopen(argv[6],"wb"); fwrite(Us,8,N,f); fwrite(hs,4,N,f); fclose(f); return 0; }
  return 2;
}
