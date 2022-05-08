from django.db import models

import folium
import json
import pandas as pd
import numpy as np
from haversine import haversine

dong_path = './visualization/data/seouldongfixed.geojson'
dong = json.load(open(dong_path,encoding = 'UTF-8'))

class ZigBang:
    def __init__(self, path):
        self.path = path
    def load_data(self):
        zigbang = pd.read_csv(self)
        zigbang = zigbang.drop("Unnamed: 0",axis=1)

        return zigbang

    def lease_type(x,zigbang):
    
        def fee_max(x,zigbang):
            mask = zigbang["월세"] <= x
            zigbang = zigbang[mask].reset_index(drop=True)

            return zigbang
    
        def deposit_max(x,zigbang):
            mask = (zigbang["보증금"] <= x) & (zigbang["보증금"] >= 100)
            zigbang=zigbang[mask].reset_index(drop=True)

            return zigbang
    
        if x == "월세":
            mask = zigbang['전세/월세'] == "월세"
            zigbang=zigbang[mask].reset_index(drop=True)
            
            y = input("월세 상한 : ")
            zigbang = fee_max(int(y), zigbang)
    
            z = input("보증금 상한 : ")
            zigbang = deposit_max(int(z), zigbang)
    
        elif x == "전세":
            mask = zigbang['전세/월세'] == "전세"
            zigbang=zigbang[mask].reset_index(drop=True)
    
            z = input("보증금 상한 : ")
            zigbang = deposit_max(int(z), zigbang)
        
        return zigbang
    
zig=ZigBang.load_data('./visualization/data/zigbang.csv')
zig = ZigBang.lease_type(input("월세/전세 : "),zig)

# 지하철

def func_sub(zig):

    sub_path = './visualization/data/sub_station.csv'
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

    store_path = './visualization/data/store.csv'
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

    daiso_path = './visualization/data/seoul_daiso.csv'
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

    park_path = './visualization/data/seoul_ecotourism_xy.csv'
    park = pd.read_csv(park_path)

    park_com=pd.DataFrame(index=range(len(zig)), columns=['개수','유무'])

    for i in range(len(zig)):
        mask = ((park['x'] - zig.loc[i,"경도"])**2 + (park['y'] - zig.loc[i,"위도"])**2)**0.5 <= 0.0075
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

    sc_path = './visualization/data/studycafe.csv'
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

    star_path = './visualization/data/starbucks.csv'
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

    fast_path = './visualization/data/fastfood.csv'
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

# 병원

def func_hospital(zig):

    hosp_path = './visualization/data/seoul_hospital_loc.csv'
    hospital = pd.read_csv(hosp_path)
    
    hospital_com = pd.DataFrame(index=range(len(zig)), columns=['개수','유무'])

    for i in range(len(zig)):
        mask = ((hospital['경도'] - zig.loc[i,"경도"])**2 + (hospital['위도'] - zig.loc[i,"위도"])**2)**0.5 <= 0.0025
        sty_mask=hospital[mask].reset_index()

        if len(sty_mask) >= 1:
            hospital_com.loc[i,["개수"]]=1
            hospital_com.loc[i,["유무"]]='있음'
        else:
            hospital_com.loc[i,["개수"]]=0
            hospital_com.loc[i,["유무"]]='없음'
        
    return hospital_com

subway_lst = func_sub(zig)
daiso_cnt = func_daiso(zig)
store_cnt = func_store(zig)
park_cnt = func_park(zig)
study_cnt = func_studycafe(zig)
starbucks_cnt = func_starbucks(zig)
fastfoods_cnt = func_fastfoods(zig)
hospital_cnt = func_hospital(zig)
