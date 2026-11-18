/* 네모의꿈 냉장고장 3D 미리보기 · 가견적 (design.html) */
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
var EX={robot:{n:'로봇청소기장',w:450},range:{n:'렌지장',w:600},rice:{n:'밥솥장',w:600},bar:{n:'홈바장',w:600}};
var JOBS={
  'new':{n:'냉장고장 새로 짜기 (맞춤제작)'},
  part:{n:'옵션 냉장고장 칸막이 제거'},
  gap:{n:'칸막이 제거 + 틈새장'}
};
var S={job:'new',fr:[{t:'k4',w:912,h:1855,d:690,m:''},{t:'k1',w:595,h:1855,d:690,m:''}],ex:{robot:false,range:false,rice:false,bar:false},space:'',open:false,view:'3d',area:''};

// ---------- 상태 저장 (주소 뒤에 붙여서 견적 문자에 같이 보냄) ----------
function enc(){
  var f=S.fr.map(function(x){return [x.t,x.w,x.h,x.d,x.m.replace(/[~|]/g,'')].join('~')}).join('|');
  var e=Object.keys(EX).filter(function(k){return S.ex[k]}).join('.');
  return 'j='+S.job+'&f='+encodeURIComponent(f)+'&e='+e+'&s='+(S.space||'');
}
function dec(h){
  try{
    var p={};h.replace(/^#/,'').split('&').forEach(function(kv){var i=kv.indexOf('=');if(i>0)p[kv.slice(0,i)]=kv.slice(i+1)});
    if(p.j&&JOBS[p.j])S.job=p.j;
    if(p.f){var fr=decodeURIComponent(p.f).split('|').map(function(s){var a=s.split('~');return {t:TYPES[a[0]]?a[0]:'custom',w:+a[1]||600,h:+a[2]||1850,d:+a[3]||700,m:a[4]||''}}).slice(0,4);if(fr.length)S.fr=fr}
    if(p.e!==undefined)Object.keys(EX).forEach(function(k){S.ex[k]=p.e.split('.').indexOf(k)>=0});
    if(p.s)S.space=+p.s||'';
  }catch(e){}
}

// ---------- 가견적 ----------
function estimate(){
  if(S.job==='part')return {won:30,txt:'30만원',note:'칸막이·기둥 제거, 상부장과 천장 보강, 바닥·벽 마감, 폐자재 처리 포함'};
  if(S.job==='gap')return {won:70,txt:'70만원',note:'칸막이 제거 + 남는 폭에 틈새장까지'};
  var e=S.ex,r=e.robot,g=e.range,c=e.rice,b=e.bar,cnt=[r,g,c,b].filter(Boolean).length;
  var t=null;
  if(cnt===0)t=100;
  else if(cnt===1&&r)t=100;
  else if(cnt===1&&(g||c))t=110;
  else if(cnt===2&&g&&c)t=115;
  else if(cnt===1&&b)t=130;
  else if(cnt===2&&b&&(g||c))t=140;
  if(t!==null)return {won:t,txt:t+'만원',note:'기본 단가 기준 (냉장고장 맞춤제작)'};
  var min=b?140:(g&&c)?115:(g||c)?110:100;
  return {won:min,txt:min+'만원~',note:'구성이 많아서 사진을 보고 정확한 금액을 알려드려요'};
}

// ---------- 배치 계산 ----------
var SIDE=20,GAP=10,UP=380;
function layout(){
  var cols=[],x=SIDE;
  S.fr.forEach(function(f,i){if(i>0)x+=GAP;cols.push({k:'fr',f:f,x:x,w:f.w});x+=f.w});
  var need;
  if(S.job==='new'){
    Object.keys(EX).forEach(function(k){
      if(!S.ex[k])return;
      if(k==='rice'&&S.ex.range){return}
      x+=SIDE;cols.push({k:k,x:x,w:EX[k].w,both:k==='range'&&S.ex.rice});x+=EX[k].w;
    });
    x+=SIDE;need=x;
  }else{
    x+=SIDE;need=x;
    var sp=+S.space||0;
    if(S.job==='gap'){
      var left=sp?sp-need-SIDE:300;
      if(left>=120){x+=SIDE;cols.push({k:'gap',x:x,w:left});x+=left;x+=SIDE}
      else if(!sp){x+=SIDE;cols.push({k:'gap',x:x,w:300});x+=300;x+=SIDE}
    }
  }
  var hMax=Math.max.apply(null,S.fr.map(function(f){return f.h}));
  var bodyH=hMax+20;
  return {cols:cols,W:Math.max(x,need),need:need,H:bodyH+UP,bodyH:bodyH,D:700};
}

// ---------- 그리기 (정면 / 입체) ----------
function render(){
  var L=layout(),v=S.view==='3d',kx=v?0.42:0,ky=v?0.26:0;
  var maxD=Math.max(L.D,Math.max.apply(null,S.fr.map(function(f){return f.d})));
  var pad=90,ext=S.open?560:0;
  var minX=-pad-(S.open?280:0),maxX=L.W+L.D*kx+pad+ext*0.3,minY=-(L.H+L.D*ky)-40,maxY=(maxD-L.D+ext)*ky+150;
  function P(x,y,z){return [(x+z*kx).toFixed(1),(-y-z*ky).toFixed(1)]}  // z: 앞면 0, 뒤로 +
  function poly(pts,cls){return '<polygon class="'+cls+'" points="'+pts.map(function(p){return P(p[0],p[1],p[2]).join(',')}).join(' ')+'"/>'}
  function box(x,y,z,w,h,d,cls){ // 뒤에서 앞으로 보이는 면: 윗면, 오른쪽면, 앞면
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
  var g='',D=L.D,items=[];
  // 바닥·벽
  g+='<rect class="dz-wall" x="'+minX+'" y="'+minY+'" width="'+(maxX-minX)+'" height="'+(-minY)+'"/>';
  g+='<rect class="dz-floor" x="'+minX+'" y="0" width="'+(maxX-minX)+'" height="'+maxY+'"/>';
  // 몸통: 상부장 띠, 양옆·사이 판재
  items.push({z:D,s:box(0,L.bodyH,0,L.W,UP,D,'dz-cab')});
  var panels=[0];
  L.cols.forEach(function(c,i){if(c.k!=='fr'){panels.push(c.x-SIDE)}});
  panels.push(L.W-SIDE);
  if(S.job!=='new'&&S.fr.length>1){} // 칸막이 제거: 냉장고 사이 판재 없음
  panels.forEach(function(px){items.push({z:0,x:px,s:box(px,0,0,SIDE,L.bodyH,D,'dz-cab')})});
  // 상부장 문
  // 상부장 문: 아래 냉장고·장 폭과 똑같이 (새로 짤 땐 한 짝, 리폼은 넓으면 양문)
  var upDoors='';
  L.cols.forEach(function(c){
    var n=(S.job==='new'||c.w<=700)?1:2,dw=c.w/n;
    for(var i=0;i<n;i++)upDoors+=door(c.x+i*dw+2,L.bodyH+12,0,dw-4,UP-24,n===2?(i?'r':'l'):'l','dz-door');
  });
  // 열 (냉장고·추가 장)
  L.cols.forEach(function(c){
    if(c.k==='fr'){
      var f=c.f,z=D-f.d,s=box(c.x,0,z,c.w,f.h,f.d,'dz-fr');
      if(TYPES[f.t]&&TYPES[f.t].doors==='4'){
        // 4도어: 위 문 2짝 + 아래 서랍 2개 (가로줄 하나)
        var top=f.h*0.58,bot=f.h-top-12,dr=S.open?-260:0;
        s+=door(c.x+2,bot+12,z,c.w/2-3,top-4,'l','dz-frd')+door(c.x+c.w/2+1,bot+12,z,c.w/2-3,top-4,'r','dz-frd');
        s+=box(c.x+2,2,z+dr,c.w/2-3,bot+6,S.open?260:0,'dz-frd')+box(c.x+c.w/2+1,2,z+dr,c.w/2-3,bot+6,S.open?260:0,'dz-frd');
      }else{
        s+=door(c.x+2,4,z,c.w-4,f.h-8,'r','dz-frd');
      }
      items.push({z:z,x:c.x,s:s});
    }else{
      var h=L.bodyH,s2='',cls='dz-door';
      if(c.k==='robot'){
        s2+=box(c.x,0,0,c.w,h,0,'dz-in');
        // 로봇청소기장: 아래 150mm는 로봇이 드나드는 빈 칸, 그 위는 문 (열면 스테이션)
        s2+=poly([[c.x+2,0,0],[c.x+c.w-2,0,0],[c.x+c.w-2,150,0],[c.x+2,150,0]],'dz-hole');
        s2+=poly([[c.x+90,6,0],[c.x+c.w-90,6,0],[c.x+c.w-90,96,0],[c.x+90,96,0]],'dz-st');
        if(S.open)s2+=poly([[c.x+60,160,0],[c.x+c.w-60,160,0],[c.x+c.w-60,520,0],[c.x+60,520,0]],'dz-st');
        s2+=door(c.x+2,154,0,c.w-4,h-158,'l',cls);
        var q1=P(c.x+c.w,0,0),q2=P(c.x+c.w,150,0);
        s2+='<text class="dz-r150" x="'+(+q1[0]-14)+'" y="'+((+q1[1]+ +q2[1])/2+14)+'">150</text>';
      }else if(c.k==='range'){
        s2+=box(c.x,0,0,c.w,h,0,'dz-in');
        s2+=poly([[c.x+40,900,0],[c.x+c.w-40,900,0],[c.x+c.w-40,1200,0],[c.x+40,1200,0]],'dz-st');
        if(c.both)s2+=poly([[c.x+120,640,0],[c.x+c.w-120,640,0],[c.x+c.w-120,860,0],[c.x+120,860,0]],'dz-st');
        s2+=door(c.x+2,1260,0,c.w-4,h-1264,'l',cls)+door(c.x+2,4,0,c.w-4,600,'l',cls);
      }else if(c.k==='rice'){
        s2+=box(c.x,0,0,c.w,h,0,'dz-in');
        s2+=poly([[c.x+120,900,0],[c.x+c.w-120,900,0],[c.x+c.w-120,1120,0],[c.x+120,1120,0]],'dz-st');
        s2+=door(c.x+2,1260,0,c.w-4,h-1264,'l',cls)+door(c.x+2,4,0,c.w-4,600,'l',cls);
      }else if(c.k==='bar'){
        s2+=box(c.x,0,0,c.w,h,0,'dz-hb');
        for(var j=1;j<4;j++)s2+=poly([[c.x+10,700+j*280,0],[c.x+c.w-10,700+j*280,0],[c.x+c.w-10,712+j*280,0],[c.x+10,712+j*280,0]],'dz-shelf');
        s2+=door(c.x+2,4,0,c.w-4,640,'l',cls);
      }else if(c.k==='gap'){
        s2+=door(c.x+2,4,0,c.w-4,h-8,'l',cls);
      }
      items.push({z:0,x:c.x,s:s2});
    }
  });
  items.sort(function(a,b){return (b.z>=D)-(a.z>=D)||(a.x||0)-(b.x||0)});
  items.forEach(function(it){g+=it.s});
  g+=upDoors;
  // 치수
  var dim='',yy=v?70+ (maxD-D)*ky:60;
  L.cols.forEach(function(c){
    var a=P(c.x,0,0),b=P(c.x+c.w,0,0);
    dim+='<line class="dz-dl" x1="'+a[0]+'" y1="'+yy+'" x2="'+b[0]+'" y2="'+yy+'"/><text class="dz-dt" x="'+((+a[0]+ +b[0])/2)+'" y="'+(yy+72)+'">'+Math.round(c.w)+'</text>';
    var lab=c.k==='fr'?(TYPES[c.f.t]?TYPES[c.f.t].n.split(' (')[0]:'냉장고'):c.k==='gap'?'틈새장':c.k==='range'&&c.both?'렌지·밥솥장':EX[c.k].n;
    dim+='<text class="dz-lab" x="'+((+a[0]+ +b[0])/2)+'" y="'+(yy+140)+'">'+lab+'</text>';
  });
  var a0=P(0,0,0),a1=P(L.W,0,0);
  dim+='<text class="dz-tot" x="'+((+a0[0]+ +a1[0])/2)+'" y="'+(yy+230)+'">전체 폭 약 '+Math.round(L.W).toLocaleString()+'mm</text>';
  var vb=[minX,minY,maxX-minX,(yy+260)-minY].map(function(n){return n.toFixed(0)}).join(' ');
  $('dz-svg').setAttribute('viewBox',vb);
  $('dz-svg').innerHTML=g+dim;
  return L;
}

// ---------- 결과·문자 ----------
function summary(L){
  var e=estimate();
  $('dz-won').textContent=e.txt;
  $('dz-note').textContent=e.note+' · VAT 별도 · 출장비는 위치에 따라 조율';
  var fit=$('dz-fit'),sp=+S.space||0;
  if(!sp){fit.className='dz-fit';fit.textContent='필요한 폭은 약 '+Math.round(L.need).toLocaleString()+'mm예요. 냉장고장 자리 폭을 넣으면 들어가는지 알려드려요.'}
  else{var diff=sp-L.need;
    if(diff>=0){fit.className='dz-fit ok';fit.textContent='들어가요. 여유 약 '+Math.round(diff)+'mm'+(S.job!=='gap'&&diff>=150?' (남는 폭은 틈새장으로 쓸 수 있어요)':'')}
    else{fit.className='dz-fit no';fit.textContent='약 '+Math.round(-diff)+'mm 부족해요. '+(S.job==='new'?'구성을 줄이거나 사진을 보내주시면 방법을 찾아드려요.':'칸막이·기둥을 빼도 모자라면 새로 짜야 할 수 있어요.')}}
  var link='https://nemos-dream.com/design#'+enc();
  var frs=S.fr.map(function(f,i){return (i+1)+') '+(TYPES[f.t]?TYPES[f.t].n.split(' (')[0]:'냉장고')+(f.m?' '+f.m:'')+' '+f.w+'mm'}).join(', ');
  var exs=Object.keys(EX).filter(function(k){return S.ex[k]}).map(function(k){return EX[k].n}).join(', ');
  var body='[네모의꿈 3D 가견적 문의]\n1. 지역·아파트 : '+(S.area||'')+'\n2. 원하는 작업 : '+JOBS[S.job].n+(S.job==='new'&&exs?' + '+exs:'')+'\n3. 냉장고 : '+frs+'\n4. 냉장고장 자리 폭 : '+(sp?sp+'mm':'(모르면 비워 두세요)')+'\n5. 가견적 : '+e.txt+' (VAT 별도)\n6. 사진 : 냉장고장 자리 사진 2장 첨부해 주세요\n내 설계 보기 : '+link;
  $('dz-pre').textContent=body;
  $('dz-sms').href='sms:'+PHONE+'?&body='+encodeURIComponent(body);
  try{history.replaceState(null,'','#'+enc())}catch(e){}
}

// ---------- 입력 화면 ----------
function frRow(f,i){
  var opts=Object.keys(TYPES).map(function(k){return '<option value="'+k+'"'+(k===f.t?' selected':'')+'>'+TYPES[k].n+'</option>'}).join('');
  return '<div class="dz-fr" data-i="'+i+'"><div class="dz-frh"><b>냉장고 '+(i+1)+'</b>'+(S.fr.length>1?'<button type="button" class="dz-del" data-i="'+i+'" aria-label="냉장고 '+(i+1)+' 빼기">빼기</button>':'')+'</div>'
   +'<label class="dz-l">종류<select data-k="t">'+opts+'</select></label>'
   +'<label class="dz-l">모델명 (아시면)<input data-k="m" value="'+f.m.replace(/"/g,'')+'" placeholder="예: 냉장고 옆면 스티커의 모델명" maxlength="30"></label>'
   +'<div class="dz-mm"><label>가로<input data-k="w" type="number" inputmode="numeric" value="'+f.w+'"></label><label>높이<input data-k="h" type="number" inputmode="numeric" value="'+f.h+'"></label><label>깊이<input data-k="d" type="number" inputmode="numeric" value="'+f.d+'"></label><span>mm</span></div></div>';
}
function drawForm(){
  $('dz-frs').innerHTML=S.fr.map(frRow).join('');
  $('dz-add').hidden=S.fr.length>=4;
  document.querySelectorAll('input[name=dz-job]').forEach(function(r){r.checked=r.value===S.job});
  document.querySelectorAll('.dz-ex input').forEach(function(c){c.checked=!!S.ex[c.value];c.disabled=S.job!=='new'});
  $('dz-exbox').classList.toggle('off',S.job!=='new');
  $('dz-space').value=S.space||'';
}
function update(){var L=render();summary(L)}

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
  document.querySelectorAll('input[name=dz-job]').forEach(function(r){r.addEventListener('change',function(){S.job=r.value;drawForm();update()})});
  document.querySelectorAll('.dz-ex input').forEach(function(c){c.addEventListener('change',function(){S.ex[c.value]=c.checked;update()})});
  $('dz-space').addEventListener('input',function(){var n=Math.round(+this.value);S.space=n>=600&&n<=6000?n:'';update()});
  $('dz-area').addEventListener('input',function(){S.area=this.value.slice(0,40);summary(layout())});
  $('dz-open').addEventListener('click',function(){S.open=!S.open;this.setAttribute('aria-pressed',S.open);this.textContent=S.open?'문 닫기':'문 열어보기';render()});
  document.querySelectorAll('.dz-view button').forEach(function(b){b.addEventListener('click',function(){S.view=b.dataset.v;document.querySelectorAll('.dz-view button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});render()})});
  $('dz-copy').addEventListener('click',function(){var t=$('dz-pre').textContent;(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(function(){$('dz-toast').textContent='복사했어요. 문자 앱에 붙여 넣어 주세요.'},function(){$('dz-toast').textContent='길게 눌러서 복사해 주세요.'})});
}
if(location.hash.length>2)dec(location.hash);
drawForm();bind();update();
})();
