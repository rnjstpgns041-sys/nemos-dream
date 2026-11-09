# 매일 자동 작업 (예약 실행용 안내) — 매일 오전 8시

목표(2026-11-09 사용자 결정: 매일 연락 올 만한 키워드 페이지 30개 + GEO 질문·답변 10개): 사람들이 네이버에 **실제로 검색하는 말**로 페이지를 만든다. 아무도 검색하지 않는 동네 조합은 만들지 않는다.
사람에게 묻지 않고 끝까지 한다.

1. `git pull origin main`
2. `python3 tools/daily.py 30` → 연락이 오는 작업(수전·싱크볼·후드·식세기장·상부장·맞춤가구·비용·가격·칸막이 제거·시공·철거·설치 불가)을 큰 도시부터 지역 키워드 페이지 30개로 고른다 (tools/daily.json).
2-1. `python3 tools/demand.py 10 10`
   - 네이버 자동완성에서 실제 검색어를 모아 `tools/ac.json`에 저장한다.
   - 이미 페이지 제목에 들어간 검색어는 뺀다.
   - '도시 + 작업' 모양(예: 청주 냉장고장 리폼 가격)이고 맞는 키워드 페이지가 없으면 `tools/daily.json`에 더한다 → 키워드 페이지가 된다.
   - 나머지 실제 검색어는 `tools/today_qa.txt`에 적는다 (많이 뜨는 순서, 여유분 포함). 출력의 "오늘 만들 질문·답변 최대" 개수만큼 만든다.
3. GEO: `tools/today_qa.txt`의 검색어 중 손님이 많이 찾는 순서로 최대 10개만, `tools/qa.json`에 질문·답변 1개를 더한다 (위에서부터, 최대 개수까지).
   - **질문(q)에 그 검색어를 글자 그대로 넣는다.** 예: 검색어 "키친핏 냉장고장 사이즈" → q "키친핏 냉장고장 사이즈는 어떻게 맞추나요?"
     (제목에 검색어가 들어가야 다음 날 중복으로 안 잡히고, 네이버에도 그 말로 뜬다.)
   - 답은 `tools/facts.md`에 있는 사실만. 가격·기간·보증·치수 규격을 지어내지 않는다. 모르면 "사진과 냉장고 모델명을 보내주시면 알려드려요".
   - facts.md로 정직하게 답할 수 없는 검색어(다른 업체 이름, 우리가 안 하는 일(싱크대 전체 교체·욕실 수전·붙박이장 등), 셀프 시공 요령, 치수 숫자만 다른 같은 말 등)는 건너뛰고 다음 줄로.
   - 형식: {"slug": 영문-소문자-하이픈(기존과 안 겹치게), "q": 질문, "a": 2~3문장 짧은 답, "more": [문단 1~3개], "fit": 작업 slug(partition, kitchenfit, bespoke, objet, custom, reform, kimchi, homebar, range, shoe, robot, pillar, noinstall, cost, movein, fourdoor, homecafe, make, demolish, install, pricing, side, fridgebar, storage, door, ttungnaeng, interior 중 하나), "kw": 관련 키워드 페이지(예: kw-daejeon-pricing, 있는 파일만)}
4. `python3 tools/build_pages.py` → 페이지·sitemap·new-urls.txt가 만들어진다. 오류가 나면 고치고 다시.
5. 바뀐 파일 전부 커밋하고 `git push origin main`. 배포가 끝나면 deploy-succeeded 함수가 새 주소를 네이버·빙(IndexNow)에 자동으로 알린다.
6. 몇 분 뒤 https://nemos-dream.com/api/t?idx 에서 urls 수와 200 응답을 확인한다.
7. 홈페이지 스레드에 쉬운 한국어로 짧게 보고: 몇 개 올렸는지, 대표 검색어 3~5개. 실제 검색어가 10개보다 적으면 적은 대로 솔직하게 말한다.

참고: 예전 방식(`tools/daily.py`, 동네 + 작업 조합)은 검색량이 거의 없어 쓰지 않는다.
