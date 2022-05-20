'''
데이터 시각화 가로형 막대그래프를 위한 모듈입니다.
'''
from collections import Counter # 빈도수 확인을 위한 모듈
import matplotlib.pyplot as plt # 데이터 시각화를 위한 모듈

# 막대 그래프 시각화를 위한 클래스 입니다.
class VisualizationBarhPlot:
    # 본문을 기준으로한 중복제거
    # 워드클라우드에서 사용될경우 해시태그 추출
    # 연관성 없는 해시태그 제거
    # 순의 정제 과정을 통해 나온 자료를 사용합니다
    def __init__(self, data):
        self.__data = data

    def set_raw_data(self, data):
        self.__data = data

    def get_raw_data(self):
        return self.__data

    def visualization_barh(self, keyword, case, fig):
        
        if case == 'tag':
            case_cout = 30
            case_name = '해시태그'
        elif case == 'location':
            case_cout = 10
            case_name = '위치정보'
        else:
            pass

        data_count = Counter(self.__data)
        select_list = data_count.most_common(case_cout) # 리스트

        name = []
        count = []

        for tuple_data in select_list:
            name.append(tuple_data[0])
            count.append(tuple_data[1])

        # 빈도수가 많은것 부터 보여주기 위한 뒤집기
        name.reverse()
        count.reverse()

        def visualize():
            plt.title(f"{keyword} {case_name} 상위 {case_cout}개 빈도수", size=15)
            plt.barh(range(case_cout), count)
            
            plt.xlabel('빈도수', labelpad=15)
            plt.yticks(range(case_cout), name)

            plt.show()

        if fig is None:
            plt.figure(f'{keyword}', figsize=(10, 5),)
            plt.rc("font", family="Malgun Gothic")

            visualize()
        else:
            fig.add_subplot(1,2,2)
            visualize()




