

# 전/월세 데이터 불러오기
import pandas as pd

zig_path = '/content/drive/MyDrive/project/zigbang/new_zig.csv'
zig = pd.read_csv(zig_path)
zig=zig.drop("Unnamed: 0",axis=1)

def lease_type(x,zig):
    if x == "월세":
        mask = zig['전세/월세'] == "월세"
        zig=zig[mask].reset_index(drop=True)
        
        y = input("월세 상한 : ")
        zig = fee_max(int(y), zig)

        z = input("보증금 상한 : ")
        zig = deposit_max(int(z), zig)

    elif x == "전세":
        mask = zig['전/월세'] == "전세"
        zig=zig[mask].reset_index(drop=True)

        z = input("보증금 상한 : ")
        zig = deposit_max(int(z), zig)
    
    return zig

def fee_max(x,zig):
    mask = zig["월세(만원)"] <= x
    zig=zig[mask].reset_index(drop=True)
    return zig

def deposit_max(x,zig):
    mask = (zig["보증금(만원)"] <= x) & (zig["보증금(만원)"] >= 100)
    zig=zig[mask].reset_index(drop=True)
    return zig

zig = lease_type(input("월세/전세 : "),zig)

# 좌표값을 통한 거리 측정을 위해 haversine 패키지 설치
## 우선 터미널 상에서 pip install haversine 실행 필요
from haversine import haversine

# 지하철

def func_sub(zig):

    sub_path = '###'
    subway = pd.read_csv(sub_path, encoding = 'cp949')
    subway.rename(columns={
        "위도":"경도",
        "경도":"위도"
    },inplace = True)
    
    sub_com=pd.DataFrame(index=range(len(zig)), columns=['개수', '역목록','유무'])

    for i in range(len(zig)):
        mask = abs(subway["경도"] - zig.loc[i,"경도"]) + abs(subway["위도"] - zig.loc[i,"위도"]) <= 0.02
        sub_mask=subway[mask].reset_index()
        cnt=0
        sub_lst = ''

        for j in range(len(sub_mask)):

            if haversine(zig.loc[i,["경도","위도"]].to_list(), sub_mask.loc[j,["경도","위도"]].to_list()) <= 0.5:
                sub_lst += f" {sub_mask.iloc[j]['호선']} : {sub_mask.iloc[j]['역사명']} "
                cnt += 1
                sub_com.loc[i,["유무"]]=1

        sub_com.loc[i,["개수"]]=cnt
        sub_com.loc[i,["역목록"]]=str(sub_lst)
        
        
    return sub_com

#편의점

def func_store(zig):

    store_path = '###'
    store = pd.read_csv(store_path)

    store_com=pd.DataFrame(index=range(len(zig)), columns=['개수','유무'])

    for i in range(len(zig)):
        mask = ((store['경도'] - zig.loc[i,"경도"])**2 + (store['위도'] - zig.loc[i,"위도"])**2)**0.5 <= 0.00125
        sty_mask=store[mask].reset_index()

        if len(sty_mask) >= 1:
            store_com.loc[i,["개수"]]=1
            store_com.loc[i,["유무"]]="있음"
        else:
            store_com.loc[i,["개수"]]=0
            store_com.loc[i,["유무"]]="없음"
    
    return store_com

# 다이소

def func_daiso(zig):

    daiso_path = '###'
    daiso = pd.read_csv(daiso_path)

    daiso_com=pd.DataFrame(index=range(len(zig)), columns=['개수','유무'])

    for i in range(len(zig)):
        mask = ((daiso['경도'] - zig.loc[i,"경도"])**2 + (daiso['위도'] - zig.loc[i,"위도"])**2)**0.5 <= 0.0025
        sty_mask=daiso[mask].reset_index()

        if len(sty_mask) >= 1:
            daiso_com.loc[i,["개수"]]=1
            daiso_com.loc[i,["유무"]]="있음"
        else:
            daiso_com.loc[i,["개수"]]=0
            daiso_com.loc[i,["유무"]]="없음"
    
    return daiso_com

# 공원

def func_park(zig):

    park_path = '###'
    park = pd.read_csv(park_path)

    park_com=pd.DataFrame(index=range(len(zig)), columns=['개수','유무'])

    for i in range(len(zig)):
        mask = ((park['x'] - zig.loc[i,"경도"])**2 + (park['y'] - zig.loc[i,"위도"])**2)**0.5 <= 0.0025
        sty_mask=park[mask].reset_index()

        if len(sty_mask) >= 1:
            park_com.loc[i,["개수"]]=1
            park_com.loc[i,["유무"]]="있음"
        else:
            park_com.loc[i,["개수"]]=0
            park_com.loc[i,["유무"]]="없음"
    
    return park_com

# 스터디카페

def func_studycafe(zig):

    sc_path = '###'
    study = pd.read_csv(sc_path)
    study=study.drop("Unnamed: 0",axis=1)
    study=study.drop("id",axis=1)

    study_com=pd.DataFrame(index=range(len(zig)), columns=['개수','유무'])

    for i in range(len(zig)):
        mask = ((study['x'] - zig.loc[i,"경도"])**2 + (study['y'] - zig.loc[i,"위도"])**2)**0.5 <= 0.0025
        sty_mask=study[mask].reset_index()

        if len(sty_mask) >= 1:
            study_com.loc[i,["개수"]]=1
            study_com.loc[i,["유무"]]="있음"
        else:
            study_com.loc[i,["개수"]]=0
            study_com.loc[i,["유무"]]="없음"
    
    return study_com

# 스타벅스

def func_starbucks(zig):

    star_path = '###'
    starbucks = pd.read_csv(star_path)
    starbucks = starbucks.drop("Unnamed: 0",axis=1)
    
    starbucks_com = pd.DataFrame(index=range(len(zig)), columns=['개수','유무'])

    for i in range(len(zig)):
        mask = ((starbucks['x'] - zig.loc[i,"경도"])**2 + (starbucks['y'] - zig.loc[i,"위도"])**2)**0.5 <= 0.0025
        sty_mask=starbucks[mask].reset_index()

        if len(sty_mask) >= 1:
            starbucks_com.loc[i,["개수"]]=1
            starbucks_com.loc[i,["유무"]]="있음"
        else:
            starbucks_com.loc[i,["개수"]]=0
            starbucks_com.loc[i,["유무"]]="없음"
        
    return starbucks_com

# 패스트푸드

def func_fastfoods(zig):

    fast_path = '###'
    fastfoods = pd.read_csv(fast_path)
    
    fastfoods_com = pd.DataFrame(index=range(len(zig)), columns=['개수','유무'])

    for i in range(len(zig)):
        mask = ((fastfoods['경도'] - zig.loc[i,"경도"])**2 + (fastfoods['위도'] - zig.loc[i,"위도"])**2)**0.5 <= 0.0025
        sty_mask=fastfoods[mask].reset_index()

        if len(sty_mask) >= 1:
            fastfoods_com.loc[i,["개수"]]=1
            fastfoods_com.loc[i,["유무"]]='있음'
        else:
            fastfoods_com.loc[i,["개수"]]=0
            fastfoods_com.loc[i,["유무"]]='없음'
        
    return fastfoods_com

subway_lst = func_sub(zig)
daiso_cnt = func_daiso(zig)
store_cnt = func_store(zig)
park_cnt = func_park(zig)
study_cnt = func_studycafe(zig)
starbucks_cnt = func_starbucks(zig)
fastfoods_cnt = func_fastfoods(zig)

# 지도 데이터 시각화
import folium
import json

dong_path = '/content/drive/MyDrive/project/polygon/seouldongfixed.geojson'
dong = json.load(open(dong_path))

s_map = folium.Map(
    location=[37.5642135, 127.0016985],
    zoom_start=11)

folium.Choropleth(geo_data=dong,
                  data=zig,
                  fill_color='Reds',
                  fill_opacity=0.5,
                  line_opacity=0.2,
                  columns=['동','월세(만원)'],
                  key_on = 'feature.properties.EMD_KOR_NM',
                  legend_name="월세"
            ).add_to(s_map)

folium.LayerControl().add_to(s_map)

cnt=0
for i in range(len(zig)):
    if subway_lst['유무'][i]+store_cnt['개수'][i]+daiso_cnt['개수'][i] + park_cnt['개수'][i]+study_cnt['개수'][i]+fastfoods_cnt['개수'][i]+starbucks_cnt['개수'][i] !=7:
        if store_cnt['개수'][i]+daiso_cnt['개수'][i] + park_cnt['개수'][i]+study_cnt['개수'][i]+fastfoods_cnt['개수'][i]+starbucks_cnt['개수'][i] >=5:
                    cnt+=1
                    folium.Marker((zig["위도"][i], zig["경도"][i]),
                    popup = folium.Popup(f"""
<div align='center'>
  <img alt='' draggable='false' style='zoom: 22%' src='https://ic.zigbang.com/ic/items/31449074/1.jpg?w=800&amp;h=600&amp;q=70&amp;a=1'>
  <br/>
  월세 : {zig['월세(만원)'][i]} 보증금 : {zig['보증금(만원)'][i]}
  <br/>
  이 집 근처에는 무엇이 있을까요?
  <br/>
<div/>
<div align='left'>
역세권 정보 : {subway_lst['개수'][i]} / if(subway_lst['개수'][i] != 0){subway_lst['역목록'][i]} <br/> 
편의점 : {store_cnt['유무'][i]} <br/> 다이소 : {daiso_cnt['유무'][i]} <br/> 
공원 : {park_cnt['유무'][i]} <br/> 스터디 카페 : {study_cnt['유무'][i]} <br/> 
스타벅스 : {starbucks_cnt['유무'][i]} <br/> 
패스트푸드 : {fastfoods_cnt['유무'][i]} <br/>
<div/>
""",
            max_width='1500'),
                    tooltip = f"{zig['구'][i]} {zig['동'][i]}",
                    icon = folium.Icon(color="green")                   
                    ).add_to(s_map)
    else:
        cnt+=1
        folium.Marker((zig["위도"][i], zig["경도"][i]),
        popup = folium.Popup(f"""
    <div align='center'>
    <img alt='' draggable='false' style='zoom: 22%' src='https://ic.zigbang.com/ic/items/31449074/1.jpg?w=800&amp;h=600&amp;q=70&amp;a=1'>
    <br/>
    이 집 근처에는 무엇이 있을까요?
    <br/>
    <div align='left'>
    월세 : {zig['월세(만원)'][i]} 보증금 : {zig['보증금(만원)'][i]} <br/> 
    역세권 정보 : {subway_lst['개수'][i]} / {subway_lst['역목록'][i]} <br/> 
    편의점 : {store_cnt['유무'][i]} <br/> 다이소 : {daiso_cnt['유무'][i]} <br/> 
    공원 : {park_cnt['유무'][i]} <br/> 스터디 카페 : {study_cnt['유무'][i]} <br/> 
    스타벅스 : {starbucks_cnt['유무'][i]} <br/> 
    패스트푸드 : {fastfoods_cnt['유무'][i]} <br/>
    <div/>
    """,
    max_width='1500'),                  
        tooltip = f"{zig['구'][i]} {zig['동'][i]}",
        icon = folium.Icon(color="red",icon='star')                   
        ).add_to(s_map)
        
s_map