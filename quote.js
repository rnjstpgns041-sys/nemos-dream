/* 견적 폼: 문자 내용 자동 작성 + (문자 서비스 연결 시) 연락처·사진 바로 접수. 모든 페이지 공용 */
(function(){var $=function(i){return document.getElementById(i)};if(!document.querySelector('.qform'))return;
  /* 문자 견적 */
  var PHONE='010-4835-3353',form=document.querySelector('.qform'),area=$('f-area'),model=$('f-model'),msg=$('f-msg'),pre=$('f-pre'),sms=$('sms'),toast=$('toast');
  function val(n){var x=form.querySelector('input[name="'+n+'"]:checked');return x?x.value:''}
  function body(){var tags=[].map.call(form.querySelectorAll('input[name="tag"]:checked'),function(x){return x.value});
    var a=val('area'),ap=area.value.trim(),l=['[네모의꿈 견적 문의]','작업: '+val('job'),'지역: '+(a==='그 외 지역'?'':a)+(ap?(a&&a!=='그 외 지역'?' ':'')+ap:'')];
    if(model.value.trim())l.push('냉장고: '+model.value.trim());
    if(tags.length)l.push('상황: '+tags.join(', '));
    if(msg.value.trim())l.push('내용: '+msg.value.trim());
    l.push('※ 현장 사진 첨부합니다');return l.join('\n')}
  function upd(){var b=body();pre.textContent=b;sms.href='sms:'+PHONE+'?&body='+encodeURIComponent(b)}
  form.addEventListener('input',upd);form.addEventListener('change',upd);upd();
  /* 자동 접수 (문자 서비스 연결됐을 때만) */
  var send=$('send'),fp=$('f-photo'),th=$('f-thumbs'),shots=[];
  function shrink(f){return new Promise(function(ok){var r=new FileReader();r.onload=function(){var im=new Image();im.onload=function(){var k=Math.min(1,1600/Math.max(im.width,im.height)),c=document.createElement('canvas');c.width=Math.round(im.width*k);c.height=Math.round(im.height*k);c.getContext('2d').drawImage(im,0,0,c.width,c.height);var q=.82,d=c.toDataURL('image/jpeg',q);while(d.length>1.9e6&&q>.4){q-=.12;d=c.toDataURL('image/jpeg',q)}ok(d)};im.onerror=function(){ok(null)};im.src=r.result};r.onerror=function(){ok(null)};r.readAsDataURL(f)})}
  function thumbs(){th.innerHTML='';shots.forEach(function(d,i){var b=document.createElement('button');b.type='button';b.title='빼기';b.innerHTML='<img alt="">';b.firstChild.src=d;b.onclick=function(){shots.splice(i,1);thumbs()};th.appendChild(b)})}
  fp.addEventListener('change',function(){var fs=[].slice.call(fp.files,0,5-shots.length);toast.textContent=fs.length?'사진 준비 중…':'';
    Promise.all(fs.map(shrink)).then(function(r){shots=shots.concat(r.filter(Boolean)).slice(0,5);thumbs();fp.value='';toast.textContent=shots.length>=5?'사진은 5장까지예요.':''})});
  fetch('/api/quote?cfg').then(function(r){return r.json()}).then(function(c){if(!c.enabled)return;
    $('f-auto').hidden=false;send.hidden=false;sms.hidden=true;$('qhint').innerHTML='번호와 사진을 넣고 <b>견적 보내기</b>를 누르면 바로 사장님께 문자로 가요.'}).catch(function(){});
  send.addEventListener('click',function(){var ph=$('f-phone').value.trim();if(ph.replace(/\D/g,'').length<9){toast.textContent='연락받을 휴대폰 번호를 적어 주세요.';$('f-phone').focus();return}
    var a=val('area'),ap=area.value.trim();send.disabled=true;send.textContent='보내는 중…';
    fetch('/api/quote',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({job:val('job'),area:((a==='그 외 지역'?'':a)+' '+ap).trim()||a,model:model.value.trim(),msg:msg.value.trim(),phone:ph,
      tags:[].map.call(form.querySelectorAll('input[name="tag"]:checked'),function(x){return x.value}),photos:shots,website:$('f-hp').value})})
    .then(function(r){return r.json()}).then(function(j){if(!j.ok)throw 0;send.textContent='보냈어요 ✓';toast.textContent='잘 받았어요. 사진 보고 '+ph+'으로 연락드릴게요.';shots=[];thumbs();})
    .catch(function(){send.disabled=false;send.textContent='견적 보내기';toast.textContent='전송이 안 됐어요. 아래 번호로 문자나 전화 주세요.';sms.hidden=false})});
  $('copy').addEventListener('click',function(){var b=body();
    function fb(){form.querySelector('.preview').open=true;var r=document.createRange();r.selectNodeContents(pre);var s=getSelection();s.removeAllRanges();s.addRange(r);toast.textContent='내용을 선택해 두었어요. 길게 눌러 복사하세요.'}
    try{navigator.clipboard.writeText(b).then(function(){toast.textContent='복사했어요. 문자 앱에서 '+PHONE+'으로 붙여 넣고 사진을 첨부해 주세요.'},fb)}catch(e){fb()}});

})();
