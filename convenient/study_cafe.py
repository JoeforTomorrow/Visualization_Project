# 카카오 API 활용 스터디카페 검색 #

## 1. 지역구 별 스터디카페 검색 ##

import pandas as pd
import requests

KAKAO_API_KEY = "#####"
KAKAO_WEB_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json?query={} 스터디카페&page={}"

header = {"Authorization": "KakaoAK {}".format(KAKAO_API_KEY)}

gus = ['종로구','중구','용산구','성동구',
'광진구','동대문구','중랑구','성북구',
'강북구','도봉구','노원구','은평구',
'서대문구','마포구','양천구','강서구',
'구로구','금천구','영등포구','동작구',
'관악구','서초구','강남구','송파구','강동구']

example_list = []
for i in gus:
  j = 1
  while 1:
    try:
      response = requests.get(KAKAO_WEB_SEARCH_URL.format(i,j), headers=header)
      data1 = response.json()
      documents = data1["documents"]
      for k in documents:
        if [k['id'],k["place_name"],k["address_name"],k["x"],k["y"]] not in example_list:
          example_list.append([k['id'],k["place_name"],k["address_name"],k["x"],k["y"]])
      j += 1
    except:
      break

df_study_cafe = pd.DataFrame(example_list)
df_study_cafe.columns=["id","name",'place','x','y']

df_study_cafe.to_csv('df_study_cafe.csv')

## 2. 매물 별 반경 1km 이내 스터디카페 검색 ##

import pandas as pd
import requests

KAKAO_API_KEY = "#####"
KAKAO_WEB_SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json?query=스터디카페&y={}&x={}&radius=1000"

header = {"Authorization": "KakaoAK {}".format(KAKAO_API_KEY)}

y = '#####'
x = '#####'

response = requests.get(KAKAO_WEB_SEARCH_URL.format(y, x), headers=header)

data1 = response.json()
documents = data1["documents"]

lst = []
for i in documents:
  lst.append([i["id"],i["place_name"],i["address_name"],i["x"],i["y"]])

df_study_cafe = pd.DataFrame(lst)
df_study_cafe.columns=["id","name",'place','x','y']
