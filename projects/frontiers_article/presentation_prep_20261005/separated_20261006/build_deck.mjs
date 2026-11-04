import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile,FileBlob} from '@oai/artifact-tool';
import {resolvePresentationFont,applyPresentationChartFont,finalizePresentation} from '/Users/omer/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations/container_tools/artifact_tool_utils.mjs';
const ROOT='/Users/omer/workspace/personal/repos/gifted-masking';
const PACK=path.join(ROOT,'projects/frontiers_article/presentation_prep_20261005/separated_20261006');
const SOURCEPACK=path.join(ROOT,'projects/frontiers_article/presentation_prep_20261005/results_discussion_20261006');
const W='/private/tmp/gifted-separated-deck-20261006';
const SKILL='/Users/omer/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations';
const V=process.env.DECK_VERSION||'v1';
const D=JSON.parse(await fs.readFile(path.join(SOURCEPACK,'DATA.json'),'utf8'));
const font=resolvePresentationFont({fontFamily:'Helvetica Neue'});
const C={bg:'#F6F3ED',ink:'#18363D',muted:'#52656B',teal:'#006B69',blue:'#496F8A',rust:'#B85E45',gold:'#B28A42',light:'#DCE8E4',grid:'#D6DCD7',white:'#FFFFFF',gray:'#C8C8C2'};
const lecture=JSON.parse(await fs.readFile(path.join(PACK,'NOTES.json'),'utf8'));
const original=await PresentationFile.importPptx(await FileBlob.load(path.join(ROOT,'output/pptx/masking_mechanisms_first_set.pptx')));
const proto=original.toProto();proto.slides=proto.slides.slice(0,3);proto.charts=[];
const P=Presentation.load(proto);let count=1000;const spec=[];
const openingRefs=JSON.parse(await fs.readFile(path.join(PACK,'OPENING_SOURCES.json'),'utf8'));
const originalSpec=JSON.parse(await fs.readFile(path.join(ROOT,'projects/frontiers_article/presentation_prep_20261005/SLIDE_SPEC.json'),'utf8')).slides;
for(let i=0;i<3;i++){
 const s=P.slides.items[i],old=s.speakerNotes.textFrame.toString();
 const meta=lecture[i];
 s.speakerNotes.textFrame.setText(meta.script+'\n\nTiming: '+meta.seconds+' seconds.\n\nSource notes from opening slide:\n'+openingRefs[i]);
 spec.push({slide:i+1,title:originalSpec[i].title,...meta,sources:['Opening slides from masking_mechanisms_first_set.pptx']});
}

function tx(s,t,x,y,w,h,size=28,color=C.ink,bold=false,align='left'){const o=s.shapes.add({name:'text-'+(++count),geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});o.text=t;o.text.style={typeface:font,fontSize:size,color,bold,alignment:align,autoFit:'none'};return o;}
function rect(s,x,y,w,h,fill,line='none',lw=0){return s.shapes.add({name:'shape-'+(++count),geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:line,width:lw}});}
function node(s,t,x,y,w,h,color=C.teal){const o=s.shapes.add({name:'node-'+(++count),geometry:'roundRect',position:{left:x,top:y,width:w,height:h},fill:C.bg,line:{fill:color,width:2}});o.text=t;o.text.style={typeface:font,fontSize:27,color,bold:true,alignment:'center',verticalAlignment:'middle',autoFit:'none'};return o;}
function arrow(s,a,b,from='right',to='left',kind='straight',color=C.muted){return s.shapes.connect(a,b,{kind,fromSide:from,toSide:to,line:{fill:color,width:2.4},tail:{type:'triangle',width:'sm',length:'sm'}});}
function table(s,values,x,y,w,h,widths,size=24){const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,columnWidths:widths,values});t.borders.assign({fill:C.grid,width:.8,style:'solid'});for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){const cell=t.getCell(r,c);cell.fill=r?C.bg:C.ink;cell.text.style={typeface:font,fontSize:size,color:r?C.ink:C.white,bold:r===0,autoFit:'none'};}return t;}
function base(title,subtitle,footer,seconds,script,keys,extra=''){
 const meta=lecture[spec.length];seconds=meta.seconds;script=meta.script;
 const s=P.slides.add();s.background.fill=C.bg;
 tx(s,title,64,34,1150,119,45,C.ink,true);
 if(subtitle)tx(s,meta.section.toUpperCase()+' · '+subtitle,68,165,1144,53,25,C.muted);
 tx(s,footer,68,654,1090,55,17,C.muted);
 tx(s,String(spec.length+1).padStart(2,'0'),1180,672,40,25,16,C.muted,false,'right');
 const sources=keys.map(k=>D.sources[k]?.path||k);
 s.speakerNotes.textFrame.setText(script+'\n\nTiming: '+seconds+' seconds.\n\nSources:\n'+sources.map(f=>path.join(ROOT,f)).join('\n')+'\n\nTechnical detail:\n'+extra);
 spec.push({slide:spec.length+1,title:title.replaceAll('\n',' '),...meta,sources,qualification:extra});return s;
}

const axis={typeface:font,fontSize:21,fill:C.muted};const none={fill:'none',width:0};
function chart(s,type,opt){const c=s.charts.add(type,{titlePlacement:'none',chartFill:C.bg,plotAreaFill:C.bg,chartLine:none,plotAreaLine:none,...opt});applyPresentationChartFont(c,{fontFamily:font});return c;}
function fmt(v){return (v<0?'−':'+')+Math.abs(v).toFixed(2);}
function forest(s,items,pos,min,max,unit){let series=[{name:'Zero reference',xValues:[0,0],values:[-.55,1.55],line:{fill:C.gray,width:1.5},marker:{symbol:'none'}}];for(let i=0;i<items.length;i++){const e=items[i],y=1-i,color=e.color||C.teal;series.push({name:'95% interval '+i,xValues:[e.low,e.high],values:[y,y],line:{fill:color,width:3},marker:{symbol:'none'}},{name:'Lower cap '+i,xValues:[e.low,e.low],values:[y-.045,y+.045],line:{fill:color,width:2},marker:{symbol:'none'}},{name:'Upper cap '+i,xValues:[e.high,e.high],values:[y-.045,y+.045],line:{fill:color,width:2},marker:{symbol:'none'}},{name:e.name,xValues:[e.estimate],values:[y],line:{fill:color,width:0},fill:color,marker:{symbol:'circle',size:9},dataLabelOverrides:[{idx:0,text:fmt(e.estimate)+' pp',position:'t',showValue:true,textStyle:{typeface:font,fontSize:26,fill:color,bold:true}}]});}
return chart(s,'scatter',{position:pos,series,scatterOptions:{style:'lineWithMarkers'},hasLegend:false,xAxis:{min,max,majorUnit:unit,numberFormatCode:'0',textStyle:axis,majorGridlines:{fill:C.grid,width:1}},yAxis:{visible:false,tickLabelPosition:'none',line:{fill:'none',width:0},min:-.55,max:1.55,majorUnit:1,textStyle:axis,majorGridlines:null}});}

// Five methods-only slides. Numerical values here define rewards or design, not findings.
{
const s=base('M0  Two actions in a fixed environment','Two-armed bandit','E01 compares feedback histories and information conditions. Example rewards: b=1, a=.6, c=.25, r=2.',55,'',['src/gifted_masking/models/m0.py','src/gifted_masking/core.py','configs/frontiers_article/e01_hot_stove_standard.json'],'Expected rewards: mask=b−c; auth=a+p b−(1−p)r. Chosen Q <- Q+alpha[v(R)−Q]. v(R)=R if R>=0, lambda R otherwise. Softmax probabilities are proportional to exp(Q/tau). No persistent social state.');
const choose=node(s,'Choose',68,319,155,70,C.ink);
const mask=node(s,'Mask',318,251,210,70,C.blue),auth=node(s,'Authentic',318,403,210,70,C.teal);
arrow(s,choose,mask);arrow(s,choose,auth);
const certain=tx(s,'Certain payoff',603,252,336,42,29,C.blue,true);tx(s,'b − c = 0.75',964,252,252,45,29,C.blue,true);
const acceptedLabel=tx(s,'Accepted with probability p',603,373,491,42,27,C.teal,true);tx(s,'b + a = 1.60',964,417,250,45,28,C.teal,true);
const rejectedLabel=tx(s,'Rejected with probability 1 − p',603,462,554,42,27,C.rust,true);tx(s,'a − r = −1.40',964,506,250,45,28,C.rust,true);
arrow(s,mask,certain);arrow(s,auth,acceptedLabel);arrow(s,auth,rejectedLabel);
// Outcome branches are labels on the authentic action, not additional choices.
tx(s,'Actions: 2 behaviours',68,548,508,42,28,C.ink,true);
tx(s,'State: fixed environment',68,591,507,42,27,C.muted);
tx(s,'Learner: Q(Mask), Q(Auth)',602,591,610,42,28,C.ink,true);
}
{
const s=base('M1  Graded disclosure','Five actions between masking and full authenticity','E02 compares graded and binary actions after initial feedback; outcomes separate participation, intensity and full authenticity.',45,'',['src/gifted_masking/models/m1.py','configs/frontiers_article/e02_binary_graded_standard.json'],'Disclosure d in {0,.25,.5,.75,1}. Acceptance probability=1−(1−p)d. Reward base=a d−c(1−d), plus b on acceptance or minus r on rejection. Separate Q for each d; only chosen action updated. No state transitions or transfer/generalization.');
tx(s,'Action space',68,244,600,40,28,C.ink,true);
table(s,[['0','0.25','0.50','0.75','1'],['Q(0)','Q(.25)','Q(.50)','Q(.75)','Q(1)']],68,296,1144,111,[229,229,229,229,228],29);
tx(s,'Masking',69,415,220,38,25,C.blue,true);tx(s,'Full authenticity',925,415,285,38,25,C.teal,true,'right');
tx(s,'Acceptance probability: 1 − (1 − p)d',68,482,1144,47,32,C.ink,true);
tx(s,'State: fixed receptivity p',68,548,538,42,29,C.muted);
tx(s,'Learner: five independent Q-values',645,548,569,44,29,C.ink,true);
tx(s,'Experience at one level updates that level only.',68,605,1144,38,27,C.teal,true);
}
{
const s=base('M2  Persistent social states','Two actions in every state; Q-learning includes future value','Reward precedes the next state. Masking preserves state unless the separate turnover or escape process occurs.',75,'',['src/gifted_masking/models/m2.py','src/gifted_masking/analysis/m2_optimal.py','configs/frontiers_article/e03_m2_regime_standard.json'],'States Neutral, Accepted, Stigmatized. From Neutral, authenticity accepts with p; otherwise stigma. Accepted authenticity pays b+a, then turnover delta can reset Neutral. Stigmatized masking pays b2−c; authenticity redeems with p/2 for b+a or fails for a−r2. Escape eta applies only if still stigmatized after the action. Newly entered Accepted/Stigmatized are not immediately subjected to turnover/escape. Q(s,a) <- Q(s,a)+alpha[v(R)+gamma max Q(s_next,.)−Q(s,a)]. Oracle uses objective untransformed rewards and gamma=.9.');
const n=node(s,'Neutral',69,335,177,75,C.ink),a=node(s,'Accepted',443,255,225,75,C.teal),st=node(s,'Stigmatized',443,420,225,75,C.rust);
arrow(s,n,a);arrow(s,n,st);
tx(s,'Authentic +\nacceptance',265,249,172,77,24,C.teal,true);tx(s,'Authentic +\nrejection',265,429,173,74,24,C.rust,true);
tx(s,'State space',68,223,360,35,25,C.muted);
tx(s,'Learner memory: 3 × 2 values',729,229,482,43,28,C.ink,true);
table(s,[['State','Mask','Authentic'],['Neutral','Q(N,M)','Q(N,A)'],['Accepted','Q(A,M)','Q(A,A)'],['Stigmatized','Q(S,M)','Q(S,A)']],731,296,481,201,[181,142,158],22);
tx(s,'Accepted: turnover δ can return the learner to Neutral.',68,530,1144,42,29);
tx(s,'Stigmatized: redemption p/2; otherwise escape η may return to Neutral.',68,579,1144,62,27);
}
{
const s=base('M3  Choosing a group and a behaviour','Group receptivities are fixed; the flat model has 2K actions','E04 varies K and the action representation. E05 subtracts comparison cost only from accepted authenticity in the receptive group.',70,'',['src/gifted_masking/models/m3.py','configs/frontiers_article/e04_m3_search_architectures_standard.json','configs/frontiers_article/e05_m3_bflpe_crossover_standard.json'],'Flat action a decodes to group=floor(a/2) and authenticity=(a mod 2)==1. One good group p_good=.85; others p_bad=.20 in reference design. Mask payoff b−c is shared in the environment but its Q-values are separate in flat model. Hierarchical policy chooses group then behavior. Global-mask representation has K authentic-in-group arms plus one masking arm. A selected group is an action component, not an M2 persistent state. Comparison cost bf subtracts only from b+a on accepted authentic trials in good group.');
tx(s,'Action space in the flat model',68,236,1144,43,29,C.ink,true);
table(s,[['Receptive group','Other group','… Group K'],['Mask₁','Mask₂','Maskₖ'],['Authentic₁','Authentic₂','Authenticₖ']],68,291,1144,189,[381,381,382],27);
tx(s,'State: fixed group probabilities',68,504,558,43,27,C.muted);
tx(s,'Learner: 2K action values',694,504,520,43,28,C.ink,true);
tx(s,'Alternative representations',68,561,421,37,24,C.muted,true);
tx(s,'Choose group, then behaviour   |   Share one masking action',68,602,1144,42,28,C.teal,true);
}
{
const s=base('M4  Behaviour changes receptivity','Two actions; a continuous environmental variable pₜ','Reward first, then Q update, then receptivity update. Bounds are p_min=.05 and p_max=.95; update directions are assumptions.',55,'',['src/gifted_masking/models/m4.py','src/gifted_masking/experiments/e06.py'],'Each learner carries p_t bounded in [p_min,p_max], but only Q(Mask),Q(Auth). Accepted auth: next p=p+ka(p_max−p). Rejected auth: p−kr(p−p_min). Mask: p−km(p−p_min). Reward is sampled using current p; action Q updated before p changes. Endogenous nonstationary bandit, not an MDP learner conditioned on p_t. Formal E06 evidence is deferred.');
const act=node(s,'Mask or\nAuthentic',68,250,261,88,C.teal),out=node(s,'Outcome at\ncurrent pₜ',487,250,283,88,C.ink),future=node(s,'Update pₜ',928,250,284,88,C.blue);
arrow(s,act,out);arrow(s,out,future);
const h1=rect(s,1070,379,1,1,'none'),h2=rect(s,625,379,1,1,'none');
s.shapes.connect(future,h1,{kind:'straight',fromSide:'bottom',toSide:'top',line:{fill:C.blue,width:2.4}});
s.shapes.connect(h1,h2,{kind:'straight',fromSide:'left',toSide:'right',line:{fill:C.blue,width:2.4}});arrow(s,h2,out,'top','bottom','straight',C.blue);
table(s,[['Event','Change in pₜ'],['Accepted authenticity','+ kₐ(p_max − pₜ)'],['Rejected authenticity','− kᵣ(pₜ − p_min)'],['Masking','− kₘ(pₜ − p_min)']],68,440,675,183,[355,320],25);
tx(s,'Environment',819,440,397,36,24,C.muted,true);tx(s,'Changing receptivity pₜ',819,479,395,44,29,C.blue,true);
tx(s,'Learner memory',819,538,397,36,24,C.muted,true);tx(s,'Q(Mask), Q(Auth) only',819,577,395,44,29,C.ink,true);
}

// Result 1: two panels, distinct contrasts and windows.
{
const script='M0 lets us separate learning from changes in the opportunity itself. On the left, initial rejection reduces subsequent authentic sampling by about two point six percentage points, compared with initial acceptance. But the final-window masking contrast is close to zero, with an interval that spans zero. This history comparison therefore does not establish a lasting final-window difference. On the right, we change what initially rejected learners can experience or learn. Requiring authenticity on five percent of later interactions reduces final masking by about four point seven points. Providing authentic feedback even on masking trials reduces it by about eleven point eight points. The unchosen reward is not added to the learner’s actual return. The two interventions have different intensities, so this comparison does not rank them as practical treatments. What the model establishes is that experience and access to information can change later allocation while environmental payoffs remain fixed.';
const s=base('Feedback changes behaviour\nunder unchanged opportunities','M0 / E01: p=.75/.85 exceeds objective indifference at p*=.717','Five masters; p=.75/.85 pooled, λ=1. Dots show estimates; lines show 95% intervals. pp = percentage points.',90,script,['E01_PRIMARY','E01_INTERVENTIONS'],'History: rejection minus acceptance. Information: intervention minus baseline in the rejected stratum. History sampling uses steps 1–1999; masking uses the last 400 of T=2000 steps. n=500/cell/master.');
tx(s,'Initial rejection vs acceptance',68,225,545,44,29,C.ink,true);
forest(s,D.E01.slice(0,2).map((e,i)=>({...e,name:i?'Final masking':'Authentic sampling',color:i?C.blue:C.rust})),{left:65,top:303,width:545,height:260},-4,2,2);
tx(s,'After rejection: intervention − baseline',680,225,530,44,26,C.ink,true);
forest(s,D.E01.slice(2).map((e,i)=>({...e,name:i?'Authentic feedback':'Forced authenticity',color:i?C.teal:C.blue})),{left:677,top:303,width:535,height:260},-14,2,4);
tx(s,'Authentic sampling after the first interaction',78,390,528,34,21);tx(s,'Final masking: interval includes zero',78,495,528,34,21);tx(s,'5% forced authenticity: final masking',690,390,515,34,21);tx(s,'Authentic feedback: final masking',690,495,515,34,21);
tx(s,'Change in the stated outcome (percentage points)',370,568,650,35,21,C.muted,'', 'center');tx(s,'History affects sampling. Extra information changes later masking.',68,605,1144,42,29,C.teal,true);
}
// Result 2: preserve the two outcome windows.
{
const script='The graded model offers intermediate disclosure levels, each with an independent learned value. Here we compare those options with binary choice after initial rejection. Any disclosure increases by twenty-five and a half percentage points over subsequent interactions. Full authenticity, however, falls by nearly thirty-three points in the final window. These are different outcomes measured over different windows. More participation can therefore coexist with less full expression. In these tested cells, the expected payoff still increases linearly with disclosure, so full expression remains the objectively best endpoint. The result does not show that an intermediate level becomes objectively optimal. It also does not model a ladder on which success at one level automatically teaches the learner about the next. An empirical study would need to measure both the degree of expression and whether learning transfers between levels.';
const s=base('More participation can coexist\nwith less full expression','M1 / E02: graded choices minus binary choices after initial rejection','p=.75/.85 pooled, five masters, n=500/cell/master, T=2000. Bars are 95% intervals. Independent action values.',75,script,['E02_PRIMARY'],'Any disclosure is d>0 over steps 1–1999. Full authenticity is d=1 during the final 400 steps. Effects +25.504040052777677 pp and −32.86922325725828 pp.');
tx(s,'Any disclosure',68,297,310,42,29,C.teal,true);tx(s,'After the first interaction',68,340,315,36,22,C.muted);tx(s,'Full authenticity',68,455,310,42,29,C.rust,true);tx(s,'Final window',68,498,310,36,22,C.muted);
forest(s,D.E02.map((e,i)=>({...e,name:i?'Full authenticity':'Any disclosure',color:i?C.rust:C.teal})),{left:392,top:238,width:820,height:340},-40,40,20);
tx(s,'Change versus binary choice (percentage points)',436,582,758,35,22,C.muted,false,'center');tx(s,'Full expression remains objectively best in these tested settings.',68,612,1144,38,29,C.teal,true);
}
// Result 3: native table as a categorical parameter map.
{
const script='For M2, the benchmark includes future social consequences. The map compares learned neutral-state choices with the optimal dynamic policy. Each square is one setting of acceptance probability and recovery from stigma. The rust region contains 243 of the 357 settings. In those cells, adequate neutral-state observations favour masking while the benchmark favours authenticity. The blue region shows agreement, and gray cells are inconclusive. These are counts of parameter settings, not percentages of children. The threshold table explains why the benchmark matters. In the static model, authenticity becomes worthwhile above about point seven one seven. With persistent social states, the reference threshold falls to about point three eight four, and to point two six nine with greater recovery. Persistent acceptance creates future value, and recovery reduces the cost of stigma. The finite learner still has to discover those consequences through experience. The benchmark already knows the environment. At five selected disagreement settings, the difference persists through five thousand interactions, with documented sensitivity exceptions. We therefore have evidence of disagreement over the tested horizons, rather than proof of permanent entrenchment.';
const s=base('Learned choices can disagree\nwith the dynamic optimum','M2 / E03: neutral-state action choice across 357 parameter settings','Baseline: 160 learners/cell/master, T=1000, five masters. Map categories use adequate Neutral visits. No smoothing.',120,script,['E03_GRID','E03_THRESHOLDS','src/gifted_masking/analysis/m2_optimal.py'],'243 learned-suboptimal-mask, 107 agreement, 7 inconclusive. All 243 disagreement cells agree across every master. Dynamic thresholds are numerical bracket midpoints, not confidence intervals. Oracle uses untransformed reward and an infinite discounted horizon, gamma=.9.');
tx(s,'Recovery probability η',90,229,595,37,23,C.muted);const colors={learned_suboptimal_masking:C.rust,learner_matches_objective:C.blue,inconclusive:C.gray};
const t=s.tables.add({rows:17,columns:21,left:105,top:275,width:630,height:306,columnWidths:Array(21).fill(30),values:Array.from({length:17},()=>Array(21).fill(''))});t.borders.assign({fill:C.bg,width:.7,style:'solid'});
for(let r=0;r<17;r++){t.rows[r].height=18;for(let c=0;c<21;c++){const eta=(16-r)*.05,p=c*.05,e=D.E03.grid.find(x=>Math.abs(x.p-p)<1e-8&&Math.abs(x.eta-eta)<1e-8);const cell=t.getCell(r,c);cell.fill=colors[e.category];cell.text.style={typeface:font,fontSize:1,color:C.ink,autoFit:'none'};}}
for(let r=0;r<=16;r+=4)tx(s,((16-r)*.05).toFixed(1),18,266+r*18,79,32,21,C.muted,false,'right');for(let c=0;c<=20;c+=5)tx(s,(c*.05).toFixed(2),83+c*30,585,72,32,21,C.muted,false,'center');tx(s,'Acceptance probability p',269,617,380,30,22,C.muted);
rect(s,805,226,16,16,C.rust);tx(s,'243 / 357',833,213,366,66,46,C.rust,true);tx(s,'Learned masking,\noptimal authenticity',833,285,365,76,27);rect(s,805,369,16,16,C.blue);tx(s,'107 agreement',833,360,350,37,25);rect(s,805,411,16,16,C.gray);tx(s,'7 inconclusive',833,402,350,37,25);
tx(s,'Objective authenticity threshold',803,468,411,36,23,C.muted,true);table(s,[['Static','M2: η=0','M2: η=.8'],['.717','.384','.269']],805,508,405,95,[135,135,135],23);
}
// Result 4: context architectures and different denominators.
{
const script='The best available reward stays fixed as we add groups, but learned allocation changes. In the flat representation, each group has separate masking and authentic actions. With sixteen groups, final masking reaches eighty-four percent. Yet almost every learner has already experienced acceptance in the receptive group at least once. The two percentages have different denominators: one measures late actions, and the other counts learners with a success anywhere in the full run. Successful encounter does not ensure sustained use, and one success does not supply complete knowledge. The curves show why representation matters. Choosing a group and then a behaviour gives a similar increase in masking. Pooling masking into one shared action keeps masking near twenty-six percent. That change affects both information sharing and the initial allocation of choices, so it does not isolate one pure psychological mechanism. The supported conclusion is conditional: the effect of more contexts depends strongly on how the learner represents those choices. It cannot be generalized into a claim that more contexts always cause masking.';
const s=base('Finding a receptive group does not\nensure sustained expression','M3 / E04: the best available reward stays fixed as K increases','Flat K=16−1: +57.83 pp final masking [95% CI 57.43, 58.22]. One good group, fixed identity.\nFive masters; n=500/cell/master, T=2000. Curves show descriptive means at discrete K.',105,script,['E04_CURVES','E04_EFFECTS'],'At K=16 flat final masking=.841906, full-run accepted-good-context encounter=.9972. Shared-mask architecture also changes initial mask probability from 1/2 to 1/(K+1).');
const names={flat_2k:'Flat 2K',hierarchical:'Hierarchical',global_mask:'Shared mask'},cols={flat_2k:C.teal,hierarchical:C.rust,global_mask:C.blue};chart(s,'line',{position:{left:64,top:234,width:819,height:366},categories:['1','2','4','8','16'],series:Object.entries(names).map(([k,name])=>({name,values:D.E04[k],line:{fill:cols[k],width:3},marker:{symbol:k==='flat_2k'?'circle':k==='hierarchical'?'diamond':'square',size:7}})),hasLegend:true,legend:{position:'bottom',overlay:false,textStyle:{typeface:font,fontSize:21,fill:C.ink}},xAxis:{title:'Number of groups K',textStyle:axis,majorGridlines:null},yAxis:{title:'Final masking',min:0,max:1,majorUnit:.25,numberFormatCode:'0%',textStyle:axis,majorGridlines:{fill:C.grid,width:1}}});
tx(s,'K = 16, flat model',922,232,295,36,24,C.muted);tx(s,'84.19%',912,286,305,80,54,C.teal,true);tx(s,'of final-window actions\nwere masking',922,365,287,65,25);tx(s,'99.72%',912,445,305,75,51,C.ink,true);tx(s,'of learners experienced\nacceptance in the good group',922,518,290,83,24);
tx(s,'The effect depends on how choices are represented.',68,609,1144,41,29,C.teal,true);
}
// Result 5: exact objective boundary and archived learned crossing.
{
const script='The comparison-cost experiment changes the reward for accepted authenticity in the receptive group. The equations place objective indifference at about point four seven one. The flat four-group population crosses its behavioural boundary earlier, near point three one three, with the displayed confidence interval. At that learned crossing, authenticity in the receptive group still has an objective advantage. The vertical axis needs care: it counts learners whose most frequent individual final-window action is authenticity in the good group. Crossing fifty percent therefore has a specific modal meaning. It is not the onset of majority masking. Four separate masking actions can together occupy most interactions even when one authentic action is individually the most frequent. These boundaries answer different questions: when the opportunity loses its expected-payoff advantage, and when the learned population crosses the defined behavioural threshold. The difference is a result for this architecture and finite learning horizon.';
const s=base('The learned boundary occurs\nbefore objective indifference','M3 / E05: comparison cost reduces accepted authenticity in the receptive group','Flat K=4, λ=1, five masters, n=500/cell/master, T=2000. Modal classification is distinct from total masking.',90,script,['E05_RESPONSE','E05_CROSSINGS'],'Learned crossing=.31285211267605634; 95% CI [.307836, .316918] rounded. Objective=.47058823529411764. Curves connect archived pooled values; no refit or bootstrap.');
const a=Number(D.E05_crossing.transition_bf),b=Number(D.E05_crossing.analytic_threshold_bf);
rect(s,172.7+a/.8*690,233.3,(b-a)/.8*690,301,'#EEE7DF');
chart(s,'scatter',{position:{left:62,top:226,width:817,height:376},chartFill:'none',plotAreaFill:'none',series:[{name:'Good-authentic modal',xValues:D.E05.map(e=>e.x),values:D.E05.map(e=>e.y),line:{fill:C.teal,width:3},marker:{symbol:'circle',size:6}},{name:'50% boundary',xValues:[0,.8],values:[.5,.5],line:{fill:C.gray,width:1,style:'dashed'},marker:{symbol:'none'}},{name:'Learned',xValues:[a,a],values:[0,1],line:{fill:C.rust,width:2.4,style:'dashed'},marker:{symbol:'none'}},{name:'Objective',xValues:[b,b],values:[0,1],line:{fill:C.blue,width:2.4,style:'dashed'},marker:{symbol:'none'}}],scatterOptions:{style:'lineWithMarkers'},hasLegend:false,xAxis:{title:'Comparison cost',min:0,max:.8,majorUnit:.2,numberFormatCode:'0.0',textStyle:axis,majorGridlines:null},yAxis:{title:'Learners with good-authentic modal',min:0,max:1,majorUnit:.25,numberFormatCode:'0%',textStyle:axis,majorGridlines:{fill:C.grid,width:1}}});
tx(s,'LEARNED',926,240,277,32,21,C.rust,true);tx(s,'0.313',915,279,300,77,54,C.rust,true);tx(s,'95% CI [.308, .317]',926,357,287,36,23,C.muted);tx(s,'OBJECTIVE',926,434,277,32,21,C.blue,true);tx(s,'0.471',915,472,300,77,54,C.blue,true);tx(s,'Expected payoffs are equal',926,551,278,57,23,C.muted);tx(s,'Authenticity retains an objective advantage at the learned crossing.',68,612,1144,37,27,C.teal,true);
}

// M4 appears in results order without turning assumptions into empirical findings.
{
const s=base('M4  Formal results remain deferred','E06 evidence status','Diagnostic smoke checks do not establish robust hysteresis or irreversible entrenchment.',20,'',['projects/frontiers_article/ARTICLE_V1_MANUSCRIPT_EVIDENCE_FREEZE.md','projects/frontiers_article/presentation_prep_20261005/SIMULATION_GUIDE.md','src/gifted_masking/experiments/e06.py'],'M4 is implemented, with diagnostic smoke evidence. No confirmatory E06 result is part of the article evidence. A direct continuation/ramp test, controls, uncertainty and longer horizons are needed before a robust hysteresis claim. No new E06 run is authorized by this slide request.');
tx(s,'No confirmatory E06 result to report',68,262,1144,66,42,C.teal,true);
tx(s,'Open question',68,371,1144,43,27,C.muted,true);
tx(s,'Do different histories produce different continuation paths\nunder the same conditions?',68,423,1144,106,34,C.ink,true);
tx(s,'Needed: direct ramp tests, longer continuations and feedback ablations.',68,575,1144,64,28,C.muted);
}

// Discussion 2: mechanism synthesis.
{
const script='The results give several explanations for similar visible concealment. Under fixed opportunities, experience and access to feedback affect what the learner discovers. With partial disclosure, separate action values can support participation without full expression. Persistent social consequences change the value of an action itself, which requires a dynamic benchmark. With multiple contexts, successful encounter and sustained use depend on how choices represent and share experience. These findings should not be collapsed into one universal cause. They also show why a single measure of masking is insufficient: participation, intensity, contextual encounter and repeated use answer different questions. The results establish behaviour in specified computational models. Identifying the corresponding processes in children requires observations or experiments that distinguish these explanations.';
const s=base('Similar concealment can arise\nthrough different processes','Observed behaviour leaves several mechanisms possible','These are findings in specified computational models. Mechanisms in children require empirical evidence.',75,script,['projects/frontiers_article/integrated_article_20261004/ARTICLE.md'],'E01–E05 each use five master replications. Broader parameter and human generalization are not established. M4 remains a separate candidate extension.');
table(s,[['Process','What it helps explain'],['Experience and feedback (M0)','Underuse of a fixed opportunity'],['Separate disclosure values (M1)','Participation without full expression'],['Persistent consequences (M2)','Why immediate reward can mislead'],['Context-specific learning (M3)','Encounter without sustained use']],68,231,1144,338,[548,596],27);tx(s,'Concealment alone cannot identify the process that produced it.',68,604,1144,44,30,C.teal,true);
}
// Discussion 3: empirical questions with concrete measures.
{
const script='These models suggest what an empirical study would need to measure. First, ask what the child expects before an interaction, and compare that expectation with the feedback they actually receive. Second, examine which experiences change those expectations. Third, test whether learning transfers: does success with a small disclosure, or in one setting, change expression elsewhere? Finally, track what persists. Social standing and recovery opportunities may affect later choices beyond the immediate response. Repeated observations should record the degree of expression and the context, rather than treating all participation as equivalent. The contribution is a set of mechanisms and distinguishing predictions that we can now test.';
const s=base('What should we measure next?','Mechanisms suggest different empirical measurements','Model-derived questions for empirical study. The simulations are not calibrated to chronological age.',60,script,['projects/frontiers_article/integrated_article_20261004/ARTICLE.md'],'Empirical implications are hypotheses, not established intervention effects in children.');
const rows=[['What does the child expect?','Expectations before an interaction'],['Which experiences change it?','Feedback and subsequent expectations'],['Does learning transfer?','Expression across levels and contexts'],['What consequences persist?','Social standing, recovery and repeated use']];
rows.forEach((r,i)=>{const y=236+i*82;tx(s,r[0],68,y,561,61,30,i===0?C.teal:C.ink,true);tx(s,r[1],686,y+3,527,62,25,C.muted);if(i<3)rect(s,69,y+65,1141,1,C.grid);});tx(s,'Specific mechanisms give us predictions we can test.',68,602,1144,45,32,C.teal,true);
}

await fs.writeFile(path.join(PACK,'SLIDE_SPEC.json'),JSON.stringify({title:'Masking mechanisms: methods then results',slides:spec,slide_count:16,duration_seconds:spec.reduce((n,s)=>n+s.seconds,0),scope:'Three opening slides, five methods-only slides, five archived results slides, M4 deferred-results status, two discussion slides.'},null,2)+'\n');
const candidate=path.join(W,'build',`candidate_${V}.pptx`);await(await PresentationFile.exportPptx(P)).save(candidate);
const finalPath=path.join(W,'output',`masking_methods_then_results_${V}.pptx`);
const validation=await finalizePresentation({workspaceDir:W,candidatePath:candidate,finalPath,explicitTotalSlideCount:16,requiredNativeTableOwnerSlides:[5,6,7,8,11,15],requiredNativeChartOwnerSlides:[9,10,12,13],nativeChartTargetApplication:'powerpoint',pythonExecutable:'/Users/omer/workspace/venvs/venv314/bin/python',integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...[5,6,7,8,11,15].flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy:{basis:'reference',families:[font],referencePath:path.join(ROOT,'output/pptx/masking_mechanisms_first_set.pptx'),referenceSha256:'94b32f9a4cb58e2259ee7f82750bd86bbd53a46910294a48c7fec4d278206900'},verifyArtifactToolImport:true,receiptPath:path.join(W,'build',`validation_${V}.json`)});
const imp=await PresentationFile.importPptx(await FileBlob.load(finalPath));const renders=path.join(W,'build',`renders_${V}`);await fs.mkdir(renders,{recursive:true});
for(let i=0;i<imp.slides.items.length;i++){const slide=imp.slides.items[i],png=await imp.export({slide,format:'png',scale:1.5});await fs.writeFile(path.join(renders,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));await fs.writeFile(path.join(renders,`slide-${String(i+1).padStart(2,'0')}.json`),await(await slide.export({format:'layout'})).text());console.log('Rendered '+(i+1));}
await fs.writeFile(path.join(PACK,'SPEAKER_NOTES.md'),'# Masking mechanisms lecture\n\nMethods followed by results. Planned duration 15 minutes; 16 slides.\n\n'+spec.map(x=>'## '+x.slide+'. '+x.title+'\n\n'+x.section+' · '+x.seconds+' seconds\n\n'+x.script+'\n\nSources: '+x.sources.join('; ')).join('\n\n')+'\n');
console.log(JSON.stringify({finalPath,renders,sha256:validation.finalSha256}));
