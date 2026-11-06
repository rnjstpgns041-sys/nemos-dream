# GEO용 질문·답변 페이지 (qa-<slug>.html)와 모음 페이지(qa.html). 내용은 tools/qa.json (facts.md에 있는 사실만 쓴다)
QA = json.load(open(TOOLS + '/qa.json'))
QA_PAGES = []
for i, x in enumerate(QA):
    slug = 'qa-' + x['slug']
    sel = KWD[x['fit']][5] if x.get('fit') in KWD else FIT
    cases = ([w for w in works if sel(w)] or [w for w in works if FIT(w)])[:3]
    kw = x.get('kw') if x.get('kw') and os.path.exists(x['kw'] + '.html') else None
    near = [QA[(i + k) % len(QA)] for k in (1, 2, 3, 4) if len(QA) > k]
    body = '''<section class="qa-sec">
  <div class="wrap qa-wrap">
    <div class="qa-short"><p class="kicker">짧은 답</p><p>%(a)s</p></div>
    <div class="qa-more">%(more)s</div>
    <p class="qa-cta"><a class="btn btn-acc" href="#quote">사진 한 장으로 무료 견적 받아보기</a><a class="btn btn-soft" href="tel:%(ph)s">전화 %(ph)s</a></p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">실제 현장</p><h2>이렇게<br><em>해결했어요</em></h2></div>
    <div class="wk-grid">%(cards)s</div>
  </div>
</section>
<!--QUOTE-->
<section>
  <div class="wrap">
    <div class="area-others"><span>다른 질문</span>%(near)s<a href="qa.html">질문 전체 보기</a></div>
    <div class="area-others"><span>더 보기</span>%(kwl)s<a href="price.html">비용 안내</a><a href="as.html">AS 안내</a></div>
  </div>
</section>
''' % {'a': H.escape(x['a']), 'more': ''.join('<p>%s</p>' % H.escape(m) for m in x.get('more', [])), 'ph': PHONE,
       'cards': ''.join(card(w) for w in cases), 'near': ''.join('<a href="qa-%s.html">%s</a>' % (n['slug'], H.escape(n['q'])) for n in near),
       'kwl': ('<a href="%s.html">%s</a>' % (kw, dict(KW_PAGES).get(kw, '관련 안내'))) if kw else ''}
    ldj = crumbs([('홈', ''), ('질문과 답변', 'qa'), (x['q'], slug)]) + ld({'@context': 'https://schema.org', '@type': 'QAPage', 'mainEntity': {
        '@type': 'Question', 'name': x['q'], 'answerCount': 1, 'acceptedAnswer': {'@type': 'Answer', 'text': x['a'] + ' ' + ' '.join(x.get('more', [])), 'url': SITE + slug,
        'author': {'@type': 'Organization', 'name': '네모의꿈', 'url': SITE}}}})
    page(slug + '.html', x['q'][:40], (x['a'])[:150], '질문과 답변', H.escape(x['q']), '냉장고장 리폼·맞춤제작 대표가 직접 답해요.', body, ldj,
         crumb='<a href="qa.html">질문과 답변</a>', subnav=False)
    QA_PAGES.append((slug, x['q']))
hub = '''<section>
  <div class="wrap">
    <ul class="qa-list">%s</ul>
  </div>
</section>
''' % ''.join('<li><a href="qa-%s.html"><b>Q.</b> %s<span>%s</span></a></li>' % (x['slug'], H.escape(x['q']), H.escape(x['a'][:70]) + '…') for x in QA)
page('qa.html', '냉장고장 질문과 답변', '냉장고장 칸막이 제거, 키친핏 냉장고장 맞춤제작, 비용, AS까지 자주 묻는 질문에 대표가 직접 답해요. 문의 %s' % PHONE,
     '질문과 답변', '냉장고장<br><em>질문과 답변</em>', '손님들이 실제로 많이 묻는 질문에 짧고 정확하게 답했어요.', hub,
     crumbs([('홈', ''), ('질문과 답변', 'qa')]) + ld({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': x['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': x['a']}} for x in QA]}), subnav=False)
print('qa pages', len(QA_PAGES))
