'''
크롤링을 위한 속성과 메소드를 제공합니다.
'''
from bs4 import BeautifulSoup   # 웹 페이지를 표현하는 HTML을 분석하기 위한 모듈
# 크롤링을 위한 웹 제어 목적으로 사용하는 모듈
# 인스타그램사이트의 경우 자바스크립트로 만들어져
# 클릭등 사용자의 행동에 태그가 생성되는 등의 이유로
# requests통한 크롤링 방식에는 한계가 있기 때문에 selenium을 사용
from selenium import webdriver
# DeprecationWarning: executable_path has been deprecated, please pass in a Service object
# selenium 버전 warring해결을 위한 모듈
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# ERROR:device_event_log_impl.cc(214)] [21:24:45.043]
# Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed.
# 에러를 해결하기 위한 모듈 추가
from selenium.webdriver.chrome.options import Options
# 웹 제어에 사용될 모듈
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pickle   # 쿠키를 객체 자체 바이너리로 저장,로드 하기 위한 모듈
import re   # 정규 표현식 사용을 위한 모듈
# import unicodedata
import pandas as pd # 데이터 구조 제공 패키지

class InstagramCrawler:
    def __init__(self, u_id, u_pw, query, count, f_name):
        # webdriver는 싱글스레드 멀티쓰레딩을 지원하지않는다.
        # 초기화 부분에서 실행되면 handle오류 발생
        # self.__driver = self.__init_driver()        
        self.__data_list = []
        # 사용자의 정보로 부터 초기화
        self.__user_id = u_id
        self.__user_pw = u_pw
        self.__query_txt = query
        self.__crawling_count = count
        self.__save_file_name = f_name

    def init_driver(self):
        # 에러 해결및 브라우저 크기 조정
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        options.add_argument("--window-size=900,900") # 브라우저 크기 조정 # 띄어쓰기 안됨

        driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
        # 암묵적으로 웹 자원 로드를 위해 3초 기다려줍니다.
        # driver.implicitly_wait(3)
        # 인스타그램 접속
        url = "https://www.instagram.com/"
        driver.get(url)

        return driver

    def get_driver(self):
        return self.__driver

    def set_data_list(self, data):
        self.__data_list.append(data)

    def get_data_list(self):
        return self.__data_list

    def get_id(self):
        return self.__user_id

    def get_pw(self):
        return self.__user_pw

    def get_query_txt(self):
        return self.__query_txt

    def get_crawling_count(self):
        return self.__crawling_count

    def get_save_file_name(self):
        return self.__save_file_name

    def login_instagram(self, driver, user_id, user_pw):
        input_id = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
        input_id.send_keys(user_id)
        input_pw = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
        input_pw.send_keys(user_pw)
        input_pw.send_keys(Keys.ENTER)

    def make_cookies(self, driver, user_id):
        # 최초 1회 로그인 정보를 쿠키에 저장할 때 사용합니다.
        with open(f"./cookies/instagram_{user_id}_cookies.pkl", "wb") as f:
            pickle.dump(driver.get_cookies(), f)

    def load_cookies(self, driver, user_id):
        with open(f"./cookies/instagram_{user_id}_cookies.pkl", "rb") as f:
            cookies = pickle.load(f)
            
            for cookie in cookies:
                driver.add_cookie(cookie)

    def search_tag(self, text):
        url = "https://www.instagram.com/explore/tags/" + str(text)

        return url

    # 첫 번째 게시물 클릭
    def select_first(self, driver):
        xpath = '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div[1]/div[2]'
        first = driver.find_element(By.XPATH, xpath)
        first.click()

    # 다음 게시글 조회
    def move_next(self, driver): 
        right = driver.find_element(By.CSS_SELECTOR, '[aria-label = "다음"]')
        right.click()

     # 본문내용, 작성일자, 좋아요 수, 위치 정보, 해시태그를 수집합니다.
    def get_content(self, driver):
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        # 본문내용
        try:
            content = soup.find("div", class_ = "MOdxS").find("span").text             
        except:
            content = "None"
        # 작성일자
        try:
            date = soup.find("time", class_ = "_1o9PC").attrs["datetime"][:10]
        except AttributeError as exception:
            date = "None"
        # 좋아요 수
        try:
            tag_class_name = "_7UhW9 xLCgt qyrsm KV-D4 fDxYl T0kll"            
            like = soup.find("div", class_ = tag_class_name).find("span").text
        except:
            like = "None"
        # 위치정보
        try:
            place = soup.find("div", class_ = "M30cS").text
        except:
            place = "None"
        # 해시태그
        # tags = re.findall(r"#[^s#,\\]+", content) # 해시태그 뒤에 내용까지 포함됨
        hashtag_regex = "#[0-9a-zA-Z가-힣]*" 
        p = re.compile(hashtag_regex)

        tags = p.findall(content)
        
        data = [content, date, like, place, tags]

        return data

    # 데이저 저장 
    def save_data(self, file_name):
        results = self.get_data_list()
        results_df = pd.DataFrame(results)
        results_df.columns = ["content", "date", "like", "place", "tags"]
        
        case = file_name.split(".")[-1] # 파일저장 형식

        if case == "csv":
            results_df.to_csv(file_name, encoding = 'utf-8-sig', index = False)
        elif case == "json":
            results_df.to_json(file_name)
        else:
            pass