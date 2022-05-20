'''
예외처리 기능을 제공하는 모듈입니다.
'''
def check_input_number(case_list):
    '''
    사용자 입력에 대한 예외처리 함수입니다.

    매개변수로 선택지 리스트를 받습니다.

    기능
    ---
        1. 사용자 입력이 올바른 숫자인지 판별
        (공백, 특수기호, 음수, 소수 등 양의 정수(0 포함)가 아닌 입력을 허용하지 않습니다.)

        2. 선택지 리스트를 통해 올바른 선택을 유도합니다
    '''
    while True:
        user_input = input("입력 : ")

        if user_input.isdigit(): # 숫자
            if int(user_input) not in case_list: # 선택지를 벗어나는 입력
                print("선택지를 벗어났습니다. 다시 선택해주세요.")
            else:
                return int(user_input)
        else:
            print("입력이 잘못되었습니다. 선택지에 맞는 숫자를 입력해주세요.")
