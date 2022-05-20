'''
크롤링 진행 과정을 함수화한 모듈입니다.
'''
import os    # 데이터 저장 경로 설정을 위한 모듈
# 셀레니움을 통한 웹제어에서 브라우저가 그려지는 시간을 가지기 위해,
# 사이트가 봇으로 판단하는걸 피하기 위한 딜레이를 위한 모듈
import time
from tqdm import tqdm   # 진행상황 확인을 위한 모듈
from selenium.common.exceptions import NoSuchElementException   # 인스타그램 차단시 예외처리를 위한 모듈
# 다음 게시글에서 머무는 시간을 랜덤하게 주기위한 모듈
# 봇으로 차단되는걸 방지하기 위해
import random

# obj_insta_crawler -> insta_crawler모듈의 InstagramCrawler클래스로 생성될 객체
def crawling_process(obj_insta_crawler):
    driver = obj_insta_crawler.init_driver()
    time.sleep(3)

    # 로그인
    # 간혹 인터넷 연결 실패 에러 발생
    tester_id = obj_insta_crawler.get_id()
    tester_pw = obj_insta_crawler.get_pw()

    # 쿠키방식을 사용하는 이유
    # 1. 테스트를 위한 잦은 접속시 인터넷 접속 에러방지를 위해 로그인과정 우회
    # 2. 인스타그램 업데이트로 인한 로그인 페이지 태그 변경시 nosuchelement오류 우회 - 발견 시 수정 필요
    if os.path.isfile(f"./cookies/instagram_{tester_id}_cookies.pkl"): # 현재 폴더에 쿠키파일이 존재한다면
        obj_insta_crawler.load_cookies(driver, tester_id)
        driver.refresh()
    else:
        obj_insta_crawler.login_instagram(driver, tester_id, tester_pw)
        time.sleep(3) # 다음 페이지가 브라우저에 그려지도록 기다려줍니다.
        # 쿠키 만들기
        obj_insta_crawler.make_cookies(driver, tester_id)

    # 해시 태그 검색 주소 얻기
    query_txt = obj_insta_crawler.get_query_txt()
    result_url = obj_insta_crawler.search_tag(query_txt)
    # 검색 결과 페이지 열기
    driver.get(result_url)
    time.sleep(5)

    # 첫 번재 게시물 클릭
    obj_insta_crawler.select_first(driver)
    time.sleep(3)

    # 데이터 수집
    crawling_count = obj_insta_crawler.get_crawling_count()
    monitoring_count = 1

    for i in tqdm(range(crawling_count)):   # tqdm 진행상황 콘솔창 표시
        try:
            data = obj_insta_crawler.get_content(driver)
            obj_insta_crawler.set_data_list(data)
            obj_insta_crawler.move_next(driver)

        # 인스타그램에서 막을 경우
        # 막히지 전까지의 추출 결과를 저장하기 위해
        except NoSuchElementException as exception:
            print(f"exception: {exception}")
            print("{monitoring_count}번째 추출중 작업이 중단되었습니다.") 
            break

        else:            
            monitoring_count += 1
            # 봇으로 차단되는걸 방지하기 위해 게시글에서 머무는 시간을 랜덤하게 줍니다.
            variable  = random.randint(6, 8) # 6, 7, 8 중 하나
            time.sleep(variable)

    # 데이터 저장경로 설정
    current_directory = os.getcwd()
    data_directory = current_directory + "\\" + "data"

    if os.path.isdir(data_directory): # 설정경로에 디렉토리가 존재 한다면
        os.chdir(data_directory)
    else:
        os.makedirs(data_directory)
        os.chdir(data_directory)

    # 데이터 저장
    save_file_name = obj_insta_crawler.get_save_file_name()
    obj_insta_crawler.save_data(save_file_name)
    # 데이터 저장 결과 출력
    print_save_info(data_directory, save_file_name)   

    # 브라우저 닫기
    driver.quit()


# 콘솔 테스트를 위한 출력함수 정의
def print_save_info(path, f_name) -> None:  # -> None 함수의 리턴을 명시해 줍니다.
    result = path + f_name
    print(f"{result}에 저장 하였습니다.")
