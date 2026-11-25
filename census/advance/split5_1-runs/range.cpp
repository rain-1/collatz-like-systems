// Exact residue-tree certificate: every 1 <= n < 2^bits reaches a known cycle
// of the split5_1 map T: even n -> n/2; n=1 mod 4 -> 5n+1; n=3 mod 4 -> n+1.
// Build: g++ -O2 -std=c++17 -fopenmp range.cpp -o range ; run: ./range bits
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using U = unsigned __int128;

static std::string dec(U n){std::string s;do{s.push_back('0'+int(n%10));n/=10;}while(n);std::reverse(s.begin(),s.end());return s;}
static const U LIMIT = (~U{0}) / 8;
static inline U step(U n){
    if(!(n&1)) return n>>1;
    if(n > LIMIT) throw std::overflow_error("overflow");
    return (n&3)==1 ? 5*n+1 : n+1;
}
// minima of the two known cycles
static inline bool is_root(U n){ return n==1 || n==13; }

struct Cert {
    unsigned bits;
    U covered=0; uint64_t nodes=0, direct=0, maxsteps=0, maxdepth_leaves=0;
    // n = 2^d t + r ; the value a t + b is an iterate T^s(n), s >= 0
    void visit(unsigned d, U r, U a, U b){
        ++nodes;
        const U M = U{1}<<d;
        if(a < M || (a==M && b<r) || d==bits){
            U stop = U{1}<<(bits-d);
            const U first = (r==0)?1:0;
            covered += stop-first;
            if(a<=M && b<r) return;           // a t + b < M t + r for all t >= 0
            if(d==bits) ++maxdepth_leaves;
            if(a<M){ U lim=(b-r)/(M-a)+1; if(lim<stop) stop=lim; } // larger t descend
            for(U t=first;t<stop;++t){
                const U n=M*t+r; U x=a*t+b; ++direct; uint64_t s=0;
                while(x>=n && !is_root(x)){
                    if(++s>1000000) throw std::runtime_error("unresolved "+dec(n));
                    x=step(x);
                }
                if(s>maxsteps) maxsteps=s;
            }
            return;
        }
        for(unsigned g=0; g<2; ++g){
            const U cr=r+g*M, y=b+g*a;      // child: value 2a u + y
            if(!(y&1)) visit(d+1,cr,a,y>>1);                 // even: halve
            else if(a&1) visit(d+1,cr,2*a,y);                // odd, residue mod 4 unknown
            else if((y&3)==1) visit(d+1,cr,5*a,(5*y+1)>>1);  // 5x+1 then /2
            else visit(d+1,cr,a,(y+1)>>1);                   // x+1 then /2
        }
    }
};

int main(int argc,char**argv){
    unsigned bits = argc>1? std::stoul(argv[1]) : 40;
    if(bits<20||bits>60) throw std::invalid_argument("bits in [20,60]");
    // check the known cycles: 1 has period 5, 13 has period 35, and both minima
    for(auto [root,per] : std::vector<std::pair<unsigned,unsigned>>{{1,5},{13,35}}){
        U x=root; U mn=root;
        for(unsigned j=1;j<=per;++j){ x=step(x); mn=std::min(mn,x); if((x==root)!=(j==per)) throw std::logic_error("period"); }
        if(mn!=root) throw std::logic_error("minimum");
    }
    // Split the tree at depth SPLIT (no closure happens before depth 3 anyway;
    // nodes closed earlier are handled by a serial pass) and run subtrees in parallel.
    const unsigned SPLIT=14;
    struct Task{unsigned d;U r,a,b;};
    std::vector<Task> tasks; Cert serial{bits};
    // serial expansion to depth SPLIT, with identical closure logic
    std::vector<Task> stack{{0,0,1,0}};
    while(!stack.empty()){
        Task t=stack.back(); stack.pop_back();
        const U M=U{1}<<t.d;
        bool closes = t.a<M || (t.a==M && t.b<t.r);
        if(closes || t.d==SPLIT){ if(closes) serial.visit(t.d,t.r,t.a,t.b); else tasks.push_back(t); continue; }
        ++serial.nodes;
        for(unsigned g=0;g<2;++g){
            const U cr=t.r+g*M, y=t.b+g*t.a;
            if(!(y&1)) stack.push_back({t.d+1,cr,t.a,y>>1});
            else if(t.a&1) stack.push_back({t.d+1,cr,2*t.a,y});
            else if((y&3)==1) stack.push_back({t.d+1,cr,5*t.a,(5*y+1)>>1});
            else stack.push_back({t.d+1,cr,t.a,(y+1)>>1});
        }
    }
    U covered=serial.covered; uint64_t nodes=serial.nodes, direct=serial.direct, maxs=serial.maxsteps, deep=serial.maxdepth_leaves;
    bool fail=false; std::string msg;
    #pragma omp parallel for schedule(dynamic,1) reduction(+:nodes,direct,deep) reduction(max:maxs)
    for(long i=0;i<(long)tasks.size();++i){
        Cert c{bits};
        try{ c.visit(tasks[i].d,tasks[i].r,tasks[i].a,tasks[i].b);}catch(std::exception&e){
            #pragma omp critical
            {fail=true; msg=e.what();}
        }
        nodes+=c.nodes; direct+=c.direct; deep+=c.maxdepth_leaves; maxs=std::max(maxs,c.maxsteps);
        #pragma omp critical
        covered+=c.covered;
    }
    if(fail){ std::cerr<<"FAIL "<<msg<<"\n"; return 1; }
    if(covered != (U{1}<<bits)-1){ std::cerr<<"FAIL coverage "<<dec(covered)<<"\n"; return 1; }
    std::cout<<"bits="<<bits<<" covered="<<dec(covered)<<" nodes="<<nodes<<" direct="<<direct
             <<" depth-cap leaves="<<deep<<" max extra steps="<<maxs<<"\n";
    return 0;
}
