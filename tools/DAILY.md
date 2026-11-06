# 매일 자동 작업 (예약 실행용 안내)

매일 한 번 아래를 한다. 사람에게 묻지 않고 끝까지 한다.

1. `git pull origin main`
2. `python3 tools/daily.py 45` → 아직 없는 '동네 + 작업' 키워드 페이지 45개를 고른다.
3. `tools/qa.json`에 새 질문·답변 5개를 더한다.
   - 손님이 네이버·ChatGPT에 실제로 물어볼 만한 질문 한 문장 (예: "세종 신축 아파트 냉장고장 칸막이 제거 얼마예요?")
   - 기존 질문과 겹치지 않게 (slug와 q가 달라야 함)
   - 답은 `tools/facts.md`에 있는 사실만. 가격·기간·보증을 지어내지 않는다.
   - 형식: {"slug": 영문-소문자-하이픈, "q": 질문, "a": 2~3문장 짧은 답, "more": [문단 1~3개], "fit": 작업 slug(partition, kitchenfit, bespoke, objet, custom, reform, kimchi, homebar, range, shoe, robot, pillar, noinstall, cost, movein, fourdoor, homecafe, make, demolish, install, pricing, side, fridgebar, storage, door, ttungnaeng, interior 중 하나), "kw": 관련 키워드 페이지 이름(예: kw-sejong-partition, 있는 파일만)}
4. `python3 tools/build_pages.py` → 페이지·sitemap·new-urls.txt가 만들어진다. 오류가 나면 고치고 다시.
5. 바뀐 파일 전부 커밋하고 `git push origin main`. 배포가 끝나면 deploy-succeeded 함수가 새 주소를 네이버·빙(IndexNow)에 자동으로 알린다.
6. 몇 분 뒤 https://nemos-dream.com/api/t?idx 에서 urls 수와 200 응답을 확인한다.
