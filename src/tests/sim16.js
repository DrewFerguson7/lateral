const fs=require('fs');const js=fs.readFileSync('out/gridiron-handoff.html','utf8').split('<script>')[1].split('</script>')[0];
const els={};const mk=id=>els[id]||(els[id]={id,textContent:'',innerHTML:'',className:'',value:'',hidden:false,style:{},focus(){},removeAttribute(){},onclick:null});
const mem={};let now=1e12;const RD=Date;class FD extends RD{constructor(...a){super(...(a.length?a:[now]))}static now(){return now}}
let timers=[],id=0;const si=f=>{timers.push({id:++id,f});return id},ci=x=>{timers=timers.filter(t=>t.id!==x)};const sec=n=>{for(let i=0;i<n;i++){now+=1000;[...timers].forEach(t=>t.f())}};
let clip='';const g=new Function('document','localStorage','navigator','setInterval','clearInterval','Date',js+';return{P,HR,Q,has,chk,lab,go,mode,PG,set A(v){A=v},set B(v){B=v},set H(v){H=v},set RU(v){RU=v},get RU(){return RU},get sol(){return sol},get msg(){return msg},get C(){return C},get A(){return A},get B(){return B}}')({querySelector:s=>mk(s.replace('#',''))},{getItem:k=>k in mem?mem[k]:null,setItem:(k,v)=>mem[k]=v},{clipboard:{writeText:t=>{clip=t;return Promise.resolve()}}},si,ci,FD);
const txt=h=>h.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
// every stored Hard solution obeys its own rules
let bad=0;g.HR.forEach(l=>{const[r,s]=l.split('|'),ch=s.split('>');g.H=1;g.RU=r.split(',');g.A=ch[0];g.B=ch.at(-1);for(let i=1;i<ch.length;i+=2){if(!g.has(ch[i-1],ch[i])||!g.has(ch[i+1],ch[i])||g.chk('link',ch[i],ch.slice(0,i))!==true)bad++;if(i+1<ch.length-1&&g.chk('player',ch[i+1])!==true)bad++}if(g.chk('end',ch)!==true)bad++});
console.log('Hard solutions checked:',g.HR.length,'| rule violations:',bad);
// classic daily: clock visible during play, penalties
g.mode(0,0);els.hike.onclick();sec(8);sec(25);console.log('classic stats in play:',txt(els.stats.innerHTML));
g.go('Zzzz');const s=g.sol;g.go(g.lab(s[1]));g.go('Tom Brady');console.log('miss msg:',g.msg);
for(let i=2;i<s.length;i++)g.go(i%2?g.lab(s[i]):s[i]);console.log('classic end:',txt(els.ctl.innerHTML).slice(0,400));
els.share.onclick();await0=()=>0;
// hard daily
g.mode(0,1);console.log('hard rules:',g.RU,'| cards before hike:',txt(els.rcards.innerHTML));els.hike.onclick();sec(8);
const hs=g.sol;console.log('hard example route:',hs.map((x,i)=>i%2?g.lab(x):x).join(' → '));
// try a rule-breaking move if possible
if(g.RU.includes('noteam')){g.go(g.P[g.A].t[0]?g.lab('T:'+g.P[g.A].t[0]):'x');console.log('noteam msg:',g.msg)}
if(g.RU.includes('noqb')||g.RU.includes('defense')){const k=hs[1];const qb=Object.keys(g.P).find(n=>n!=g.A&&n!=g.B&&g.has(n,k)&&g.PG(g.P[n].pos)=='QB');if(qb){g.go(g.lab(k));g.go(qb);console.log('player-rule msg:',g.msg);if(g.C.length%2==0)g.C.pop()}}
for(let i=g.C.length;i<hs.length;i++)g.go(i%2?g.lab(hs[i]):hs[i]);
console.log('hard end:',txt(els.ctl.innerHTML).slice(0,300));
setTimeout(()=>console.log('share:',JSON.stringify(clip)),0);
