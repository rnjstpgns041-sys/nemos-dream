# 지역 페이지(area-*.html)를 풍성하게: 숫자 띠, 대표 현장 자세히, 맡기는 경우, 진행 순서, 비용표, FAQ 보강 + FAQPage JSON-LD.
# build_detail.py가 exec로 불러 쓴다(works, CASES, ld, H, os, SITE를 같이 씀).
import re as _re
def feat_case(show):
    q = [w for w in show if CASES[w['no']].get('quote')]
    return (q or show)[0]
def area_rich(body, name, show, towns):
    f = feat_case(show); c = CASES[f['no']]; no = f['no']
    pics = [x for x in ('img/c/%s-%d.jpg' % (no, k) for k in range(6)) if os.path.exists(x)][:3]
    steps = ''.join('<li><b>%s</b><p>%s</p></li>' % (H.escape(x['t']), H.escape(x['d'])) for x in c['steps'][:5])
    stats = '''<section class="area-stats-sec">
  <div class="wrap">
    <div class="area-stats">
      <div><b>직접</b><span>대표가 실측부터 시공까지</span></div>
      <div><b>하루</b><span>칸막이 제거 리폼 대부분 당일 완료</span></div>
      <div><b>평생</b><span>처짐·기울어짐 무상 AS</span></div>
    </div>
    <p class="stats-note">※ E0 등급 친환경 자재(포름알데히드 방출 0.5mg/L 이하)만 사용해요.</p>
  </div>
</section>
'''
    feat = '''<section class="area-feat-sec">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">대표 현장 자세히</p><h2>%(t)s</h2><p>%(region)s</p></div>
    <div class="area-feat">
      <div class="wk-pair case-pair"><figure><img loading="lazy" src="img/works/%(no)s-before.jpg" alt="%(t)s 공사 전"><figcaption>BEFORE</figcaption></figure><figure><img loading="lazy" src="img/works/%(no)s-after.jpg" alt="%(t)s 공사 후"><figcaption class="a">AFTER</figcaption></figure></div>
      <div class="area-feat-txt">
        <h3>이런 상황이었어요</h3><p>%(problem)s</p>
        <h3>이렇게 작업했어요</h3><ol class="case-steps">%(steps)s</ol>
      </div>
    </div>
    %(gal)s
    <div class="area-feat-res"><h3>작업 결과</h3><p>%(result)s</p></div>
    %(quote)s
    <p class="more-link"><a class="btn btn-soft" href="case-%(no)s.html">이 현장 전체 보기 →</a></p>
  </div>
</section>
''' % {'t': H.escape(c['title']), 'region': H.escape(c['region']), 'no': no, 'problem': H.escape(c['problem']), 'steps': steps,
       'gal': '<div class="case-gal">%s</div>' % ''.join('<figure><img loading="lazy" src="%s" alt="%s 작업 과정 %d"></figure>' % (x, H.escape(c['title']), n + 1) for n, x in enumerate(pics)) if pics else '',
       'result': H.escape(c['result']),
       'quote': '<blockquote class="case-quote">“%s”<cite>%s 고객님 후기</cite></blockquote>' % (H.escape(c['quote']), H.escape(c['region'])) if c.get('quote') else ''}
    more = '''<section>
  <div class="wrap">
    <div class="sec-head"><p class="kicker">%(name)s 이런 집에서 맡겨요</p><h2>우리 집도<br><em>해당되나요?</em></h2></div>
    <ul class="area-need">
      <li><b>새 냉장고가 안 들어가요</b><span>옵션 냉장고장 가운데 칸막이나 기둥에 걸려 비스포크·오브제가 안 들어가는 집</span></li>
      <li><b>무옵션으로 입주했어요</b><span>냉장고장 옵션을 안 넣어서 냉장고 모델에 맞춰 처음부터 짜야 하는 집</span></li>
      <li><b>냉장고 옆이 비어요</b><span>냉장고를 넣고 남는 폭에 홈바장, 밥솥장, 로봇청소기장을 넣고 싶은 집</span></li>
      <li><b>장을 다 뜯긴 싫어요</b><span>상부장과 프레임은 살리고 걸리는 부분만 바꾸고 싶은 집</span></li>
    </ul>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">진행 순서</p><h2>문자 한 통부터<br><em>설치까지</em></h2></div>
    <ol class="case-steps area-flow">
      <li><b>사진·모델명 문자</b><p>현장 사진, 냉장고 모델명, 아파트 이름을 문자로 보내 주세요. 사진을 보고 방법과 대략적인 금액을 알려드려요.</p></li>
      <li><b>실측</b><p>%(name)s 현장에 찾아가 높이, 깊이, 수평을 재고 냉장고 설치 가이드에 맞춰 설계해요.</p></li>
      <li><b>사전 제작</b><p>잰 치수대로 E0 등급 자재를 미리 재단해 가서 현장 작업 시간을 줄여요.</p></li>
      <li><b>설치·마감</b><p>보강하고 설치한 뒤 몰딩과 마루까지 마감하고, 고객님과 함께 확인해요.</p></li>
      <li><b>평생 AS</b><p>설치 후 처지거나 기울면 사진만 보내 주세요. 평생 책임지고 고쳐드려요.</p></li>
    </ol>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><p class="kicker">%(name)s 비용</p><h2>얼마 드는지<br><em>먼저 보세요</em></h2></div>
    <table class="area-price">
      <thead><tr><th>작업</th><th>이런 경우</th><th>비용</th></tr></thead>
      <tbody>
        <tr><td>칸막이·기둥 제거 리폼</td><td>옵션 냉장고장을 살리고 가운데만 빼서 키친핏 자리 만들기</td><td><b>30만원</b></td></tr>
        <tr><td>키친핏 냉장고장 맞춤제작</td><td>냉장고 모델에 맞춰 냉장고장을 새로 짜기</td><td><b>100만원부터</b></td></tr>
        <tr><td>홈바장·수납장 맞춤제작</td><td>냉장고 옆이나 빈 벽에 홈바장, 렌지장, 밥솥장 넣기</td><td><b>100만원부터</b></td></tr>
      </tbody>
    </table>
    <p class="price-note">VAT 별도예요. 장 크기와 추가 구성에 따라 달라져서, 사진을 보고 우리 집 금액을 정확히 알려드려요. <a href="price.html">비용 자세히 보기</a></p>
  </div>
</section>
''' % {'name': name}
    extra_faq = ('<details><summary>%s 칸막이 제거는 얼마인가요?</summary><p class="a">옵션 냉장고장을 살리고 가운데 칸막이나 기둥만 빼는 리폼은 30만원이에요(VAT 별도). 보강과 몰딩·마루 마감까지 포함해요.</p></details>'
                 '<details><summary>자재는 어떤 걸 쓰나요?</summary><p class="a">포름알데히드 방출량 0.5mg/L 이하인 E0 등급 친환경 자재로 짜요.</p></details>'
                 '<details><summary>견적은 어떻게 받나요?</summary><p class="a">현장 사진 2~3장, 냉장고 모델명, 아파트 이름을 문자로 보내 주세요. 작업 중엔 전화를 못 받을 때가 많아 문자가 가장 빨라요.</p></details>') % name
    if c.get('quote'):  # 대표 현장 후기는 아래 후기 목록에서 빼서 같은 말이 두 번 안 나오게
        body = _re.sub(r'<figure class="rv"><blockquote>“%s”</blockquote>.*?</figure>' % _re.escape(H.escape(c['quote'])), '', body, flags=_re.S)
    body = body.replace('<section class="band">', stats + feat + '<section class="band">', 1)
    i = body.rfind('\n<section>\n'); body = body[:i] + '\n' + more + body[i:]
    body = body.replace('<div class="faq">', '<div class="faq">' + extra_faq, 1)
    qa = _re.findall(r'<details><summary>(.*?)</summary><p class="a">(.*?)</p></details>', body)
    ldj = ld({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': _re.sub('<[^>]+>', '', q), 'acceptedAnswer': {'@type': 'Answer', 'text': _re.sub('<[^>]+>', '', a)}} for q, a in qa]})
    return body, ldj, SITE + 'img/works/%s-after.jpg' % no
