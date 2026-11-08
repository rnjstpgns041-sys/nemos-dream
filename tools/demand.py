# 매일 자동 추가(실제 검색어 기준).
# 1) 네이버 자동완성에 실제로 뜨는 검색어를 모은다 (tools/ac.json에 저장)
# 2) 이미 페이지 제목에 들어간 검색어는 뺀다
# 3) '도시 + 작업' 모양이면 키워드 페이지(daily.json), 나머지는 질문·답변 후보(tools/today_qa.txt)
# 사용: cd <저장소> && python3 tools/demand.py [최대개수=50] [질문최대=25]
import json, os, re, sys, time, urllib.parse, urllib.request
T = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith('--')]
N = int(args[0]) if args else 50
QMAX = int(args[1]) if len(args) > 1 else 25

def ac(q):
    u = ('https://ac.search.naver.com/nx/ac?q=' + urllib.parse.quote(q) +
         '&con=1&frm=nv&ans=2&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&run=2&rev=4&q_enc=UTF-8&st=100')
    for _ in range(3):
        try:
            return [x[0] for x in json.load(urllib.request.urlopen(u, timeout=10))['items'][0]]
        except Exception:
            time.sleep(2)
    return []

SEEDS = ['냉장고장', '키친핏 냉장고장', '비스포크 냉장고장', '오브제 냉장고장', '냉장고장 칸막이', '냉장고장 기둥',
         '냉장고장 리폼', '냉장고장 맞춤', '냉장고장 제작', '김치냉장고장', '김치냉장고 수납장', '냉장고 수납장',
         '냉장고 옆', '냉장고 틈새', '틈새장', '홈바장', '홈카페장', '렌지장', '밥솥장', '키큰장', '신발장 리폼',
         '신발장 오픈장', '로봇청소기장', '로봇청소기 수납장', '냉장고장 철거', '냉장고장 문', '냉장고장 홈바',
         '냉장고장 수납장', '냉장고 설치 안', '냉장고 안들어', '키친핏', '비스포크 키친핏', '4도어 냉장고장', '뚱냉',
         '냉장고장 인테리어', '냉장고장 시공', '냉장고장 가격', '빌트인 냉장고장', '냉장고장 옵션', '냉장고장 비용',
         '냉장고장 업체', '냉장고장 사이즈', '냉장고장 깊이', '냉장고 자리', '냉장고 들어갈 자리', '신축 냉장고장',
         '입주 냉장고장', '아파트 냉장고장', '냉장고장 리폼 비용', '냉장고장 리폼 후기', '냉장고장 칸막이 제거',
         '냉장고장 기둥 제거', '냉장고 설치 불가', '냉장고가 안 들어가요', '냉장고장 맞춤제작', '냉장고장 홈카페',
         '홈바장 제작', '홈바장 맞춤', '홈카페장 제작', '틈새장 제작', '틈새 수납장', '키큰장 제작', '밥솥장 제작',
         '렌지장 제작', '신발장 오픈장 리폼', '신발장 홈바', '현관 신발장 리폼', '로봇청소기 자리', '로봇청소기장 제작',
         '김치냉장고장 리폼', '김치냉장고 자리', '오브제 키친핏 냉장고장', '비스포크 4도어 냉장고장', '1+1+1 냉장고장',
         '냉장고 3대 냉장고장', '냉장고장 상부장', '상부장 처짐', '냉장고장 견적', '냉장고장 AS', '친환경 가구 E0',
         '주방 홈바', '거실 홈바장', '냉장고 옆 홈바', '냉장고 옆 틈새', '냉장고 사이 틈', '냉장고장 틈']
CITIES = ['대전', '세종', '천안', '아산', '청주', '홍성', '내포', '당진', '공주', '논산', '계룡', '서산', '예산',
          '보령', '진천', '충주', '오송', '오창', '유성', '둔산', '도안', '탕정', '불당']
for c in CITIES:
    SEEDS += [c + ' 냉장고장', c + ' 키친핏', c + ' 신발장', c + ' 홈바', c + ' 냉장고장 리폼', c + ' 냉장고장 제작']

# 우리 일과 관계있는 말이 있어야 하고, 안 하는 일·엉뚱한 말은 뺀다
NEED = ['냉장고장', '키친핏', '비스포크', '오브제', '칸막이', '틈새', '홈바', '신발장', '로봇청소기', '렌지장',
        '밥솥장', '김치냉장고', '냉장고 옆', '냉장고 수납', '뚱냉', '홈카페', '키큰장', '냉장고 자리', '냉장고 설치']
BLOCK = ['싱크대', '붙박이장', '막힘', '수전', '중고', '당근', '이케아', '오늘의집', '쿠팡', '다이소', '렌탈', '판매',
         '구매', '최저가', '할인', '도배', '마루', '장판', '에어컨', '세탁기', '건조기', '스타일러', '식기세척기',
         '청소', '고장', '수리', '숙소', '홈바운드', '리바트', '한샘', '젠우드', '트리니홈', '정리', '이동', '옮기', '커튼', '필름',
         '부산', '대구', '울산', '광주', '전주', '인천', '서울', '경기', '수원', '용인', '김포', '평택', '창원', '제주', '소음', '전기세', '용량', '추천 순위', '모델명', '단종', '내돈내산', '디시', '도면']

ac_path = T + '/ac.json'
data = {}
if '--cache' in sys.argv and os.path.exists(ac_path):
    data = json.load(open(ac_path)); SEEDS = []; lvl1 = []
for q in SEEDS:
    data[q] = ac(q); time.sleep(0.5)
if SEEDS: lvl1 = sorted({p for v in data.values() for p in v} - set(data))
for q in lvl1:                      # 한 단계 더 (예: '키친핏 냉장고장 사이즈' → '…사이즈 재는법')
    if any(w in q for w in NEED) and not any(b in q for b in BLOCK):
        data[q] = ac(q); time.sleep(0.5)
json.dump(data, open(ac_path, 'w'), ensure_ascii=False, indent=0)
phrases = sorted({p.strip() for v in data.values() for p in v})
# 가구 일을 찾는 말이어야 한다 (냉장고 자체를 사려는 검색은 뺀다)
WORK = ['장', '칸막이', '기둥', '리폼', '제작', '시공', '설치', '철거', '홈바', '자리', '맞춤', '인테리어', '문달기', '문짝']
phrases = [p for p in phrases if any(w in p for w in NEED) and not any(b in p.replace('냉장고장', '') for b in BLOCK) and len(p) >= 5
           and any(w in p.replace('냉장고', '') for w in WORK)]
# 많이 뜨는 검색어(여러 검색에서 반복해서 나온 말)부터
cnt = {}
for v in data.values():
    for i, p in enumerate(v): cnt[p] = cnt.get(p, 0) + 10 - min(i, 9)
CORE = ['냉장고장', '칸막이', '키친핏', '냉장고 자리', '냉장고 설치']
phrases.sort(key=lambda p: (not any(w in p for w in CORE), -cnt.get(p, 0)))
print('실제 검색어', len(phrases), '(자동완성 조회', len(data), '번)')
if not phrases:
    print('자동완성을 못 가져왔어요. 오늘은 만들지 않아요.'); sys.exit(0)

def norm(s): return re.sub(r'[\s·,.?!]', '', s)
titles = []
for f in os.listdir('.'):
    if f.endswith('.html'):
        h = open(f, encoding='utf-8').read(6000)
        m = re.search(r'<title>([^<|]*)', h)
        if m: titles.append(norm(m.group(1)))
qa = json.load(open(T + '/qa.json'))
titles += [norm(x['q']) for x in qa]
covered = lambda p: any(norm(p) in t for t in titles)

src = open(T + '/kw_pages.py').read()
kws = re.findall(r"^ ?\('([a-z]+)', '([^']+)', '[^']*', '(?:guide|fridge|x-)", src, re.M)
regs = re.findall(r"^ \('([a-z]+)', '([^']+)', '[a-z-]+', \(", src[src.index('KW_REGIONS = ['):src.index('HOODS2 = [')], re.M)
# 짧은 지역 이름도 받기 (예: '유성' → 대전 유성)
alias = {}
for slug, name in regs:
    alias[name] = slug
    alias[name.split()[-1]] = slug
alias['홍성'] = alias['내포'] = 'naepo'
kwmap = {norm(name): slug for slug, name, *_ in kws}
kwmap.update({norm('냉장고장 칸막이'): 'partition', norm('냉장고장 기둥'): 'pillar', norm('냉장고장 맞춤'): 'custom',
              norm('냉장고장 리폼 가격'): 'cost', norm('냉장고장 제작 비용'): 'pricing', norm('냉장고장 비용'): 'pricing',
              norm('키친핏'): 'kitchenfit', norm('홈바'): 'homebar', norm('신발장'): 'shoe', norm('냉장고장 수납'): 'storage'})

dj = T + '/daily.json'
done = json.load(open(dj)) if os.path.exists(dj) else []
seen = {'%s-%s' % tuple(x) for x in done} | {f[3:-5] for f in os.listdir('.') if f.startswith('kw-')}
kwpick, qpick = [], []
for p in phrases:
    if covered(p): continue
    city = next((c for c in sorted(alias, key=len, reverse=True) if p.startswith(c + ' ')), None)
    if city:
        rest = norm(p[len(city):])
        k = kwmap.get(rest)
        if k:
            combo = '%s-%s' % (alias[city], k)
            if combo not in seen and [alias[city], k] not in kwpick:
                kwpick.append([alias[city], k])
            continue
    qpick.append(p)
kwpick = kwpick[:N]
qmax = max(0, min(QMAX, N - len(kwpick)))
qpick = qpick[:qmax + 15]   # 답할 수 없는 말은 건너뛸 수 있게 여유분
print('오늘 만들 질문·답변 최대', qmax)
json.dump(done + kwpick, open(dj, 'w'), ensure_ascii=False, indent=0)
open(T + '/today_qa.txt', 'w').write('\n'.join(qpick) + ('\n' if qpick else ''))
print('키워드 페이지', len(kwpick), kwpick)
print('질문·답변 후보', len(qpick))
print('\n'.join(qpick))
