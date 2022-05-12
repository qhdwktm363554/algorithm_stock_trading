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

        sql = "select code from stock_item_all"
        code = db_engine.execute(sql).fetchall()
        bong_list = []
        for a, b in enumerate(code):
            bong_list.append(code[a][0])
        print(bong_list)


        #################################################첫번째 수집 시작~!!############################################################################
        outer_list = []
        for n, i in enumerate(bong_list):
            url = f"https://finance.naver.com/item/main.naver?code={i}"
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            inner_list = []

            inner_list.append(i)
            # a:code_name / c: 동일업종 / b: 동일업종PER /  d: 추정PER / e: 추정EPS / f: 목표주가
            try:
                a = soup.select_one('#middle > div.h_company > div.wrap_company > h2 > a').get_text()
                inner_list.append(a)
            except AttributeError:
                a = "N/A"
                inner_list.append(a)
                # print(f"{i}에 NoneType error 가 발생했다")
            try:
                c = soup.select_one('#content > div.section.trade_compare > h4 > em > a').get_text()
                inner_list.append(c)
            except AttributeError:
                c = "N/A"
                inner_list.append(c)
                # print(f"{i}에 NoneType error 가 발생했다")
            try:
                b = soup.select_one('#tab_con1 > div:nth-child(6) > table > tbody > tr.strong > td > em').get_text()
                inner_list.append(b)
            except AttributeError:
                b = "N/A"
                inner_list.append(b)
                # print(f"{i}에 NoneType error 가 발생했다")
            try:
                d = soup.select_one('#_cns_per').get_text()
                inner_list.append(d)
            except AttributeError:
                d = "N/A"
                inner_list.append(d)
                # print(f"{i}에 NoneType error 가 발생했다")
            try:
                e = soup.select_one('#_cns_eps').get_text()
                inner_list.append(e)
            except AttributeError:
                e = "N/A"
                inner_list.append(e)
                # print(f"{i}
            try:
                f = soup.select_one('#tab_con1 > div:nth-child(4) > table > tbody > tr:nth-child(1) > td > em').get_text()
                inner_list.append(f)
            except AttributeError:
                f = "N/A"
                inner_list.append(f)
                # print(f"{i}에 NoneType error 가 발생했다")
            outer_list.append(inner_list)
            print(f"{n}/{len(bong_list)} is done")

        col = ['code','code_name', 'field', 'field_per', 'per_estimated', 'eps_estimated', 'n_target_price']
        df = pd.DataFrame(outer_list, columns = col)

        for col_name in col:
            df[f"{col_name}"] = df[f"{col_name}"].str.replace(',', '', regex=True)

        today = datetime.datetime.today().strftime("%Y%m%d")
        df['n_date'] = today
        df = df.replace('N/A', np.nan, regex=True)

        recipe_name = "navercrawling_per"
        print(df)

        ###여기는 db에 df 넣기 전에 data가 이미 존재하는지 확인~!####
        sql_bong = "SELECT n_date from daily_buy_list.navercrawling_per order by n_date desc limit 1"
        exist_check = db_engine.execute(sql_bong).fetchall()[0][0]
        if today == exist_check:
            quit()

        df.to_sql(
            recipe_name,
            db_engine, if_exists='append',
            dtype={
                'code': Text,
                'code_name': VARCHAR(length=128),
                'field': VARCHAR(length=128),
                'field_per': Float,
                'per_estimated': Float,
                'eps_estimated': Float,
                'n_target_price': Float,
                'n_date': Text,
            }
        )
        print(f"봉현아 {today}자 naver_crawling_완료 후 db에 update 완료했다~!!!")
        na.send_email(na.smtp_info, na.msg_3)






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