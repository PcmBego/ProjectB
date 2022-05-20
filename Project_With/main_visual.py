'''
시각화 테스트용 메인입니다.

화면정의서 시나리오로 구현 예정입니다.
'''
from crawler_pkg import *
import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *
import exception_function as ex_func

# 사용자 입력 예외처리
def exception_input():
    while True:
        print("[Step2]")
        print("원하시는 지하철역을 선택해 주세요.")
        print("(현재는 모란, 판교, 홍대만 선택 가능합니다.)")
        print("1. 모란 2. 판교 3. 홍대 0. 프로그램 종료")

        # keyword = input("입력 : ")
        case_list = [1, 2, 3, 0]
        choice = ex_func.check_input_number(case_list)
        print()

        ready_data = ["모란", "판교", "홍대"]

        # if keyword.replace(" ", "") == "":
        #     print("검색어가 입력되지 않았습니다. 다시 입력해주세요.")
        # elif keyword not in ready_data:
        #     print("자료가 준비되지 않았습니다. 다시 입력해주세요. (모란, 판교, 홍대)")
        # else:
        #     break

        if choice == 1:
            keyword = ready_data[0]
            break
        elif choice == 2:
            keyword = ready_data[1]
            break
        elif choice == 3:
            keyword = ready_data[2]
            break
        elif choice == 0:
            print("=" * 80)
            print("프로그램을 종료합니다.")
            print("=" * 80)
            sys.exit()
        else:
            pass

    return keyword

# 시각화 시나리오 프로세스
def visualization_process(app, keyword):
    # print("=" * 80)
    # print("안녕하세요.")
    # print("지하철역을 입력하면 주변 지역의 서비스를 알려드리는 WITH입니다.")
    # print("=" * 80)
    # print()

    # keyword = exception_input()
    # print()

    print("[Step3]")
    print(f"{keyword} 키워드에 대한 검색 결과물 중 시각화하고 싶은 자료를 선택해 주세요.")
    print("1. 해시태그 정보")
    print("2. 위치 정보")
    print("3. 이전 (키워드 변경)")
    print("0. 프로그램 종료")


    case_list = [1, 2, 3, 0]
    choice = ex_func.check_input_number(case_list)
    print()

    if choice == 1:
        print("=" * 80)
        print("자주 나오는 단어를 통해 주변 지역 서비스를 보여 드리겠습니다.")
        print("막대그래프와 워드클라우드를 통해 단어의 빈도수를 나타냅니다.")
        print("=" * 80)
        print("※ 시각화창을 닫으면 계속 진행됩니다.")
        print()
        visual_wordcloud_process(keyword)
        return True

    elif choice == 2:
        print("=" * 80)
        print("위치 정보를 통해 주변 지역 서비스를 보여 드리겠습니다.")
        print("=" * 80)
        print("※ 시각화창을 닫으면 계속 진행됩니다.")
        print()
        visual_map_process(keyword, app)
        return True

    elif choice == 3:
        return False

    elif choice == 0:
        print("=" * 80)
        print("프로그램을 종료합니다.")
        print("=" * 80)
        sys.exit()

    else:
        pass
    
    print()


def main_visual_process():
    '''
    시각화를 수행하는 메인함수입니다.

    사용자의 입력이 끝을 알릴 때까지 수행합니다.
    '''
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    while True:
        keyword = exception_input()
        
        while True:
            next_step = visualization_process(app, keyword)

            if next_step == True:
                print("[Step4]")
                print("시각화 프로그램을 계속 진행하시겠습니까?")
                print("1. 예 2. 아니오 0. 프로그램 종료")

                case_list = [1, 2, 0]
                check_continue = ex_func.check_input_number(case_list)
                print()

                if check_continue == 1:
                    continue
                elif check_continue == 2:
                    keep_step = False
                    break
                elif check_continue == 0:
                    print("=" * 80)
                    print("프로그램을 종료합니다.")
                    print("=" * 80)
                    sys.exit()
                else:
                    pass
            else:
                keep_step = None
                break

        if keep_step == False:        
            break
            

if __name__ == "__main__":
    main_visual_process()

    # app = QCoreApplication.instance()
    # if app is None:
    #     app = QApplication(sys.argv)
    
    # while True:
    #     visualization_process(app)

    #     check_continue = int(input("3. 계속하시겠습니까? [ 1. 예 2. 아니오 ] : "))
    #     print()

    #     if check_continue == 2:
    #         print("4. 종료합니다.")
    #         break
    #     else:
    #         pass