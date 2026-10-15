const fs=require('fs');const js=fs.readFileSync('out/gridiron-handoff.html','utf8').split('<script>')[1].split('</script>')[0];
const el={textContent:'',innerHTML:'',style:{},focus(){},removeAttribute(){}};
const g=new Function('document','localStorage','navigator','setInterval','clearInterval',js+';return{Q,RULES,solveRules,set A(v){A=v},set B(v){B=v},set H(v){H=v},set RU(v){RU=v}}')({querySelector:()=>el},{getItem:()=>null,setItem(){}},{},()=>0,()=>0);
let seed=20261008;const rnd=()=>(seed=(seed*1103515245+12345)>>>0)/2**32;
const ids=['college','college','number','noteam','noqb','defense','old','mix','nomain','long'];
const clash=[['noteam','nomain'],['defense','noqb'],['college','college']];
const out=[],t0=Date.now(),cnt={};let rerolls=0;
g.H=1;
for(const e of g.Q){const p=e.split('~')[0].split('>');g.A=p[0];g.B=p.at(-1);let line=null;
 for(let tries=0;tries<12&&!line;tries++){const a=ids[rnd()*ids.length|0];let b=ids[rnd()*ids.length|0];if(a==b||clash.some(([x,y])=>(a==x&&b==y)||(a==y&&b==x))){tries--;continue}
  g.RU=[a,b];const s=g.solveRules();if(s){line=[a,b].join(',')+'|'+s.join('>');cnt[a]=(cnt[a]||0)+1;cnt[b]=(cnt[b]||0)+1}else rerolls++}
 if(!line){g.RU=['college'];const s=g.solveRules();line='college|'+(s?s.join('>'):p.join('>'))}
 out.push(line)}
fs.writeFileSync('hr.txt',out.join('\n'));
console.log(out.length,'puzzles in',((Date.now()-t0)/1000).toFixed(0)+'s | rerolls',rerolls,'| rule use',JSON.stringify(cnt));
console.log(out.slice(0,5).join('\n'));
