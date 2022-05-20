# 외부 모듈 설치
import environment_construction as e_const
e_const.check_module_process()
print("외부 모듈 설치가 완료되었습니다.")
print("프로그램 WITH를 실행합니다.")
print()

import main
import main_visual
import os
import exception_function as ex_func

def engine_process():
    '''
    프로그램을 실핼하는 메인 함수입니다.

    모듈 설치를 제외한 모든 과정을 포함합니다.
    '''
    print("=" * 80)
    print("안녕하세요.")
    print("지하철역을 입력하면 주변 지역의 서비스를 알려드리는 프로그램 WITH입니다.")
    print("=" * 80)
    print()

    while True:
        print("[Step1]")
        print("원하시는 프로세스를 선택해 주세요.")
        print("1. 크롤링")
        print("2. 시각화")
        print("0. 프로그램 종료")

        case_list = [1, 2, 0]
        choice = ex_func.check_input_number(case_list)
        print()

        if choice == 1:
            print("=" * 80)
            print("크롤링을 진행하겠습니다.")
            print("=" * 80)
            print()
            # 크롤링 프로세스의 반복 수행은 반영하지 않겠습니다.
            main.main_process()
            break
        elif choice == 2:
            print("=" * 80)
            print("시각화를 진행하겠습니다.")
            print("=" * 80)
            print()

            path_1 = f"./data/insta_crawling_모란_900개.csv"
            path_2 = f"./data/insta_crawling_판교_900개.csv"
            path_3 = f"./data/insta_crawling_홍대_900개.csv"

            # 원활한 시각화 진행을 위해서 모든 키워드에 대해
            # 크롤링 자료가 존재할 때만 시각화를 진행하겠습니다.
            # exception_input() 내부의 ready_data반영으로 예외처리 여지가 있습니다.
            if os.path.isfile(path_1) and os.path.isfile(path_2) and os.path.isfile(path_3): # 크롤링 파일이 모두 존재한다면
                main_visual.main_visual_process()
                continue
            else:
                print("모든 크롤링 데이터가 준비되지 않았습니다.")
                print("크롤링을 먼저 진행해 주세요.")
                print()
                continue
        elif choice == 0:
            print("=" * 80)
            print("프로그램을 종료합니다.")
            print("=" * 80)
            break
        else:
            pass

if __name__ == "__main__":

    # 프로그램 실행
    engine_process()

    
    
