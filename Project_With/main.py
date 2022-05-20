'''
크롤링 테스트용 메인입니다.
'''
from crawler_pkg import * # 크롤링, 시각화 기능을 제공하는 패키지입니다.
# 멀티프로세싱을 위한 모듈
# multiprocess의 pool은 top-level method에서만 사용할 수 있습니다.
from multiprocessing import Pool

# 사용자 정보를 자동화 함
# 전달 인수: query_list - 정의어 목록
def automate_user_data(user_query_list):
    # 사용자 입력정보
    tester_id_list = ["Crawler_test_With", "Crawler_test2_With", "Crawler_test3_With"] 
    tester_pw_list = ["sugar0202", "sugar0202", "sugar0202"]

    # 가변 정보 
    # insta_crawler1
    query_txt_list = ["모란", "판교", "홍대"] 
    crawling_count_list = [900 , 900, 900] 

    selected_list = []

    for i in range(3):
        if query_txt_list[i] in user_query_list:
            save_file_name = f"insta_crawling_{query_txt_list[i]}_{crawling_count_list[i]}개.csv"
            insta_crawler = InstagramCrawler(tester_id_list[i], tester_pw_list[i], query_txt_list[i], crawling_count_list[i], save_file_name)
            selected_list.append(insta_crawler)

    return selected_list

def main_process():
    '''
    크롤링을 수행하는 메인함수 입니다.

    현재 매개변수 없이 사전정의된 키워드로 병렬처리 크롤링을 수행합니다.
    '''
    query_txt_list = ["모란", "판교", "홍대"]
    object_list = automate_user_data(query_txt_list)

    # selenium은 다중 브라우저 테스트를 지원합니다.
    # 자동화된 병렬 테스트를 수행합니다.
    # 크롤링 시간을 단축 할 수 있습니다.
    # 멀티 프로세스 (병렬처리)
    pocesesse_count = len(query_txt_list)
    pool = Pool(processes = pocesesse_count) # pocesesse_count 개의 프로세스를 사용합니다
    pool.map(crawling_process, object_list)

if __name__ == "__main__":

    main_process()

    # query_txt_list = ["모란", "판교", "홍대"]
    # object_list = automate_user_data(query_txt_list)

    # # selenium은 다중 브라우저 테스트를 지원합니다.
    # # 자동화된 병렬 테스트를 수행합니다.
    # # 크롤링 시간을 단축 할 수 있습니다.
    # # 멀티 프로세스 (병렬처리)
    # pocesesse_count = len(query_txt_list)
    # pool = Pool(processes = pocesesse_count) # pocesesse_count 개의 프로세스를 사용합니다
    # pool.map(crawling_process, object_list)