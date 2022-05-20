'''
데이터 시각화 지도상에 위치표시를 위한 모듈입니다.

위치정보의 위도, 경도를 알아오기 위해 카카오API를 사용합니다.
'''
from .visualization_abstract import *
from .visualization_barh import *

import requests
from tqdm import tqdm   # 데이터저장 진행과정을 보여주기 위해 사용
import folium as g # 데이터 시각화를 위해 사용
import sys
import io # 파일관리를 위해 사용
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

# 정제-지도상 위치 표시 시각화를 위한 클래스 입니다.
class VisualizationMap(Visualization):
    # 추상 클래스를 상속받았았기 때문에 @abstractmethod가 붙은 추상 메서드를 모두 구현해야 합니다.
    def __init__(self, keyword):
        # raw : 가공되지 않은
        self.__raw_data = pd.read_csv(f"./data/insta_crawling_{keyword}_900개.csv")

    def set_raw_data(self, keyword):
        self.__raw_data = pd.read_csv(f"./data/insta_crawling_{keyword}_900개.csv")
        
    def get_raw_data(self):
        return self.__raw_data

    # 본문내용을 기준으로 중복인 게시글을 제거합니다.
    def drop_duplicate_raw_data(self):
        self.__raw_data.drop_duplicates(subset=["content"], inplace=True)   # 원본을 변경합니다.

    # 원시데이터에서 위치정보 항목만을 추출합니다.
    def refine_raw_data(self):
        location_total = []

        for location in self.__raw_data["place"]:
            if pd.isnull(location) == False: # 판다스를 이용한 결측치 처리
                location_total.append(location)
       
        return location_total

        # 다른방법
        # location_counts = self.__raw_data["place"].value_counts() # series형태로 반환됩니다.
        # location_counts = self.__raw_data["place"] # series형태로 반환됩니다.

        # locations = list(location_counts.index) # series의 인덱스 값은 위치정보 입니다.

        # return locations

    # 원시데이터에서 연관없는 데이터를 제거합니다.
    def remove_unrelated_data(self, keyword, location_total):
        # 위치정보 중복처리
        location_duplicated = []

        for location in location_total:
            if location not in location_duplicated:
                location_duplicated.append(location)

        return location_duplicated

    # 카카오 API를 통해 위도, 경도, 카카오 위치명을 데이터로 반환하는 내부메서드입니다.
    def __find_places_use_kakaoAPI(self, searching):
        url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={searching}'
        headers = {"Authorization" : "KakaoAK ee47317fe29597b8b01687a06822e004"}

        places = requests.get(url, headers=headers).json()["documents"]

        place = places[0]           # 인스타 위치명
        name = place["place_name"]  # 카카오 위치명
        y = place["y"]              # 위도
        x = place["x"]              # 경도

        data = name, y, x, searching

        return data
     
    # 정제과정을 거친 위치정보 데이터를 가지고
    # __find_places_use_kakaoAPI() 메서드를 통해 가공된 데이터를 저장합니다.
    # 추후 DB에 저장할 예정입니다.
    def save_locations_information(self, locations_selected, keyword):
        locations_information = []

        # 진행도에 대한 설명 추가
        print("kakaoAPI를 통한 위도,경도 추가 작업을 진행합니다.")
        for location in tqdm(locations_selected):
            try:
                data = self.__find_places_use_kakaoAPI(location)
                locations_information.append(data)
            except:
                pass
        print()
        
        # map 사용시 index out of range 에러
        # iterater에서 띄어쓰기된 글자 들어갈때 에러 같은데..
        # 추후 해결
        # try:
        #     data = map(self.__find_places_use_kakaoAPI, tqdm(locations_selected))
        #     locations_information.append(data)
        # except:
        #     pass

        # 저장경로 설정
        self.make_save_directory() # abs묘듈에 존재

        locations_inform_df = pd.DataFrame(locations_information)
        locations_inform_df.columns =["카카오위치명", "위도", "경도", "인스타위치명"]

        # 카카오위치명 기준으로 중복처리
        # 데이터 베이스에서 기본키로 사용하기 위해 추가
        locations_inform_df.drop_duplicates(subset=["카카오위치명"], inplace=True)

        path = f"./data/location_information/insta_location_information_{keyword}.csv"
        locations_inform_df.to_csv(path, encoding = 'utf-8-sig', index = False)

        # print(f"{path}에 저장 하였습니다.")

        return path

# GUI로 보여주기 위한 함수 입니다.
def visual_map_app_execute(map, app):
    web_view = QWebEngineView()
    web_view.setWindowTitle("위치 정보")
    web_view.setHtml(map.getvalue().decode()) # 저장된 데이터를 해석합니다.
    web_view.resize(1024, 768)
    web_view.show()

    app.exec()
    
# VisualizationMap 클래스를 활용한 시각화 전체 과정입니다.
# 지도 시각화를 위한 gui 사용에서 어플리케이션 객체를 전달인수로 받습니다. 
def visual_map_process(keyword, app):
    # step0 - 객체 생성
    obj_insta_map = VisualizationMap(keyword)
    # step1 - 중복 제거
    obj_insta_map.drop_duplicate_raw_data()
    # step2 - 위치정보 추리기
    location_total = obj_insta_map.refine_raw_data()
    # step3 - 키워드별 연관없는 위치정보 제거
    locations_selected = obj_insta_map.remove_unrelated_data(keyword, location_total)
    # locations_selected = locations
    # step4 - 위도, 경도 추가등의 데이터 가공 및 저장
    # 부모 클래스 파일에 import os 존재
    path = f"./data/location_information/insta_location_information_{keyword}.csv"
    if os.path.isfile(path):
        print("정제된 파일이 이미 존재합니다. 해당파일로 지도 시각화를 진행하겠습니다.")
        print()
        save_path = path
    else:
        save_path = obj_insta_map.save_locations_information(locations_selected, keyword)
    # step5 - 시각화
    start_location = {'모란' : [37.43194, 127.12890],
                    '홍대' : [37.55769, 126.92448],
                    '판교' : [37.39499, 127.11116]}

    g_map = g.Map(location = start_location[keyword], zoom_start=16)

    insta_locations_df = pd.read_csv(save_path)
    # insta_locations_df.head()

    # for i in range(len(insta_locations_df)):
    #     latitude = insta_locations_df.loc[i]["위도"]
    #     longtitude = insta_locations_df.loc[i]["경도"]
    #     name  = insta_locations_df.loc[i]["카카오위치명"]

    #     marker = g.Marker(location=[latitude, longtitude],
    #                     popup=name, icon=g.Icon(color="red"))

    #     marker.add_to(g_map)

    # 내장함수 zip() 활용
    for latitude, longtitude, name in zip(insta_locations_df["위도"],
                                            insta_locations_df["경도"],
                                            insta_locations_df["카카오위치명"]):
        marker = g.Marker(location=[latitude, longtitude],
                        popup=name, icon=g.Icon(color="red"))

        marker.add_to(g_map)

    
    # folium을 활용한 지도시각화
    # g_map 객체 호출로 interactive window 콘솔창에서 확인이 가능합니다.(최상위에서만)
    # 하지만 함수 내부에서의 g_map 객체 호출 후 외부에서 함수 호출로 사용할 땐
    # 함수 호출만으로는 콘솔창에 표시되지 않습니다.
    # 최상위의 호출로만 사용되야 되기 때문에 return으로 값을 받아와 다시 객체 홀출로 사용하여야 하고
    # 모듈을 사용한 호출에서는 if __name__ == "__main__": 안에서 객체 호출을 하여야하는데
    # 이경우 최상위가 아니기 때문에 콘솔창에 출력이 되지않습니다.
    # 이를 해결하기 위해
    # html로 저장한 후 파일을 들여다봐 확인이 가능하지만
    # 좀더 프로그램 실행중의 과정으로 보여주기 위해
    # PyQt5의 웹엔진을 활용 GUI를 도입 새로운 창으로 시각화 결과를 보여줍니다.

    # io.BytesIO()
    # 바이트 배열을 이진 파일로 다룰 수 있게 해주는 클래스
    data = io.BytesIO() # 새로운 창에서 보여줄수 있게 데이터를 저장합니다.
    g_map.save(data, close_file=False) # 저장시 파일을 닫으면 접근할 수 없게 됩니다.                  
    # g_map.save(data) 
    # g_map.save("./data/insta_map.html")

    # 지도화
    visual_map_app_execute(data, app)

    # 이벤트 루프 동시사용 문제
    # 바그래프
    # compare_bar = VisualizationBarhPlot(location_total)
    # case = 'location'
    # fig = None
    # compare_bar.visualization_barh(keyword, case, fig)

    