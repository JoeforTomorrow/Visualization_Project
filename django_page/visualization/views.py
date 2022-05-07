from django.shortcuts import render
from .models import *
import folium



def home(request):
    
    s_map = folium.Map(
        location=[37.5642135, 127.0016985],
        zoom_start=11,
#        width = '70%', height = '70%'
        )
    
    
    folium.Choropleth(geo_data=dong,
                      data=zig,
                      fill_color='Greens',
                      fill_opacity=0.5,
                      line_opacity=0.2,
                      columns=['동','월세'],
                      key_on = 'feature.properties.EMD_KOR_NM',
                      legend_name="월세"
                ).add_to(s_map)
    
    folium.LayerControl().add_to(s_map)
    
    cnt=0
    for i in range(len(zig)):
        if (subway_lst['유무'][i] + store_cnt['개수'][i] + park_cnt['개수'][i] + starbucks_cnt['개수'][i] + hospital_cnt['개수'][i]) == 5:
            cnt+=1
            folium.Marker((zig["위도"][i], zig["경도"][i]),
            popup = folium.Popup(f"""
<div align='center'>
  <br/>
  <img alt='' draggable='false' src='{zig['이미지'][i]}?w=150&amp;h=120&amp;q=70&amp;a=1'><br/>
  <a href='{zig['주소'][i]}'>해당 페이지로 이동</a><br/>
  <span>월세 : {zig['월세'][i]} 보증금 : {zig['보증금'][i]}</span><br/>
  <div align='center'><strong>이 집 근처에는...</strong>
    <div align='left'>
      <span style="font-weight:bold">주변 역 정보</span> : {subway_lst['개수'][i]}개 / {subway_lst['역목록'][i]}<br/>
      <span style="font-weight:bold">편의점</span> : {store_cnt['유무'][i]}<br/>
      <span style="font-weight:bold">다이소</span> : {daiso_cnt['유무'][i]}<br/>
      <span style="font-weight:bold">공원</span> : {park_cnt['유무'][i]}<br/>
      <span style="font-weight:bold">스터디 카페</span> : {study_cnt['유무'][i]}<br/>
      <span style="font-weight:bold">스타벅스</span> : {starbucks_cnt['유무'][i]}<br/>
      <span style="font-weight:bold">패스트푸드</span> : {fastfoods_cnt['유무'][i]}<br/>
      <span style="font-weight:bold">병원</span> : {hospital_cnt['유무'][i]}
    </div>
  </div>
</div>
""",
                max_width='1500'),
                        tooltip = f"{zig['구'][i]} {zig['동'][i]}",
                        icon = folium.Icon(color="red", icon='star')                   
                        ).add_to(s_map)
        elif (subway_lst['유무'][i]==1) and (store_cnt['개수'][i] + daiso_cnt['개수'][i] + park_cnt['개수'][i] + study_cnt['개수'][i] + fastfoods_cnt['개수'][i] + starbucks_cnt['개수'][i] + hospital_cnt['개수'][i] >= 4):
            cnt+=1
            folium.Marker((zig["위도"][i], zig["경도"][i]),
            popup = folium.Popup(f"""
<div align='center'>
  <br/>
  <img alt='' draggable='false' src='{zig['이미지'][i]}?w=150&amp;h=120&amp;q=70&amp;a=1'><br/>
  <a href='{zig['주소'][i]}'>해당 페이지로 이동</a><br/>
  <span>월세 : {zig['월세'][i]} 보증금 : {zig['보증금'][i]}</span><br/>
  <div align='center'><strong>이 집 근처에는...</strong>
    <div align='left'>
      <span style="font-weight:bold">주변 역 정보</span> : {subway_lst['개수'][i]}개 / {subway_lst['역목록'][i]}<br/>
      <span style="font-weight:bold">편의점</span> : {store_cnt['유무'][i]}<br/>
      <span style="font-weight:bold">다이소</span> : {daiso_cnt['유무'][i]}<br/>
      <span style="font-weight:bold">공원</span> : {park_cnt['유무'][i]}<br/>
      <span style="font-weight:bold">스터디 카페</span> : {study_cnt['유무'][i]}<br/>
      <span style="font-weight:bold">스타벅스</span> : {starbucks_cnt['유무'][i]}<br/>
      <span style="font-weight:bold">패스트푸드</span> : {fastfoods_cnt['유무'][i]}<br/>
      <span style="font-weight:bold">병원</span> : {hospital_cnt['유무'][i]}
    </div>
  </div>
</div>
        """,
        max_width='1500'),                  
            tooltip = f"{zig['구'][i]} {zig['동'][i]}",
            icon = folium.Icon(color="green",icon="home")                   
            ).add_to(s_map)
    
    maps=s_map._repr_html_()
            
    return render(
        request,
        'visualization/index.html',
        {'map':maps}
    )
            
    
    
    