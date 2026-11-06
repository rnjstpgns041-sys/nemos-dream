/* 문자 견적: 버튼을 누르면 양식이 미리 적힌 문자창이 열린다(메이저 집수리처럼 입력 폼 없음). 모든 페이지 공용 */
(function(){
  var $=function(i){return document.getElementById(i)},form=document.querySelector('.qform'),pre=$('f-pre'),toast=$('toast');
  if(!form||!pre)return;
  var NUM='01048353353',PHONE='010-4835-3353',body=pre.textContent;
  var ios=/iPhone|iPad|iPod|Macintosh/i.test(navigator.userAgent);
  var mob=matchMedia('(pointer:coarse)').matches||/Android|iPhone|iPad/i.test(navigator.userAgent);
  var href='sms:'+NUM+(ios?'&':'?')+'body='+encodeURIComponent(body);
  function say(t){if(toast)toast.textContent=t}
  function copy(){try{navigator.clipboard.writeText(body).then(function(){say('양식을 복사했어요. 휴대폰 문자로 '+PHONE+'에 붙여 넣고 사진을 첨부해 주세요.')},sel)}catch(e){sel()}}
  function sel(){var r=document.createRange();r.selectNodeContents(pre);var s=getSelection();s.removeAllRanges();s.addRange(r);say('양식을 선택해 두었어요. 길게 눌러 복사하세요.')}
  $('copy')&&$('copy').addEventListener('click',copy);
  if(mob){
    /* 휴대폰: 문자 버튼과 '사진 견적' 버튼 모두 바로 문자창으로 */
    [].forEach.call(document.querySelectorAll('a[href^="sms:"],a.btn[href$="#quote"]'),function(a){a.href=href});
    document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="sms:"]');if(!a)return;
      try{navigator.clipboard.writeText(body)}catch(x){}say('문자창에서 빈칸 채우고 사진만 첨부해 보내 주세요.')},true);
  }else{
    /* PC: 문자창이 안 열리니 양식 복사 안내 */
    var sms=$('sms');if(sms)sms.lastChild.textContent='무료 견적 문자 양식 복사하기';
    $('qhint').innerHTML='PC에서는 문자창이 안 열려요. 양식을 복사해서 휴대폰 문자로 <b>'+PHONE+'</b>에 보내 주세요. 사진이 없어도 괜찮아요.';
    document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="sms:"]');if(!a)return;e.preventDefault();
      if(a.id!=='sms')form.scrollIntoView({behavior:'smooth',block:'center'});copy()},true);
  }
  var mc=document.querySelector('.mcta');if(mc&&'IntersectionObserver' in window)new IntersectionObserver(function(es){mc.style.display=es[0].isIntersecting?'none':''},{rootMargin:'-20% 0px -20% 0px'}).observe(form);
})();
