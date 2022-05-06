import requests
from bs4 import BeautifulSoup
import pandas as pd

# 네이버 지도 검색결과를 크롤링하는 함수입니다.
# 검색할 자치구를 gu 파라미터로 받아옵니다.
# 찾고싶은것을 search 파라미터로 받아옵니다.
# 보고싶은 검색 결과 페이지를 page 파라미터로 받아옵니다.
def naver_map_crawler(gu ,search, page):
    url = "https://map.naver.com/v5/api/search?"
    payload = {
        "caller": "pcweb",
        "query": gu + search,
        "type": "all",
        "searchCoord": "",
        "page": page,
        "displayCount": 20,
        "isPlaceRecommendationReplace": "true",
        "lang": "ko",
    }
    headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'
    }
    response = requests.get(url, params = payload,headers = headers)
    x = response.json()['result']['place']['list']
    return x

lst = []
# 서울 내 25개 자치구 리스트
gus = ['종로구','중구','용산구','성동구',
'광진구','동대문구','중랑구','성북구',
'강북구','도봉구','노원구','은평구',
'서대문구','마포구','양천구','강서구',
'구로구','금천구','영등포구','동작구',
'관악구','서초구','강남구','송파구','강동구']
for gu in gus:
    for i in range(1,100):
        # 페이지 끝까지 가도록 try, except 구문을 활용했습니다.
        try:
            lst.append(naver_map_crawler(gu,"검색어",i))
        except:
            break

# 크롤링 결과를 DataFrame에 넣는 작업
df = pd.DataFrame()
for item in lst:
    id   = item["id"]
    name = item["name"]
    addr = item["address"].split(" ")
    si   = addr[0] # 시
    gu   = addr[1] # 자치구
    dong = addr[2] # 법정동
    lat  = item["y"] #위도
    lng  = item["x"] # 경도
    x = pd.Series([id,name,si,gu,dong,lat,lng])
    df = df.append(x,ignore_index=True)

df = df.reset_index()
df = df.drop("index",1)
# 컬럼명 설정
df_final = df.set_axis(['id','매장명','시','구','동','위도','경도'],1,inplace=False)
# csv파일로 추출
df_final.to_csv("df_final.csv")