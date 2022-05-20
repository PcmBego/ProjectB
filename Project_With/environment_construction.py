'''
여러환경에서 사용될 수 있도록 프로젝트에 필요한 외부 모듈들을 설치합니다.

프로젝트 진행중 필요한 모듈을 추가 예정입니다. 
'''
import sys
import subprocess

def check_module_process():
    '''
    프로그램에서 사용될 외부 모듈 설치를 진행하는 함수입니다.
    '''
    print("=" * 80)
    print("[프로그램에서 사용될 외부 모듈 설치를 진행합니다.]")
    # pip 관리 시스템 업그레이드
    print("PIP(Python Package Index)를 업데이트 합니다.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    print("=" * 80)
    print()

    # 크롤링
    print("=" * 80)
    print("[크롤링에 사용될 모듈들을 확인합니다.]")
    print("01 bs4 모듈 확인 중입니다.")
    try:    
        import bs4
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "BeautifulSoup4"])

    print("02 selenium 모듈 확인 중입니다.")
    try:
        import selenium
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "selenium"])

    print("03 webdriver_manager 모듈 확인 중입니다.")
    try:    
        import webdriver_manager
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "webdriver_manager"])

    print("04 pandas 모듈 확인 중입니다.")
    try:    
        import pandas
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pandas"])
        
    print("05 tqdm 모듈 확인 중입니다.")
    try:   
        import tqdm
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "tqdm"])

    print("06 기타 모듈 확인 중입니다.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "lxml"]) # 빠른 파싱을 위해
    print("=" * 80)
    print()

    # 시각화
    print("=" * 80)
    print("[시각화에 사용될 모듈들을 확인합니다.]")

    print("01 matplotlib 모듈 확인 중입니다.")
    try:
        import matplotlib
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "matplotlib"])

    print("02 wordcloud 모듈 확인 중입니다.")
    try:
        import wordcloud
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "wordcloud"])
    
    print("03 folium 모듈 확인 중입니다.")
    try:
        import folium
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "folium"])

    print("=" * 80)
    print()

    # GUI
    print("=" * 80)
    print("[GUI에 사용될 모듈들을 확인합니다.]")
    print("01 PyQt5 모듈 확인 중입니다.")
    try:
        import PyQt5
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "PyQt5"]) 
    
    print("02 PyQt5.QtWebEngineWidgets 모듈 확인 중입니다.")
    try:
        import PyQt5.QtWebEngineWidgets # GUI 웹엔진 사용을 위해 (추가 설치 필요)
    except:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "PyQtWebEngine"])

    print("=" * 80)
    print()

    # 데이터 베이스 연동
    # try:
    #     import pymysql
    # except:
    #     subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pymysql"])

    # 버전 확인
    print("=" * 80)
    print("[버전 정보]")
    # 크롤링
    print(f"python : {sys.version}")
    print(f"bs4 : {bs4.__version__}")
    print(f"selenium : {selenium.__version__}")
    print(f"webdriver_manager : {webdriver_manager.__version__}")
    print(f"tqdm : {tqdm.__version__}")

    # 시각화
    print(f"matplotlib : {matplotlib.__version__}")
    print(f"wordcloud : {wordcloud.__version__}")
    print(f"folium : {folium.__version__}")

    # GUI
    # print(PyQt5.ver)
    # print(PyQt5.QtWebEngineWidgets.__version__)

    # 데이터 베이스 연동
    # print(f"pymysql : {pymysql.__version__}")
    print("=" * 80)
    print()

if __name__ == "__main__":
    check_module_process()
