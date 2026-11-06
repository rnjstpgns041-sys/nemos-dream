# 지역 + 검색어 페이지 50개(kw-<지역>-<작업>.html): 10개 지역 x 5개 작업.
# 지역 소개는 AREAS/SUBS에서, 작업 설명·순서·질문은 GUIDES와 아래 KWS에서 가져와 섞는다. build_detail.py가 exec로 부른다.
GD = {g[0]: g for g in GUIDES}
AINTRO = {a[0]: a[3] for a in AREAS}; AINTRO.update({x[0]: x[4] for x in SUBS})
ANAME2 = {a[0]: a[1] for a in AREAS}; ANAME2.update({x[0]: x[1] for x in SUBS})

KJOB = {k: '냉장고장 새로 제작' for k in ('kitchenfit', 'custom', 'make', 'install')}
KJOB.update({k: '홈바장·수납장' for k in ('homebar', 'homecafe', 'fridgebar', 'storage', 'side')})
KJOB.update({'shoe': '신발장 리폼', 'robot': '로봇청소기장·밥솥장', 'range': '로봇청소기장·밥솥장'})
def qarea(aslug, rn):
    if aslug.startswith('daejeon'): return '대전'
    if aslug == 'sejong': return '세종'
    if aslug in ('cheonan', 'chungnam-asan'): return '천안·아산'
    if aslug in ('cheongju', 'chungbuk-ochang', 'chungbuk-osong'): return '청주'
    if aslug == 'hongseong': return '홍성·내포'
    return rn
KW_REGIONS = [  # (slug, 검색에 쓰는 이름, 지역 페이지 slug, 지역 사례를 고를 글자들)
 ('daejeon', '대전', 'daejeon', ('대전',)),
 ('sejong', '세종', 'sejong', ('세종',)),
 ('cheonan', '천안', 'cheonan', ('천안',)),
 ('asan', '아산', 'chungnam-asan', ('아산',)),
 ('cheongju', '청주', 'cheongju', ('청주',)),
 ('naepo', '내포 홍성', 'hongseong', ('홍성', '내포')),
 ('yuseong', '대전 유성', 'daejeon-yuseong', ('유성',)),
 ('dunsan', '대전 둔산', 'daejeon-seogu', ('서구', '둔산')),
 ('ochang', '청주 오창', 'chungbuk-ochang', ('오창',)),
 ('dangjin', '당진', 'chungnam-dangjin', ('당진',)),
 ('gongju', '공주', 'chungnam-gongju', ('공주',)),
 ('nonsan', '논산', 'chungnam-nonsan', ('논산',)),
 ('gyeryong', '계룡', 'chungnam-gyeryong', ('계룡',)),
 ('seosan', '서산', 'chungnam-seosan', ('서산',)),
 ('yesan', '예산', 'chungnam-yesan', ('예산', '내포')),
 ('boryeong', '보령', 'chungnam-boryeong', ('보령',)),
 ('jincheon', '진천', 'chungbuk-jincheon', ('진천',)),
 ('chungju', '충주', 'chungbuk-chungju', ('충주',)),
 ('osong', '청주 오송', 'chungbuk-osong', ('오송',)),
 ('daedeok', '대전 대덕', 'daejeon-daedeok', ('대덕',)),
 ('doan', '대전 도안', 'daejeon-yuseong', ('도안',)),
 ('tangjeong', '아산 탕정', 'chungnam-asan', ('탕정',)),
 ('buldang', '천안 불당', 'cheonan', ('불당',)),
 ('junggu', '대전 중구', 'daejeon-junggu', ('중구', '선화', '중촌')),
 ('donggu', '대전 동구', 'daejeon-donggu', ('동구',)),
]
# 매일 자동 추가용 동네 (2026-11-06~): 신축·입주 많은 동네
HOODS2 = [
 ('noeun', '대전 노은', 'daejeon-yuseong', ('노은',)), ('gwanjeo', '대전 관저', 'daejeon-seogu', ('관저',)),
 ('gasuwon', '대전 가수원', 'daejeon-seogu', ('가수원',)), ('tanbang', '대전 탄방', 'daejeon-seogu', ('탄방',)),
 ('yongmun', '대전 용문동', 'daejeon-seogu', ('용문',)), ('gapcheon', '대전 갑천지구', 'daejeon-seogu', ('갑천',)),
 ('hakha', '대전 학하', 'daejeon-yuseong', ('학하',)), ('bongmyeong', '대전 봉명동', 'daejeon-yuseong', ('봉명',)),
 ('jijok', '대전 지족동', 'daejeon-yuseong', ('지족',)), ('yongsan', '대전 용산동', 'daejeon-yuseong', ('용산',)),
 ('seonhwa', '대전 선화동', 'daejeon-junggu', ('선화',)), ('jungchon', '대전 중촌동', 'daejeon-junggu', ('중촌',)),
 ('daeheung', '대전 대흥동', 'daejeon-junggu', ('대흥',)),
 ('naseong', '세종 나성동', 'sejong', ('나성',)), ('dajeong', '세종 다정동', 'sejong', ('다정',)),
 ('goun', '세종 고운동', 'sejong', ('고운',)), ('bangok', '세종 반곡동', 'sejong', ('반곡',)),
 ('boram', '세종 보람동', 'sejong', ('보람',)), ('saerom', '세종 새롬동', 'sejong', ('새롬',)),
 ('haemil', '세종 해밀동', 'sejong', ('해밀',)), ('sanul', '세종 산울동', 'sejong', ('산울',)),
 ('jochiwon', '세종 조치원', 'sejong', ('조치원',)),
 ('sinbang', '천안 신방동', 'cheonan', ('신방',)), ('cheongdang', '천안 청당동', 'cheonan', ('청당',)),
 ('baekseok', '천안 백석동', 'cheonan', ('백석',)), ('dujeong', '천안 두정동', 'cheonan', ('두정',)),
 ('seongseong', '천안 성성동', 'cheonan', ('성성',)),
 ('baebang', '아산 배방', 'chungnam-asan', ('배방',)), ('mojong', '아산 모종동', 'chungnam-asan', ('모종',)),
 ('yonghwa', '아산 용화동', 'chungnam-asan', ('용화',)),
 ('gagyeong', '청주 가경동', 'cheongju', ('가경',)), ('dongnam', '청주 동남지구', 'cheongju', ('동남',)),
 ('techno', '청주 테크노폴리스', 'cheongju', ('테크노',)), ('bokdae', '청주 복대동', 'cheongju', ('복대', '지웰')),
 ('yullyang', '청주 율량동', 'cheongju', ('율량',)), ('bangseo', '청주 방서동', 'cheongju', ('방서',)),
]
KW_REGIONS += HOODS2
# 매일 순서: 동네별로 많이 찾는 작업부터
DAILY_KORDER = ['partition', 'kitchenfit', 'bespoke', 'objet', 'custom', 'reform', 'noinstall', 'movein', 'cost', 'kimchi', 'pillar', 'fourdoor', 'pricing', 'make', 'install', 'homebar', 'side', 'robot', 'range', 'shoe']

# 가이드 페이지가 없는 작업용 설명 묶음: (링크 slug, 이름, -, -, -, -, 특징, 순서, -, 질문)
GD['x-homebar'] = ('services', '홈바장·수납장', '', '', '', '',
  [('빈 벽을 포인트로', 'LED 간접 조명과 유리문 진열장으로 거실이나 주방 벽에 포인트를 만들어요.'), ('냉장고장과 한 세트', '냉장고장 옆 남는 폭에 같은 자재와 색으로 홈바장을 이어서 짜요.'), ('콘센트·조명 배선', '커피머신, 전자레인지 쓸 자리를 생각해 콘센트와 조명 위치를 같이 잡아요.'), ('E0 친환경 자재', '포름알데히드 방출량 0.5mg/L 이하인 E0 등급 자재로 짜요.')],
  [('사진·치수 문자', '놓을 자리 사진과 대략적인 폭을 문자로 보내 주세요.'), ('실측과 디자인', '현장을 재고 조명, 유리문, 선반 구성을 정해요.'), ('사전 제작', '치수대로 미리 재단해 가서 현장 작업 시간을 줄여요.'), ('설치와 조명', '수평을 잡고 설치한 뒤 조명까지 켜서 확인해요.')], None,
  [('홈바장 비용은 얼마인가요?', '디자인 홈바장은 100만원부터예요(VAT 별도). 크기, 조명, 유리문 같은 구성에 따라 달라져요.'), ('냉장고장이랑 같이 짤 수 있나요?', '네. 같은 자재와 색으로 한 번에 짜면 라인이 맞아서 더 깔끔해요.')])
GD['x-range'] = ('services', '렌지장·밥솥장', '', '', '', '',
  [('남는 폭 활용', '냉장고를 넣고 남는 폭에 전자레인지, 밥솥, 에어프라이어 자리를 만들어요.'), ('슬라이드 선반', '밥솥은 김이 빠지게 앞으로 당겨 쓰는 슬라이드 선반으로 짜요.'), ('콘센트 위치', '가전 쓸 자리에 맞춰 콘센트 위치를 미리 잡아요.'), ('E0 친환경 자재', '포름알데히드 방출량 0.5mg/L 이하인 E0 등급 자재로 짜요.')],
  [('가전·사진 문자', '넣을 가전 종류와 자리 사진을 문자로 보내 주세요.'), ('실측과 설계', '가전 크기와 열이 빠질 틈까지 계산해 설계해요.'), ('사전 제작', '치수대로 미리 재단해 가서 현장 작업을 줄여요.'), ('설치와 확인', '설치 후 슬라이드 선반과 문이 잘 움직이는지 함께 확인해요.')], None,
  [('렌지장·밥솥장만 따로 짤 수 있나요?', '네. 냉장고장 옆 남는 폭이나 빈 벽에 따로 짤 수 있어요. 사진을 보내 주시면 금액을 알려드려요.'), ('밥솥 김 때문에 장이 상하지 않나요?', '앞으로 당겨 쓰는 슬라이드 선반으로 짜서 김이 장 안에 차지 않게 해요.')])
GD['x-shoe'] = ('services', '신발장 리폼', '', '', '', '',
  [('프레임은 그대로', '신발장 틀은 살리고 문짝과 내부만 바꿔서 비용과 시간을 줄여요.'), ('중간 오픈장', '가운데를 열린 칸으로 바꿔 키, 지갑, 소품을 올려 두는 자리를 만들어요.'), ('LED 홈바', '오픈장 안에 간접 조명을 넣어 현관 분위기를 바꿔요.'), ('하루 시공', '대부분 하루 안에 끝나요.')],
  [('사진 문자', '현관 신발장 사진을 문자로 보내 주세요.'), ('구성 정하기', '오픈장 위치, 조명, 선반 수를 정해요.'), ('사전 제작', '문짝과 내부 자재를 미리 재단해 가요.'), ('설치와 마감', '문짝과 오픈장을 달고 조명까지 확인해요.')], None,
  [('신발장 리폼 비용은 얼마인가요?', '구성에 따라 달라서 사진을 보고 알려드려요. 프레임을 살리는 리폼이라 새로 짜는 것보다 부담이 적어요.'), ('신발장 전체를 바꿔야 하나요?', '아니요. 틀은 그대로 두고 가운데 칸이나 문짝만 바꾸는 경우가 많아요.')])

GD['x-robot'] = ('services', '로봇청소기장', '', '', '', '',
  [('스테이션 자리 맞춤', '로봇청소기 스테이션 높이와 폭을 재서 문을 닫아도 쏙 들어가게 짜요.'), ('스스로 드나드는 바닥', '서랍 레일을 빼고 바닥 높이를 맞춰서 청소기가 혼자 나갔다 들어올 수 있게 해요.'), ('하부장·냉장고장 옆 활용', '잘 안 쓰는 하부장 한 칸이나 냉장고장 옆 남는 폭을 청소기 자리로 바꿔요.'), ('주방 가구와 같은 색', '문짝 색을 주방 가구에 맞춰서 원래 있던 장처럼 보여요.')],
  [('사진·모델 문자', '놓을 자리 사진과 로봇청소기 모델명을 문자로 보내 주세요.'), ('치수 확인', '스테이션 크기와 문 여닫는 방향을 확인해요.'), ('사전 제작', '내부와 문짝을 미리 재단해 가요.'), ('설치와 확인', '설치한 뒤 청소기가 잘 드나드는지 직접 돌려 봐요.')], None,
  [('로봇청소기장 비용은 얼마인가요?', '자리와 구성에 따라 달라서 사진을 보고 알려드려요. 냉장고장을 짜면서 같이 만들면 따로 하는 것보다 부담이 적어요.'), ('스테이션이 큰 모델도 들어가나요?', '모델명을 알려주시면 스테이션 높이와 폭에 맞춰 칸을 짜요.')])

GD['x-cost'] = ('price', '비용', '', '', '', '',
  [('칸막이·기둥 제거 30만원', '걸리는 칸막이나 기둥만 빼고 상부장과 천장을 보강해요. 마감과 폐자재 처리까지 포함이에요.'), ('새로 짜기 100만원부터', '냉장고 모델에 맞춰 냉장고장을 새로 짜요. 크기와 구성에 따라 달라져요.'), ('홈바장 100만원부터', 'LED 조명, 유리문 같은 구성에 따라 달라져요.'), ('사진 보고 금액 안내', '시공 전에 사진을 보고 먼저 금액을 알려드려요. 모두 VAT 별도예요.')],
  [('사진 문자', '냉장고장 사진과 냉장고 모델명을 문자로 보내 주세요.'), ('금액 안내', '사진을 보고 리폼인지 새로 짜기인지, 금액이 얼마인지 알려드려요.'), ('일정 잡기', '냉장고 배송일에 맞춰 시공 날짜를 정해요.'), ('시공과 마감', '대표가 직접 시공하고 마감까지 확인해요.')], None,
  [('왜 업체마다 금액이 다른가요?', '보강을 하는지, 마감과 폐자재 처리가 포함인지에 따라 달라요. 저희 30만원에는 보강, 마감, 폐자재 처리가 다 들어가요.')])

FIT = lambda w: w['f'] == 'fridge'
KWS = [  # (slug, 검색어, 제목 뒤 문구, 가이드 slug, 가격 문구, 사례 고르기, 이 작업만의 설명, 추가 질문)
 ('partition', '냉장고장 칸막이 제거', '30만원 · 대부분 하루 시공', 'guide-partition', '칸막이·기둥 제거 리폼 30만원 (VAT 별도, 보강·마감·폐자재 처리 포함)',
  GD['guide-partition'][8], '옵션 냉장고장 가운데 칸막이 때문에 새 냉장고가 안 들어갈 때 장 전체를 뜯을 필요는 없어요. 걸리는 칸막이만 빼고, 받치던 무게만큼 상부장과 천장을 보강해요.',
  [('칸막이를 빼면 상부장이 처지지 않나요?', '칸막이가 받치던 무게만큼 상부장과 천장을 2단으로 보강해요. 처짐·기울어짐은 평생 무상 AS예요.')]),
 ('kitchenfit', '키친핏 냉장고장', '모델 맞춤 제작 · 시공 사례', 'guide-kitchenfit', '키친핏 냉장고장 맞춤제작 100만원부터 (VAT 별도)',
  GD['guide-kitchenfit'][8], '키친핏 냉장고는 장과 1cm 정도만 띄워서 넣어야 일체형처럼 보여요. 그래서 냉장고 모델의 설치 가이드 치수에 맞춰 높이, 깊이, 도어 두께까지 맞춰 짜요.',
  [('키친핏 냉장고장은 냉장고를 사고 나서 맞추나요?', '네. 모델마다 치수가 달라서 냉장고 모델을 먼저 정하고, 그 설치 가이드에 맞춰 짜는 게 안전해요.')]),
 ('bespoke', '비스포크 냉장고장', '설치 불가 해결 · 맞춤제작', 'fridge-bespoke', '기둥 제거 리폼 30만원, 새로 짜기 100만원부터 (VAT 별도)',
  lambda w: FIT(w) and ('비스포크' in fr(w) or '비스포크' in w['t'] or '키친핏' in w['t']), '삼성 비스포크 키친핏을 옵션 냉장고장에 넣으려다 설치 불가를 듣는 집이 많아요. 기둥을 빼서 자리를 만들거나, 무옵션 세대라면 비스포크 설치 가이드에 맞춰 장을 새로 짜요.',
  [('비스포크 설치 기사님이 설치 불가라고 했어요.', '대부분 냉장고장 가운데 기둥이나 깊이 때문이에요. 냉장고 모델명과 장 사진을 보내 주시면 기둥 제거로 될지, 새로 짜야 할지 알려드려요.')]),
 ('objet', '오브제 냉장고장', '1+1+1 기둥 제거 · 맞춤제작', 'fridge-objet', '기둥 제거 리폼 30만원, 새로 짜기 100만원부터 (VAT 별도)',
  lambda w: FIT(w) and ('오브제' in fr(w) or '오브제' in w['t'] or '칸막이' in w['t'] or '기둥' in w['t']), 'LG 오브제 1+1+1처럼 여러 대를 나란히 넣는 냉장고는 옵션 냉장고장 가운데 기둥에 걸려 붙지 않는 경우가 많아요. 기둥을 빼고 보강해서 나란히 붙게 만들어요.',
  [('오브제 1+1+1이 다 들어갈까요?', '모델 조합에 따라 필요한 폭이 달라요. 모델명을 알려주시면 기둥을 빼고 몇 cm가 확보되는지 계산해서 알려드려요.')]),
 ('custom', '냉장고장 맞춤제작', '100만원부터 · 대표 직접 시공', 'guide-kitchenfit', '냉장고장 맞춤제작 100만원부터, 홈바장·렌지장 추가 가능 (VAT 별도)',
  lambda w: w['no'] in ('223833108339', '224277045640', '224432139660', '223906771954', '224176609693', '223831173880'), '무옵션으로 입주했거나 옵션 장이 마음에 안 들 때, 냉장고 모델에 맞춰 냉장고장을 처음부터 짜요. 남는 폭에는 홈바장, 렌지장, 밥솥장, 로봇청소기장을 함께 넣을 수 있어요.',
  [('냉장고장 옆에 홈바장도 같이 짤 수 있나요?', '네. 같은 자재와 색으로 맞춰서 한 번에 짜요. 냉장고 옆 틈에 홈카페장을 만든 현장도 있어요.')]),
 ('reform', '냉장고장 리폼', '다 뜯지 않고 필요한 곳만 · 30만원부터', 'guide-partition', '부분 리폼 30만원부터 (VAT 별도)',
  lambda w: FIT(w) or w['no'] in ('224432139660',), '냉장고장을 다 뜯고 새로 짤 필요 없이, 칸막이·기둥 제거나 상부장 재사용처럼 필요한 부분만 바꿔서 새 냉장고 자리를 만들어요. 남는 폭은 수납장이나 밥솥장으로 채워요.',
  [('냉장고장 리폼과 새로 짜는 것 중 뭐가 나아요?', '프레임과 상부장이 멀쩡하면 리폼이 비용과 시간이 적게 들어요. 깊이나 높이가 안 맞으면 새로 짜는 게 나아요. 사진을 보고 알려드려요.')]),
 ('kimchi', '김치냉장고장', '냉장고+김치냉장고 자리 · 맞춤제작', 'guide-partition', '칸막이 제거 30만원, 새로 짜기 100만원부터 (VAT 별도)',
  lambda w: w['no'] in ('223843274881', '223828245418', '224277045640') or FIT(w), '냉장고와 김치냉장고를 나란히 넣는 냉장고장은 가운데 칸막이 위치가 새 냉장고와 안 맞는 경우가 많아요. 칸막이를 옮기거나 빼서 두 대가 딱 맞게 들어가게 해요.',
  [('김치냉장고 자리만 따로 만들 수 있나요?', '네. 냉장고장 옆이나 남는 폭에 김치냉장고 크기에 맞춰 칸을 만들 수 있어요. 모델명을 알려주세요.')]),
 ('homebar', '홈바장 맞춤제작', 'LED 조명·유리문 · 100만원부터', 'x-homebar', '디자인 홈바장 100만원부터 (VAT 별도)',
  lambda w: w['f'] == 'bar' or w['no'] in ('224176609693', '224277045640'), '거실이나 주방 빈 벽, 냉장고장 옆 남는 폭에 LED 조명과 유리문을 넣은 홈바장을 맞춰 짜요. 커피머신이나 와인잔을 둘 자리까지 같이 설계해요.',
  [('홈바장에 조명을 넣을 수 있나요?', '네. LED 간접 조명을 넣어 밤에 켜 두면 분위기가 확 살아요.')]),
 ('range', '렌지장 밥솥장', '남는 폭에 가전 자리 · 맞춤제작', 'x-range', '사진을 보고 금액 안내 (냉장고장과 함께 짜면 100만원부터, VAT 별도)',
  lambda w: w['no'] in ('224432139660', '224277045640', '224439467559', '224176609693') or FIT(w), '냉장고를 넣고 남는 폭이나 빈 벽에 전자레인지, 밥솥, 에어프라이어를 넣는 장을 맞춰 짜요. 밥솥은 김이 빠지게 당겨 쓰는 슬라이드 선반으로 만들어요.',
  [('냉장고장 리폼하면서 밥솥장도 같이 할 수 있나요?', '네. 대전 현장에서 칸막이를 철거하고 남는 폭에 밥솥장을 만든 적이 있어요.')]),
 ('shoe', '신발장 리폼', '중간 오픈장·LED 홈바 · 하루 시공', 'x-shoe', '사진을 보고 금액 안내 (VAT 별도)',
  lambda w: w['no'] in ('224285887538', '223917629832', '223851396466'), '현관 붙박이 신발장 틀은 그대로 두고, 가운데를 오픈장으로 바꾸거나 LED 조명 홈바장으로 바꿔요. 대부분 하루 안에 끝나요.',
  [('신발장 수납이 줄지 않나요?', '오픈장 위아래 칸은 그대로 신발장으로 쓰고, 가운데 한 칸만 오픈장으로 바꾸는 경우가 많아서 수납은 크게 줄지 않아요.')]),
 ('robot', '로봇청소기장', '스테이션 자리 맞춤 · 사진 견적', 'x-robot', '사진을 보고 금액 안내 (냉장고장과 함께 짜면 100만원부터, VAT 별도)',
  lambda w: w['no'] in ('223836523971', '224271127551', '223833108339'), '로봇청소기 스테이션이 거실이나 주방에 그대로 나와 있으면 자리도 차지하고 눈에 띄어요. 하부장 한 칸이나 냉장고장 옆 남는 폭을 청소기 전용 칸으로 바꿔서, 문을 닫아도 청소기가 스스로 드나들게 만들어요.',
  [('아일랜드 식탁 아래에도 만들 수 있나요?', '네. 아일랜드 하부장 서랍을 빼고 청소기가 드나드는 칸으로 바꾼 현장이 있어요.')]),
 ('pillar', '냉장고장 기둥 제거', '1+1+1·4도어 자리 만들기 · 30만원', 'fridge-objet', '칸막이·기둥 제거 리폼 30만원 (VAT 별도)',
  lambda w: FIT(w) and ('기둥' in w['t'] or '1+1+1' in fr(w) or '오브제' in w['t']), '옵션 냉장고장 가운데 세로 기둥 때문에 냉장고 두세 대를 나란히 못 넣는 경우가 많아요. 기둥만 빼고 상부장을 보강하면 1+1+1이나 4도어 냉장고가 들어갈 폭이 나와요. 장 전체를 새로 짤 필요가 없어요.',
  [('기둥을 빼도 상부장이 안전한가요?', '기둥이 받치던 무게만큼 상부장과 천장을 보강해요. 처짐·기울어짐은 평생 무상 AS예요.')]),
 ('noinstall', '냉장고 설치 불가', '냉장고장 때문에 안 들어갈 때 · 30만원부터', 'guide-partition', '칸막이·기둥 제거 30만원, 새로 짜기 100만원부터 (VAT 별도)',
  FIT, '새 냉장고 배송 날 기사님이 "설치 불가"라고 하는 이유는 대부분 냉장고장의 칸막이, 기둥, 깊이 때문이에요. 냉장고 모델명과 장 사진만 보내 주시면 칸막이만 빼면 되는지, 장을 새로 짜야 하는지 바로 알려드려요.',
  [('배송 날짜가 잡혀 있는데 그 전에 될까요?', '칸막이·기둥 제거는 대부분 하루면 끝나요. 날짜를 알려주시면 배송 전에 맞춰 일정을 잡아 드려요.')]),
 ('cost', '냉장고장 리폼 비용', '칸막이 제거 30만원 · 새로 짜기 100만원부터', 'x-cost', '칸막이·기둥 제거 30만원, 새로 짜기 100만원부터 (VAT 별도)',
  FIT, '냉장고장 리폼 비용은 무엇을 하느냐에 따라 크게 달라요. 걸리는 칸막이나 기둥만 빼는 리폼은 30만원이고, 냉장고 모델에 맞춰 장을 새로 짜면 100만원부터예요. 사진만 보내 주시면 어느 쪽인지, 금액이 얼마인지 먼저 알려드려요.',
  [('30만원에 뭐가 포함돼요?', '칸막이·기둥 제거, 상부장과 천장 보강, 바닥·벽 마감, 폐자재 처리까지 다 포함이에요(VAT 별도).')]),
 ('movein', '입주 냉장고장', '신축 입주 전 냉장고 자리 만들기', 'guide-kitchenfit', '칸막이 제거 30만원, 새로 짜기 100만원부터 (VAT 별도)',
  lambda w: FIT(w) and ('신축' in w['t'] or '신축' in (CASES[w['no']].get('title') or '') or w['no'] in ('223833108339', '223830329933', '224271127551', '223845410630')), '신축 아파트 옵션 냉장고장은 일반 양문형 냉장고에 맞춰져 있어서, 새로 산 키친핏이나 1+1+1 냉장고가 안 들어가는 경우가 많아요. 입주 전에 냉장고 모델명만 알려주시면 칸막이만 빼면 되는지, 무옵션이라 새로 짜야 하는지 알려드리고 입주 날짜에 맞춰 시공해요.',
  [('입주 전에 시공할 수 있나요?', '네. 입주 청소나 사전 점검 날처럼 집에 들어갈 수 있는 날에 맞춰 시공하는 경우가 많아요.')]),
 ('fourdoor', '4도어 냉장고장', '비스포크·오브제 4도어 자리 · 30만원부터', 'guide-kitchenfit', '칸막이·기둥 제거 30만원, 새로 짜기 100만원부터 (VAT 별도)',
  lambda w: FIT(w) and ('비스포크' in fr(w) or '오브제' in fr(w) or '키친핏' in w['t']), '4도어 냉장고는 양문형보다 폭과 깊이가 달라서 옵션 냉장고장에 안 맞는 경우가 많아요. 칸막이나 기둥만 빼서 자리를 넓힐지, 모델 설치 가이드에 맞춰 새로 짤지 사진을 보고 알려드려요.',
  [('4도어 냉장고와 김치냉장고를 같이 넣을 수 있나요?', '네. 두 모델의 폭을 합쳐서 칸을 다시 나눠요. 모델명을 알려주시면 들어가는지 먼저 계산해 드려요.')]),
 ('homecafe', '홈카페장', '커피머신·가전 자리 · 냉장고장 옆 맞춤', 'x-homebar', '디자인 홈바장 100만원부터, 냉장고장과 함께 짜면 사진 보고 안내 (VAT 별도)',
  lambda w: w['no'] in ('224277045640', '224176609693', '223831173880', '224432139660'), '냉장고장 옆 남는 폭이나 주방 빈 벽에 커피머신, 전기포트, 컵을 한곳에 두는 홈카페장을 맞춰 짜요. 냉장고장을 리폼하면서 같은 자재와 색으로 함께 만들면 원래 있던 장처럼 이어져요.',
  [('냉장고장 리폼하면서 홈카페장도 같이 만들 수 있나요?', '네. 대전 현장에서 냉장고장 리폼과 함께 홈카페장을 추가한 적이 있어요.')]),
 ('make', '냉장고장 제작', '냉장고 모델 맞춤 · 100만원부터', 'guide-kitchenfit', '냉장고장 제작 100만원부터, 칸막이 제거 리폼 30만원 (VAT 별도)',
  lambda w: w['no'] in ('223833108339', '223906771954', '224176609693', '223831173880') or FIT(w), '냉장고장 제작은 냉장고를 먼저 정하고, 그 모델의 설치 가이드에 맞춰 높이, 깊이, 도어 두께까지 계산해서 짜는 게 기본이에요. 대표가 직접 재고, 미리 재단해 가서 현장에서는 설치와 마감에 집중해요.',
  [('냉장고장 제작 기간은 얼마나 걸려요?', '실측 뒤 자재를 재단해 가서, 현장 설치는 대부분 하루 안에 끝나요. 일정은 냉장고 배송일에 맞춰 잡아요.')]),
 ('demolish', '냉장고장 철거', '다 뜯기 전에 사진 먼저 · 30만원부터', 'guide-partition', '부분 철거 리폼 30만원, 철거 후 새로 짜기 100만원부터 (VAT 별도)',
  FIT, '냉장고장을 통째로 철거하면 바닥과 벽 마감, 상부장 처리까지 일이 커져요. 철거하기 전에 사진을 보내 주시면 걸리는 칸막이나 기둥만 빼면 되는지, 철거하고 새로 짜야 하는지 먼저 알려드려요.',
  [('철거하면 바닥과 벽은 어떻게 해요?', '칸막이가 있던 자리는 도배와 마루가 안 돼 있어서, 자재로 채워 마감해요. 철거 후 새로 짤 때도 마감까지 같이 해요.')]),
 ('install', '냉장고장 시공', '대표 직접 실측·시공 · 대부분 하루', 'guide-kitchenfit', '칸막이 제거 30만원, 새로 짜기 100만원부터 (VAT 별도)',
  FIT, '냉장고장 시공은 실측, 재단, 설치, 마감 순서로 진행해요. 저희는 대표가 직접 재고 직접 설치해서, 냉장고와 장 사이 간격과 수평까지 현장에서 바로 맞춰요. 칸막이 제거 같은 리폼은 대부분 하루면 끝나요.',
  [('시공할 때 먼지가 많이 나나요?', '치수에 맞게 자재를 미리 재단해 가서 현장에서 자르는 작업을 줄여요.')]),
 ('pricing', '냉장고장 가격', '리폼 30만원 · 제작 100만원부터', 'x-cost', '칸막이·기둥 제거 30만원, 새로 짜기 100만원부터 (VAT 별도)',
  FIT, '냉장고장 가격은 리폼이냐 새로 짜느냐에 따라 달라요. 칸막이나 기둥만 빼는 리폼은 30만원, 냉장고 모델에 맞춰 새로 짜면 100만원부터예요. 홈바장이나 렌지장을 같이 짜면 구성에 따라 더해져요.',
  [('냉장고장 가격에 철거와 마감이 포함돼요?', '칸막이 제거 30만원에는 보강, 마감, 폐자재 처리가 포함이에요(VAT 별도).')]),
 ('side', '냉장고 옆 수납장', '남는 틈새 맞춤 · 키큰장·틈새장', 'x-range', '사진을 보고 금액 안내 (냉장고장과 함께 짜면 100만원부터, VAT 별도)',
  lambda w: w['no'] in ('224432139660', '224277045640', '224439467559', '224271127551') or FIT(w), '냉장고를 넣고 옆에 애매하게 남는 틈은 그냥 두면 먼지만 쌓여요. 폭에 맞춰 키큰장, 틈새장, 밥솥장으로 짜서 냉장고장과 한 세트처럼 보이게 만들어요.',
  [('폭이 20cm 정도만 남아도 짤 수 있나요?', '네. 좁은 틈은 앞으로 빼서 쓰는 틈새장이나 긴 물건 보관 칸으로 짜요. 칸막이를 재활용해 문을 만든 현장도 있어요.')]),
 ('fridgebar', '냉장고장 홈바', '냉장고 옆 LED 홈바 · 100만원부터', 'x-homebar', '디자인 홈바장 100만원부터 (VAT 별도)',
  lambda w: w['no'] in ('224277045640', '224176609693', '223831173880', '223917629832'), '냉장고장 옆 남는 폭이나 상부를 LED 조명 홈바로 바꾸면 주방 분위기가 확 달라져요. 냉장고장과 같은 자재와 색으로 맞춰 짜서 원래 한 세트였던 것처럼 보여요.',
  [('냉장고장 리폼하면서 홈바도 같이 할 수 있나요?', '네. 냉장고장 리폼과 함께 홈카페장을 추가한 대전 현장이 있어요.')]),
 ('storage', '냉장고장 수납장', '남는 칸·상부장 수납 맞춤', 'x-range', '사진을 보고 금액 안내 (냉장고장과 함께 짜면 100만원부터, VAT 별도)',
  lambda w: w['no'] in ('224439467559', '224432139660', '224277045640', '224271127551') or FIT(w), '냉장고장을 고치면서 남는 칸이나 상부장을 수납장으로 바꾸면 주방이 훨씬 넓게 쓰여요. 냉장고 옆 틈은 키큰장이나 밥솥장으로, 칸막이를 뺀 자리는 선반 수납장으로 맞춰 짜요.',
  [('냉장고장 칸막이를 빼고 수납장을 추가할 수 있나요?', '네. 세종 현장에서 칸막이를 철거하고 옆에 수납장을 추가한 적이 있어요.')]),
 ('door', '냉장고장 문달기', '남는 칸·틈새에 문짝 맞춤', 'x-range', '사진을 보고 금액 안내 (VAT 별도)',
  lambda w: w['no'] in ('224271127551', '223833108339', '224439467559') or FIT(w), '냉장고장 옆 남는 칸이나 틈이 훤히 보이면 지저분해 보여요. 폭과 높이에 맞춰 문짝을 짜서 달면 깔끔한 수납장이 돼요. 칸막이를 재활용해 문을 만든 현장도 있어요.',
  [('뺀 칸막이로 문을 만들 수 있나요?', '네. 신축 아파트 현장에서 뺀 칸막이를 재활용해 남는 틈을 막는 문으로 만든 적이 있어요.')]),
 ('ttungnaeng', '뚱냉 냉장고장', '일반 냉장고 깊이 맞춤 · 리폼·제작', 'guide-partition', '칸막이 제거 30만원, 새로 짜기 100만원부터 (VAT 별도)',
  FIT, '키친핏이 아닌 일반 냉장고(뚱냉)는 깊이가 깊어서 냉장고장 앞으로 튀어나오기 쉬워요. 냉장고 깊이와 문 여는 공간을 보고, 칸막이만 빼서 넣을지 깊이에 맞춰 새로 짤지 정해요.',
  [('뚱냉도 냉장고장에 넣을 수 있나요?', '네. 폭과 깊이를 보고 칸을 다시 나누거나, 깊이에 맞춰 새로 짜요. 모델명을 알려주시면 먼저 계산해 드려요.')]),
 ('interior', '냉장고장 인테리어', '주방 색에 맞춘 냉장고장·홈바', 'guide-kitchenfit', '칸막이 제거 30만원, 새로 짜기 100만원부터, 홈바장 100만원부터 (VAT 별도)',
  lambda w: FIT(w) or w['f'] == 'bar', '냉장고장은 주방에서 가장 큰 가구라 색과 구성만 바꿔도 주방 인상이 달라져요. 주방 가구 색에 맞춰 문짝을 고르고, 남는 폭에는 LED 홈바나 키큰장을 넣어 한 세트처럼 짜요.',
  [('주방 가구랑 색을 맞출 수 있나요?', '네. 기존 주방 가구 색에 맞춰 문짝과 마감 자재를 골라요.')]),
]
_NEW = ['gongju', 'nonsan', 'gyeryong', 'seosan', 'yesan', 'boryeong', 'jincheon', 'chungju', 'osong', 'daedeok']
_BIG = ['daejeon', 'sejong', 'cheonan', 'cheongju', 'asan']
COMBOS = [(r, k) for r in [x[0] for x in KW_REGIONS[:10]] for k in ('partition', 'kitchenfit', 'bespoke', 'objet', 'custom')]
COMBOS += [(r, k) for k in ('partition', 'kitchenfit') for r in _NEW]
COMBOS += [(r, 'reform') for r in _BIG + ['naepo', 'dangjin', 'seosan']]
COMBOS += [(r, 'kimchi') for r in _BIG + ['naepo']]
COMBOS += [(r, 'homebar') for r in _BIG + ['ochang']]
COMBOS += [(r, k) for k in ('range', 'shoe') for r in _BIG]
# 3차 50개 (2026-10-27)
_MID = ['yuseong', 'dunsan', 'ochang', 'naepo', 'dangjin']
COMBOS += [(r, 'custom') for r in _NEW]
COMBOS += [(r, 'bespoke') for r in _NEW]
COMBOS += [(r, 'reform') for r in _NEW + _MID if (r, 'reform') not in COMBOS]
COMBOS += [(r, 'kimchi') for r in _MID if (r, 'kimchi') not in COMBOS]
COMBOS += [(r, 'homebar') for r in _MID if (r, 'homebar') not in COMBOS]
COMBOS += [(r, k) for k in ('range', 'shoe') for r in _MID]
# 4차 50개 (2026-10-28): 문의가 많은 문제형 검색어 위주
_TOP = _BIG + _MID
COMBOS += [(r, k) for k in ('noinstall', 'pillar', 'robot') for r in _TOP]
COMBOS += [(r, 'objet') for r in _NEW]
COMBOS += [(r, 'kimchi') for r in ['gongju', 'nonsan', 'seosan', 'daedeok', 'chungju']]
COMBOS += [(r, 'homebar') for r in ['gongju', 'nonsan', 'seosan', 'daedeok', 'chungju']]
# 5차 50개 (2026-10-29)
_BIGNEW = ['gongju', 'nonsan', 'seosan', 'daedeok', 'chungju']
COMBOS += [(r, k) for k in ('noinstall', 'pillar') for r in _NEW]
COMBOS += [(r, k) for k in ('cost', 'movein') for r in _TOP + _BIGNEW]
# 6차 50개 (2026-10-30)
_REST = ['gyeryong', 'yesan', 'boryeong', 'jincheon', 'osong']
COMBOS += [(r, k) for k in ('fourdoor', 'homecafe') for r in _TOP]
COMBOS += [(r, k) for k in ('cost', 'movein', 'kimchi', 'homebar') for r in _REST]
COMBOS += [(r, k) for k in ('robot', 'range') for r in _BIGNEW]
# 7차 50개 (2026-10-31): 새 아파트가 많은 동네
_HOOD = ['doan', 'tangjeong', 'buldang', 'junggu', 'donggu']
COMBOS += [(r, k) for r in _HOOD for k in ('partition', 'kitchenfit', 'bespoke', 'objet', 'custom', 'noinstall', 'movein')]
COMBOS += [(r, 'fourdoor') for r in _NEW]
COMBOS += [(r, 'homecafe') for r in _BIGNEW]
# 8차 50개 (2026-11-01): 네이버 자동완성에 실제로 뜨는 검색어
COMBOS += [(r, k) for k in ('make', 'demolish', 'install', 'pricing') for r in _TOP]
COMBOS += [(r, k) for k in ('side', 'fridgebar') for r in _BIG]
# 9차 50개 (2026-11-02): 자동완성 검색어 2
COMBOS += [(r, k) for k in ('storage', 'door', 'ttungnaeng', 'interior') for r in _TOP]
COMBOS += [(r, k) for k in ('ttungnaeng', 'storage') for r in _BIGNEW]
# 10차 50개 (2026-11-03): 신축 많은 동네(도안·탕정·불당·중구·동구) 핵심 검색어 + 큰 도시 제작·설치·가격 + 옆장·홈바
COMBOS += [(r, k) for r in _HOOD for k in ('reform', 'kimchi', 'cost', 'pillar', 'fourdoor')]
COMBOS += [(r, k) for k in ('make', 'install', 'pricing') for r in _BIGNEW]
COMBOS += [(r, k) for k in ('side', 'fridgebar') for r in _MID]
# 11차 50개 (2026-11-04): 작은 도시 제작·시공·가격, 신축 동네 홈바·렌지장·로봇청소기장·제작, 중간 도시 옆장·홈바·철거
COMBOS += [(r, k) for k in ('make', 'install', 'pricing') for r in _REST]
COMBOS += [(r, k) for r in _HOOD for k in ('homebar', 'range', 'robot', 'make')]
COMBOS += [(r, k) for k in ('side', 'fridgebar', 'demolish') for r in _BIGNEW]
# 12차 50개 (2026-11-05): 신축 동네 시공·가격·수납장·신발장, 작은 도시 로봇청소기장·렌지장·철거·수납장, 중간 도시 문달기·인테리어
COMBOS += [(r, k) for r in _HOOD for k in ('install', 'pricing', 'storage', 'shoe')]
COMBOS += [(r, k) for k in ('robot', 'range', 'demolish', 'storage') for r in _REST]
COMBOS += [(r, k) for k in ('door', 'interior') for r in _BIGNEW]
# 13차 50개 (2026-11-06): 신축 동네·작은 도시 옆장·홈바·철거·뚱냉·홈카페·문달기·인테리어 (전화 문의로 이어지는 작업)
COMBOS += [(r, k) for r in _HOOD for k in ('side', 'fridgebar', 'demolish', 'ttungnaeng', 'homecafe')]
COMBOS += [(r, k) for k in ('side', 'fridgebar', 'door', 'interior', 'ttungnaeng') for r in _REST]
# 매일 자동으로 추가된 조합 (tools/daily.py가 채움)
import os as _os
_DJ = TOOLS + '/daily.json'
DAILY = json.load(open(_DJ)) if _os.path.exists(_DJ) else []
COMBOS += [tuple(x) for x in DAILY if tuple(x) not in COMBOS]
WANT = {'cost': '냉장고장 리폼·제작 (견적 문의)', 'pricing': '냉장고장 리폼·제작 (견적 문의)', 'noinstall': '새 냉장고가 장에 안 들어가요', 'movein': '입주 전 냉장고장 리폼·제작', 'interior': '냉장고장 리폼·제작', 'ttungnaeng': '뚱냉(일반 냉장고) 자리 냉장고장', 'door': '냉장고장 문 달기'}
REG = {x[0]: x for x in KW_REGIONS}; KWD = {x[0]: x for x in KWS}
KW_PAGES = []
for rs, ks in COMBOS:
    KW_PAGES.append(('kw-%s-%s' % (rs, ks), '%s %s' % (REG[rs][1], KWD[ks][1])))
for rs, ks in COMBOS:
    if True:
        rs, rn, aslug, rkeys = REG[rs]; ks, kn, tail, gslug, price, sel, kintro, kfaq = KWD[ks]
        slug = 'kw-%s-%s' % (rs, ks); g = GD[gslug]
        cand = [w for w in works if sel(w)] or [w for w in works if FIT(w)]
        local = [w for w in cand if any(k in (CASES[w['no']].get('region') or '') or k in CASES[w['no']]['city'] for k in rkeys)]
        show = (local + [w for w in cand if w not in local])[:6]
        f = local[0] if local else show[0]; c = CASES[f['no']]
        steps = ''.join('<li><b>%s</b><p>%s</p></li>' % (H.escape(t), H.escape(d)) for t, d in g[7]) if g[7] else ''.join('<li><b>%s</b><p>%s</p></li>' % (H.escape(x['t']), H.escape(x['d'])) for x in c['steps'][:4])
        pts = ''.join('<div class="factor"><span class="ic">%02d</span><h3>%s</h3><p>%s</p></div>' % (n, t, d) for n, (t, d) in enumerate(g[6], 1))
        faq = [('%s도 와 주시나요?' % rn, '네. %s %s 상담부터 실측, 시공, AS까지 대표가 직접 가요. 사진과 아파트 이름을 문자로 보내 주시면 일정과 금액을 함께 알려드려요.' % (rn, kn))] + kfaq + list(g[9])[:2] + [
               ('견적은 어떻게 받나요?', '현장 사진 2~3장, 냉장고 모델명, 아파트 이름을 문자로 보내 주세요. 작업 중엔 전화를 못 받을 때가 많아 문자가 가장 빨라요.')]
        same_r = ''.join('<a href="kw-%s-%s.html">%s %s</a>' % (rs, k[0], rn, k[1]) for k in KWS if k[0] != ks and (rs, k[0]) in COMBOS)
        same_k = ''.join('<a href="kw-%s-%s.html">%s %s</a>' % (r[0], ks, r[1], kn) for r in KW_REGIONS if r[0] != rs and (r[0], ks) in COMBOS)
        body = '''<section class="kw-top">
  <div class="wrap">
    <div class="area-intro"><p>%(kintro)s</p><p class="muted">%(rintro)s</p></div>
    <div class="area-stats">
      <div><b>%(price_big)s</b><span>%(price_lbl)s</span></div>
      <div><b>직접</b><span>대표가 실측부터 시공까지</span></div>
      <div><b>평생</b><span>처짐·기울어짐 무상 AS</span></div>
    </div>
    <p class="stats-note">※ E0 등급 친환경 자재(포름알데히드 방출 0.5mg/L 이하)만 사용해요.</p>
  </div>
</section>

<!--RV-->

<section class="band">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">%(rn)s %(kn)s</p><h2>이렇게<br><em>해 드려요</em></h2></div>
    <div class="factors">%(pts)s</div>
  </div>
</section>

<section class="area-feat-sec">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">%(fk)s</p><h2>%(ft)s</h2><p>%(fr)s</p></div>
    <div class="area-feat">
      <div class="wk-pair case-pair"><figure><img loading="lazy" src="img/works/%(fno)s-before.jpg" alt="%(ft)s 공사 전"><figcaption>BEFORE</figcaption></figure><figure><img loading="lazy" src="img/works/%(fno)s-after.jpg" alt="%(ft)s 공사 후"><figcaption class="a">AFTER</figcaption></figure></div>
      <div class="area-feat-txt"><h3>이런 상황이었어요</h3><p>%(fp)s</p><h3>결과</h3><p>%(fres)s</p>%(fq)s<p class="more-link feat-btns" style="text-align:left"><a class="btn btn-acc" href="#quote">사진 한 장으로 무료 견적 받아보기</a><a class="btn btn-soft" href="case-%(fno)s.html">이 현장 자세히 보기 →</a></p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">진행 순서</p><h2>%(kn)s<br><em>이렇게 작업해요</em></h2></div>
    <ol class="case-steps area-flow">%(steps)s</ol>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-head"><p class="kicker">실제 현장</p><h2>%(kn)s<br><em>작업 사례</em></h2></div>
    <div class="wk-grid">%(cards)s</div>
    <p class="price-note">%(price)s. 사진을 보고 우리 집 금액을 알려드려요. <a href="#quote"><b>사진 보내고 금액 받기</b></a> · <a href="price.html">비용 자세히 보기</a></p>
  </div>
</section>

<!--QUOTE-->

<section class="band">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">자주 묻는 질문</p><h2>%(rn)s %(kn)s<br><em>궁금한 점</em></h2></div>
    <div class="faq">%(faq)s</div>
    <div class="area-others"><span>%(rn)s 다른 작업</span>%(same_r)s</div>
    <div class="area-others"><span>다른 지역 %(kn)s</span>%(same_k)s</div>
    <div class="area-others"><span>더 보기</span><a href="area-%(aslug)s.html">%(aname)s 냉장고장 안내</a><a href="%(glink)s.html">%(gname)s %(gsuf)s</a><a href="works.html">작업 기록 전체</a><a href="qa.html">질문과 답변</a></div>
  </div>
</section>
''' % {'kintro': H.escape(kintro), 'rintro': H.escape(AINTRO[aslug]), 'price_big': {'partition': '30만원', 'kitchenfit': '100만원~', 'custom': '100만원~', 'homebar': '100만원~', 'range': '사진 견적', 'shoe': '하루', 'robot': '사진 견적', 'pillar': '30만원', 'cost': '30만원', 'homecafe': '100만원~', 'make': '100만원~', 'demolish': '30만원~', 'install': '하루', 'pricing': '30만원', 'side': '사진 견적', 'fridgebar': '100만원~', 'storage': '사진 견적', 'door': '사진 견적', 'ttungnaeng': '30만원~', 'interior': '30만원~'}.get(ks, '30만원~'),
       'price_lbl': {'partition': '칸막이 제거 리폼', 'kitchenfit': '맞춤제작 (VAT 별도)', 'custom': '맞춤제작 (VAT 별도)', 'homebar': '디자인 홈바장 (VAT 별도)', 'range': '사진 보고 금액 안내', 'shoe': '대부분 하루 시공', 'reform': '부분 리폼부터 (VAT 별도)', 'kimchi': '칸막이 제거부터 (VAT 별도)', 'robot': '사진 보고 금액 안내', 'pillar': '기둥 제거 리폼 (VAT 별도)', 'noinstall': '칸막이·기둥 제거부터 (VAT 별도)', 'cost': '칸막이 제거 · 새로 짜기 100만원~', 'movein': '칸막이 제거부터 (VAT 별도)', 'fourdoor': '칸막이·기둥 제거부터 (VAT 별도)', 'homecafe': '디자인 홈바장 (VAT 별도)', 'make': '냉장고장 제작 (VAT 별도)', 'demolish': '부분 철거 리폼부터 (VAT 별도)', 'install': '리폼은 대부분 하루 시공', 'pricing': '칸막이 제거 · 제작 100만원~', 'side': '사진 보고 금액 안내', 'fridgebar': '디자인 홈바장 (VAT 별도)', 'storage': '사진 보고 금액 안내', 'door': '사진 보고 금액 안내', 'ttungnaeng': '칸막이 제거부터 (VAT 별도)', 'interior': '칸막이 제거부터 (VAT 별도)'}.get(ks, '기둥 제거부터 (VAT 별도)'),
       'n': len(works), 'rn': rn, 'kn': kn, 'pts': pts, 'fk': ('%s 현장' % rn) if local else '가까운 지역 대표 현장', 'ft': H.escape(c['title']), 'fr': H.escape(c['region']), 'fno': f['no'],
       'fp': H.escape(c['problem']), 'fres': H.escape(c['result']),
       'fq': '<blockquote class="case-quote" style="font-size:16px">“%s”<cite>고객님 후기</cite></blockquote>' % H.escape(c['quote']) if c.get('quote') else '',
       'steps': steps, 'cards': ''.join(card(w) for w in show if w is not f), 'price': price,
       'faq': ''.join('<details><summary>%s</summary><p class="a">%s</p></details>' % (H.escape(q), H.escape(a)) for q, a in faq),
       'same_r': same_r, 'same_k': same_k, 'aslug': aslug, 'aname': ANAME2[aslug], 'gslug': gslug, 'glink': g[0], 'gname': g[1], 'gsuf': '가이드' if gslug in ('guide-partition', 'guide-kitchenfit', 'fridge-bespoke', 'fridge-objet') else '자세히 보기'}
        ldj = crumbs([('홈', ''), (ANAME2[aslug], 'area-' + aslug), ('%s %s' % (rn, kn), slug)]) + ld({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]})
        page(slug + '.html', '%s %s · %s' % (rn, kn, tail),
             ('%s %s. %s %s. 실제 시공 사례 전후 사진, 작업 순서, 평생 AS. 문의 %s' % (rn, kn, kintro.split('.')[0] + '.', price.split(' (')[0], PHONE))[:160],
             '%s 출장' % rn, '%s<br><em>%s</em>' % (rn, kn), '%s, 대표가 직접 재고 짜서 설치해요.' % tail, body, ldj,
             crumb='<a href="area-%s.html">%s</a> <span>›</span> %s' % (aslug, ANAME2[aslug], kn), og_image=SITE + 'img/works/%s-after.jpg' % f['no'], subnav=False, job=WANT.get(ks, kn), area=rn, hero_pair=f['no'])
print('kw pages', len(KW_PAGES))
