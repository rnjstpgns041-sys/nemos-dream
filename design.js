/* 네모의꿈 냉장고장 3D 설계 · 가견적 (design.html)
   1. 냉장고 입력 → 2. 키큰장 → 3. 확인·보내기 */
(function(){
'use strict';
var $=function(id){return document.getElementById(id)};
var PHONE='01048353353';
// 예시 치수 (mm). 정확한 치수는 모델 설치 가이드로 다시 확인한다.
var TYPES={
  k1:{n:'키친핏 1도어 (냉장·냉동·김치)',w:595,h:1855,d:690,doors:'1'},
  k4:{n:'키친핏 4도어',w:912,h:1855,d:690,doors:'4'},
  big:{n:'양문형·일반 4도어 (뚱냉)',w:912,h:1800,d:920,doors:'4'},
  custom:{n:'직접 입력',w:600,h:1850,d:700,doors:'1'}
};
var TALL={
  none:{n:'없음 (냉장고만)',w:0},
  two:{n:'키큰장 (투도어)',w:600},
  one:{n:'키큰장 (원도어)',w:450},
  bar:{n:'홈바장',w:600},
  rice:{n:'밥솥장',w:600},
  ricerange:{n:'밥솥렌지장',w:600},
  ovenrange:{n:'오븐렌지장',w:600}
};
var LOWS={norm:{n:'일반장'},drawer:{n:'서랍장'},oven:{n:'오븐 일반장'},rice:{n:'밥솥 일반장'}};
var JOBS={
  'new':{n:'냉장고장 새로 짜기 (맞춤제작)'},
  part:{n:'옵션 냉장고장 칸막이 제거'},
  gap:{n:'칸막이 제거 + 틈새장'}
};
var S={job:'new',fr:[{t:'k4',w:912,h:1855,d:690,m:''},{t:'k1',w:595,h:1855,d:690,m:''}],
  tall:'two',pos:'r',low:'norm',robot:false,unk:false,space:'',open:false,view:'front',area:'',step:0};

// ---------- 상태 저장 (주소 뒤에 붙여서 견적 문자에 같이 보냄) ----------
function enc(){
  var f=S.fr.map(function(x){return [x.t,x.w,x.h,x.d,x.m.replace(/[~|&#]/g,'')].join('~')}).join('|');
  return 'j='+S.job+'&f='+encodeURIComponent(f)+'&t='+S.tall+'&p='+S.pos+'&l='+S.low+'&r='+(S.robot?1:0)+'&s='+(S.space||'');
}
function dec(h){
  try{
    var p={};h.replace(/^#/,'').split('&').forEach(function(kv){var i=kv.indexOf('=');if(i>0)p[kv.slice(0,i)]=kv.slice(i+1)});
    if(p.j&&JOBS[p.j])S.job=p.j;
    if(p.f){var fr=decodeURIComponent(p.f).split('|').map(function(s){var a=s.split('~');return {t:TYPES[a[0]]?a[0]:'custom',w:+a[1]||600,h:+a[2]||1850,d:+a[3]||700,m:a[4]||''}}).slice(0,4);if(fr.length)S.fr=fr}
    if(p.t&&TALL[p.t])S.tall=p.t;
    if(p.p==='l'||p.p==='r')S.pos=p.p;
    if(p.l&&LOWS[p.l])S.low=p.l;
    if(p.r!==undefined)S.robot=p.r==='1';
    if(p.e!==undefined&&p.t===undefined){ // 예전 링크(e=robot.range…) 호환
      var e=p.e.split('.');S.robot=e.indexOf('robot')>=0;
      S.tall=e.indexOf('bar')>=0?'bar':(e.indexOf('range')>=0&&e.indexOf('rice')>=0)?'ricerange':e.indexOf('range')>=0?'ovenrange':e.indexOf('rice')>=0?'rice':(S.robot?'two':'none');
    }
    if(p.s)S.space=+p.s||'';
  }catch(e){}
}

// ---------- 가견적 ----------
function estimate(){
  if(S.job==='part')return {txt:'30만원',note:'칸막이·기둥 제거, 상부장과 천장 보강, 바닥·벽 마감, 폐자재 처리 포함'};
  if(S.job==='gap')return {txt:'70만원',note:'칸막이 제거 + 남는 폭에 틈새장까지'};
  var T=S.tall,has=T!=='none';
  var r=has&&S.robot,
      c=T==='rice'||T==='ricerange'||(has&&S.low==='rice'),
      g=T==='ricerange'||T==='ovenrange'||(has&&S.low==='oven'),
      b=T==='bar',cnt=[r,g,c,b].filter(Boolean).length,t=null;
  if(cnt===0)t=100;
  else if(cnt===1&&r)t=100;
  else if(cnt===1&&(g||c))t=110;
  else if(cnt===2&&g&&c)t=115;
  else if(cnt===1&&b)t=130;
  else if(cnt===2&&b&&(g||c))t=140;
  var drawer=has&&S.low==='drawer';
  if(t!==null)return {txt:t+'만원'+(drawer?'~':''),note:drawer?'서랍장은 서랍 수에 따라 조금 달라져요':'기본 단가 기준 (냉장고장 맞춤제작)'};
  var min=b?140:(g&&c)?115:(g||c)?110:100;
  return {txt:min+'만원~',note:'구성이 많아서 사진을 보고 정확한 금액을 알려드려요'};
}

// ---------- 배치 계산 ----------
var LOW=820,SIDE=20,GAP=10,UP=380,G=12; // LOW: 냉장고·키큰장 가운데 가로줄 높이, G: 문 사이 굵은 줄 반폭
function frW(){var w=0;S.fr.forEach(function(f,i){w+=f.w+(i?GAP:0)});return w}
function layout(){
  var cols=[],sp=+S.space||0,fw=frW(),need,tw=0,x=SIDE;
  var hasTall=S.job==='new'&&S.tall!=='none';
  if(hasTall){
    tw=TALL[S.tall].w;
    if(sp){var rest=sp-SIDE*3-fw;if(rest>=300)tw=Math.min(rest,1200)}
  }
  function fridges(){S.fr.forEach(function(f,i){if(i>0)x+=GAP;cols.push({k:'fr',f:f,x:x,w:f.w});x+=f.w})}
  function tall(){cols.push({k:S.tall,x:x,w:tw});x+=tw}
  if(hasTall&&S.pos==='l'){tall();x+=SIDE;fridges()}
  else{fridges();if(hasTall){x+=SIDE;tall()}}
  x+=SIDE;need=hasTall?SIDE*3+fw+300:x;
  if(S.job==='gap'){
    var left=sp?sp-x-SIDE:300;
    if(left>=120||!sp){left=left>=120?left:300;cols.push({k:'gap',x:x,w:left});x+=left+SIDE}
  }
  var hMax=Math.max.apply(null,S.fr.map(function(f){return f.h}));
  return {cols:cols,W:x,need:need,H:hMax+20+UP,bodyH:hMax+20,D:700};
}

// ---------- 그리기 (정면 / 입체) ----------
function render(){
  var L=layout(),v=S.view==='3d',kx=v?0.42:0,ky=v?0.26:0;
  var maxD=Math.max(L.D,Math.max.apply(null,S.fr.map(function(f){return f.d})));
  var pad=90,ext=S.open?560:0;
  var minX=-pad-(S.open?280:0),maxX=L.W+L.D*kx+pad+ext*0.3,minY=-(L.H+L.D*ky)-80,maxY=(maxD-L.D+ext)*ky+150;
  function P(x,y,z){return [(x+z*kx).toFixed(1),(-y-z*ky).toFixed(1)]}  // z: 앞면 0, 뒤로 +
  function rect(x,y,w,h,cls){return poly([[x,y,0],[x+w,y,0],[x+w,y+h,0],[x,y+h,0]],cls)}
  function poly(pts,cls){return '<polygon class="'+cls+'" points="'+pts.map(function(p){return P(p[0],p[1],p[2]).join(',')}).join(' ')+'"/>'}
  function box(x,y,z,w,h,d,cls){ // 보이는 면: 윗면, 오른쪽면, 앞면
    var s='';
    if(v&&d>0){s+=poly([[x,y+h,z],[x+w,y+h,z],[x+w,y+h,z+d],[x,y+h,z+d]],cls+' top');
      s+=poly([[x+w,y,z],[x+w,y,z+d],[x+w,y+h,z+d],[x+w,y+h,z]],cls+' side');}
    s+=poly([[x,y,z],[x+w,y,z],[x+w,y+h,z],[x,y+h,z]],cls+' front');
    return s;
  }
  function door(x,y,z,w,h,hinge,cls){ // hinge: 'l'|'r'
    if(!S.open)return poly([[x,y,z],[x+w,y,z],[x+w,y+h,z],[x,y+h,z]],cls);
    var a=0.8,hx=hinge==='l'?x:x+w,dx=Math.cos(a)*w*(hinge==='l'?1:-1),dz=-Math.sin(a)*w;
    return poly([[hx,y,z],[hx+dx,y,z+dz],[hx+dx,y+h,z+dz],[hx,y+h,z]],cls+' open');
  }
  function doors(x,y,w,h,cls){ // 폭이 아주 넓을 때만 양문
    if(w>720)return door(x+G,y,0,w/2-G*1.5,h,'l',cls)+door(x+w/2+G/2,y,0,w/2-G*1.5,h,'r',cls);
    return door(x+G,y,0,w-G*2,h,S.pos==='l'?'l':'r',cls);
  }
  function drawer(x,y,w,h,cls){ // 서랍: 열면 앞으로 빠짐
    var d=S.open?-300:0;
    return box(x+G,y,d,w-G*2,h,S.open?300:0,cls||'dz-door');
  }
  var g='',D=L.D,items=[];
  g+='<rect class="dz-wall" x="'+minX+'" y="'+minY+'" width="'+(maxX-minX)+'" height="'+(-minY)+'"/>';
  g+='<rect class="dz-floor" x="'+minX+'" y="0" width="'+(maxX-minX)+'" height="'+maxY+'"/>';
  // 몸통: 상부장 띠, 양옆·사이 판재
  items.push({z:D,s:box(0,L.bodyH,0,L.W,UP,D,'dz-cab')+box(-18,L.H,-18,L.W+36,30,D+18,'dz-cab')});
  var panels=[0];
  L.cols.forEach(function(c,i){if(i>0&&(c.k!=='fr'||L.cols[i-1].k!=='fr'))panels.push(c.x-SIDE)});
  panels.push(L.W-SIDE);
  panels.forEach(function(px){items.push({z:0,x:px,s:box(px,0,0,SIDE,L.bodyH,D,'dz-cab')})});
  // 상부장 문: 아래 냉장고·장 폭과 똑같이
  var upDoors='';
  L.cols.forEach(function(c){
    var n=c.w<=700||(S.job==='new'&&c.k==='fr')?1:2,dw=c.w/n;
    for(var i=0;i<n;i++)upDoors+=door(c.x+i*dw+2,L.bodyH+12,0,dw-4,UP-24,n===2?(i?'r':'l'):'l','dz-door');
  });
  L.cols.forEach(function(c){
    if(c.k==='fr'){
      var f=c.f,z=D-f.d,s=box(c.x,0,z,c.w,L.bodyH-(D-f.d>0?0:0),f.d,'dz-fr');
      // 가운데 가로줄(LOW)은 옆 키큰장 줄과 이어진다. 문 사이는 굵은 줄로 보인다
      var dr=S.open?-260:0,top=L.bodyH-LOW-G*1.5,lo=LOW-G*1.5,hw=c.w/2-G*1.5;
      if(TYPES[f.t]&&TYPES[f.t].doors==='4'){
        s+=door(c.x+G,LOW+G/2,z,hw,top,'l','dz-frd')+door(c.x+c.w/2+G/2,LOW+G/2,z,hw,top,'r','dz-frd');
        s+=box(c.x+G,G,z+dr,hw,lo,S.open?260:0,'dz-frd')+box(c.x+c.w/2+G/2,G,z+dr,hw,lo,S.open?260:0,'dz-frd');
      }else{
        // 1도어: 위 문 + 아래 서랍 2칸
        var dh=lo/2-G/2;
        s+=door(c.x+G,LOW+G/2,z,c.w-G*2,top,'r','dz-frd');
        s+=box(c.x+G,G,z+dr,c.w-G*2,dh,S.open?260:0,'dz-frd')+box(c.x+G,G*2+dh,z+dr*0.6,c.w-G*2,dh,S.open?260:0,'dz-frd');
      }
      items.push({z:z,x:c.x,s:s});
      return;
    }
    var h=L.bodyH,s2='',x=c.x,w=c.w;
    if(c.k==='gap'){items.push({z:0,x:x,s:rect(x,0,w,h,'dz-seam')+door(x+G,G,0,w-G*2,h-G*2,'l','dz-door')});return}
    s2+=rect(x,0,w,h,'dz-seam');
    // --- 하부장 (0 ~ LOW) ---
    var b0=0;
    if(S.robot){
      s2+=rect(x+G,0,w-G*2,150,'dz-hole')+rect(x+w/2-Math.min(130,w/2-30),6,Math.min(260,w-60),90,'dz-st');
      var q1=P(x+w,0,0),q2=P(x+w,150,0);
      s2+='<text class="dz-r150" x="'+(+q1[0]-14)+'" y="'+((+q1[1]+ +q2[1])/2+14)+'">150</text>';
      b0=150+G;
    }else b0=G;
    var lh=LOW-G/2-b0;
    if(S.low==='drawer'){
      var n=lh>400?3:2,dh=(lh-G*(n-1))/n;
      for(var i=0;i<n;i++)s2+=drawer(x,b0+i*(dh+G),w,dh);
    }else if(S.low==='oven'||S.low==='rice'){
      // 가전이 들어가는 칸(문 없음) + 아래 작은 서랍
      var nh=S.low==='oven'?Math.min(lh-140,560):Math.min(lh-200,330),ny=LOW-G/2-nh;
      s2+=rect(x+G,ny,w-G*2,nh,'dz-niche');
      if(S.low==='oven'){s2+=rect(x+24,ny+20,w-48,nh-40,'dz-st')+rect(x+50,ny+nh-80,w-100,14,'dz-hdl')}
      else{s2+=rect(x+w/2-130,ny+10,260,Math.min(220,nh-40),'dz-st')+rect(x+12,ny,w-24,10,'dz-shelf')}
      if(ny-b0>60)s2+=drawer(x,b0,w,ny-b0-G);
    }else if(!(c.k==='one'&&!S.robot)){
      s2+=doors(x,b0,w,lh,'dz-door');
    }
    // --- 위쪽 (LOW ~ 몸통 끝) ---
    var u0=LOW+G/2,uh=h-u0-G;
    if(c.k==='two'){
      s2+=doors(x,u0,w,uh,'dz-door'); // 투도어: 위 문 + 아래 문
    }else if(c.k==='one'){
      if(S.low==='norm'&&!S.robot)s2+=doors(x,G,w,h-G*2,'dz-door'); // 원도어: 통문 하나
      else s2+=doors(x,u0,w,uh,'dz-door');
    }else if(c.k==='bar'){
      s2+=rect(x+G,u0,w-G*2,uh-400-G,'dz-hb');
      for(var j=0;j<3;j++)s2+=rect(x+G+4,u0+180+j*240,w-G*2-8,12,'dz-shelf');
      s2+=door(x+G,h-400-G,0,w-G*2,400,'l','dz-door');
    }else if(c.k==='rice'){
      s2+=rect(x+G,u0,w-G*2,420,'dz-niche')+rect(x+w/2-130,u0+20,260,200,'dz-st')+rect(x+12,u0,w-24,10,'dz-shelf');
      s2+=doors(x,u0+420+G,w,uh-420-G,'dz-door');
    }else if(c.k==='ricerange'){
      s2+=rect(x+G,u0,w-G*2,700,'dz-niche')+rect(x+w/2-130,u0+20,260,200,'dz-st')+rect(x+40,u0+380,w-80,280,'dz-st')+rect(x+12,u0+350,w-24,12,'dz-shelf');
      s2+=doors(x,u0+700+G,w,uh-700-G,'dz-door');
    }else if(c.k==='ovenrange'){
      s2+=rect(x+G,u0,w-G*2,880,'dz-niche')+rect(x+24,u0+20,w-48,520,'dz-st')+rect(x+50,u0+460,w-100,14,'dz-hdl')+rect(x+40,u0+580,w-80,260,'dz-st')+rect(x+12,u0+560,w-24,12,'dz-shelf');
      s2+=doors(x,u0+880+G,w,uh-880-G,'dz-door');
    }
    items.push({z:0,x:x,s:s2});
  });
  items.sort(function(a,b){return (b.z>=D)-(a.z>=D)||(a.x||0)-(b.x||0)});
  items.forEach(function(it){g+=it.s});
  g+=upDoors;
  // 치수
  var dim='',yy=v?70+(maxD-D)*ky:60;
  // 칸 사이(판재 20, 냉장고 사이 10) 눈금
  var seps=[[0,SIDE]];
  L.cols.forEach(function(c,i){var nx=i<L.cols.length-1?L.cols[i+1].x:L.W;seps.push([c.x+c.w,nx-(c.x+c.w)])});
  seps.forEach(function(sp){var m=P(sp[0]+sp[1]/2,0,0);
    dim+='<line class="dz-tick" x1="'+m[0]+'" y1="'+(yy-30)+'" x2="'+m[0]+'" y2="'+(yy+90)+'"/><text class="dz-sp" x="'+m[0]+'" y="'+(yy+150)+'">'+Math.round(sp[1])+'</text>'});
  L.cols.forEach(function(c){
    var a=P(c.x,0,0),b=P(c.x+c.w,0,0);
    dim+='<text class="dz-dt" x="'+((+a[0]+ +b[0])/2)+'" y="'+(yy+72)+'">'+Math.round(c.w)+'</text>';
    var lab=c.k==='fr'?(TYPES[c.f.t]?TYPES[c.f.t].n.split(' (')[0]:'냉장고'):c.k==='gap'?'틈새장':TALL[c.k].n.replace(' (투도어)','').replace(' (원도어)','');
    if(c.k!=='fr'&&c.k!=='gap'&&S.robot)lab+=' + 로봇';
    dim+='<text class="dz-lab" x="'+((+a[0]+ +b[0])/2)+'" y="'+(yy+215)+'">'+lab+'</text>';
  });
  var a0=P(0,0,0),a1=P(L.W,0,0);
  dim+='<text class="dz-tot" x="'+((+a0[0]+ +a1[0])/2)+'" y="'+(yy+300)+'">전체 폭 약 '+Math.round(L.W).toLocaleString()+'mm</text>';
  var vb=[minX,minY,maxX-minX,(yy+330)-minY].map(function(n){return n.toFixed(0)}).join(' ');
  $('dz-svg').setAttribute('viewBox',vb);
  $('dz-svg').innerHTML=g+dim;
  return L;
}

// ---------- 결과·문자 ----------
function frName(f){return (TYPES[f.t]?TYPES[f.t].n.split(' (')[0]:'냉장고')+(f.m?' '+f.m:'')+' '+f.w+'mm'}
function tallTxt(){
  if(S.job!=='new')return '';
  if(S.tall==='none')return '없음 (냉장고만)';
  return TALL[S.tall].n+' · '+(S.pos==='l'?'왼쪽':'오른쪽')+' / 하부장 '+LOWS[S.low].n+(S.robot?' + 로봇청소기 공간':'');
}
function summary(L){
  var e=estimate();
  $('dz-won').textContent=e.txt;
  $('dz-note').textContent=e.note+' · VAT 별도 · 출장비는 위치에 따라 조율';
  var fit=$('dz-fit'),sp=+S.space||0;
  if(!sp){fit.className='dz-fit';fit.textContent='필요한 폭은 약 '+Math.round(L.W).toLocaleString()+'mm예요. 냉장고장 자리 폭을 넣으면 들어가는지 알려드려요.'}
  else{var diff=sp-L.need;
    if(diff>=0){fit.className='dz-fit ok';fit.textContent=S.job==='new'&&S.tall!=='none'?'들어가요. 키큰장은 남는 폭에 맞춰 약 '+Math.round(L.cols.filter(function(c){return c.k===S.tall})[0].w)+'mm로 그렸어요.':'들어가요. 여유 약 '+Math.round(sp-L.W+(S.job==='gap'?0:0))+'mm'}
    else{fit.className='dz-fit no';fit.textContent='약 '+Math.round(-diff)+'mm 부족해요. '+(S.job==='new'?'구성을 줄이거나 사진을 보내주시면 방법을 찾아드려요.':'칸막이·기둥을 빼도 모자라면 새로 짜야 할 수 있어요.')}}
  var link='https://nemos-dream.com/design#'+enc();
  var frs=S.fr.map(function(f,i){return (i+1)+') '+frName(f)}).join(', ');
  var body='[네모의꿈 3D 가견적 문의]\n1. 지역·아파트 : '+(S.area||'')+'\n2. 원하는 작업 : '+JOBS[S.job].n+'\n3. 냉장고 : '+frs+(S.job==='new'?'\n4. 키큰장 : '+tallTxt():'')+'\n5. 냉장고장 자리 폭 : '+(sp?sp+'mm':'(모르면 비워 두세요)')+'\n6. 가견적 : '+e.txt+' (VAT 별도)\n7. 사진 : 냉장고장 자리 사진 2장 첨부해 주세요\n내 설계 보기 : '+link;
  $('dz-pre').textContent=body;
  $('dz-sms').href='sms:'+PHONE+'?&body='+encodeURIComponent(body);
  // 확인 화면 요약
  var rows=[['작업',JOBS[S.job].n],['냉장고',S.fr.map(frName).join('\n')]];
  if(S.job==='new')rows.push(['키큰장',tallTxt()]);
  rows.push(['자리 폭',sp?sp+'mm':'모름 (기본값으로 그림)'],['전체 폭','약 '+Math.round(L.W).toLocaleString()+'mm'],['가견적',e.txt+' (VAT 별도)']);
  $('dz-sum').innerHTML=rows.map(function(r){return '<dt>'+r[0]+'</dt><dd>'+esc(r[1]).replace(/\n/g,'<br>')+'</dd>'}).join('');
  try{history.replaceState(null,'','#'+enc())}catch(e){}
}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}

// ---------- 입력 화면 ----------
function frRow(f,i){
  var opts=Object.keys(TYPES).map(function(k){return '<option value="'+k+'"'+(k===f.t?' selected':'')+'>'+TYPES[k].n+'</option>'}).join('');
  return '<div class="dz-fr" data-i="'+i+'"><div class="dz-frh"><b>냉장고 '+(i+1)+'</b>'+(S.fr.length>1?'<button type="button" class="dz-del" data-i="'+i+'" aria-label="냉장고 '+(i+1)+' 빼기">빼기</button>':'')+'</div>'
   +(S.unk?'':'<label class="dz-l">모델명 / 색상<input data-k="m" value="'+esc(f.m)+'" placeholder="모델명 입력 (예: 옆면 스티커)" maxlength="30"></label>')
   +'<label class="dz-l">종류<select data-k="t">'+opts+'</select></label>'
   +'<div class="dz-mm"><label>가로<input data-k="w" type="number" inputmode="numeric" value="'+f.w+'"></label><label>높이<input data-k="h" type="number" inputmode="numeric" value="'+f.h+'"></label><label>깊이<input data-k="d" type="number" inputmode="numeric" value="'+f.d+'"></label><span>mm</span></div></div>';
}
// 작은 아이콘 (키큰장 형태·하부장)
function icon(k){
  var r=function(x,y,w,h,c){return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="1.5" class="'+c+'"/>'};
  var s='';
  if(k==='none')s=r(5,3,18,34,'i-o')+'<line x1="6" y1="36" x2="22" y2="4" class="i-x"/>';
  else if(k==='two')s=r(4,3,10,21,'i-d')+r(14,3,10,21,'i-d')+r(4,25,20,12,'i-d');
  else if(k==='one')s=r(7,3,14,21,'i-d')+r(7,25,14,12,'i-d');
  else if(k==='bar')s=r(4,3,20,21,'i-hb')+'<line x1="5" y1="10" x2="23" y2="10" class="i-s"/><line x1="5" y1="17" x2="23" y2="17" class="i-s"/>'+r(4,25,20,12,'i-d');
  else if(k==='rice')s=r(4,3,20,11,'i-d')+r(4,14,20,10,'i-n')+r(10,16,8,6,'i-a')+r(4,25,20,12,'i-d');
  else if(k==='ricerange')s=r(4,3,20,7,'i-d')+r(4,10,20,14,'i-n')+r(10,11,8,5,'i-a')+r(7,17,14,6,'i-a')+r(4,25,20,12,'i-d');
  else if(k==='ovenrange')s=r(4,3,20,5,'i-d')+r(4,8,20,16,'i-n')+r(7,9,14,5,'i-a')+r(6,15,16,8,'i-a')+r(4,25,20,12,'i-d');
  else if(k==='norm')s=r(4,3,20,21,'i-o')+r(4,25,10,12,'i-d')+r(14,25,10,12,'i-d');
  else if(k==='drawer')s=r(4,3,20,21,'i-o')+r(4,25,20,6,'i-d')+r(4,31,20,6,'i-d');
  else if(k==='oven')s=r(4,3,20,21,'i-o')+r(4,25,20,8,'i-n')+r(6,26,16,6,'i-a')+r(4,33,20,4,'i-d');
  else if(k==='lrice')s=r(4,3,20,21,'i-o')+r(4,25,20,7,'i-n')+r(10,26,8,5,'i-a')+r(4,32,20,5,'i-d');
  return '<svg viewBox="0 0 28 40" aria-hidden="true">'+s+'</svg>';
}
function pickHtml(name,map,cur,iconKey){
  return Object.keys(map).map(function(k){return '<label><input type="radio" name="'+name+'" value="'+k+'"'+(k===cur?' checked':'')+'>'+icon(iconKey?iconKey(k):k)+'<span>'+map[k].n+'</span></label>'}).join('');
}
function drawForm(){
  $('dz-frs').innerHTML=S.fr.map(frRow).join('');
  $('dz-add').hidden=S.fr.length>=4;
  $('dz-unk').checked=S.unk;
  document.querySelectorAll('input[name=dz-job]').forEach(function(r){r.checked=r.value===S.job});
  $('dz-tall').innerHTML=pickHtml('dz-tall',TALL,S.tall);
  $('dz-low').innerHTML=pickHtml('dz-low',LOWS,S.low,function(k){return k==='rice'?'lrice':k});
  var isNew=S.job==='new',noTall=S.tall==='none';
  $('dz-off').hidden=isNew;$('dz-optbox').hidden=!isNew;$('dz-posl').hidden=!isNew||noTall;
  $('dz-low').classList.toggle('off',noTall);$('dz-robot').disabled=noTall;
  document.querySelectorAll('input[name=dz-low]').forEach(function(r){r.disabled=noTall});
  $('dz-robot').checked=S.robot&&!noTall;
  $('dz-pos').value=S.pos;
  $('dz-space').value=S.space||'';
  $('dz-space').placeholder='기본값 '+Math.round(layout().W);
}
function go(n){
  S.step=Math.max(0,Math.min(2,n));
  document.querySelectorAll('.dz-step').forEach(function(el){el.hidden=+el.dataset.s!==S.step});
  document.querySelectorAll('#dz-steps button').forEach(function(b){b.setAttribute('aria-current',+b.dataset.s===S.step?'step':'false')});
  $('dz-prev').style.visibility=S.step?'visible':'hidden';
  $('dz-next').hidden=S.step===2;
}
function update(){var L=render();summary(L)}

// 그림 저장 (PNG)
function savePng(){
  var svg=$('dz-svg'),cl=svg.cloneNode(true),src=svg.querySelectorAll('*'),dst=cl.querySelectorAll('*');
  for(var i=0;i<src.length;i++){var cs=getComputedStyle(src[i]);
    dst[i].setAttribute('style','fill:'+cs.fill+';stroke:'+cs.stroke+';stroke-width:'+cs.strokeWidth+';opacity:'+cs.opacity+';font:'+cs.fontWeight+' '+cs.fontSize+' sans-serif;text-anchor:'+cs.textAnchor)}
  var vb=svg.viewBox.baseVal,W=1600,H=Math.round(W*vb.height/vb.width);
  cl.setAttribute('xmlns','http://www.w3.org/2000/svg');cl.setAttribute('width',W);cl.setAttribute('height',H);
  var img=new Image();
  img.onload=function(){
    var cv=document.createElement('canvas');cv.width=W;cv.height=H+90;var x=cv.getContext('2d');
    x.fillStyle='#fff';x.fillRect(0,0,W,H+90);x.drawImage(img,0,0,W,H);
    x.fillStyle='#00843d';x.font='bold 34px sans-serif';x.fillText('네모의꿈 냉장고장 설계 · 가견적 '+estimate().txt+' (VAT 별도) · 010-4835-3353',30,H+56);
    cv.toBlob(function(b){var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='네모의꿈-냉장고장-설계.png';document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},1500);
      $('dz-toast').textContent='그림을 저장했어요. 문자 보낼 때 같이 첨부해도 돼요.'},'image/png');
  };
  img.onerror=function(){$('dz-toast').textContent='이 브라우저에서는 저장이 안 돼요. 화면을 캡처해 주세요.'};
  img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(new XMLSerializer().serializeToString(cl));
}

function bind(){
  $('dz-frs').addEventListener('input',function(ev){
    var t=ev.target,row=t.closest('.dz-fr');if(!row)return;var f=S.fr[+row.dataset.i],k=t.dataset.k;
    if(k==='t'){var T=TYPES[t.value];f.t=t.value;if(t.value!=='custom'){f.w=T.w;f.h=T.h;f.d=T.d}
      row.querySelector('[data-k=w]').value=f.w;row.querySelector('[data-k=h]').value=f.h;row.querySelector('[data-k=d]').value=f.d}
    else if(k==='m')f.m=t.value;
    else{var n=Math.round(+t.value);if(n>=300&&n<=2200)f[k]=n;else return}
    update();
  });
  $('dz-frs').addEventListener('click',function(ev){var b=ev.target.closest('.dz-del');if(!b)return;S.fr.splice(+b.dataset.i,1);drawForm();update()});
  $('dz-add').addEventListener('click',function(){S.fr.push({t:'k1',w:595,h:1855,d:690,m:''});drawForm();update()});
  $('dz-unk').addEventListener('change',function(){S.unk=this.checked;drawForm()});
  document.querySelectorAll('input[name=dz-job]').forEach(function(r){r.addEventListener('change',function(){S.job=r.value;drawForm();update()})});
  $('dz-tall').addEventListener('change',function(ev){S.tall=ev.target.value;drawForm();update()});
  $('dz-low').addEventListener('change',function(ev){S.low=ev.target.value;update()});
  $('dz-robot').addEventListener('change',function(){S.robot=this.checked;update()});
  $('dz-pos').addEventListener('change',function(){S.pos=this.value;update()});
  $('dz-space').addEventListener('input',function(){var n=Math.round(+this.value);S.space=n>=600&&n<=6000?n:'';update()});
  $('dz-area').addEventListener('input',function(){S.area=this.value.slice(0,40);summary(layout())});
  $('dz-open').addEventListener('click',function(){S.open=!S.open;this.setAttribute('aria-pressed',S.open);this.textContent=S.open?'문 닫기':'문 열기';render()});
  document.querySelectorAll('.dz-view button').forEach(function(b){b.addEventListener('click',function(){S.view=b.dataset.v;document.querySelectorAll('.dz-view button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});render()})});
  document.querySelectorAll('#dz-steps button').forEach(function(b){b.addEventListener('click',function(){go(+b.dataset.s)})});
  $('dz-prev').addEventListener('click',function(){go(S.step-1);$('dz-steps').scrollIntoView({behavior:'smooth',block:'start'})});
  $('dz-next').addEventListener('click',function(){go(S.step+1);$('dz-steps').scrollIntoView({behavior:'smooth',block:'start'})});
  $('dz-png').addEventListener('click',savePng);
  $('dz-copy').addEventListener('click',function(){var t=$('dz-pre').textContent;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){$('dz-toast').textContent='복사했어요. 문자 앱에 붙여 넣어 주세요.'},function(){$('dz-toast').textContent='길게 눌러서 복사해 주세요.'})});
}
if(location.hash.length>2)dec(location.hash);
drawForm();bind();update();go(0);
})();
