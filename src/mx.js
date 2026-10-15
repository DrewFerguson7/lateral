const fs=require('fs');const js=fs.readFileSync('out/gridiron-handoff.html','utf8').split('<script>')[1].split('</script>')[0];
const el={textContent:'',innerHTML:'',style:{},focus(){},removeAttribute(){}};
const g=new Function('document','localStorage','navigator','setInterval','clearInterval',js+';return{Q,searchBest,scoreChain,set A(v){A=v},set B(v){B=v},set H(v){H=v},set sol(v){sol=v}}')({querySelector:()=>el},{getItem:()=>null,setItem(){}},{},()=>0,()=>0);
const lim=+process.argv[2]||Infinity,out={},t0=Date.now();let n3=0,n=0;
const jobs=g.Q.slice(0,lim).flatMap(e=>{const p=e.split('~');return[[p[0].split('>'),0],[p[1].split('>'),1]]});jobs.push([['Tom Brady','T:TB','Mike Evans','#13','Odell Beckham'],0]);
for(const [s,h] of jobs){const A=s[0],B=s.at(-1);g.H=h;g.A=A;g.B=B;g.sol=s;const[bp,bv]=g.searchBest(A,B);out[A+'>'+B+'>'+h]=[bp.join('>'),bv];n++;if(bp.length>5)n3++;}
console.log(n,'searched in',((Date.now()-t0)/1000).toFixed(1)+'s | best route is 3 handoffs in',n3);
if(lim===Infinity)fs.writeFileSync('mx.json',JSON.stringify(out));
