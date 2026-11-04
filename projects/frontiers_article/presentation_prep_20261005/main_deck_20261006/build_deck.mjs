import fs from 'node:fs/promises';
import path from 'node:path';
import {Presentation,PresentationFile,FileBlob} from '@oai/artifact-tool';
import {resolvePresentationFont,applyPresentationChartFont,finalizePresentation} from '/Users/omer/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations/container_tools/artifact_tool_utils.mjs';
const ROOT='/Users/omer/workspace/personal/repos/gifted-masking';
const PACK=path.join(ROOT,'projects/frontiers_article/presentation_prep_20261005');
const W='/private/tmp/gifted-main-deck-20261006';
const SKILL='/Users/omer/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations';
const VERSION=process.env.DECK_VERSION||'v1';
const font=resolvePresentationFont({fontFamily:'Helvetica Neue'});
const spec=JSON.parse(await fs.readFile(path.join(PACK,'SLIDE_SPEC.json'),'utf8'));
const index=JSON.parse(await fs.readFile(path.join(PACK,'SOURCE_INDEX.json'),'utf8'));
const data=JSON.parse(await fs.readFile(path.join(PACK,'MAIN_DECK_DATA.json'),'utf8'));
const main=spec.slides.filter(x=>!x.appendix);
const pres=Presentation.create({slideSize:{width:1280,height:720}});
const C={bg:'#F6F3ED',ink:'#18363D',muted:'#52656B',teal:'#006B69',blue:'#496F8A',rust:'#B85E45',gold:'#B28A42',light:'#DCE8E4',grid:'#D6DCD7',white:'#FFFFFF'};
let cnt=0;
function tx(s,t,x,y,w,h,size=28,color=C.ink,bold=false,align='left'){
 const o=s.shapes.add({name:'text-'+(++cnt),geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});o.text=t;o.text.style={typeface:font,fontSize:size,color,bold,alignment:align,autoFit:'none'};return o;
}
function node(s,t,x,y,w,h,color=C.teal){
 const o=s.shapes.add({name:'diagram-node-'+(++cnt),geometry:'roundRect',position:{left:x,top:y,width:w,height:h},fill:C.bg,line:{fill:color,width:2}});o.text=t;o.text.style={typeface:font,fontSize:25,color,bold:true,alignment:'center',verticalAlignment:'middle',autoFit:'none'};return o;
}
function arrow(s,a,b,from='right',to='left',kind='straight',color=C.muted){return s.shapes.connect(a,b,{kind,fromSide:from,toSide:to,line:{fill:color,width:2.2},tail:{type:'triangle',width:'sm',length:'sm'}});}
function base(n,title,sub='',foot=''){
 const s=pres.slides.add();s.background.fill=C.bg;tx(s,title,64,42,1150,86,47,C.ink,true);
 if(sub)tx(s,sub,68,131,1144,54,25,C.muted);
 if(foot)tx(s,foot,68,650,1095,57,17,C.muted);
 tx(s,String(n).padStart(2,'0'),1176,665,42,28,17,C.muted,false,'right');
 const item=main[n-1];let refs=item.source_ids.map(id=>{const v=index.sources[id];return id+': '+(v.path||v.url||'')+(v.external_sources?'\n'+v.external_sources.map(z=>z.title+' '+z.url).join('\n'):'');}).join('\n');
 s.speakerNotes.textFrame.setText(item.speaker_notes+'\n\nTiming: '+item.seconds+' seconds.\n\nSources:\n'+refs+'\n\nInterpretation: '+(item.visible_qualification||''));return s;
}
function extra(s,t){s.speakerNotes.textFrame.setText(s.speakerNotes.textFrame.toString?.()||'');}
function table(s,values,x,y,w,h,widths,fsz=24){
 const tb=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:w,height:h,columnWidths:widths,values});
 tb.borders.assign({fill:C.grid,width:0.8,style:'solid'});
 for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){
  const cell=tb.getCell(r,c);cell.fill=r===0?C.ink:C.bg;cell.text.style={typeface:font,fontSize:fsz,color:r===0?C.white:C.ink,bold:r===0,autoFit:'none'};
 }
 return tb;
}
const axisText={typeface:font,fontSize:20,fill:C.muted};
const noLine={fill:'none',width:0};
function chart(s,type,options){const ch=s.charts.add(type,{titlePlacement:'none',chartFill:C.bg,plotAreaFill:C.bg,chartLine:noLine,plotAreaLine:noLine,...options});applyPresentationChartFont(ch,{fontFamily:font});return ch;}
// 1. Introductory question; image establishes the situation without asserting the mechanism.
{
 const s=base(1,'What mechanisms could\nexplain masking?','','Swiatek (1995) · Chan (2005) · Foust, Rudasill & Callahan (2006)');
 tx(s,'Research documents ability concealment\namong gifted learners.',68,262,640,105,32);
 tx(s,'Patterns vary across age\nand social settings.',68,385,580,98,32);
 s.images.add({blob:await fs.readFile(path.join(PACK,'assets/child_apart_from_peers.png')),contentType:'image/png',alt:'An observant young child stands apart from four interacting peers. Generated illustration.',fit:'contain',position:{left:708,top:238,width:530,height:360}});
 tx(s,'We examine possible learning mechanisms.',68,554,1090,55,34,C.teal,true);
 s.speakerNotes.textFrame.setText(main[0].speaker_notes+'\n\n35 seconds.\nSwiatek (1995): https://doi.org/10.1177/001698629503900305\nChan (2005): https://files.eric.ed.gov/fulltext/EJ746277.pdf\nFoust et al. (2006): https://files.eric.ed.gov/fulltext/EJ753971.pdf\nAge findings are mixed. The simulations are not calibrated to chronological age. Earlier social-coping and learning mechanisms exist; no blanket novelty claim is made.\nImage: generated using the built-in image generator, 6 October 2026. Illustration only, not an empirical observation. Prompt and provenance: assets/ASSET_SOURCES.json.');
}
// 2. Actual film still.
{
 const s=base(2,'A close second','','The Incredibles (2004) · Pixar / Walt Disney Pictures · Film illustration');
 tx(s,'“Second. Close second, yeah!”',68,132,1130,50,32,C.teal,true);
 s.images.add({blob:await fs.readFile(path.join(PACK,'assets/dash_school_race.jpg')),contentType:'image/jpeg',alt:'Dash at the end of the school race in The Incredibles, giving two thumbs up among the other runners.',fit:'contain',position:{left:68,top:190,width:1144,height:390}});
 tx(s,'Social expectations can shape displayed ability.',68,598,1140,45,31);
 s.speakerNotes.textFrame.setText(main[1].speaker_notes+'\n\n30 seconds. The film illustrates explicit social instruction; parental instruction is not directly implemented in M0.\nFilm: Brad Bird, The Incredibles (2004), Pixar/Walt Disney Pictures.\nOfficial context: https://www.pixar.com/the-incredibles\nQuote: https://clip.cafe/the-incredibles-2004/do-we-have-to-have-cheerleaders-at-the-track-meet/\nStill source: https://cinefilms-planet.fr/fleche-parr-personnage-dans-les-indestructibles/\nImage: https://cinefilms-planet.fr/wp-content/uploads/2010/04/fleche-parr-personnage-les-indestructibles-10-1.jpg');
}
// 3. Shared learning process.
{
 const s=base(3,'Learning from social experience','Experience changes expectations, which influence the next choice.','A step is one interaction, not a calibrated year. Negative outcomes can receive extra weight.');
 const labels=['Choose\nan action','Experience\nan outcome','Update its\nlearned value','Choose\nagain'];const nodes=labels.map((t,i)=>node(s,t,68+i*295,242,235,112));
 for(let i=0;i<3;i++)arrow(s,nodes[i],nodes[i+1]);
 tx(s,'Baseline feedback concerns the chosen action.',68,414,1130,54,32,C.teal,true);
 tx(s,'Higher-valued actions become more likely.\nExploration continues.',68,488,1090,100,31);
}
// 4. Two-arm setup and two kinds of evidence.
{
 const s=base(4,'M0 · Masking or authenticity','Two actions • fixed receptivity p • no persistent social state','E01: p=.75/.85 pooled, λ=1; 500 learners/cell/master, T=2000, five masters. History final-window CI spans zero.');
 const choose=node(s,'Choose',70,226,160,72,C.ink);const mask=node(s,'Mask',318,190,196,62,C.blue);const auth=node(s,'Authentic',318,290,196,62,C.teal);arrow(s,choose,mask);arrow(s,choose,auth);
 tx(s,'Certain reward',562,191,250,38,25,C.muted);tx(s,'0.75',841,188,310,45,32,C.blue,true);arrow(s,mask,s.shapes.items[s.shapes.items.length-2]);
 const yes=tx(s,'Accepted: p',560,277,245,38,25,C.muted);arrow(s,auth,yes);tx(s,'+1.60',841,273,160,45,32,C.teal,true);
 const no=tx(s,'Rejected: 1 − p',560,325,270,38,25,C.muted);arrow(s,auth,no);tx(s,'−1.40',841,321,170,45,32,C.rust,true);
 tx(s,'THEORY',68,403,460,34,20,C.muted,true);tx(s,'Higher expected payoff\nfor authenticity: p > .717',68,444,495,91,34,C.teal,true);tx(s,'At p=.75: 0.85 versus 0.75',68,559,495,45,27);
 tx(s,'SIMULATIONS',640,403,530,34,20,C.muted,true);tx(s,'−2.58 pp  authentic sampling',640,446,565,43,29,C.ink,true);tx(s,'After initial rejection · 95% CI [−3.58, −1.59]',640,492,570,36,20,C.muted);
 tx(s,'−11.81 pp  final masking',640,544,565,43,29,C.ink,true);tx(s,'Extra feedback · 95% CI [−12.66, −10.97]',640,590,570,36,20,C.muted);
}
// 5. Graded disclosure and contrasting outcomes.
{
 const s=base(5,'M1 · Participation and full expression differ','Five independently learned disclosure levels; no transfer between action values.','E02: after initial rejection; p=.75/.85 pooled; five masters. CIs: [25.30,25.71] and [−34.20,−31.53] pp.');
 tx(s,'Disclosure',68,202,180,42,25,C.muted);
 const ds=['0','¼','½','¾','1'];for(let i=0;i<5;i++)tx(s,ds[i],262+i*174,196,140,55,37,i===0?C.blue:C.teal,true,'center');
 chart(s,'bar',{position:{left:65,top:277,width:835,height:306},categories:['Any disclosure\npost-initial','Full authenticity\nfinal window'],series:[{name:'Change vs binary choice',values:[25.504040052777677,-32.86922325725828],valuesFormatCode:"0.00",dataLabelOverrides:[{idx:0,text:'+25.50',position:'inEnd',showValue:true,textStyle:{typeface:font,fontSize:21,fill:C.white,bold:true}},{idx:1,text:'−32.87',position:'inEnd',showValue:true,textStyle:{typeface:font,fontSize:21,fill:C.white,bold:true}}],points:[{idx:0,fill:C.teal},{idx:1,fill:C.rust}]}],barOptions:{direction:'bar',grouping:'clustered',gapWidth:20},hasLegend:false,xAxis:{visible:true,tickLabelPosition:'none',textStyle:axisText,majorGridlines:null},yAxis:{visible:true,min:-40,max:40,majorUnit:20,title:'Change versus binary choice (pp)',numberFormatCode:'0',textStyle:axisText,majorGridlines:{fill:C.grid,width:1}},dataLabels:{showValue:true,position:'inEnd',textStyle:{typeface:font,fontSize:21,fill:C.white,bold:true}}});
 tx(s,'Full authenticity\nFinal window',515,322,372,84,25,C.ink,true);
 tx(s,'Any disclosure\nAfter the first interaction',80,420,360,84,25,C.ink,true);
 tx(s,'Change versus binary choice (percentage points)',150,552,730,33,21,C.muted);
 tx(s,'More participation\ncan coexist with\nless full expression.',938,322,290,200,31,C.teal,true);
 tx(s,'Theory: the payoff is linear in disclosure; the full endpoint is best in these cells.',68,599,1134,42,25);
}
// 6. M2: social states are distinct from actions.
{
 const s=base(6,'M2 · Persistent social consequences','Actions: Mask / Authentic in every state • Learner: 3 × 2 state–action values','243/357 counts parameter settings, not learners. Neutral-state comparison; full-information discounted benchmark.');
 const n=node(s,'Neutral',72,285,185,68,C.ink);const a=node(s,'Accepted',425,211,190,68,C.teal);const st=node(s,'Stigmatized',425,369,190,68,C.rust);arrow(s,n,a);arrow(s,n,st);
 tx(s,'Authentic +\nacceptance',268,202,151,72,22,C.teal);tx(s,'Authentic +\nrejection',268,379,151,72,22,C.rust);
 tx(s,'Mask / Authentic',62,363,207,40,22,C.muted);tx(s,'Mask / Authentic',413,289,230,40,22,C.muted);tx(s,'Mask / Authentic',413,447,230,40,22,C.muted);
 tx(s,'Turnover returns Accepted to Neutral.\nEscape can return Stigmatized to Neutral;\nredemption can establish acceptance.',68,521,570,100,24);
 tx(s,'THEORY · Neutral authenticity threshold',697,209,526,38,21,C.muted,true);
 table(s,[['Static M0','M2: η=0','M2: η=.8'],['.717','.384','.269']],696,258,516,131,[172,172,172],27);
 tx(s,'243 / 357',700,436,512,84,60,C.teal,true);tx(s,'settings favour learned masking\nwhile the dynamic optimum\nfavours authenticity',705,522,505,106,27);
 s.speakerNotes.textFrame.setText(main[5].speaker_notes+'\n\n100 seconds. State/action distinction: actions are Mask or Authentic in every state. Q has three rows and two columns. The diagram shows the main Neutral branches; masking remains Neutral. Accepted persists unless turnover δ; Stigmatized persists unless successful redemption p/2 or subsequent escape η. Rewards precede next-state transitions; newly entered states are not immediately turned over or escaped. Thresholds: static .716667, dynamic .383942 at η=0, .269012 at η=.8, other reference settings held fixed.\nSources: src/gifted_masking/models/m2.py; src/gifted_masking/analysis/m2_optimal.py; projects/frontiers_article/publication_v1/data/e03_objective_thresholds.csv; '+index.sources.E03_GRID.path+'; '+index.sources.E03_CONFIG.path+'; projects/frontiers_article/integrated_article_20261004/ARTICLE.md');
}
// 7. M3: representation changes which actions compete.
{
 const s=base(7,'M3 · Context is part of the choice','Flat model: choose one of 2K group–behaviour pairs • group receptivities stay fixed','E04: one good context, fixed identity; five-master means. Encounter is over the full run; masking is the final-window action fraction.');
 table(s,[['Group 1','Group 2','… Group K'],['Mask₁ / Authentic₁','Mask₂ / Authentic₂','Maskₖ / Authenticₖ']],69,198,1144,112,[381,381,382],23);
 const names={flat_2k:'Flat 2K',hierarchical:'Hierarchical',global_mask:'Shared mask'};const colors={flat_2k:C.teal,hierarchical:C.rust,global_mask:C.blue};
 chart(s,'line',{position:{left:66,top:343,width:800,height:279},categories:['1','2','4','8','16'],series:Object.entries(names).map(([k,v])=>({name:v,values:data.E04[k],line:{fill:colors[k],width:3},marker:{symbol:'circle',size:6}})),hasLegend:true,legend:{position:'bottom',overlay:false,textStyle:{typeface:font,fontSize:20,fill:C.ink}},xAxis:{title:'Number of contexts K',textStyle:axisText,majorGridlines:null},yAxis:{title:'Final masking',min:0,max:1,majorUnit:.25,numberFormatCode:'0%',textStyle:axisText,majorGridlines:{fill:C.grid,width:1}}});
 tx(s,'At K = 16, flat model',910,349,325,38,22,C.muted);tx(s,'84.19%',911,389,300,70,51,C.teal,true);tx(s,'final masking',914,459,300,35,25);
 tx(s,'99.72%',911,507,300,67,49,C.ink,true);tx(s,'had experienced acceptance\nin the good context',914,574,300,61,22);
}
// 8. Comparison-cost curve and separate learned/objective boundaries.
{
 const s=base(8,'M3 · Social comparison changes the boundary','Comparison cost reduces accepted authenticity in the receptive group.','E05: flat K=4, λ=1, five masters. Learned crossing is a modal-population boundary, not majority-masking onset.');
 const crossing=Number(data.E05_crossing.transition_bf),objective=Number(data.E05_crossing.analytic_threshold_bf);
 chart(s,'scatter',{position:{left:59,top:206,width:820,height:404},series:[{name:'Good-authentic is modal',xValues:data.E05.map(x=>x.x),values:data.E05.map(x=>x.y),line:{fill:C.teal,width:3},marker:{symbol:'circle',size:5}},{name:'Learned boundary',xValues:[crossing,crossing],values:[0,1],line:{fill:C.rust,width:2,style:'dashed'},marker:{symbol:'none'}},{name:'Objective boundary',xValues:[objective,objective],values:[0,1],line:{fill:C.blue,width:2,style:'dashed'},marker:{symbol:'none'}}],scatterOptions:{style:'lineWithMarkers'},hasLegend:false,xAxis:{title:'Comparison cost',min:0,max:.8,majorUnit:.2,textStyle:axisText,numberFormatCode:'0.0',majorGridlines:null},yAxis:{title:'Learners with good-authentic modal',min:0,max:1,majorUnit:.25,numberFormatCode:'0%',textStyle:axisText,majorGridlines:{fill:C.grid,width:1}}});
 tx(s,'LEARNED',923,237,270,30,20,C.rust,true);tx(s,'0.313',918,276,310,80,55,C.rust,true);tx(s,'95% CI [.308, .317]',923,355,290,36,22,C.muted);
 tx(s,'OBJECTIVE',923,431,270,30,20,C.blue,true);tx(s,'0.471',918,471,310,80,55,C.blue,true);tx(s,'Expected payoffs are equal',923,550,290,61,22,C.muted);
}
// 9. M4: evolving receptivity does not mean state-conditioned Q-learning.
{
 const s=base(9,'M4 · Behaviour changes future receptivity','Actions: Mask / Authentic • Environment: continuous pₜ • Learner: only two Q-values','Implemented extension; formal E06 results deferred. Direction-of-change rules are model assumptions; hysteresis is not established.');
 const q=node(s,'Q(Mask), Q(Auth)',69,223,280,74,C.ink);const c=node(s,'Choose an action',447,223,290,74,C.teal);const p=node(s,'Current pₜ',931,223,273,74,C.blue);arrow(s,q,c);
 const o=node(s,'Outcome and reward',445,372,294,76,C.ink);arrow(s,c,o,'bottom','top');arrow(s,p,o,'bottom','right','elbow',C.blue);
 arrow(s,o,q,'left','bottom','elbow');tx(s,'Updates the chosen\nQ-value',71,395,311,84,26);
 table(s,[['Event','Next receptivity'],['Accepted authenticity','Increases'],['Rejected authenticity','Decreases'],['Masking','Decreases']],821,362,388,237,[235,153],22);
 tx(s,'pₜ is bounded between .05 and .95.\nThe learner does not condition Q on pₜ.',69,527,686,81,29,C.teal,true);
}
// 10. Compare action spaces, state spaces and learner memory.
{
 const s=base(10,'What changes across the models?','Action = a choice • State = the current environmental condition','E01–E05: five independent master replications. Findings concern specified models; mechanisms in human learners remain empirical questions.');
 table(s,[['Model','Actions','Environmental state','Learner memory'],['M0','2 behaviours','Fixed receptivity','2 action values'],['M1','5 disclosure levels','Fixed receptivity','5 action values'],['M2','2 behaviours','3 social states','3 × 2 values'],['M3, flat','2K group–behaviour pairs','Fixed group receptivities','2K action values'],['M4','2 behaviours','Continuous receptivity pₜ','2 action values']],68,215,1144,385,[115,345,352,332],23);
 s.speakerNotes.textFrame.setText('Read each model along three columns: what can be chosen, what the environment carries forward, and what the learner remembers. M2 explicitly conditions its choices on social state. M3 chooses a context–behaviour pair. M4 changes the environment, but still learns two action values. E01 to E05 each use five master replications. These results establish model behaviours; human mechanisms require empirical tests.\n\n35 seconds.\nSources: src/gifted_masking/models/m0.py; src/gifted_masking/models/m1.py; src/gifted_masking/models/m2.py; src/gifted_masking/models/m3.py; src/gifted_masking/models/m4.py; projects/frontiers_article/integrated_article_20261004/ARTICLE.md.');
}
// 11. Close with the empirical questions implied by distinct candidate mechanisms.
{
 const s=base(11,'Different mechanisms imply different questions','','Model-derived questions for empirical study');
 tx(s,'What does the child expect?',68,212,1138,61,39,C.teal,true);
 tx(s,'Which experiences change that expectation?',68,303,1140,65,37);
 tx(s,'Does learning transfer between situations?',68,397,1140,65,37);
 tx(s,'What consequences persist?',68,490,1138,62,39);
}
const candidate=path.join(W,'build',`candidate_${VERSION}.pptx`);await (await PresentationFile.exportPptx(pres)).save(candidate);
const finalPath=path.join(W,'output',`masking_mechanisms_first_set_${VERSION}.pptx`);
const result=await finalizePresentation({workspaceDir:W,candidatePath:candidate,finalPath,explicitTotalSlideCount:11,requiredNativeTableOwnerSlides:[6,7,9,10],requiredNativeChartOwnerSlides:[5,7,8],materializeLiteralChartWorkbooks:true,nativeChartTargetApplication:'powerpoint',pythonExecutable:'/Users/omer/workspace/venvs/venv314/bin/python',integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...[6,7,9,10].flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:path.join(W,'build',`validation_${VERSION}.json`)});
const imported=await PresentationFile.importPptx(await FileBlob.load(finalPath));const renders=path.join(W,'build',`renders_${VERSION}`);await fs.mkdir(renders,{recursive:true});
for(let i=0;i<imported.slides.items.length;i++){
 const slide=imported.slides.items[i];const png=await imported.export({slide,format:'png',scale:1.5});await fs.writeFile(path.join(renders,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));const layout=await slide.export({format:'layout'});await fs.writeFile(path.join(renders,`slide-${String(i+1).padStart(2,'0')}.json`),await layout.text());console.log('Rendered slide '+(i+1));
}
await fs.writeFile(path.join(W,'build',`final_text_${VERSION}.json`),JSON.stringify((await imported.inspect({kind:'slide,textbox,shape,table,chart,notes',maxChars:200000})).ndjson));
console.log(JSON.stringify({finalPath,renders,font,validation:result},null,2));
