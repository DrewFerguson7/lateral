const fs=require('fs');const js=fs.readFileSync('out/gridiron-handoff.html','utf8').split('<script>')[1].split('</script>')[0];
const els={};const mk=id=>els[id]||(els[id]={id,textContent:'',innerHTML:'',className:'',value:'',hidden:false,style:{},focus(){},removeAttribute(){},onclick:null,onsubmit:null,oninput:null});
const mem={};let now=1e12;const RD=Date;class FD extends RD{constructor(...a){super(...(a.length?a:[now]))}static now(){return now}}
let timers=[],id=0;const si=f=>{timers.push({id:++id,f});return id},ci=x=>{timers=timers.filter(t=>t.id!==x)};const tick=ms=>{for(let t=0;t<ms;t+=250){now+=250;[...timers].forEach(x=>x.f())}};
const g=new Function('document','localStorage','navigator','setInterval','clearInterval','Date',js+';return{P,NM,has,lab,tab,bkGo,get BK(){return BK}}')({querySelector:s=>mk(s.replace('#',''))},{getItem:k=>k in mem?mem[k]:null,setItem:(k,v)=>mem[k]=v},{},si,ci,FD);
const txt=h=>h.replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
els.goBK.onclick();console.log('tab shown:',!els.gB.hidden,'| pre:',g.BK.ph,/bkHike/.test(els.bkCtl.innerHTML));
els.bkHike.onclick();const team=g.BK.ch[0];console.log('start team:',g.lab(team),'| board:',els.bkOn.textContent);
// play 6 correct moves greedily
for(let step=0;step<6;step++){const ch=g.BK.ch,cur=ch.at(-1);
 if(ch.length%2){const n=g.NM.find(x=>!ch.includes(x)&&g.has(x,cur)&&g.P[x].t.length+g.P[x].u.length+g.P[x].c.length>2);g.bkGo(n)}
 else{const p=g.P[cur],k=[...p.u.map(u=>'#'+u),...p.c.map(c=>'C:'+c),...p.t.map(t=>'T:'+t)].find(k=>!ch.includes(k));g.bkGo(g.lab(k))}}
console.log('after 6 moves:',g.BK.ch.map(x=>x[1]==':'||x[0]=='#'?g.lab(x):x).join(' → '),'| players:',txt(els.bkStats.innerHTML));
g.bkGo('Zzzz Nobody');console.log('unknown name (no strike):',g.BK.S,'|',g.BK.msg);
const wrong=g.BK.ch.length%2?'Tom Brady':'Akron Pros';g.bkGo(wrong);console.log('wrong answer strike:',g.BK.S,'|',g.BK.msg);
tick(31000);console.log('clock ran out strike:',g.BK.S,'|',g.BK.msg);
tick(31000);console.log('third strike ends:',g.BK.ph,'|',txt(els.bkCtl.innerHTML).slice(0,120),'| saved best:',mem.bkbest);
