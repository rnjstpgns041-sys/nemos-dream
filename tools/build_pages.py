# 네모의꿈 하위 페이지 생성 스크립트 (메뉴 5개: 하는 일/작업 기록/비용/진행 방법/자주 묻는 질문)
# 사용: cd <저장소> && python3 tools/build_pages.py
# index.html의 head/footer를 공유해서 services.html, works.html, price.html, process.html, faq.html을 만든다.
import re, json, os, html as H
TOOLS = os.path.dirname(os.path.abspath(__file__))

s = open('index.html').read()

PAGES = [('services.html', '하는 일'), ('works.html', '작업 기록'), ('price.html', '비용'),
         ('process.html', '진행 방법'), ('faq.html', '자주 묻는 질문')]
PHONE = '010-4835-3353'
LOGO = '<svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true"><rect x="1" y="1" width="24" height="24" rx="7" fill="#03c75a"/><rect x="7.5" y="7.5" width="11" height="11" rx="3" fill="#fff"/></svg>'

CALL_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2a1 1 0 011-.25 11.4 11.4 0 003.6.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1z" fill="currentColor"/></svg>'
def nav(cur, home=False):
    links = ''.join('<a href="%s"%s>%s</a>' % (f, ' aria-current="page"' if f == cur else '', t) for f, t in PAGES)
    q = '#quote' if home else 'index.html#quote'
    return ('<nav class="nav" aria-label="주요 메뉴">\n  <div class="wrap">\n    <a class="logo" href="%s">%s네모의꿈</a>\n'
            '    <div class="nav-links">%s</div>\n    <a class="btn btn-acc btn-sm btn-call" href="tel:010-4835-3353">%s전화 상담</a>\n  </div>\n</nav>'
            % ('#top' if home else 'index.html', LOGO, links, CALL_ICON))

# ---- index.html: 메뉴를 페이지 링크로 ----
_m = re.search(r'var works=\[(.*?)\n  \];', s, re.S)
_st = ''
for _line in _m.group(1).strip().split('\n'):
    _g = dict(re.findall(r"(\w):'([^']*)'", _line)); _no = re.search(r"'(\d{12})'", _line).group(1)
    _st += ('<a class="work" href="case-%s.html"><img class="after" loading="lazy" alt="%s 시공 후" src="img/works/%s-after.jpg"><span class="before"><img loading="lazy" alt="%s 시공 전" src="img/works/%s-before.jpg"><span>BEFORE</span></span>'
            '<div class="info"><span class="where"><i>%s</i><i class="g">%s</i></span><h3>%s</h3><p class="meta">%s</p></div></a>'
            % (_no, H.escape(_g['t']), _no, H.escape(_g['t']), _no, {'fridge': '냉장고장', 'bar': '홈바·신발장', 'etc': '수납장'}[_g['f']], H.escape(_g['w']), H.escape(_g['t']), _g['d']))
s = re.sub(r'<div class="log" id="works-grid">.*?</div>\n', lambda m: '<div class="log" id="works-grid">%s</div>\n' % _st, s, count=1, flags=re.S)

i = s.index('<nav class="nav"'); j = s.index('</nav>', i) + 6
s = s[:i] + nav(None, True) + s[j:]
open('index.html', 'w').write(s)

head = s[:s.index('<body>')]
footer = s[s.index('<footer>'):s.index('</footer>') + 9].replace('href="#quote"', 'href="index.html#quote"')
area = re.search(r'<div class="areas">.*?</div>', s, re.S).group(0)

REVEAL = '''<script>
(function(){
  if('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.sec-head,.card,.price,.step,.fact,.faq,.areas,.sd,.tl-item,.wk,.factor,.guide>div,.cta-band .wrap').forEach(function(el,i){el.classList.add('reveal');el.style.transitionDelay=(i%3)*60+'ms';io.observe(el)});
    setTimeout(function(){document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')})},2500);
  }
})();
</script>'''

QFORM = re.search(r'<section id="quote".*?</section>', s, re.S).group(0)
RVS = re.findall(r'<figure class="rv">.*?</figure>', s, re.S)
def rv_strip(seed=''):
    # 블로그에 남은 실제 고객 후기 3개 (페이지마다 다르게)
    if not RVS: return ''
    i = sum(map(ord, seed)) % len(RVS)
    pick = [RVS[(i + k) % len(RVS)] for k in range(3)]
    pick = [re.sub(r'<a href="https://blog[^"]*"[^>]*>블로그 원문 ↗</a>', '', x) for x in pick]
    return ('<section class="rv-mini">\n  <div class="wrap">\n    <p class="rv-mini-h">시공 끝나고 고객님이 블로그에 남긴 말씀</p>\n'
            '    <div class="rvs">%s</div>\n    <p class="rv-mini-cta"><a class="btn btn-acc" href="#quote">사진 한 장으로 무료 견적 받아보기</a></p>\n  </div>\n</section>\n' % ''.join(pick))

import urllib.parse as _U
def qform(job=None, area=None, town=''):
    # 문자 양식에 이 페이지의 지역·작업을 미리 채운다 (job=원하는 작업, area/town=지역)
    f = QFORM
    where, want = (town or area or ''), (job or '')
    if not (where or want): return f
    body = H.unescape(re.search(r'<pre id="f-pre"[^>]*>(.*?)</pre>', f, re.S).group(1))
    body = body.replace('1. 지역·아파트 : ', '1. 지역·아파트 : ' + (where + ' ' if where else '')).replace('2. 원하는 작업 : ', '2. 원하는 작업 : ' + want)
    if any(w in want for w in ('수전', '싱크볼', '후드', '식세기', '상부장')):   # 냉장고 작업이 아니면 사진 안내를 바꾼다
        body = re.sub(r'3\. 냉장고 모델 : [^\n]*', '3. 모델명 : (아시면)', body)
        body = re.sub(r'4\. 사진 : [^\n]*', '4. 사진 : 작업할 곳 사진 2장 첨부해 주세요 (멀리서 1장, 가까이서 1장)', body)
    f = re.sub(r'(<pre id="f-pre"[^>]*>).*?(</pre>)', lambda m: m.group(1) + H.escape(body, quote=False) + m.group(2), f, flags=re.S)
    f = re.sub(r'href="sms:01048353353\?&amp;body=[^"]*"', 'href="sms:01048353353?&amp;body=%s"' % _U.quote(body), f)
    return f

def page(fn, title, desc, kicker, h1, sub, body, extra_js='', crumb='', og_image=None, subnav=True, job=None, area=None, town='', hero_pair=None):
    h = head
    h = re.sub(r'<title>.*?</title>', '<title>%s | 네모의꿈 키친핏 냉장고장</title>' % title, h)
    h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % H.escape(desc), h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s | 네모의꿈">' % title, h)
    u = 'https://nemos-dream.com/' + fn[:-5]
    h = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % u, h)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % u, h)
    if og_image:
        h = re.sub(r'<meta property="og:image" content="[^"]*">', '<meta property="og:image" content="%s">' % og_image, h)
        h = re.sub(r'<meta property="og:image:(width|height)" content="[^"]*">\n', '', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', h, flags=re.S)
    crumb = crumb or title
    others = ''.join('<a href="%s"%s>%s</a>' % (f, ' aria-current="page"' if f == fn else '', t) for f, t in PAGES)
    pair = (('    <a class="hero-pair" href="case-%s.html"><figure><img src="img/works/%s-before.jpg" alt="공사 전"><figcaption>BEFORE</figcaption></figure><figure><img src="img/works/%s-after.jpg" alt="공사 후"><figcaption class="a">AFTER</figcaption></figure></a>\n' % (hero_pair, hero_pair, hero_pair)) if hero_pair else '')
    out = (h + '<body>\n\n' + nav(fn) + '\n\n'
           '<header class="page-hero">\n  <div class="wrap">\n    <p class="crumb"><a href="index.html">홈</a> <span>›</span> %s</p>\n'
           '    <p class="kicker">%s</p>\n    <h1>%s</h1>\n    <p class="page-sub">%s</p>\n'
           '    <p class="page-call"><a class="btn btn-acc btn-call" href="tel:010-4835-3353"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2a1 1 0 011-.25 11.4 11.4 0 003.6.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1z" fill="currentColor"/></svg>010-4835-3353 전화 상담</a><a class="btn btn-soft" href="#quote">사진 한 장으로 무료 견적 받아보기</a></p>\n    <p class="hero-note">사진 몇 장이면 금액을 알려드려요 · 대표가 직접 시공 · 처짐 평생 AS</p>\n'
           '%s'
           '    %s\n  </div>\n</header>\n\n' % (crumb, kicker, h1, sub, pair, '<div class="subnav" aria-label="다른 메뉴">%s</div>' % others if subnav else '')
           + ((body.replace('<!--RV-->', rv_strip(fn)) if '<!--RV-->' in body else body).replace('<!--QUOTE-->', qform(job, area, town)) if '<!--QUOTE-->' in body else body + '\n' + ('' if fn.startswith('case-') else rv_strip(fn)) + qform(job, area, town)) + '\n\n'
           + footer + '\n\n<div class="mcta"><a class="btn btn-acc btn-call" href="tel:%s">%s전화 상담</a><a class="btn btn-soft" href="#quote">사진 한 장 무료견적</a></div>\n\n' % (PHONE, CALL_ICON)
           + extra_js + '\n' + REVEAL + '\n<script src="quote.js" defer></script>\n\n</body>\n</html>\n')
    out = out.replace('href="index.html#quote"', 'href="#quote"')
    open(fn, 'w').write(out)

def gal(names, alts):
    big = '<figure class="g-main"><img src="img/g/%s.jpg" alt="%s" loading="lazy"></figure>' % (names[0], alts[0])
    th = ''.join('<figure><img src="img/g/%s.jpg" alt="%s" loading="lazy"></figure>' % (n, a) for n, a in zip(names[1:], alts[1:]))
    return '<div class="gallery">%s<div class="g-thumbs">%s</div></div>' % (big, th)

def check(items):
    return '<ul class="check">' + ''.join('<li>%s</li>' % x for x in items) + '</ul>'

# ================= 하는 일 =================
SV = [
 ('new', '대표 작업 · 키친핏 맞춤제작', '키친핏 냉장고장 맞춤제작',
  '저희가 가장 많이 하는 일이에요. 냉장고 설치 가이드를 보고 높이, 깊이, 도어 두께까지 맞춰 설계하고, E0 등급 친환경 자재로 직접 짜서 설치해요. 냉장고를 넣으면 도어 라인과 가구가 나란히 떨어지는 키친핏이 나와요. 남는 폭은 키큰장, 홈바장, 로봇청소기장으로 채우고 색상도 주방 가구에 맞춰요.',
  ['신축 아파트에서 냉장고장 옵션을 뺐을 때', '비스포크·오브제처럼 키친핏 냉장고를 넣을 때', '냉장고와 주방 가구 라인을 맞추고 싶을 때', '렌지장·밥솥장·홈바장도 함께 넣고 싶을 때'],
  ['E0 친환경 자재', '1+1+1 · 4+4 · 4+3도어', '키큰장', '렌지장·밥솥장', '홈바장', '로봇청소기장'], '냉장고장 맞춤제작 <b>100만원부터</b>',
  ['new-0', 'new-1', 'new-6', 'new-4'], ['무옵션 세대에 맞춤제작한 키친핏 냉장고장', '공사 전: 비어 있는 냉장고 자리', '상부장과 키큰장 프레임을 짜는 중', '현장에서 판재를 재단하는 모습'], 'fridge'),
 ('pillar', '냉장고장 리폼', '칸막이·기둥 제거 리폼',
  '이미 옵션 냉장고장이 있는데 키친핏 냉장고가 가운데 기둥에 걸린다면, 장을 다 뜯지 않고 기둥만 빼서 자리를 만들어요. 기존 자재를 다시 써서 비용을 아낄 수 있어요.',
  ['옵션 냉장고장에 키친핏 냉장고가 안 들어갈 때', '설치 기사님이 설치 불가라고 하고 가셨을 때', '멀쩡한 장을 버리기 아까울 때'],
  ['가운데 칸막이 제거', '천장 보강', '수평 재설치', '남는 폭 틈새장'], '칸막이 제거 <b>30만원</b> · 틈새장까지 <b>70만원</b>',
  ['pillar-6', 'pillar-1', 'pillar-3', 'pillar-5'], ['기둥을 빼고 냉장고 세 대를 나란히 넣은 모습', '공사 전: 가운데 기둥이 있는 냉장고장', '기둥을 빼고 상부장을 다시 거는 중', '공사 후: 기둥 없이 트인 냉장고 자리'], 'fridge'),
 ('bar', '맞춤 제작', '홈바장 · 조명 진열장',
  '빈 벽이나 냉장고장 옆에 조명이 들어가는 홈바장을 짜요. 유리문 진열장, 간접 조명, 와이드 홈바까지 원하는 모양으로 만들어요.',
  ['거실이나 주방 벽이 허전할 때', '컵과 소품을 보여주며 수납하고 싶을 때', '냉장고장에 포인트를 주고 싶을 때'],
  ['간접 조명', '유리문 진열장', '와이드 홈바', '라운드 홈바'], '디자인 홈바 <b>100만원부터</b>',
  ['bar-3', 'bar-1', 'bar-2', 'bar-4'], ['조명 유리문 홈바장 완성 모습', '공사 전: 비어 있던 벽', '홈바장 조명을 켠 모습', '조명이 들어간 원목 상판'], 'bar'),
 ('shoe', '현관 · 리폼', '신발장 오픈장',
  '프레임은 그대로 두고 가운데만 열린 선반으로 바꿔요. 열쇠, 향초, 소품을 올려두기 좋고 LED 조명을 넣으면 현관 분위기가 확 달라져요. 대부분 하루면 끝나요.',
  ['신발장이 멀쩡해서 바꾸기 아까울 때', '현관이 답답해 보일 때', '필름 시공만으로는 아쉬울 때'],
  ['중간 오픈장', 'LED 조명', '문짝 재단', '내부 보강'], None,
  ['shoe-4', 'shoe-1', 'shoe-2', 'shoe-3'], ['LED 조명을 넣은 신발장 오픈장', '공사 전: 문짝으로 막힌 신발장', '가운데를 오픈장으로 바꾼 모습', '오픈장 안쪽 선반'], 'bar'),
 ('robot', '주방 · 리폼', '로봇청소기장',
  '아일랜드 하부장이나 남는 폭을 로봇청소기 전용 자리로 바꿔요. 서랍 레일을 분리하고 바닥을 맞춰서 청소기가 스스로 드나들 수 있게 해요.',
  ['로봇청소기 둘 곳이 마땅치 않을 때', '하부장 한 칸이 잘 안 쓰일 때', '거실에 청소기 스테이션이 보이는 게 싫을 때'],
  ['아일랜드 하부장', '레일 분리', '로보락·비스포크 제트봇'], None,
  ['robot-3', 'robot-1', 'robot-2', 'robot-4'], ['로봇청소기 자리를 만든 하부장', '공사 전: 서랍이 있던 하부장', '서랍을 분리하는 중', '완성된 로봇청소기장'], 'etc'),
 ('cafe', '거실 · 제작', '수납장 · 홈카페장',
  '냉장고 자리를 맞추고 남는 틈이나 거실 벽을 쓸모 있는 수납 공간으로 만들어요. 커피머신과 컵을 둘 홈카페장, 조명이 들어간 원목 수납장도 짜요.',
  ['냉장고 옆에 애매한 틈이 남을 때', '커피머신 자리가 필요할 때', '거실 수납이 부족할 때'],
  ['틈새 수납장', '홈카페장', '원목 홈바 수납장'], None,
  ['cafe-2', 'cafe-1', 'cafe-3', 'cafe-4'], ['냉장고 옆 틈새에 만든 홈카페장', '공사 전 냉장고 자리', '홈카페장 조명', '원목 홈바 수납장'], 'etc'),
]
idx = ''.join('<a href="#%s">%s</a>' % (k, t) for k, _, t, *_ in SV)
body = '<section class="sv-wrap">\n  <div class="wrap">\n    <div class="jump">%s</div>\n' % idx
for n, (k, cat, t, p, who, chips, price, g, galt, f) in enumerate(SV):
    body += ('    <article class="sd%s" id="%s">\n      %s\n      <div class="sd-text"><span class="cat">%s</span><h2>%s</h2><p>%s</p>'
             '<h3>이럴 때 찾으세요</h3>%s<div class="chipset">%s</div>%s'
             '<div class="sd-btns"><a class="btn btn-acc" href="index.html#quote">이 작업 견적 받기</a><a class="btn btn-soft" href="works.html#%s">작업 사진 보기</a></div></div>\n    </article>\n'
             % (' rev' if n % 2 else '', k, gal(g, galt), cat, t, p, check(who), ''.join('<span>%s</span>' % c for c in chips),
                '<p class="sd-price">%s</p>' % price if price else '', f))
body += '''    <div class="also"><h3>이런 작업도 해요</h3><p>식세기장, 밥솥장, 수전·싱크볼 교체, 주방 후드처럼 주방 싱크대와 관련된 작업도 함께 해요. 목록에 없어도 사진과 함께 물어봐 주세요.</p></div>
  </div>
</section>
'''
page('services.html', '하는 일', '키친핏 냉장고장 맞춤제작이 대표 작업이에요. 칸막이·기둥 제거 리폼, 홈바장, 신발장 오픈장, 로봇청소기장, 홈카페장까지. 네모의꿈이 하는 일을 사진과 함께 소개해요.',
     '하는 일', '키친핏 냉장고장을<br><em>직접 짜고 설치해요</em>', '냉장고장 맞춤제작이 저희 대표 작업이에요. 홈바장, 신발장, 수납장까지 대표가 직접 재고 만들고 설치해요.', body)

# ================= 작업 기록 =================
m = re.search(r'var works=\[(.*?)\n  \];', s, re.S)
works = []
for line in m.group(1).strip().split('\n'):
    g = dict(re.findall(r"(\w):'([^']*)'", line))
    u = re.search(r"u:(Z|S)\+'(\d+)'", line)
    g['u'] = ('https://blog.naver.com/zibaejang/' if u.group(1) == 'Z' else 'https://blog.naver.com/soorigome/') + u.group(2)
    g['no'] = u.group(2)
    works.append(g)
body = '''<section class="band wk-sec">
  <div class="wrap">
    <div class="chips-wrap"><div class="chips" role="group" aria-label="작업 종류로 거르기">
      <button class="chip" type="button" data-f="all" aria-pressed="true">전체<small></small></button>
      <button class="chip" type="button" data-f="fridge" aria-pressed="false">냉장고장<small></small></button>
      <button class="chip" type="button" data-f="bar" aria-pressed="false">홈바·신발장<small></small></button>
      <button class="chip" type="button" data-f="etc" aria-pressed="false">수납장<small></small></button>
    </div></div>
    <div class="wk-grid" id="wk">%s</div>
    <p class="wk-more">더 많은 현장은 블로그에 계속 올라와요. <a href="https://blog.naver.com/zibaejang" target="_blank" rel="noopener">네모의꿈 블로그 ↗</a> <a href="https://blog.naver.com/soorigome" target="_blank" rel="noopener">집수리비버 블로그 ↗</a></p>
  </div>
</section>
'''
KW = {'fridge': '냉장고장', 'bar': '홈바·신발장', 'etc': '수납장'}
def wk_card(r):
    e = H.escape
    return ('<article class="wk" data-f="%s"><div class="wk-pair"><figure><img loading="lazy" src="img/works/%s-before.jpg" alt="%s 공사 전"><figcaption>BEFORE</figcaption></figure><figure><img loading="lazy" src="img/works/%s-after.jpg" alt="%s 공사 후"><figcaption class="a">AFTER</figcaption></figure></div>'
            '<div class="wk-info"><span class="where"><i>%s</i><i class="g">%s</i></span><h2><a href="case-%s.html">%s</a></h2><p>%s</p><div class="wk-foot"><span>%s</span><a href="case-%s.html">자세히 보기 →</a></div></div></article>'
            % (r['f'], r['no'], e(r['t']), r['no'], e(r['t']), KW[r['f']], e(r['w']), r['no'], e(r['t']), e(r['p']), r['d'], r['no']))
body = body % ''.join(wk_card(w) for w in works)
js = '''<script>
(function(){
  var K={fridge:1,bar:1,etc:1};
  var cards=[].slice.call(document.querySelectorAll('#wk .wk'));
  document.querySelectorAll('.chip').forEach(function(c){var f=c.dataset.f;c.querySelector('small').textContent=cards.filter(function(r){return f==='all'||r.dataset.f===f}).length});
  function pick(f){document.querySelectorAll('.chip').forEach(function(x){x.setAttribute('aria-pressed',x.dataset.f===f)});cards.forEach(function(r){r.hidden=!(f==='all'||r.dataset.f===f)})}
  document.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){pick(c.dataset.f)})});
  var h=location.hash.slice(1);pick(K[h]?h:'all');
})();
</script>'''
page('works.html', '작업 기록', '대전, 세종, 천안, 청주, 홍성, 정읍, 수원에서 한 냉장고장 리폼과 맞춤가구 현장 %d곳의 공사 전후 사진이에요.' % len(works),
     '작업 기록', '공사 전과 후,<br><em>나란히 놓고 보세요</em>', '블로그에 올린 실제 현장 %d곳이에요. 왼쪽이 공사 전, 오른쪽이 공사 후예요.' % len(works), body, js)

# ================= 비용 =================
pr = re.search(r'<div class="prices">.*?</div>\n    </div>', s, re.S).group(0)
pr = pr.replace('src="img/', 'src="img/')
body = '''<section>
  <div class="wrap">
    <div class="sec-head"><p class="kicker">기본 단가</p><h2>블로그에 공개한<br><em>그대로예요</em></h2><p>모든 금액은 VAT 별도예요. 현장 상태와 크기에 따라 달라질 수 있어서, 사진을 보고 최종 금액을 알려드려요.</p></div>
    %s
    <p class="price-note">홈바에는 일반 콘센트가 기본으로 들어가고, 매립형 멀티콘센트로 바꾸면 비용이 추가돼요.</p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">맞춤제작과 리폼</p><h2>우리 집엔<br><em>어떤 게 맞을까요?</em></h2></div>
    <div class="vs">
      <div class="vs-card"><span class="pill">맞춤제작 · 대표 작업</span><h3>냉장고에 딱 맞게 새로 짜요</h3><p>무옵션 세대이거나 냉장고와 주방 가구 라인을 맞추고 싶을 때, 냉장고 설치 가이드에 맞춰 처음부터 짜요. 원하는 조합을 자유롭게 넣을 수 있어요.</p>%s</div>
      <div class="vs-card"><span class="pill">리폼</span><h3>있는 장을 살려요</h3><p>옵션 냉장고장이 이미 있다면 기존 자재를 다시 써서 기둥만 빼고 자리를 만들어요. 자재가 거의 더 들어가지 않아 비용을 아낄 수 있어요.</p>%s</div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><p class="kicker">금액이 달라지는 경우</p><h2>견적은 이런 걸<br><em>보고 정해요</em></h2></div>
    <div class="factors">
      <div class="factor"><span class="ic">01</span><h3>작업 범위</h3><p>칸막이만 빼는지, 상부장까지 다시 거는지, 틈새장을 더하는지에 따라 달라져요.</p></div>
      <div class="factor"><span class="ic">02</span><h3>현장 구조</h3><p>장이 틀어져 있거나 천장 보강이 더 필요하면 작업이 늘어나요.</p></div>
      <div class="factor"><span class="ic">03</span><h3>자재와 추가 장</h3><p>홈바장, 렌지장, 밥솥장처럼 더하는 장과 조명, 콘센트에 따라 달라져요.</p></div>
      <div class="factor"><span class="ic">04</span><h3>지역과 거리</h3><p>출장비는 무조건 붙지 않고 작업 종류와 위치에 따라 조율해요.</p></div>
    </div>
  </div>
</section>
''' % (pr, check(['냉장고 높이·깊이·도어 두께까지 맞춤', 'E0 등급 친환경 자재', '키큰장·렌지장·홈바장 조합 자유', '맞춤제작 100만원부터']), check(['기존 상부장과 자재 재사용', '기둥 제거와 천장 보강', '부분 리폼 30만원']))
page('price.html', '비용', '키친핏 냉장고장 맞춤제작 100만원부터, 디자인 홈바 100만원부터, 칸막이 제거 리폼 30만원. 네모의꿈 냉장고장 제작·리폼 비용을 공개해요.',
     '비용', '냉장고장 제작 비용,<br><em>미리 확인하세요</em>', '숨기지 않고 공개한 기본 단가예요. 사진을 보내주시면 우리 집 금액을 바로 알려드려요.', body)

# ================= 진행 방법 =================
TL = [
 ('문자로 상담', '사진 · 지역 · 냉장고 모델', '냉장고 자리 사진과 시공 지역, 넣을 냉장고 모델명을 문자로 보내주세요. 렌지장, 홈바장처럼 같이 넣고 싶은 것도 함께 적어 주세요.', None),
 ('실측과 설계', '설치 가이드까지 확인해요', '현장을 직접 재고, 냉장고 설치 가이드를 보고 높이와 깊이, 도어 두께까지 맞춰 설계해요.', 'new-1', '공사 전: 비어 있는 냉장고 자리'),
 ('재단과 사전 제작', '현장에서 자르지 않아요', '들어갈 판재는 치수에 맞게 미리 재단해서 가져가요. 그래서 시공 날 먼지와 시간이 줄어요.', 'new-4', '판재를 재단하는 모습'),
 ('프레임 세우기', '수평부터 잡아요', '양옆 기둥장부터 세우면서 수평과 수직을 맞춰요. 매일 여닫는 가구라 여기서 품질이 갈려요.', 'new-5', '양옆 프레임을 세운 모습'),
 ('상부장·키큰장 짜기', '남는 공간까지 수납으로', '냉장고 높이에 맞춰 상부장 공간을 최대한 살리고, 남는 폭은 키큰장으로 채워요.', 'new-6', '상부장과 키큰장 프레임'),
 ('문짝과 마감', '색상까지 맞춰요', '문짝을 달고 주방 가구 색상에 맞춰 마감해요. 상부와 양옆 틈새도 이어서 공간 낭비 없이 정리해요.', 'new-3', '문짝을 단 냉장고장'),
 ('완성', '키친핏으로 딱 맞게', '냉장고를 넣으면 도어 라인과 가구가 나란히 떨어지는 키친핏이 나와요. 처짐과 기울어짐은 평생 AS로 책임져요.', 'new-0', '완성된 키친핏 냉장고장'),
]
tl = ''
for n, t in enumerate(TL, 1):
    ph = '<figure><img src="img/g/%s.jpg" alt="%s" loading="lazy"></figure>' % (t[3], t[4]) if t[3] else '<div class="tl-sms"><p class="bub me">입주 전이에요. 냉장고장 옵션을 뺐는데 비스포크에 맞게 짜고 싶어요. 사진 보내요!</p><p class="bub them">모델명 확인했어요. 설치 가이드에 맞춰 실측 날짜 잡아드릴게요.</p></div>'
    tl += '      <li class="tl-item"><span class="tl-no">%d</span><div class="tl-body"><small>%s</small><h3>%s</h3><p>%s</p></div>%s</li>\n' % (n, t[1], t[0], t[2], ph)
body = '''<section>
  <div class="wrap">
    <div class="sec-head"><p class="kicker">맞춤제작 현장으로 보는 순서</p><h2>문자 한 통부터<br><em>키친핏 완성까지</em></h2><p>냉장고장 옵션을 빼고 입주한 신축 아파트에 키친핏 냉장고장을 맞춤제작한 현장이에요. 실제 작업 순서 그대로 보여드려요. 칸막이 제거 리폼 순서는 <a href="works.html#fridge">작업 기록</a>에서 볼 수 있어요.</p></div>
    <ol class="tl">
%s    </ol>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">사진 찍는 법</p><h2>이렇게 보내주시면<br><em>견적이 정확해요</em></h2></div>
    <div class="guide">
      <div><span class="ic">1</span><h3>전체 사진 1장</h3><p>냉장고장 전체가 한 화면에 들어오게 정면에서 찍어 주세요.</p></div>
      <div><span class="ic">2</span><h3>가까이 1장 이상</h3><p>기둥, 천장 쪽, 바닥 쪽이 보이게 가까이에서 찍어 주세요.</p></div>
      <div><span class="ic">3</span><h3>지역과 아파트</h3><p>같은 지역이라도 거리에 따라 일정이 달라져서 꼭 필요해요.</p></div>
      <div><span class="ic">4</span><h3>냉장고 모델명</h3><p>폭과 문 여는 각도까지 맞춰서 설치 불가가 나오지 않게 해요.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><p class="kicker">걸리는 시간</p><h2>대부분<br><em>하루면 끝나요</em></h2></div>
    <div class="steps-wide">
      <div><span class="pill">맞춤제작</span><h3>실측하고 맞춰 짜요</h3><p>냉장고장, 홈바장을 새로 짤 땐 실측한 치수로 미리 만들어 가고 설치 일정은 상담 때 알려드려요.</p></div>
      <div><span class="pill">리폼</span><h3>대부분 그날 끝나요</h3><p>칸막이 제거, 신발장 오픈장 리폼은 대부분 하루 안에 끝나고 당일 사용할 수 있어요. 대전 서구 구조변경 현장은 두 사람이 3시간 걸렸어요.</p></div>
    </div>
  </div>
</section>
''' % tl
page('process.html', '진행 방법', '문자 상담부터 실측과 설계, 사전 제작, 설치, 마감까지. 네모의꿈 키친핏 냉장고장 맞춤제작 순서를 실제 현장 사진으로 보여드려요.',
     '진행 방법', '견적부터 시공까지<br><em>이렇게 진행돼요</em>', '상담한 사람이 직접 와서 끝까지 시공해요. 실제 현장 사진으로 순서를 보여드릴게요.', body)

# ================= 자주 묻는 질문 =================
FAQ = [
 ('냉장고장 리폼', [
  ('키친핏 냉장고가 뭔가요?', '주방 가구와 냉장고가 딱 맞게 설계된 스타일이에요. 장과 냉장고 사이가 1cm 정도로 붙어서 남는 공간 없이 일체형처럼 보여요. 삼성 비스포크, LG 오브제 같은 냉장고가 대표적이에요.'),
  ('냉장고를 먼저 사야 하나요, 리폼을 먼저 해야 하나요?', '냉장고를 먼저 정해 주세요. 모델마다 폭과 문 여는 각도가 달라서, 모델에 맞춰 리폼해야 배송 당일에 설치 불가가 나오지 않아요.'),
  ('신축 아파트인데도 리폼이 필요한가요?', '오히려 신축에서 가장 많이 해요. 옵션 냉장고장은 양문형 냉장고와 김치냉장고 규격으로 두 칸이 나뉜 경우가 많아 키친핏 냉장고와 맞지 않거든요.'),
  ('칸막이만 철거할 수도 있나요?', '가능해요. 키친핏이 아니라면 틈새 기둥만 빼도 설치되는 경우가 많고, 남는 폭은 수납장이나 밥솥장으로 쓸 수 있어요.'),
  ('어떤 냉장고 조합까지 되나요?', '1도어, 4도어, 1+1+1, 4+4, 4+3도어처럼 냉장고 구성에 맞춰 자유롭게 조합해요. 김치냉장고까지 네 대를 나란히 넣은 현장도 있어요.'),
 ]),
 ('비용과 일정', [
  ('비용은 어느 정도인가요?', '상부장을 그대로 쓰고 칸막이만 빼는 리폼은 30만원, 남는 폭에 틈새장까지 짜면 70만원, 냉장고장을 새로 짜는 건 100만원부터예요. 금액은 VAT 별도예요. <a href="price.html">비용 자세히 보기</a>'),
  ('철거비나 폐자재 처리비가 따로 붙나요?', '리폼할 때 철거, 상부 보강, 폐자재 처리는 기본가에 들어 있어요. 따로 추가하지 않아요.'),
  ('출장비가 따로 있나요?', '무조건 붙지는 않아요. 작업 종류와 위치에 따라 조율해요. 사진과 지역을 먼저 알려주시면 함께 안내해 드려요.'),
  ('작업은 얼마나 걸리나요?', '칸막이 제거나 신발장 오픈장 리폼은 대부분 하루 안에 끝나고 당일 사용할 수 있어요. 구조를 크게 바꾸는 작업은 상담 때 일정을 따로 알려드려요.'),
 ]),
 ('시공과 AS', [
  ('기둥을 빼도 상부장이 처지지 않나요?', '기둥이 받치던 무게만큼 상부장과 천장을 2단으로 보강해요. 10년, 20년이 지나도 처지지 않게 작업하고, 처짐·기울어짐은 평생 AS로 책임집니다.'),
  ('평생 AS는 어떤 경우에 해 주나요?', '저희가 시공한 냉장고장, 상부장, 홈바장이 처지거나 기울어지면 기간 제한 없이 무상으로 다시 잡아 드려요. 10년이 지나서 처지거나 떨어져도 연락 주시면 책임지고 해 드려요. <a href="as.html">AS 안내 자세히 보기</a>'),
  ('AS는 어떻게 신청하나요?', '처지거나 기울어진 부분 사진과 시공한 집 주소를 문자로 보내주세요. 사진으로 먼저 확인하고 방문 날짜를 잡아 고쳐 드려요.'),
  ('다른 업체에 하청을 주나요?', '아니요. 한샘·현대리바트 시공팀장 출신 대표가 상담부터 시공까지 직접 해요. 하청 없이 직영으로 작업해요.'),
  ('기둥 뺀 자리 바닥과 벽은 어떻게 되나요?', '도배가 안 된 부분은 현장에서 나온 자재로 보수하고, 마루는 미리 준비한 자재로 깔끔하게 마감해요. 전체 도배를 따로 하시는 집은 말씀해 주시면 건드리지 않아요.'),
  ('셀프로 해도 되나요?', '권하지 않아요. 상부장을 떼어낼 때 떨어질 위험이 있어 두 사람이 해야 하고, 천장 보강과 수평 맞추기가 제대로 안 되면 나중에 처질 수 있어요.'),
  ('자재는 어떤 걸 쓰나요?', 'E0 등급 친환경 자재를 써요. E0는 포름알데히드 방출량이 0.5mg/L 이하인 등급으로, 일반 E1 등급(1.5mg/L 이하)보다 기준이 엄격해요. 냉장고장과 수납장은 매일 음식과 그릇을 꺼내는 가구라 새집 냄새가 덜한 자재를 골라요.'),
  ('색상이나 조명도 고를 수 있나요?', '기존 마감 톤에 맞추는 게 기본이에요. 원하시면 다른 색상, 홈바 간접 조명, 손잡이 없는 푸시 도어도 가능해요.'),
 ]),
 ('문의', [
  ('견적은 어떻게 받나요?', '냉장고장 사진 2장 이상, 시공 지역, 작업 내용을 문자로 보내주세요. 작업 중엔 소음 때문에 전화를 못 받을 때가 많아서 문자가 가장 빨라요. <a href="index.html#quote">사진 한 장으로 무료 견적 받아보기</a>'),
  ('냉장고장 말고 다른 작업도 하나요?', '홈바장, 로봇청소기장, 밥솥장, 신발장, 식세기장과 수전, 싱크볼, 주방 후드처럼 주방 싱크대 관련 작업도 해요.'),
 ]),
]
body = '<section>\n  <div class="wrap faq-page">\n'
body += '    <div class="jump">%s</div>\n' % ''.join('<a href="#faq-%d">%s</a>' % (n, c) for n, (c, _) in enumerate(FAQ))
for n, (c, qs) in enumerate(FAQ):
    body += '    <h2 class="faq-cat" id="faq-%d">%s</h2>\n    <div class="faq">\n' % (n, c)
    body += ''.join('      <details><summary>%s</summary><p class="a">%s</p></details>\n' % q for q in qs)
    body += '    </div>\n'
body += '''  </div>
</section>

<section class="band" id="area">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">출장 지역</p><h2>멀어도 <em>갑니다</em></h2><p>대전·충청이 가장 빠르고, 전북과 경기 남부도 일정 맞춰 가요. 목록에 없어도 문자로 물어봐 주세요.</p></div>
    %s
  </div>
</section>
''' % area
faq_ld = '<script type="application/ld+json">%s</script>' % json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
    {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub(r'<[^>]+>', '', a).strip()}} for _, qs in FAQ for q, a in qs]}, ensure_ascii=False)
page('faq.html', '자주 묻는 질문', '냉장고장 리폼 순서, 비용, 출장비, 작업 시간, 처짐 AS, 출장 지역까지. 네모의꿈에 자주 묻는 질문을 모았어요.',
     '자주 묻는 질문', '이것도 많이<br><em>물어보세요</em>', '상담 때 실제로 많이 받는 질문을 모았어요. 찾는 답이 없으면 문자로 물어봐 주세요.', body, faq_ld)
exec(open(TOOLS + '/build_detail.py').read())
# 지난 커밋 sitemap과 비교해 새로 생긴 주소를 new-urls.txt에 적는다 → 배포가 끝나면 deploy-succeeded 함수가 네이버·빙(IndexNow)에 자동으로 알린다
import subprocess
try: _old = set(re.findall(r'<loc>(.*?)</loc>', subprocess.run(['git', 'show', 'HEAD:sitemap.xml'], capture_output=True, text=True).stdout))
except Exception: _old = set()
_new = [u for u in re.findall(r'<loc>(.*?)</loc>', open('sitemap.xml').read()) if u not in _old] if _old else []
open('new-urls.txt', 'w').write('\n'.join(_new) + ('\n' if _new else ''))
print('new urls', len(_new))
print('built')
