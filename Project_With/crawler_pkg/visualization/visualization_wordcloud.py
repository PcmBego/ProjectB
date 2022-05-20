'''
데이터 시각화 워드클라우드를 위한 모듈입니다.
'''
from .visualization_abstract import *
from .visualization_barh import *

from collections import Counter # 빈도수 확인을 위한 모듈
import matplotlib.pyplot as plt # 데이터 시각화를 위한 모듈
from wordcloud import ImageColorGenerator, WordCloud # 시각화를 워드클라우드로 하기 위한 모듈
import platform # 플랫폼별 액세스를 위한 모듈
from PIL import Image # 워드 클라우드 모양설정을 위한 모듈
import numpy as np # 이미지 픽셀 값 배열 형태 변환을 위한 모듈


# 웹 크로링을 통해 추출된 자료를 바탕으로 원하는 결과물을 얻기 위한 정제 과정을 수행합니다.
# 정제-워드클라우드 시각화를 위한 클래스 입니다.
class VisualizationWordCloud(Visualization):
    def __init__(self, keyword):
        # raw : 가공되지 않은 - 원시데이터
        self.__raw_data = pd.read_csv(f"./data/insta_crawling_{keyword}_900개.csv")

    def set_raw_data(self, keyword):
        self.__raw_data = pd.read_csv(f"./data/insta_crawling_{keyword}_900개.csv")

    def get_raw_data(self):
        return self.__raw_data

    # 본문내용을 기준으로 중복인 게시글을 제거합니다.
    def drop_duplicate_raw_data(self):
        self.__raw_data.drop_duplicates(subset=["content"], inplace=True)   # 원본을 변경합니다.

    # 원시데이터에서 해시태그 항목만을 추출합니다.
    def refine_raw_data(self):
        tags_total = []

        for tags in self.__raw_data["tags"]:
            tags_list = tags[2:-2].split("', '")    # ', ' 기준으로 나누어 리스트로 만들어 줍니다.
            for tag in tags_list:
                tags_total.append(tag)

        return tags_total

    # 키워드별 해시태그 중 연관없는 해시태그를 제거합니다.
    def remove_unrelated_data(self, keyword, tags_total):
        dump_word = ['', '#', '#맞팔', '#좋아요반사',  '#선팔하면맞팔', '#선팔', '#좋아요', '#좋반', '#팔로우', '#선팔맞팔'
                    ,"#맞팔환영", '#좋아요테러', '#followforfollowback', '#likeforlikes', '#맞팔선팔', '#맞팔해요', '#맞팔선팔환영'
                    ,'#선팔맞팔환영', '#fff', '#follow', '#likeforfollow', '#followme', '#like4likes', '#follow4followback', '#f4f']

        if keyword == "모란":
            dump_word += [] # 추가 필요
        elif keyword == "판교":
            dump_word += []    # 추가 필요
        elif keyword == "홍대":
            dump_word += [] # 추가 필요
        else:
            pass

        tags_total_selected = []
        count_unrelated_data = 0

        for tag in tags_total:
            if tag.strip() not in dump_word:
                tags_total_selected.append(tag)
            else:
                count_unrelated_data += 1

        tags_total_cout = len(tags_total)
        
        print(f"총 {tags_total_cout}개의 해시태그들 중 {count_unrelated_data}개의 연관없는 해시태그가 제거 되었습니다.")
        print()

        return tags_total_selected

# VisualizationWordCloud 클래스를 활용한 시각화 전체 과정입니다.
def visual_wordcloud_process(keyword):
    # step0 - 객체 생성
    obj_insta_wordcloud = VisualizationWordCloud(keyword)
    # step1 - 중복 제거
    obj_insta_wordcloud.drop_duplicate_raw_data()
    # step2 - 테그 추리기
    tags_total = obj_insta_wordcloud.refine_raw_data()
    # step3 - 키워드별 연관없는 태그 제거
    tags_total_selected = obj_insta_wordcloud.remove_unrelated_data(keyword, tags_total)
    # step4 - 빈도수 확인
    tags_count_selected = Counter(tags_total_selected)
    # step5 - 시각화
    # 플랫폼별 액세스
    if platform.system() == "Windows":   # 윈도우 환경일 경우
        font_path_window = "c:/Windows/Fonts/malgun.ttf"
    else:   # 다른 환경일 경우 추가
        pass

    # 키워드에 맞는 이미지 파일을 읽어옵니다.
    img = Image.open(f"./crawler_pkg/visualization/img/{keyword}.png") 

    # 워드클라우드에 적합한 형태로 변환하기
    img.convert("RGBA")
    mask = Image.new("RGB", img.size, (255, 255, 255))
    mask.paste(img, img)
    mask_arr = np.array(mask) # 펙셀 값 배열 형태 변환

    wordcloud = WordCloud(font_path=font_path_window, background_color="white"
                        , max_words=100, relative_scaling=0.3
                        , width=800, height=400
                        , mask=mask_arr)
    wordcloud.generate_from_frequencies(tags_count_selected)

    # 색상 관련
    color_mask = np.array(img)
    image_colors = ImageColorGenerator(color_mask)
    wordcloud.recolor(color_func=image_colors)

    fig =plt.figure(f'{keyword}', figsize=(25, 10),)
    fig.add_subplot(1,2,1)

    plt.rc("font", family="Malgun Gothic")
    plt.imshow(wordcloud, interpolation='bilinear') # interpolation : 보간법
    plt.axis("off") # 그래프 축 제거

    # 비교본 바 그래프 추가
    compare_bar = VisualizationBarhPlot(tags_total_selected)
    case = 'tag'
    compare_bar.visualization_barh(keyword, case, fig)

    # plt.show()