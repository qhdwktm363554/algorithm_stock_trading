# version 1.3.2
print("collector 프로그램이 시작 되었습니다!")

from library.collector_api import *

class Collector:
    print("collector 클래스에 들어왔습니다.")

    def __init__(self):
        print("__init__ 함수에 들어왔습니다.")
        self.collector_api = collector_api()

    def collecting(self):
        self.collector_api.code_update_check()            # 이 부분은 수업에서만 주석처리하는 부분 (data collecting 때문에 안하려고)
        # self.collector_api._create_stock_info()
        # self.collector_api._create_stock_finance()          # 이 부분은 test 용 - stock_finance table 생성하는지 check 위해서 활성화. 실전에서는 주석해라

if __name__ == "__main__":
    print("__main__에 들어왔습니다.")
    # 아래는 키움증권 openapi를 사용하기 위해 사용하는 한 줄! 이해 할 필요 X
    app = QApplication(sys.argv)
    c = Collector()
    # 데이터 수집 시작 -> 주식 종목, 종목별 금융 데이터 모두 데이터베이스에 저장.
    c.collecting()
