'''
데이터 시각화를 위해 사용되는 클래스들의 부모클래스로 추상클래스로 정의된 모듈입니다.

추상클래스는 인스턴스화 될 수 없습니다.
파생 클래스의 매서드 구현을 강제하기 위해 @abstractmethod 추상메서드를 사용합니다.
파생 클래스에서 사용될 메서드를 빈 메서드로 정의 합니다.

파생 클래스의 동일하게 사용되는 메서드를 정의 합니다.(부모 클래스)
'''
from abc import * # 추상클래스를 만들기 위해 사용되는 모듈
import pandas as pd
import os

class Visualization(metaclass=ABCMeta):
    # 추상 메서드를 만들 때 pass만 넣어서 빈 메서드로 만듭니다.
    # 왜냐하면 추상 클래스는 인스턴스를 만들 수 없으니 추상 메서드도 호출할 일이 없기 때문입니다.
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod    
    def set_raw_data(self):
        pass
 
    @abstractmethod    
    def get_raw_data(self):
        pass

    # 원시데이터의 중복을 제거합니다.
    @abstractmethod
    def drop_duplicate_raw_data(self):
        pass

    # 원시데이터에서 원하는 항목만을 추출합니다.
    @abstractmethod
    def refine_raw_data(self):
        pass

    # 원시데이터에서 연관없는 데이터를 제거합니다.
    @abstractmethod
    def remove_unrelated_data(self):
        pass

    def make_save_directory(self):
        current_directory = os.getcwd()
        data_directory = current_directory + "/data/location_information"

        if os.path.isdir(data_directory): # 설정경로에 디렉토리가 존재 한다면
            pass
        else:
            os.makedirs(data_directory)