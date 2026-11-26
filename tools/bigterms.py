# 많이 찾는 큰 검색어 추적 (2026-11-26 사용자 결정: 앞으로는 많이 찾는 검색어 위주)
# 1) 네이버 자동완성 상위어를 큰 씨앗어에서 모은다 (지역 없는 말 + 충청 큰 도시 말)
# 2) 휴대폰 네이버 첫 화면에 웹사이트 칸이 있는지, nemos-dream.com 이 나오는지, 어떤 사이트가 나오는지 기록
# 사용: python3 tools/bigterms.py  → tools/bigterms.json (날짜별 기록 누적), 요약 출력
import json, os, re, time, urllib.parse, urllib.request, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS = ['냉장고장', '냉장고장 칸막이', '키친핏 냉장고장', '냉장고장 리폼', '냉장고장 제작', '비스포크 냉장고장',
         '김치냉장고장', '오브제 냉장고장', '대전 냉장고장', '세종 냉장고장', '천안 냉장고장', '청주 냉장고장', '아산 냉장고장']
SKIP = ('셀프', '장난감', '장기보관', '무게', '부산', '대구', '인천', '광주', '전주', '서울', '경기', '수원', '창원', '울산')
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148'
NAV = ('naver', 'pstatic', 'navercorp', 'w3.org', 'schema.org')
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=25).read().decode('utf-8', 'ignore')
def ac(s):
    u = 'https://ac.search.naver.com/nx/ac?q=' + urllib.parse.quote(s) + '&con=1&frm=nv&ans=2&r_format=json&r_enc=UTF-8&r_unicode=0&t_koreng=1&run=2&rev=4&q_enc=UTF-8&st=100'
    try: return [i[0] for i in json.loads(get(u))['items'][0]]
    except Exception: return []
terms = []
for s in SEEDS:
    for t in ac(s)[:6]:
        if '냉장고' in t and not any(k in t for k in SKIP) and t not in terms: terms.append(t)
    time.sleep(0.5)
rows = []
for t in terms:
    try: h = get('https://m.search.naver.com/search.naver?query=' + urllib.parse.quote(t))
    except Exception: continue
    sites = []
    for m in re.finditer(r'href="https?://([^"/]+)(/[^"]*)?"', h):
        d = m.group(1)
        if any(x in d for x in NAV): continue
        u = d + (m.group(2) or '/')
        if 'youtube' in d or 'ohou.se' in d: continue
        if not any(u.split('/')[0] == x.split('/')[0] for x in sites): sites.append(u[:90])
    rows.append({'q': t, 'web': bool(sites), 'nemos': 'nemos-dream.com' in h, 'blog_ours': ('zibaejang' in h or 'soorigome' in h), 'sites': sites[:6]})
    time.sleep(1)
p = os.path.join(HERE, 'bigterms.json')
hist = json.load(open(p)) if os.path.exists(p) else {}
hist[datetime.date.today().isoformat()] = rows
json.dump(hist, open(p, 'w'), ensure_ascii=False, indent=1)
print('큰 검색어', len(rows), '| 웹사이트 칸 있음', sum(r['web'] for r in rows), '| 홈페이지 나옴', sum(r['nemos'] for r in rows), '| 우리 블로그 나옴', sum(r['blog_ours'] for r in rows))
for r in rows: print(('★' if r['nemos'] else ' '), ('웹' if r['web'] else '  '), ('블' if r['blog_ours'] else '  '), r['q'], r['sites'][:3])
