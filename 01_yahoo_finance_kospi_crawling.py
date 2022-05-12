from selenium import webdriver
import numpy as np
import os
import pandas as pd
from bs4 import BeautifulSoup
import datetime
from library import cf
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, VARCHAR, DATE, Float, Text
import pymysql
pymysql.install_as_MySQLdb()

# 여기 아래는 naver mail 보내는 library
import naver_mailing as na

# 여기서는 selenium으로 naver증권을 열어서 불필요한 부분을 삭제하고, 필요한 부분을 선택해서
# BeautifulSoup으로 현재 browser의 html을 parsing한 후 table의 data 정보를 crawling 하는거다.

class KINDCrawler_bong:
    def __init__(self):
        pass

    def craw(self):    # web browser가 뜨지 않게 하기 위해서 아래를 쓴다.
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        path = self.chrome_driver_update() # 크롬 드라이버를 자동으로 path 위치에 설치합니다

        # 아래에서 path 뒤에 options=options를 쓰면 창이 뜨지 않는다. 나중에 이 부분은 수정이 필요하다.
        # driver = webdriver.Chrome(path)
        driver = webdriver.Chrome(path, options=options)

        # 아래 list로 data를 다 받을거다
        data = []
        # p == 0은 kospi고, 1은 kosdaq이다. / i는 page를 돌려줌

        db_url = URL(
            drivername="mysql+mysqldb",
            username=cf.db_id,
            password=cf.db_passwd,
            host=cf.db_ip,
            port=cf.db_port,
            database='daily_buy_list'
        )

        db_engine = create_engine(db_url)

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@[yahoo finance]에서 kospi  index 오늘 날짜만 crawling@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        yahoo_list = []
        url = "https://finance.yahoo.com/quote/%5EKS11/history?p=%5EKS11"
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        selector1 = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > tbody > tr:nth-child(1) > td.Py\(10px\).Ta\(start\).Pend\(10px\) > span"
        a = soup.select_one(selector1).get_text()
        # 처음 a는 그냥 Jan 17, 2022 형식의 그냥 string format인데 아래를 통해서 일단 datetime형식으로 만든다.
        b = datetime.datetime.strptime(a, "%b %d, %Y")
        #  그 후 아래를 통해서 datetime을 string format으로 만든다. 이건 그냥 한줄로 만든게 좋지만 이해를 위해 따로 만들기로 하자.
        c = b.strftime('%Y%m%d')
        yahoo_list.append(c)

        selector_Open = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > tbody > tr:nth-child(1) > td:nth-child(2) > span"
        selector_High = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > tbody > tr:nth-child(1) > td:nth-child(3) > span"
        selector_Low = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > tbody > tr:nth-child(1) > td:nth-child(4) > span"
        selector_Close = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > tbody > tr:nth-child(1) > td:nth-child(5) > span"
        selector_Adj_close = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > tbody > tr:nth-child(1) > td:nth-child(6) > span"
        selector_Volume = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > tbody > tr:nth-child(1) > td:nth-child(7) > span"

        loop = [selector_Open,selector_High, selector_Low, selector_Close, selector_Adj_close, selector_Volume]
        for i in loop:
            bong = soup.select_one(i).get_text()
            yahoo_list.append(bong)
        print(yahoo_list)
        yahoo_list = [yahoo_list]
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        ya_col = ['Date', 'Open','High', 'Low', 'Close', 'Adj Close', 'Volume']
        df = pd.DataFrame(yahoo_list, columns=ya_col)
        for col_name in ya_col:
            df[f"{col_name}"] = df[f"{col_name}"].str.replace(',', '', regex=True)
        print(df)
        db_engine = create_engine(db_url)

        ############여기 아래는 sql로 df 넣기 전에 검증용을 하는건다. 1. column 명 일치하는지 / 2.오늘날짜와 일치하는지 확인 / 3.넣으려는 잘짜의 data 있는지 확인######
        #1.column 명 일치하는지 확인
        DateName = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > thead > tr > th:nth-child(1) > span"
        OpenName = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > thead > tr > th:nth-child(2) > span"
        HighName = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > thead > tr > th:nth-child(3) > span"
        LowName = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > thead > tr > th:nth-child(4) > span"
        CloseName = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > thead > tr > th:nth-child(5) > span"
        AdjName = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > thead > tr > th:nth-child(6) > span"
        VolName = "#Col1-1-HistoricalDataTable-Proxy > section > div.Pb\(10px\).Ovx\(a\).W\(100\%\) > table > thead > tr > th:nth-child(7) > span"
        col_veri = []
        loop2 = [DateName, OpenName, HighName, LowName, CloseName, AdjName, VolName]
        for a in loop2:
            hee = soup.select_one(a).get_text()
            col_veri.append(hee)
        correct_col = ['Date', 'Open', 'High', 'Low', 'Close*', 'Adj Close**', 'Volume']
        # 2.오늘날짜랑 crawling의 날짜가 동일한지 확인
        today = datetime.datetime.today().strftime("%Y%m%d")
        # 3.넣으려는 날짜의 data가 있는지 확인
        sql_check = "SELECT date from daily_buy_list.kospi_index order by date desc limit 1"
        bong_exist = db_engine.execute(sql_check).fetchall()[0][0]
        if correct_col != col_veri or today != c or yahoo_list[0] == bong_exist:
            na.send_email(na.smtp_info, na.msg_6)
            quit()
        ####################################검증끝~! 통과했으면 다음으로 넘어가서 sql로 넣어라#####################################

        db_name = "kospi_index"
        df.to_sql(
            db_name,
            db_engine, if_exists='append',
            dtype={
                'Date': Text,
                'Open': Float,
                'High': Float,
                'Low': Text,
                'Close': Float,
                'Adj Close': Float,
                'Volume': Float,
            }
        )
        print(f"봉현아 {today}자 yahoo_finance_crawling_완료 후 db에 update 완료했다~!!!")
        na.send_email(na.smtp_info, na.msg_5)

    # 아래는 kind_crawling.py에서 그대로 복사해서 온거다. 자꾸 이상한걸 가져오길래 이렇게 함.
    def chrome_driver_update(self):
        print("chrome_driver_update..")
        update = True
        # pip install check-chromedriver
        package_name = 'chromedriver-autoinstaller'
        pip_show_list = os.popen(f"pip show {package_name}").read().strip().split('\n')
        for pip_show_str in pip_show_list:
            if package_name not in pip_show_str:
                continue
            else:
                update = False
                break
        if update:
            os.system(f'pip install {package_name}==0.2.2')
            print(f"성공적으로 {package_name} 패키지를 설치 했습니다")

        import chromedriver_autoinstaller
        path = chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                              # and if it doesn't exist, download it automatically,
                                              # then add chromedriver to path
        print("chrome_driver_update 완료!")
        return path

if __name__ == "__main__":
    client = KINDCrawler_bong()
    client.craw()