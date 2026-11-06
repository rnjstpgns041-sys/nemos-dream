# 네모의꿈 시공 사례 상세 페이지(case-<번호>.html)와 지역 페이지(area-*.html), sitemap.xml, robots.txt 생성
# build_pages.py 끝에서 exec로 불린다(같은 head/footer/page()를 쓴다). 사례 내용은 cases.json(블로그 글에서 정리)에 있다.
import os, json, html as H
from datetime import date

CASES = json.load(open(TOOLS + '/cases.json'))
SITE = 'https://nemos-dream.com/'
WMAP = {w['no']: w for w in works}
KIND = {'fridge': '냉장고장', 'bar': '홈바·신발장', 'etc': '수납장'}

def ld(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False)

def crumbs(items):
    return ld({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': n, 'name': t, 'item': SITE + u} for n, (t, u) in enumerate(items, 1)]})

def card(w, h='h3'):
    no = w['no']
    return ('<a class="wk wk-link" href="case-%s.html"><div class="wk-pair"><figure><img loading="lazy" src="img/works/%s-before.jpg" alt="%s 공사 전"><figcaption>BEFORE</figcaption></figure>'
            '<figure><img loading="lazy" src="img/works/%s-after.jpg" alt="%s 공사 후"><figcaption class="a">AFTER</figcaption></figure></div>'
            '<div class="wk-info"><span class="where"><i>%s</i><i class="g">%s</i></span><%s>%s</%s><p>%s</p><div class="wk-foot"><span>%s</span><b>자세히 보기 →</b></div></div></a>'
            % (no, no, H.escape(w['t']), no, H.escape(w['t']), KIND[w['f']], H.escape(w['w']), h, H.escape(w['t']), h, H.escape(w['p']), w['d']))

# ================= 시공 사례 상세 =================
os.makedirs('img/c', exist_ok=True)
for w in works:
    no = w['no']; c = CASES[no]
    c['region'] = c.get('region') or w['w']
    blog = 'soorigome' if 'soorigome' in w['u'] else 'zibaejang'
    src = '/tmp/claude-0/-home-user/2f5814ee-e92a-5fd0-ab01-f1cd9b2d7402/scratchpad/dl/%s_%s/' % (blog, no)
    pics = []
    for k, ph in enumerate(c.get('photos') or []):
        dst = 'img/c/%s-%d.jpg' % (no, k)
        if not os.path.exists(dst) and os.path.exists(src + ph):
            from PIL import Image
            im = Image.open(src + ph).convert('RGB'); im.thumbnail((900, 900)); im.save(dst, quality=80, optimize=True)
        if os.path.exists(dst): pics.append(dst)
    facts = [('지역', c['region']), ('작업', KIND[w['f']]), ('냉장고', c.get('fridge')), ('작업 시간', c.get('duration')), ('비용', c.get('cost')), ('작업일', w['d'])]
    facts = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (k, H.escape(v)) for k, v in facts if v)
    steps = ''.join('<li><b>%s</b><p>%s</p></li>' % (H.escape(s['t']), H.escape(s['d'])) for s in c['steps'])
    gal_ = ''.join('<figure><img loading="lazy" src="%s" alt="%s 작업 과정 %d"></figure>' % (p, H.escape(c['title']), n + 1) for n, p in enumerate(pics))
    faq_ = ''.join('<details><summary>%s</summary><p class="a">%s</p></details>' % (H.escape(q['q']), H.escape(q['a'])) for q in (c.get('faq') or []))
    rel = [x for x in works if x['f'] == w['f'] and x['no'] != no][:3]
    body = '''<section class="case">
  <div class="wrap">
    <div class="case-top">
      <div class="wk-pair case-pair"><figure><img src="img/works/%(no)s-before.jpg" alt="%(t)s 공사 전"><figcaption>BEFORE</figcaption></figure><figure><img src="img/works/%(no)s-after.jpg" alt="%(t)s 공사 후"><figcaption class="a">AFTER</figcaption></figure></div>
      <div class="case-side">
        <dl class="case-facts">%(facts)s</dl>
        <h2>이런 상황이었어요</h2><p>%(problem)s</p>
        <div class="sd-btns"><a class="btn btn-acc" href="index.html#quote">비슷한 작업 견적 받기</a><a class="btn btn-soft" href="%(u)s" target="_blank" rel="noopener">블로그 원문 ↗</a></div>
      </div>
    </div>
    <div class="case-body">
      <h2>이렇게 작업했어요</h2>
      <ol class="case-steps">%(steps)s</ol>
      %(gal)s
      <h2>작업 결과</h2><p>%(result)s</p>
      %(quote)s%(tip)s%(faq)s
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">비슷한 현장</p><h2>이런 작업도<br><em>함께 보세요</em></h2></div>
    <div class="wk-grid wk-3">%(rel)s</div>
    <p class="more-link"><a class="btn btn-soft" href="works.html">작업 기록 전체 보기 →</a></p>
  </div>
</section>
''' % {'no': no, 't': H.escape(c['title']), 'facts': facts, 'problem': H.escape(c['problem']), 'u': w['u'], 'steps': steps,
       'gal': '<div class="case-gal">%s</div>' % gal_ if gal_ else '', 'result': H.escape(c['result']),
       'quote': '<blockquote class="case-quote">“%s”<cite>고객님 후기</cite></blockquote>' % H.escape(c['quote']) if c.get('quote') else '',
       'tip': '<div class="also case-tip"><h3>알아두면 좋아요</h3><p>%s</p></div>' % H.escape(c['tip']) if c.get('tip') else '',
       'faq': '<h2>이 현장에서 받은 질문</h2><div class="faq">%s</div>' % faq_ if faq_ else '',
       'rel': ''.join(card(x) for x in rel)}
    js = crumbs([('홈', ''), ('작업 기록', 'works'), (c['title'], 'case-' + no)])
    page('case-%s.html' % no, c['title'], ('%s %s. %s' % (c['region'], c['title'], c['problem']))[:150],
         '%s · %s' % (H.escape(c['region']), KIND[w['f']]), H.escape(c['title']), H.escape(w['p']), body, js,
         crumb='<a href="works.html">작업 기록</a> <span>›</span> 현장', og_image=SITE + 'img/works/%s-after.jpg' % no, subnav=False)

# ================= 지역 페이지 =================
AREAS = [
 ('daejeon', '대전', ['대전'], '대전은 저희가 가장 자주 가는 곳이에요. 선화동, 용문동, 중촌동, 서구, 유성구 문지동까지 대전 곳곳의 신축 아파트에서 냉장고장을 짜고 고쳤어요. 가까워서 실측과 일정 잡기가 가장 빨라요.',
  '서구 · 유성구 · 중구 · 동구 · 대덕구 어디든 가요.'),
 ('sejong', '세종', ['세종'], '세종은 신축 아파트가 많아서 냉장고장 옵션과 새 냉장고 크기가 안 맞는 집이 많아요. 장을 다 뜯지 않고 칸막이만 빼거나, 무옵션 세대라면 냉장고 모델에 맞춰 새로 짜 드려요.',
  '대전에서 가까워 일정 잡기가 쉬워요.'),
 ('cheonan', '천안·아산', ['천안'], '천안·아산도 정기적으로 가는 지역이에요. 입주 전에 사 둔 LG 오브제 냉장고가 냉장고장 기둥 때문에 들어가지 않던 천안 현장처럼, 냉장고 모델에 맞춰 자리를 만들어 드려요.',
  '천안과 아산 어디든 가요.'),
 ('cheongju', '청주', ['청주'], '청주에서는 냉장고장과 함께 조명 유리문 홈바장처럼 집에 포인트가 되는 장도 많이 짰어요. 냉장고장 맞춤제작과 홈바장을 한 번에 맡기시면 색상과 라인을 맞춰 드려요.',
  '청주는 물론 진천, 충주까지 가요.'),
 ('hongseong', '홍성·내포', ['홍성'], '내포신도시 신축 아파트처럼 냉장고와 김치냉장고 칸이 나뉜 냉장고장에서 기둥을 빼고 지지대를 보강한 현장이 있어요. 거리가 있어도 일정을 맞춰 찾아가요.',
  '홍성 · 내포신도시 · 예산 · 당진 · 서산까지 가요.'),
]
# 동네별 페이지(area-<부모>-<동네>.html): 부모 지역 페이지 아래에 붙는다. (slug, 이름, 부모 slug, 찾을 지역 글자, 소개, 동네 목록)
SUBS = [
 ('daejeon-yuseong', '대전 유성구', 'daejeon', '유성구', '유성구는 도안, 노은, 죽동, 학하처럼 새 아파트 단지가 많은 곳이에요. 문지동 효성해링턴플레이스에서는 현관 신발장 가운데를 LED 홈바장으로 바꿔 드렸어요.', '도안동 · 노은동 · 죽동 · 학하동 · 봉명동 · 문지동 · 관평동'),
 ('daejeon-seogu', '대전 서구', 'daejeon', '서구', '서구에서는 가장동 삼성래미안의 냉장고장을 키친핏 냉장고에 맞게 구조를 바꾸고, 용문동 둔산더샵엘리프에서는 오브제 냉장고 자리를 만들어 드렸어요.', '둔산동 · 용문동 · 가장동 · 관저동 · 탄방동 · 갈마동 · 도마동'),
 ('daejeon-junggu', '대전 중구', 'daejeon', '중구', '중구는 선화동 하늘채 스카이엔, 중촌동 중촌SK뷰처럼 신축 아파트에서 냉장고장 칸막이와 기둥을 빼는 작업을 여러 번 했어요.', '선화동 · 중촌동 · 용두동 · 목동 · 대흥동 · 태평동 · 문화동'),
 ('daejeon-donggu', '대전 동구', 'daejeon', '동구', '동구도 대전 안이라 실측과 일정 잡기가 빨라요. 재개발로 새로 들어서는 아파트에서 옵션 냉장고장이 새 냉장고와 안 맞을 때 찾아가요.', '용운동 · 가양동 · 대동 · 판암동 · 신흥동 · 삼성동'),
 ('daejeon-daedeok', '대전 대덕구', 'daejeon', '대덕구', '대덕구도 대전 안이라 가까워요. 냉장고를 바꾸면서 기존 냉장고장에 안 들어갈 때, 칸막이만 빼거나 모델에 맞춰 새로 짜 드려요.', '송촌동 · 법동 · 중리동 · 신탄진동 · 석봉동 · 비래동'),
 ('chungnam-asan', '아산', 'cheonan', '아산', '아산은 천안과 함께 다니는 지역이에요. 탕정과 배방의 새 아파트처럼 옵션 냉장고장이 키친핏 냉장고와 안 맞는 집에서 칸막이를 빼거나 새로 짜 드려요.', '탕정면 · 배방읍 · 모종동 · 풍기동 · 온양동'),
 ('chungnam-gongju', '공주', 'sejong', '공주', '공주는 세종과 대전 사이라 일정 맞추기가 어렵지 않아요. 냉장고장 맞춤제작과 칸막이 제거 모두 상담할 수 있어요.', '신관동 · 웅진동 · 월송동 · 금흥동'),
 ('chungnam-nonsan', '논산', 'daejeon', '논산', '논산도 대전에서 다니는 거리예요. 새 냉장고가 기존 장에 안 들어갈 때 사진과 냉장고 모델명을 먼저 보내 주시면 방법과 금액을 알려 드려요.', '내동 · 취암동 · 부창동 · 연무읍'),
 ('chungnam-gyeryong', '계룡', 'daejeon', '계룡', '계룡은 대전 바로 옆이라 가까워요. 냉장고장 칸막이 제거처럼 하루면 끝나는 리폼도 부담 없이 맡기실 수 있어요.', '엄사면 · 금암동 · 두마면'),
 ('chungnam-geumsan', '금산', 'daejeon', '금산', '금산도 대전에서 가까운 지역이에요. 냉장고장뿐 아니라 홈바장, 수납장 맞춤제작도 함께 상담해요.', '금산읍 · 추부면 · 복수면'),
 ('chungnam-dangjin', '당진', 'hongseong', '당진', '당진은 홍성·내포 현장과 함께 다니는 지역이에요. 신축 아파트의 옵션 냉장고장을 살려서 키친핏 냉장고 자리를 만드는 리폼을 많이 물어보세요.', '당진동 · 수청동 · 송악읍 · 합덕읍'),
 ('chungnam-seosan', '서산', 'hongseong', '서산', '서산도 내포에서 가까워 함께 일정을 잡아요. 냉장고 모델에 맞춘 키친핏 냉장고장 맞춤제작부터 칸막이 제거까지 해요.', '예천동 · 석남동 · 동문동 · 대산읍'),
 ('chungnam-yesan', '예산', 'hongseong', '예산', '예산은 내포신도시와 붙어 있어요. 내포 반도유보라마크에디션에서 냉장고장 가운데 가림막을 빼고 지지대를 보강한 현장이 가까운 사례예요.', '삽교읍 · 예산읍 · 덕산면'),
 ('chungnam-boryeong', '보령', 'hongseong', '보령', '보령은 홍성 남쪽이라 내포 쪽 일정과 묶어서 찾아가요. 사진을 먼저 보내 주시면 방문 전에 방법과 금액을 알려 드려요.', '대천동 · 명천동 · 동대동 · 주교면'),
 ('chungbuk-ochang', '청주 오창', 'cheongju', '오창', '오창은 신축 단지가 많아 냉장고장 옵션과 냉장고 크기가 안 맞는 집이 많아요. 청주에서 조명 유리문 홈바장을 짠 것처럼 냉장고장과 홈바장을 함께 맞춰 드려요.', '오창읍 · 각리 · 양청리 · 구룡리'),
 ('chungbuk-osong', '청주 오송', 'cheongju', '오송', '오송은 세종과 청주 사이라 다니기 편해요. 키친핏 냉장고장 맞춤제작과 칸막이 제거 리폼을 모두 해요.', '오송읍 · 오송생명과학단지 일대'),
 ('chungbuk-jincheon', '진천', 'cheongju', '진천', '진천은 혁신도시처럼 새 아파트가 많은 곳이에요. 청주 현장과 함께 일정을 잡아 찾아가요.', '덕산읍(충북혁신도시) · 진천읍 · 광혜원면'),
 ('chungbuk-eumseong', '음성', 'cheongju', '음성', '음성도 충북혁신도시와 붙어 있어 진천 쪽 일정과 함께 다녀요. 냉장고 모델명과 사진을 먼저 보내 주세요.', '맹동면(충북혁신도시) · 음성읍 · 금왕읍'),
 ('chungbuk-chungju', '충주', 'cheongju', '충주', '충주도 청주 현장과 함께 찾아가요. 거리가 있는 만큼 사진으로 먼저 방법을 정하고, 실측 한 번에 제작까지 이어지게 준비해요.', '호암동 · 연수동 · 칠금동 · 기업도시'),
 ('chungbuk-okcheon', '옥천', 'daejeon', '옥천', '옥천은 대전 동쪽 바로 옆이라 가까워요. 냉장고장 칸막이 제거나 맞춤제작 모두 상담해요.', '옥천읍 · 군북면 · 이원면'),
]
exec(open(TOOLS + '/area_rich.py').read())
def city(w): return CASES[w['no']]['city']
for slug, name, cities, intro, reach in AREAS:
    mine = [w for w in works if city(w) in cities]
    near = [w for w in works if w not in mine and w['f'] == 'fridge' and city(w) in ('대전', '세종', '천안', '청주', '홍성')]
    show = mine + near[:max(0, 6 - len(mine))]
    others = ''.join('<a href="area-%s.html">%s</a>' % (s, n) for s, n, *_ in AREAS if s != slug)
    title = '%s 키친핏 냉장고장 맞춤제작 · 리폼' % name
    body = '''<section>
  <div class="wrap">
    <div class="area-intro"><p>%(intro)s</p><p class="muted">%(reach)s</p></div>
    <div class="area-svc">
      <a class="area-card pop" href="services.html#new"><span class="pill">대표 작업</span><h3>키친핏 냉장고장 맞춤제작</h3><p>냉장고 모델의 설치 가이드에 맞춰 높이, 깊이, 도어 두께까지 맞춰 새로 짜요.</p><b>100만원부터</b></a>
      <a class="area-card" href="services.html#pillar"><span class="pill">리폼</span><h3>칸막이·기둥 제거</h3><p>옵션 냉장고장을 살리고 가운데 기둥만 빼서 키친핏 냉장고 자리를 만들어요.</p><b>30만원</b></a>
      <a class="area-card" href="services.html#bar"><span class="pill">맞춤제작</span><h3>홈바장 · 수납장</h3><p>냉장고 옆 남는 폭이나 빈 벽에 홈바장, 렌지장, 밥솥장을 맞춰 넣어요.</p><b>100만원부터</b></a>
    </div>
    <p class="price-note">금액은 VAT 별도예요. 사진을 보고 우리 집 금액을 알려드려요. <a href="price.html">비용 자세히 보기</a></p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">%(name)s 현장</p><h2>%(name)s에서 한<br><em>실제 작업이에요</em></h2>%(nearnote)s</div>
    <div class="wk-grid">%(cards)s</div>
    %(reviews)s
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><p class="kicker">%(name)s 고객님이 많이 묻는 것</p><h2>궁금한 점을<br><em>모았어요</em></h2></div>
    <div class="faq">
      <details><summary>%(name)s도 출장비가 따로 붙나요?</summary><p class="a">무조건 붙지는 않아요. 작업 종류와 위치에 따라 조율해요. 사진과 아파트 이름을 먼저 알려주시면 함께 안내해 드려요.</p></details>
      <details><summary>냉장고를 아직 안 샀는데 먼저 상담해도 되나요?</summary><p class="a">네. 다만 모델마다 폭과 문 여는 각도가 달라서, 최종 제작은 냉장고 모델을 정한 뒤에 맞춰요. 그래야 배송 날 설치 불가가 나오지 않아요.</p></details>
      <details><summary>작업은 하루면 끝나나요?</summary><p class="a">칸막이 제거 같은 리폼은 대부분 하루 안에 끝나고 당일 사용할 수 있어요. 맞춤제작은 실측한 치수로 미리 만들어 가서 설치하고, 일정은 상담 때 알려드려요.</p></details>
      <details><summary>설치 후에 처지면 어떻게 하나요?</summary><p class="a">기둥을 빼거나 새로 짠 장의 처짐·기울어짐은 평생 AS로 책임져요. <a href="as.html">AS 안내 보기</a></p></details>
    </div>
    <div class="area-others"><span>다른 지역</span>%(others)s</div>%(subs)s
    <div class="area-others"><span>작업별 안내</span><a href="guide-kitchenfit.html">키친핏 냉장고장 맞춤제작</a><a href="guide-partition.html">칸막이 제거 리폼</a><a href="fridge-bespoke.html">비스포크 냉장고장</a><a href="fridge-objet.html">오브제 냉장고장</a></div>
  </div>
</section>
''' % {'intro': intro, 'reach': reach, 'name': name, 'cards': ''.join(card(w, 'h3') for w in show), 'others': others, 'subs': ('<div class="area-others"><span>가까운 동네</span>%s</div>' % ''.join('<a href="area-%s.html">%s</a>' % (x[0], x[1]) for x in SUBS if x[2] == slug)) if any(x[2] == slug for x in SUBS) else '',
       'reviews': ('<h3 class="rv-title">고객님 후기</h3><div class="rv-grid rv-2">%s</div>' % ''.join('<figure class="rv"><blockquote>“%s”</blockquote><figcaption><b>%s</b><span>%s</span><a href="case-%s.html">현장 보기 →</a></figcaption></figure>' % (H.escape(CASES[w['no']]['quote']), H.escape(w['w']), H.escape(w['t']), w['no']) for w in show if CASES[w['no']].get('quote') and w['no'] != '224285887538')) if any(CASES[w['no']].get('quote') for w in show) else '',
       'nearnote': '<p>가까운 지역 현장도 함께 보여드려요.</p>' if len(mine) < len(show) else ''}
    body, ldj, ogi = area_rich(body, name, show, reach)
    js = crumbs([('홈', ''), (name, 'area-' + slug)]) + ldj
    title = ('%s 냉장고장 리폼·맞춤제작 시공 사례 %d건' % (name, len(mine))) if len(mine) >= 3 else ('%s 냉장고장 리폼·맞춤제작 · 시공 사례와 비용' % name)
    page('area-%s.html' % slug, title, '%s에서 실제 시공한 냉장고장 사례를 공사 전후 사진과 작업 과정으로 보여드려요. 칸막이 제거 리폼 30만원, 키친핏 냉장고장 맞춤제작 100만원부터(VAT 별도). E0 자재, 대표 직접 시공, 평생 AS. 문의 %s' % (name, PHONE),
         '%s 출장' % name, '%s<br><em>키친핏 냉장고장</em>' % name, '%s에서도 냉장고 모델에 맞춰 실측하고, 대표가 직접 짜서 설치해요.' % name, body, js,
         crumb=name, og_image=ogi, subnav=False)

# ================= 동네별 페이지 =================
ANAME = {a[0]: a[1] for a in AREAS}
for slug, name, parent, key, intro, towns in SUBS:
    pname = ANAME[parent]; pcity = [a for a in AREAS if a[0] == parent][0][2]
    mine = [w for w in works if key in (CASES[w['no']].get('region') or '')]
    near = [w for w in works if w not in mine and city(w) in pcity]
    if len(mine) + len(near) < 4:
        near += [w for w in works if w not in mine + near and w['f'] == 'fridge' and city(w) in ('대전', '세종', '천안', '청주', '홍성')]
    show = mine + near[:max(0, 6 - len(mine))]
    sibs = ''.join('<a href="area-%s.html">%s</a>' % (x[0], x[1]) for x in SUBS if x[2] == parent and x[0] != slug)
    body = """<section>
  <div class="wrap">
    <div class="area-intro"><p>%(intro)s</p><p class="muted">%(towns)s 어디든 실측하러 가요.</p></div>
    <div class="area-svc">
      <a class="area-card pop" href="guide-kitchenfit.html"><span class="pill">대표 작업</span><h3>%(name)s 키친핏 냉장고장 맞춤제작</h3><p>냉장고 모델의 설치 가이드에 맞춰 높이, 깊이, 도어 두께까지 맞춰 E0 등급 자재로 새로 짜요.</p><b>100만원부터</b></a>
      <a class="area-card" href="guide-partition.html"><span class="pill">리폼</span><h3>%(name)s 냉장고장 칸막이 제거</h3><p>옵션 냉장고장을 살리고 가운데 기둥만 빼서 키친핏 냉장고 자리를 만들어요. 상부장은 보강해요.</p><b>30만원</b></a>
      <a class="area-card" href="services.html#bar"><span class="pill">맞춤제작</span><h3>홈바장 · 수납장</h3><p>냉장고 옆 남는 폭이나 빈 벽에 홈바장, 렌지장, 밥솥장을 맞춰 넣어요.</p><b>100만원부터</b></a>
    </div>
    <p class="price-note">금액은 VAT 별도예요. 사진과 냉장고 모델명을 보내 주시면 우리 집 금액을 알려드려요. <a href="price.html">비용 자세히 보기</a></p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">%(name)s 가까운 현장</p><h2>%(head)s</h2></div>
    <div class="wk-grid">%(cards)s</div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><p class="kicker">%(name)s 고객님이 묻는 것</p><h2>궁금한 점을<br><em>모았어요</em></h2></div>
    <div class="faq">
      <details><summary>%(name)s까지 와 주시나요?</summary><p class="a">네. %(towns)s까지 찾아가요. 사진과 아파트 이름을 먼저 보내 주시면 방문 일정과 금액을 함께 알려드려요.</p></details>
      <details><summary>냉장고를 아직 안 샀는데 먼저 상담해도 되나요?</summary><p class="a">네. 다만 모델마다 폭과 문 여는 각도가 달라서, 최종 제작은 냉장고 모델을 정한 뒤에 맞춰요.</p></details>
      <details><summary>칸막이만 빼면 상부장이 처지지 않나요?</summary><p class="a">칸막이가 받치던 무게만큼 상부장과 천장을 보강해요. 처짐·기울어짐은 평생 AS로 책임져요. <a href="as.html">AS 안내 보기</a></p></details>
    </div>
    <div class="area-others"><span>%(pname)s 전체</span><a href="area-%(parent)s.html">%(pname)s 냉장고장 안내</a></div>
    %(sibs)s
    <div class="area-others"><span>작업별 안내</span><a href="guide-kitchenfit.html">키친핏 냉장고장 맞춤제작</a><a href="guide-partition.html">칸막이 제거 리폼</a><a href="fridge-bespoke.html">비스포크 냉장고장</a><a href="fridge-objet.html">오브제 냉장고장</a></div>
  </div>
</section>
""" % {'intro': intro, 'towns': towns, 'name': name, 'pname': pname, 'parent': parent, 'cards': ''.join(card(w, 'h3') for w in show),
       'head': ('%s에서 한<br><em>실제 작업이에요</em>' % name) if mine else ('가까운 지역에서 한<br><em>실제 작업이에요</em>'),
       'sibs': ('<div class="area-others"><span>가까운 동네</span>%s</div>' % sibs) if sibs else ''}
    body, ldj, ogi = area_rich(body, name, show, towns)
    js = crumbs([('홈', ''), (pname, 'area-' + parent), (name, 'area-' + slug)]) + ldj
    page('area-%s.html' % slug, ('%s 냉장고장 리폼·맞춤제작 시공 사례 %d건' % (name, len(mine))) if len(mine) >= 3 else ('%s 냉장고장 리폼·맞춤제작 · 시공 사례와 비용' % name),
         '%s 냉장고장 칸막이 제거 리폼 30만원, 키친핏 냉장고장 맞춤제작 100만원부터(VAT 별도). %s 출장 실측, 가까운 시공 사례의 공사 전후 사진과 작업 과정, E0 자재, 평생 AS. 문의 %s' % (name, towns.split(' · ')[0], PHONE),
         '%s 출장' % name, '%s<br><em>냉장고장 맞춤제작</em>' % name, '%s에서도 냉장고 모델에 맞춰 실측하고, 대표가 직접 짜서 설치해요.' % name, body, js,
         crumb=name, og_image=ogi, subnav=False)

# ================= 검색어별 안내 페이지 =================
def fr(w): return (CASES[w['no']].get('fridge') or '')
GUIDES = [
 ('guide-kitchenfit', '키친핏 냉장고장 맞춤제작', '키친핏 냉장고장 맞춤제작 가이드', '맞춤제작 가이드', '키친핏 냉장고장<br><em>맞춤제작 가이드</em>',
  '키친핏 냉장고장은 냉장고와 장 사이를 1cm 정도로 붙여 일체형처럼 보이게 짜는 장이에요. 무옵션 세대이거나 옵션 장이 냉장고와 안 맞을 때, 냉장고 모델의 설치 가이드에 맞춰 처음부터 짜요.',
  [('냉장고 먼저', '모델을 먼저 정해요. 키친핏은 사이즈가 정확해야 해서, 장을 먼저 짜면 다시 작업해야 할 수 있어요.'),
   ('설치 가이드', '모델별 설치 가이드를 보고 높이, 깊이, 도어 두께까지 맞춰 설계해요.'),
   ('남는 공간', '냉장고를 넣고 남는 폭은 키큰장, 홈바장, 로봇청소기장으로 채워요.'),
   ('E0 친환경 자재', '포름알데히드 방출량 0.5mg/L 이하인 E0 등급 자재로 짜고, 주방 가구 색상에 맞춰 마감해요.')],
  [('모델 확인', '냉장고 모델명과 현장 사진을 문자로 받아요.'), ('실측과 설계', '현장을 재고 설치 가이드에 맞춰 설계해요.'), ('사전 제작', '치수에 맞게 미리 재단해 가서 현장 작업을 줄여요.'), ('설치와 마감', '수평을 잡고 프레임, 상부장, 문짝 순서로 설치해요.')],
  lambda w: w['no'] in ('223833108339', '224277045640', '224432139660', '224176609693', '223906771954'),
  [('신축인데 옵션을 빼도 되나요?', '네. 옵션 냉장고장은 보통 양문형 냉장고 기준으로 설계돼서, 키친핏 같은 넓은 일체형 냉장고는 공간이 부족한 경우가 많아요. 그래서 옵션을 빼고 모델에 맞춰 따로 짜는 집이 많아요.'),
   ('맞춤제작 비용은 얼마인가요?', '냉장고장 맞춤제작은 100만원부터예요. 넣는 장의 개수, 홈바장이나 조명 같은 추가 구성에 따라 달라지고 VAT 별도예요.'),
   ('남는 공간은 어떻게 쓰나요?', '넉넉하면 키큰장 대신 홈바장이나 로봇청소기장을 넣을 수 있어요. 냉장고 옆 틈에 홈카페장을 만든 현장도 있어요.')]),
 ('guide-partition', '냉장고장 칸막이 제거 리폼', '냉장고장 칸막이 제거 리폼 가이드', '칸막이 제거 가이드', '냉장고장 칸막이 제거<br><em>리폼 가이드</em>',
  '새로 산 냉장고가 옵션 냉장고장 가운데 칸막이나 기둥에 걸려 안 들어갈 때, 장을 다 뜯지 않고 칸막이만 빼서 자리를 만드는 작업이에요. 상부장은 다시 쓰고, 기둥이 받치던 무게만큼 보강해요.',
  [('부분 철거', '전체 철거가 아니에요. 프레임과 측판, 상부장은 살리고 걸리는 부분만 빼요.'),
   ('보강 필수', '칸막이만 잘라내면 상부장이 처지기 쉬워요. 상부장과 천장을 2단으로 보강해요.'),
   ('바닥·벽 마감', '칸막이가 있던 자리는 도배와 마루가 안 돼 있어서, 자재로 채워 마감해요.'),
   ('당일 사용', '단순 칸막이 제거는 3~4시간이면 끝나고 대부분 그날 냉장고를 넣어요.')],
  [('상부장 내리기', '반대쪽 상부장이 처지지 않게 지지대로 받치고 상부장을 내려요.'), ('칸막이 철거', '칸막이와 기둥을 빼고 냉장고 들어갈 폭을 다시 재요.'), ('보강과 재설치', '상부장과 천장을 보강하고 수평을 맞춰 다시 걸어요.'), ('마감과 틈새장', '바닥과 벽을 마감하고, 남는 폭은 수납장으로 만들어요.')],
  lambda w: w['f'] == 'fridge' and any(k in w['t'] for k in ('칸막이', '기둥', '가림막', '자리 만들기', '구조')),
  [('비용은 얼마인가요?', '상부장을 그대로 쓰고 칸막이만 빼서 틈새장을 만드는 부분 리폼은 30만원이에요(VAT 별도). 철거, 상부 보강, 폐자재 처리는 기본가에 들어 있어요.'),
   ('셀프로 해도 되나요?', '권하지 않아요. 상부장은 높고 무거워서 떨어질 위험이 있고, 보강 없이 빼면 시간이 지나며 장이 주저앉을 수 있어요.'),
   ('냉장고를 사기 전에 해도 되나요?', '냉장고 모델을 먼저 정하고 그 사이즈에 맞춰 리폼하는 순서가 가장 좋아요.')]),
 ('fridge-bespoke', '삼성 비스포크 냉장고장', '삼성 비스포크 냉장고장 맞춤제작·리폼', '비스포크 냉장고장', '삼성 비스포크<br><em>냉장고장</em>',
  '비스포크 키친핏 냉장고를 옵션 냉장고장에 넣으려다 설치 불가를 듣는 집이 많아요. 기둥을 빼서 자리를 만들거나, 무옵션 세대라면 비스포크 설치 가이드에 맞춰 장을 새로 짜요.',
  [('설치 불가 해결', '옵션 장의 기둥 때문에 안 들어가면 기둥을 빼고 보강해서 자리를 만들어요.'), ('자재 재사용', '기존 냉장고장 자재를 다시 써서 공간만 넓힐 수 있어요.'), ('새로 짜기', '무옵션 세대는 비스포크 모델에 맞춰 처음부터 짜요.'), ('평생 AS', '처짐·기울어짐은 평생 무상으로 책임져요.')],
  None, lambda w: '비스포크' in fr(w) or '비스포크' in w['t'], []),
 ('fridge-objet', 'LG 오브제 냉장고장', 'LG 오브제 냉장고장 맞춤제작·리폼', '오브제 냉장고장', 'LG 오브제<br><em>냉장고장</em>',
  'LG 오브제 1+1+1처럼 여러 대를 나란히 넣는 냉장고는 옵션 냉장고장 가운데 기둥에 걸려 붙지 않는 경우가 많아요. 기둥을 빼고 보강해서 오브제가 나란히 붙게 만들어요.',
  [('1+1+1 · 4도어', '냉장고 구성에 맞춰 칸을 다시 나눠요. 김치냉장고까지 네 대를 나란히 넣은 현장도 있어요.'), ('기둥 제거', '가운데 기둥을 빼고 상부장과 천장을 보강해요.'), ('옵션 장 살리기', '옵션 냉장고장 틀은 그대로 두고 필요한 부분만 바꿔요.'), ('당일 사용', '대부분 하루 안에 끝나고 그날 냉장고를 넣어요.')],
  None, lambda w: '오브제' in fr(w) or '오브제' in w['t'], []),
]
for slug, name, title, kicker, h1, intro, points, steps, sel, faq in GUIDES:
    mine = [w for w in works if sel(w)]
    pts = ''.join('<div class="factor"><span class="ic">%02d</span><h3>%s</h3><p>%s</p></div>' % (n, t, d) for n, (t, d) in enumerate(points, 1))
    st = ('<section class="band"><div class="wrap"><div class="sec-head"><p class="kicker">진행 순서</p><h2>이렇게<br><em>작업해요</em></h2></div><div class="guide">%s</div></div></section>'
          % ''.join('<div><span class="ic">%d</span><h3>%s</h3><p>%s</p></div>' % (n, t, d) for n, (t, d) in enumerate(steps, 1))) if steps else ''
    fq = ('<section><div class="wrap"><div class="sec-head"><p class="kicker">자주 묻는 질문</p><h2>많이<br><em>물어보세요</em></h2></div><div class="faq">%s</div></div></section>'
          % ''.join('<details><summary>%s</summary><p class="a">%s</p></details>' % (q, a) for q, a in faq)) if faq else ''
    areas_ = ''.join('<a href="area-%s.html">%s %s</a>' % (s, n, name) for s, n, *_ in AREAS)
    body = '''<section>
  <div class="wrap">
    <div class="area-intro"><p>%s</p></div>
    <div class="factors">%s</div>
    <p class="price-note">%s <a href="price.html">비용 자세히 보기</a></p>
  </div>
</section>
%s
<section class="%s">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">실제 현장 %d곳</p><h2>%s<br><em>작업 사례</em></h2></div>
    <div class="wk-grid">%s</div>
  </div>
</section>
%s
<section class="band">
  <div class="wrap">
    <div class="area-others"><span>지역별로 보기</span>%s</div>
  </div>
</section>
''' % (intro, pts, '냉장고장 맞춤제작 100만원부터, 칸막이 제거 부분 리폼 30만원(VAT 별도).', st, '' if steps else 'band', len(mine), name, ''.join(card(w) for w in mine), fq, areas_)
    ldj = crumbs([('홈', ''), (name, slug)])
    if faq:
        ldj += ld({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]})
    page(slug + '.html', title, ('%s %s 실제 현장 %d곳과 비용, 진행 순서를 확인하세요. 대전·세종·천안·청주 출장, 대표 직접 시공.' % (intro.split('.')[0] + '.', name, len(mine)))[:160],
         kicker, h1, '대표가 직접 재고, 짜고, 설치해요. 실제 현장 사진으로 보여드려요.', body, ldj, crumb=name, subnav=False)
GUIDE_LINKS = ''.join('<a href="%s.html">%s</a>' % (g[0], g[1]) for g in GUIDES)

# ================= AS 안내 =================
body = '''<section>
  <div class="wrap">
    <div class="sec-head"><p class="kicker">보장 내용</p><h2>무엇을, 언제까지<br><em>책임지나요</em></h2></div>
    <div class="factors">
      <div class="factor"><span class="ic">01</span><h3>대상</h3><p>네모의꿈이 시공한 냉장고장, 상부장, 홈바장 같은 맞춤가구와 리폼한 장이에요.</p></div>
      <div class="factor"><span class="ic">02</span><h3>범위</h3><p>장이 처지거나 기울어지는 문제예요. 기둥을 뺀 리폼 현장도 똑같이 책임져요.</p></div>
      <div class="factor"><span class="ic">03</span><h3>기간</h3><p>평생이에요. 10년이 지나서 처지거나 떨어져도 연락 주시면 책임지고 고쳐 드려요.</p></div>
      <div class="factor"><span class="ic">04</span><h3>비용</h3><p>처짐·기울어짐 AS는 무상이에요.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">신청 방법</p><h2>문자 한 통이면<br><em>바로 확인해요</em></h2></div>
    <div class="guide">
      <div><span class="ic">1</span><h3>사진 보내기</h3><p>처지거나 기울어진 부분 사진을 문자로 보내주세요.</p></div>
      <div><span class="ic">2</span><h3>주소 알려주기</h3><p>시공한 집 주소와 아파트 이름을 같이 적어 주세요.</p></div>
      <div><span class="ic">3</span><h3>사진 확인</h3><p>사진으로 원인을 먼저 보고 방문 날짜를 잡아요.</p></div>
      <div><span class="ic">4</span><h3>방문 보수</h3><p>대표가 직접 가서 수평을 다시 잡고 보강해요.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><p class="kicker">자신 있는 이유</p><h2>처음부터<br><em>안 처지게 짜요</em></h2></div>
    <div class="vs">
      <div class="vs-card" style="background:var(--surface)"><span class="pill">2단 보강</span><h3>상부장과 천장을 함께 잡아요</h3><p>기둥이 받치던 무게만큼 상부장과 천장에 2단 보강을 해요. 10년, 20년이 지나도 처지지 않게 하는 게 목표예요.</p></div>
      <div class="vs-card" style="background:var(--surface)"><span class="pill">직접 시공</span><h3>하청 없이 대표가 해요</h3><p>한샘·현대리바트 시공팀장 출신 대표가 상담부터 시공, AS까지 직접 해요. 그래서 끝까지 책임질 수 있어요.</p></div>
    </div>
    <h3 class="rv-title">블로그에 남긴 약속</h3>
    <div class="rv-grid rv-2">
      <figure class="rv"><blockquote>“만약 10년이 지나서 처지거나 떨어진다면 편하게 연락주세요. 책임지고 AS 해드리겠습니다!!”</blockquote><figcaption><b>대전 둔산더샵엘리프 시공기</b><a href="https://blog.naver.com/zibaejang/223845410630" target="_blank" rel="noopener">블로그 원문 ↗</a></figcaption></figure>
      <figure class="rv"><blockquote>“상부장 처짐시 A/S 평생 해드리겠습니다.”</blockquote><figcaption><b>대전 신축 아파트 시공기</b><a href="https://blog.naver.com/soorigome/224277045640" target="_blank" rel="noopener">블로그 원문 ↗</a></figcaption></figure>
      <figure class="rv"><blockquote>“처짐 기울어짐 AS 평생 보장”</blockquote><figcaption><b>홍성 내포 반도유보라 시공기</b><a href="https://blog.naver.com/zibaejang/223843274881" target="_blank" rel="noopener">블로그 원문 ↗</a></figcaption></figure>
    </div>
    <p class="price-note">처짐·기울어짐 말고 다른 문제가 생겨도 사진을 보내 주시면 상황을 보고 안내해 드려요.</p>
  </div>
</section>
'''
page('as.html', 'AS 안내', '네모의꿈이 시공한 냉장고장·상부장·홈바장의 처짐·기울어짐은 평생 무상 AS. 보장 대상, 범위, 신청 방법을 안내해요. 문의 %s' % PHONE,
     'AS 안내', '처지거나 기울면<br><em>평생 고쳐드려요</em>', '저희가 짠 장은 끝까지 저희가 책임져요. 사진 한 장만 보내주세요.', body, crumbs([('홈', ''), ('AS 안내', 'as')]), subnav=False)

exec(open(TOOLS + '/kw_pages.py').read())
exec(open(TOOLS + '/qa_pages.py').read())

# ================= sitemap / robots =================
today = date.today().isoformat()
urls = [''] + [f[:-5] for f, _ in PAGES] + ['as'] + [g[0] for g in GUIDES] + ['area-' + a[0] for a in AREAS] + ['area-' + x[0] for x in SUBS] + [k[0] for k in KW_PAGES] + ['qa'] + [q[0] for q in QA_PAGES] + ['case-' + w['no'] for w in works]
open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (SITE, u, today) for u in urls) + '</urlset>\n')
open('robots.txt', 'w').write('User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % SITE)
print('detail built', len(works), 'cases', len(AREAS), 'areas')

# ================= 사장님 통계 페이지 /admin/stats/ (비밀번호 잠금, 검색 제외) =================
names = {'/': '첫 화면', '/services': '하는 일', '/works': '작업 기록', '/price': '비용', '/process': '진행 방법', '/faq': '자주 묻는 질문', '/as': 'AS 안내'}
names.update({'/area-' + a[0]: '지역: ' + a[1] for a in AREAS})
names.update({'/area-' + x[0]: '지역: ' + x[1] for x in SUBS})
names.update({'/' + k[0]: '검색어: ' + k[1] for k in KW_PAGES})
names.update({'/' + g[0]: '안내: ' + g[1] for g in GUIDES})
names.update({'/' + q[0]: '질문: ' + q[1] for q in QA_PAGES}); names['/qa'] = '질문과 답변'
names.update({'/case-' + w['no']: '사례: ' + CASES[w['no']]['title'] for w in works})
os.makedirs('admin/stats', exist_ok=True)
st = open(TOOLS + '/admin_stats_template.html').read()
open('admin/stats/index.html', 'w').write(st.replace('__NAMES__', json.dumps(names, ensure_ascii=False)))
