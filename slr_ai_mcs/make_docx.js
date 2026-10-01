const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,WidthType,ShadingType,HeadingLevel,PageOrientation,LevelFormat,BorderStyle,Footer,PageNumber,AlignmentType}=require('docx');
const md=fs.readFileSync(__dirname+'/REPORT.md','utf8').split('\n');
const TOTAL=13680; // landscape A4-ish usable width in DXA (letter 15840-2*1080)
function runs(t,size,bold0){
  const out=[];const re=/(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|`[^`]+`)/g;let last=0,m;
  while((m=re.exec(t))){ if(m.index>last)out.push(new TextRun({text:t.slice(last,m.index),size,bold:bold0}));
    const s=m[0]; if(s.startsWith('**'))out.push(new TextRun({text:s.slice(2,-2),bold:true,size}));
    else if(s.startsWith('`'))out.push(new TextRun({text:s.slice(1,-1),font:'Consolas',size}));
    else out.push(new TextRun({text:s.slice(1,-1),italics:true,size,bold:bold0}));
    last=m.index+s.length;}
  if(last<t.length)out.push(new TextRun({text:t.slice(last),size,bold:bold0}));
  return out;}
function cells(l){return l.trim().replace(/^\|/,'').replace(/\|$/,'').split('|').map(s=>s.trim());}
function mkTable(rows){
  const head=cells(rows[0]);const body=rows.slice(2).map(cells);const n=head.length;
  const w=head.map((h,i)=>{const lens=body.map(r=>(r[i]||'').length).sort((a,b)=>a-b);
    const p=lens[Math.floor(lens.length*0.8)]||0;return Math.min(Math.max(p,h.length,6),90);});
  const sum=w.reduce((a,b)=>a+b,0);let cw=w.map(x=>Math.max(500,Math.floor(x/sum*TOTAL)));
  const diff=TOTAL-cw.reduce((a,b)=>a+b,0);cw[cw.indexOf(Math.max(...cw))]+=diff;
  const bd={style:BorderStyle.SINGLE,size:4,color:'BBBBBB'};const borders={top:bd,bottom:bd,left:bd,right:bd};
  const sz=n>=10?13:16;
  const mk=(t,i,hd)=>new TableCell({borders,width:{size:cw[i],type:WidthType.DXA},
    shading:hd?{fill:'1F3864',type:ShadingType.CLEAR,color:'auto'}:undefined,margins:{top:40,bottom:40,left:60,right:60},
    children:[new Paragraph({children:hd?[new TextRun({text:t,bold:true,color:'FFFFFF',size:sz})]:runs(t,sz)})]});
  return new Table({width:{size:TOTAL,type:WidthType.DXA},columnWidths:cw,
    rows:[new TableRow({tableHeader:true,children:head.map((t,i)=>mk(t,i,true))}),
      ...body.map(r=>new TableRow({cantSplit:false,children:head.map((_,i)=>mk(r[i]||'',i,false))}))]});}
const kids=[];let i=0;
while(i<md.length){const l=md[i];
  if(l.startsWith('|')){const t=[];while(i<md.length&&md[i].startsWith('|')){t.push(md[i]);i++;}kids.push(mkTable(t));kids.push(new Paragraph({children:[]}));continue;}
  if(/^# /.test(l))kids.push(new Paragraph({heading:HeadingLevel.TITLE,children:[new TextRun({text:l.slice(2),bold:true})]}));
  else if(/^## /.test(l))kids.push(new Paragraph({heading:HeadingLevel.HEADING_1,children:[new TextRun(l.slice(3))]}));
  else if(/^### /.test(l))kids.push(new Paragraph({heading:HeadingLevel.HEADING_2,children:[new TextRun(l.slice(4))]}));
  else if(/^\s*- /.test(l)){const lvl=l.match(/^\s*/)[0].length>=2?1:0;kids.push(new Paragraph({numbering:{reference:'b',level:lvl},children:runs(l.replace(/^\s*- /,''),21)}));}
  else if(/^\d+\. /.test(l))kids.push(new Paragraph({numbering:{reference:'n',level:0},children:runs(l.replace(/^\d+\. /,''),21)}));
  else if(l.trim())kids.push(new Paragraph({spacing:{after:100},children:runs(l,21)}));
  i++;}
const doc=new Document({
  styles:{default:{document:{run:{font:'Calibri',size:21}}},paragraphStyles:[
    {id:'Title',name:'Title',basedOn:'Normal',run:{size:36,bold:true,color:'1F3864'},paragraph:{spacing:{after:200}}},
    {id:'Heading1',name:'Heading 1',basedOn:'Normal',next:'Normal',quickFormat:true,run:{size:28,bold:true,color:'1F3864'},paragraph:{spacing:{before:300,after:120},outlineLevel:0}},
    {id:'Heading2',name:'Heading 2',basedOn:'Normal',next:'Normal',quickFormat:true,run:{size:24,bold:true,color:'2E5597'},paragraph:{spacing:{before:200,after:100},outlineLevel:1}}]},
  numbering:{config:[
    {reference:'b',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:270}}}},
                          {level:1,format:LevelFormat.BULLET,text:'–',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:1000,hanging:270}}}}]},
    {reference:'n',levels:[{level:0,format:LevelFormat.DECIMAL,text:'%1.',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:540,hanging:300}}}}]}]},
  sections:[{properties:{page:{size:{width:12240,height:15840,orientation:PageOrientation.LANDSCAPE},margin:{top:1080,bottom:1080,left:1080,right:1080}}},
    footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({children:['Page ',PageNumber.CURRENT],size:16})]})]})},
    children:kids}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(__dirname+'/AI_MCS_synthesis.docx',b);console.log('written')});
