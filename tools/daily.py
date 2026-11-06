# 매일 자동 추가: 아직 없는 '동네 + 작업' 조합을 N개 골라 daily.json에 더한다. 그다음 build_pages.py로 페이지를 만든다.
# 사용: cd <저장소> && python3 tools/daily.py 45 && python3 tools/build_pages.py
import json, os, re, sys
T = os.path.dirname(os.path.abspath(__file__))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 45
src = open(T + '/kw_pages.py').read()
g = {}
exec(src[src.index('HOODS2 = ['):src.index('# 가이드 페이지가 없는 작업용 설명 묶음')].replace('KW_REGIONS += HOODS2', ''), g)
allreg = re.findall(r"^ \('([a-z]+)', '[^']+', '[a-z-]+', \(", src[src.index('KW_REGIONS = ['):src.index('HOODS2 = [')], re.M)
allkw = re.findall(r"^ ?\('([a-z]+)', '[^']+', '[^']*', '(?:guide|fridge|x-)", src, re.M)
have = {f[3:-5] for f in os.listdir('.') if f.startswith('kw-') and f.endswith('.html')}
dj = T + '/daily.json'
done = json.load(open(dj)) if os.path.exists(dj) else []
seen = have | {'%s-%s' % tuple(x) for x in done}
queue = [(r[0], k) for k in g['DAILY_KORDER'] for r in g['HOODS2']]
queue += [(r, k) for r in allreg for k in allkw]
pick = []
for r, k in queue:
    if '%s-%s' % (r, k) not in seen and (r, k) not in pick:
        pick.append((r, k))
    if len(pick) >= N: break
json.dump(done + [list(x) for x in pick], open(dj, 'w'), ensure_ascii=False, indent=0)
print('added', len(pick), 'left', len([1 for r, k in queue if '%s-%s' % (r, k) not in seen]) - len(pick))
