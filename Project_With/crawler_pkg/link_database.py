'''
데이테베이스 연동 관련 모듈입니다.

시각화를 위해 정제된 데이터를 데이터베이스에 저장합니다.
'''
import pymysql
import csv
from decimal import Decimal
import pandas as pd

class LinkDataBase:
    def __init__(self):
        self.__host = "localhost" # # host = '127.0.0.1' 사용가능 (자신의 컴퓨터를 의미한다)
        self.__port = 3306
        self.__user = 'root'
        self.__password = '1234'
        self.__conn = self.__create_connection()
        # 객체가 생성될 때
        # 커서를 생성합니다.
        self.__cursor = self.__conn.cursor()

    def __del__(self):
        # 객체가 소멸될 때
        # 데이터 베이스 닫습니다.
        self.__cursor.close()
        # print("데이터베이스가 닫혔습니다")

    # 1. 데이터 베이스 연결
    def __create_connection(self): # 각 메소드별로 연결하고 연결을 끊고를 반복할지 고민 필요
        conn = pymysql.connect(
            host = self.__host,
            port = self.__port,
            user = self.__user,
            passwd = self.__password,
            db = "instagram_location_db",
            charset = "utf8",
            use_unicode = True)
        
        return conn

    # 2. 데이터 베이스 만들기
    def create_database(self):
        # 커서 생성
        # 커서는 데이터베이스에 SQL문을 실행하거나, 실행된 결과를 돌려받는 통로로 생각하면 된다
        # cursor = self.__conn.cursor()

        # MySQL에서 실행될 커리문 입력
        # 이미 생성되 있다면 지우고 다시 생성합니다
        # 추후 데이터 관리에 위험할 수 있으니
        # 만들어진 후 코드가 어떻게 사용될지 고민이 필요합니다.
        # 데이터 베이스 생성후에는 
        # 커서를 만들 때 연결해서 사용합니다.
        sql = "DROP DATABASE IF EXISTS `instagram_location_db`;"

        # 데이터 입력
        # 임시로 저장된 상태
        self.__cursor.execute(sql)

        sql = "CREATE DATABASE `instagram_location_db`;" 
        self.__cursor.execute(sql)

        # 입력한 데이터 저장
        # 저장 명령
        self.__conn.commit()

        # 데이터 베이스 닫기
        # self.__conn.close()

    # 3. 테이블 만들기
    # 테이블을 만드는 SQL문을 커서이름.execute()함수의 매개변수로 넘겨주면
    # SQL문이 데이터베이스에 실행된다.
    def create_table(self, location_name):
        # cursor = self.__conn.cursor()

        # 데이터베이스 접근
        # db = "instagram_location_db" 추가하면 없어도 될 부분
        sql = "USE `instagram_location_db`;"
        self.__cursor.execute(sql) 

        sql = f"DROP TABLE IF EXISTS `{location_name}_table`;"
        self.__cursor.execute(sql) 

        # float 부동소수점
        # decimal 고정소수점 
        # 사용 이유 오차없이 좀더 정확한 소수점 표현을 위해
        sql = f"CREATE TABLE IF NOT EXISTS `{location_name}_table`(\
                kakao_api_name    VARCHAR(100)        NOT NULL,\
                latitude          DECIMAL(20,15)      NOT NULL,\
                longtitude        DECIMAL(20,15)      NOT NULL,\
                instagram_name    VARCHAR(100)        NOT NULL,\
                PRIMARY KEY (kakao_api_name));" 
        self.__cursor.execute(sql) 

        self.__conn.commit()

        # self.__conn.close()

    
    # 테이블에 레코드 입력하기
    def insert_data(self, location_name):
        # 데이터베이스 접근
        sql = "USE `instagram_location_db`;"
        self.__cursor.execute(sql)

        path = f"./data/location_information/insta_location_information_{location_name}.csv"
        # UnicodeDecodeError 발생
        # cp949방식으로 디코딩을 할 수 없다
        # encoding='cp949' 추가
        with open(path, encoding='utf-8') as file:
            # 저장할 데이터를 먼저 읽어옵니다.
            data = csv.reader(file)

            # 헤더를 제외시킵니다.
            next(data)
            
            for row in data:
                sql = f"INSERT INTO `{location_name}_table`(kakao_api_name, latitude, longtitude, instagram_name)\
                        VALUES('{row[0]}', {Decimal(row[1])}, {Decimal(row[2])}, '{row[3]}');"
                self.__cursor.execute(sql)
            
            self.__conn.commit()

    def test_print(self, location_name):
        sql = f"SELECT * FROM `{location_name}_table`"

        test_df = pd.read_sql(sql, self.__conn)
        print(test_df)

# 테스트
if __name__ == "__main__":
# result =  cur.fetchall()
# print(result)
    location_name = '모란'

    test = LinkDataBase()
    test.create_database()
    test.create_table(location_name)
    test.insert_data(location_name)

    test.test_print(location_name)


