import geohash2
import requests
import pandas as pd
import threading
import time

def zigbang_crwler(typ, dong):
    try:
        # 1. 동이름으로 위도 경도 구하기
        url = "https://apis.zigbang.com/search?q={}".format(dong)
        response = requests.get(url)
        items = response.json()["items"]
        for item in items:
            if item['_source']['local1'] == "서울시":
                lat, lng = item["lat"], item["lng"]
        # 2. 위도 경도로 geohash 알아내기
        geohash = geohash2.encode(lat, lng, precision=5)

        # 3. 직방 api에 geohash를 parameter로 넘겨 해당 geohash의 매물 리스트 가져오기
        # 찾는 매물의 타입 또한 파라미터로 넘긴다 ( 원룸, 투룸, 오피스텔, 빌라 등등 )
        url = f"https://apis.zigbang.com/v2/items?\
        deposit_gteq=0&domain=zigbang&geohash={geohash}&rent_gteq=0&sales_type_in=전세|월세&service_type={typ}"
        response = requests.get(url)
        items = response.json()["items"]
        # requests에서 받아온 정보 중 매물의 id만을 ids 리스트에 저장한다.
        ids = [item["item_id"] for item in items]

        # 4. id로 매물 정보 가져오기
        url = "https://apis.zigbang.com/v2/items/list"
        params = {
          "domain": "zigbang",
          "withCoalition": "false",
          "item_ids": ids[:900],
        }

        response = requests.post(url, params)
        items = response.json()["items"]
        return [item for item in items if dong in item["address"]]
    except :
        pass
    time.sleep(3) # 크롤링 돌리다 밴 당하는 상황을 막기 위해 3초씩 지연

lst = ['서울내 467개'] # 리스트가 세로로 너무 길어 이런 형태로 표현했습니다.
zigbang = []
for dong in lst:
    try:
        zigbang.append("원룸",dong)
        zigbang.append("오피스텔", dong)
    except:
        pass

# 리스트 안에 리스트가 저장된 형태기때문에 하나의 리스트를 만들기 위한 함수 정의
def flatten_list(_2d_list):
    flat_list = []
    for element in _2d_list:
        if type(element) is list:
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

zigbang_lst = list(flatten_list(zigbang))
zigbang_df = pd.DataFrame(zigbang_lst)

# item_id를 통해 중복항목 제거
zigbang_df = zigbang_df.drop_duplicates(subset = "item_id")

# 쓸모없는 column들 제거
zigbang_df = zigbang_df.drop(["section_type",'sales_title','공급면적','전용면적','계약면적','room_type_title','title',
       'is_first_movein','is_zzim','floor_string','address2','address3','room_type',
       'status','tags','reg_date', 'is_new'],1)

# column 명 재설정
zigbang_df.rename(columns = {"random_location":"lat_lng"},inplace = True)

# 위도 경도가 하나의 데이터로 붙어있어 분리하여 각각의 컬럼에 넣는 작업을 했다.
lat = []
lng = []

for i in range(0,len(zigbang_df)):
    try:
        lat.append(zigbang_df['lat_lng'][i]['lat'])
        lng.append(zigbang_df['lat_lng'][i]['lng'])
    except:
        pass
# 매물 주소 column 생성
for i in range(0, len(zigbang_df)):
    zigbang_df["주소"][i] = "https://www.zigbang.com/home/oneroom/items/" + str(zigbang_df["item_id"][i])

# 시 구 동 구분해서 각각의 컬럼으로 넣기
for i in range(0, len(zigbang_df)):
    zigbang_df["시"][i] = zigbang_df["address1"][i].split(" ")[0]
    zigbang_df["구"][i] = zigbang_df["address1"][i].split(" ")[1]
    zigbang_df["동"][i] = zigbang_df["address1"][i].split(" ")[2]

# 쓸 일 없는 컬럼들 제거
zigbang_df = zigbang_df.drop(["item_id","address1","lat_lng","address","건물층수"],axis = 1)

# 컬럼 명 재설정
zigbang_df.rename(columns = {'images_thumbnail' : "이미지", 'lng' : '경도', 'lat' : '위도', 'sales_type':'전세/월세', 'deposit':'보증금', 'rent':'월세',
       'size_m2':"m2", 'floor':"층수", 'building_floor':"건물층수", 'service_type':"원룸/오피스텔",
       'manage_cost':'관리비'}, inplace = True)

# csv 파일로 저장하기.
zigbang_df.to_csv("zigbang_img_link.csv")