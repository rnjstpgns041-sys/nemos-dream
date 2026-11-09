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

# ===== AI 검색(GEO)용 안내 파일: llms.txt(요약+목록), llms-full.txt(질문·답변 전문) =====
LLM_HEAD = '''# 네모의꿈 (NEMO'S DREAM)

> 대전·세종·천안·아산·청주·홍성 내포 등 충청 전역의 키친핏 냉장고장 맞춤제작·설치, 냉장고장 칸막이·기둥 제거 리폼 업체. 한샘·현대리바트 시공팀장 출신 대표가 상담부터 시공·AS까지 직접 한다(하청 없음).

- 전화·문자: %(ph)s (작업 중엔 전화를 못 받을 때가 많아 문자 견적이 빠름: 사진 2장 이상 + 지역 + 작업 내용)
- 홈페이지: %(site)s
- 가격(VAT 별도): 칸막이·기둥 제거 리폼 30만원(철거·상부장과 천장 보강·바닥 벽 마감·폐자재 처리 포함), 냉장고장 새로 짜기 100만원부터(약 100~140만원), 디자인 홈바장 100만원부터(100~240만원). 그 밖의 작업은 사진을 보고 안내.
- 기간: 칸막이 제거·신발장 오픈장 리폼은 대부분 하루(단순 칸막이 제거 3~4시간). 새로 짤 때도 미리 재단해 현장 설치는 대부분 하루.
- 자재: E0 등급 친환경 자재(포름알데히드 0.5mg/L 이하)
- AS: 시공한 냉장고장·상부장·홈바장의 처짐·기울어짐은 기간 제한 없이 무상
- 그 밖의 작업: 홈바장, 렌지장·밥솥장, 로봇청소기장, 신발장 리폼, 틈새장·수납장, 식세기장, 주방 수전·싱크볼·후드

## 주요 페이지
- [하는 일](%(site)sservices): 냉장고장 맞춤제작, 칸막이·기둥 제거 리폼, 홈바장 등
- [비용](%(site)sprice): 작업별 가격
- [작업 기록](%(site)sworks): 실제 시공 사례(공사 전·후 사진)
- [자주 묻는 질문](%(site)sfaq)
- [질문과 답변 모음](%(site)sqa)
- [AS 안내](%(site)sas)

## 질문과 답변
''' % {'ph': PHONE, 'site': SITE}
open('llms.txt', 'w').write(LLM_HEAD + ''.join('- [%s](%sqa-%s): %s\n' % (x['q'], SITE, x['slug'], x['a']) for x in QA))
open('llms-full.txt', 'w').write(LLM_HEAD.replace('## 질문과 답변\n', '') + '## 질문과 답변 전문\n\n' + ''.join(
    '### %s\n%s\n%s\n출처: %sqa-%s\n\n' % (x['q'], x['a'], '\n'.join(x.get('more', [])), SITE, x['slug']) for x in QA))
print('llms.txt', len(QA))
