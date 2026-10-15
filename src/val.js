// Validates every stored route against the built data: daily/unlimited solutions, Hard solutions, best routes, home examples, teammate hints.
const fs=require('fs');const js=fs.readFileSync('out/gridiron-handoff.html','utf8').split('<script>')[1].split('</script>')[0];
const el={textContent:'',innerHTML:'',style:{},focus(){},removeAttribute(){}};
const g=new Function('document','localStorage','navigator','setInterval','clearInterval',js+';return{Q,HR,MX,P,has,chk,set A(v){A=v},set B(v){B=v},set H(v){H=v},set RU(v){RU=v}}')({querySelector:()=>el},{getItem:()=>null,setItem(){}},{},()=>0,()=>0);
const bad=[];
const route=(s,why,rules)=>{const c=typeof s=='string'?s.split('>'):s;
 if(!c.every((x,i)=>i%2||g.P[x]))return bad.push([why,'unknown player',c.join('>')]);
 for(let i=1;i<c.length;i+=2){if(!g.has(c[i-1],c[i])||!g.has(c[i+1],c[i]))return bad.push([why,`${c[i-1]} / ${c[i+1]} don't share ${c[i]}`,c.join('>')])}
 if(new Set(c.filter((x,i)=>i%2)).size!=(c.length-1)/2)return bad.push([why,'connector reused',c.join('>')]);
 if(rules){g.H=1;g.RU=rules;g.A=c[0];g.B=c.at(-1);
  for(let i=1;i<c.length;i+=2){const v=g.chk('link',c[i],c.slice(0,i));if(v!==true)return bad.push([why,v,c.join('>')])}
  for(let i=2;i<c.length-1;i+=2){const v=g.chk('player',c[i]);if(v!==true)return bad.push([why,v,c.join('>')])}
  const v=g.chk('end',c);if(v!==true)bad.push([why,v,c.join('>')]);g.H=0}};
let n=0;
g.Q.forEach((e,qi)=>{const p=e.split('~');route(p[0],`puzzle ${qi} classic`);n++;if(p[1]&&p[1].includes('>')){route(p[1],`puzzle ${qi} alt`);n++}
 const B=p[0].split('>').at(-1);for(const m of (p[3]||'').split(';').filter(Boolean)){n++;if(!g.P[m])bad.push([`puzzle ${qi} hint`,'unknown teammate',m]);
  else if(!g.P[m].t.some(t=>g.P[B].t.includes(t)))bad.push([`puzzle ${qi} hint`,`${m} never shared a team with ${B}`,m])}
 const h=(g.HR[qi]||'').split('|');if(h[1]){route(h[1],`puzzle ${qi} hard`,h[0].split(','));n++}});
for(const[k,v]of Object.entries(g.MX))if(v&&v[0]){route(v[0],'best '+k);n++}
route(['Tom Brady','T:TB','Ronde Barber','#20','Ed Reed'],'home quick');
console.log('checked',n+2,'routes/hints | problems:',bad.length);for(const b of bad)console.log(JSON.stringify(b));
