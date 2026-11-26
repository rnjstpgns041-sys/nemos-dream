# 매일 자동 작업 (예약 실행용 안내) — 매일 오전 8시

## 2026-11-26 사용자 결정: 앞으로는 "사람들이 많이 찾는 검색어" 위주로 작업한다
- 동네 + 작업 키워드 페이지(`tools/daily.py 30`)는 **더 이상 만들지 않는다.** 1,281개 중 40일 동안 방문이 있었던 건 110개뿐이었다.
- 페이지 합치기·삭제는 사용자 승인 전까지 하지 않는다.
사람에게 묻지 않고 끝까지 한다.

1. `git pull origin main`
2. `python3 tools/bigterms.py` → 네이버 자동완성 상위 큰 검색어(약 50개)마다 휴대폰 네이버 첫 화면에 웹사이트 칸이 있는지, 홈페이지가 나오는지 기록(tools/bigterms.json).
3. 대표 페이지: 오늘 결과에서 **웹사이트 칸이 있는데(웹) 홈페이지가 안 나오는(★ 없음)** 검색어 중 많이 찾는 것부터 **최대 2개**를 골라, 그 검색어로 시작하는 제목의 대표 페이지를 `tools/build_detail.py`의 GUIDES에 더한다(예: partition-cost, fridge-cabinet-price).
   - 이미 같은 뜻의 대표 페이지가 있으면 새로 만들지 말고 그 페이지의 소개·질문을 그 검색어에 맞게 보강한다.
   - 내용은 `tools/facts.md`와 `tools/cases.json` 사실만. 첫 문장에 "네모의꿈(010-4835-3353)"과 검색어 그대로.
   - 대상이 없으면 만들지 않는다(억지로 만들지 않기).
4. GEO: `python3 tools/demand.py 10 10` 후 `tools/today_qa.txt`에서 아래 규칙으로 최대 10개 `tools/qa.json`에 추가 (없으면 0개).
   - **질문(q)에 그 검색어를 글자 그대로 넣는다.** 예: 검색어 "키친핏 냉장고장 사이즈" → q "키친핏 냉장고장 사이즈는 어떻게 맞추나요?"
     (제목에 검색어가 들어가야 다음 날 중복으로 안 잡히고, 네이버에도 그 말로 뜬다.)
   - 답은 `tools/facts.md`에 있는 사실만. 가격·기간·보증·치수 규격을 지어내지 않는다. 모르면 "사진과 냉장고 모델명을 보내주시면 알려드려요".
   - facts.md로 정직하게 답할 수 없는 검색어(다른 업체 이름, 우리가 안 하는 일(싱크대 전체 교체·욕실 수전·붙박이장 등), 셀프 시공 요령, 치수 숫자만 다른 같은 말 등)는 건너뛰고 다음 줄로.
   - 형식: {"slug": 영문-소문자-하이픈(기존과 안 겹치게), "q": 질문, "a": 2~3문장 짧은 답, "more": [문단 1~3개], "fit": 작업 slug(partition, kitchenfit, bespoke, objet, custom, reform, kimchi, homebar, range, shoe, robot, pillar, noinstall, cost, movein, fourdoor, homecafe, make, demolish, install, pricing, side, fridgebar, storage, door, ttungnaeng, interior 중 하나), "kw": 관련 키워드 페이지(예: kw-daejeon-pricing, 있는 파일만)}
5. `python3 tools/build_pages.py` → 페이지·sitemap·new-urls.txt가 만들어진다. 오류가 나면 고치고 다시.
6. 바뀐 파일 전부 커밋하고 `git push origin main`. 배포가 끝나면 deploy-succeeded 함수가 새 주소를 네이버·빙(IndexNow)에 자동으로 알린다.
7. 몇 분 뒤 https://nemos-dream.com/api/t?idx 에서 urls 수와 200 응답을 확인한다.
8. 홈페이지 스레드에 쉬운 한국어로 짧게 보고: 큰 검색어 중 홈페이지가 나오는 수(어제와 비교), 새로 만든·보강한 대표 페이지, GEO 몇 개. 적으면 적은 대로 솔직하게.

참고: `tools/daily.py`(동네 + 작업 조합)는 2026-11-26부터 쓰지 않는다. 단 demand.py가 자동완성에서 실제로 찾은 "도시 + 작업" 검색어(예: 청주 냉장고장 리폼 가격)는 실제로 찾는 말이라 계속 키워드 페이지로 만든다.
