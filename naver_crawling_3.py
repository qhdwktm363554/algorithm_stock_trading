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

        #################################################첫번째 수집 시작~!!############################################################################
        for p in range(0, 2):
            for i in range(1, 40):
                url = f'https://finance.naver.com/sise/sise_market_sum.nhn?sosok={p}&page={i}'
                driver.get(url)
                # 아래에서 맨 첫번째 페이지면 불필요한 checkbox를 해제 후 필요한거 선택
                if p == 0 and i == 1:
                    # check box에서 해당 부분 우클릭 '검사' 후 copy --> selector 하면 아래 selector를 얻을 수 있다.
                    existing_checked_selector = ['#option1', '#option15', '#option21', '#option4', '#option6',
                                                 '#option12']
                    new_checked_selector = ['#option25', '#option11', '#option6', '#option12', '#option18', '#option24']
                    for selector in existing_checked_selector:
                        selected_tab = driver.find_element_by_css_selector(selector)
                        selected_tab.click()
                    for selector_2 in new_checked_selector:
                        selected_tab = driver.find_element_by_css_selector(selector_2)
                        selected_tab.click()
                    # 아래는 적용하기 버튼을 누르는 과정이다.
                    selected_tab_3 = driver.find_element_by_css_selector(
                        '#contentarea_left > div.box_type_m > form > div > div > div > a:nth-child(1) > img')
                    selected_tab_3.click()
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')

                if i == 1:
                    col = list(soup.select_one('table.type_2 tr').stripped_strings)

                for row in soup.select('table.type_2 tr:not(:has(th, [colspan]))'):
                    data.append([x.text for x in row.select('td:not(.title)')])

                # break

        # 아래를 해준 이유는 만약에 webpage에서 col이 바꼈을 때 알려줘야 하기 때문이다. mail로 보내줘야 한다~!!!
        if col != ['N', '종목명', '현재가', '전일비', '등락률', '액면가', '매출액증가율', '영업이익증가율', 'PER', 'ROE', 'ROA', 'PBR', '토론실']:
            na.send_email(na.smtp_info, na.msg_2)     # 여기를 자동 mail 보내주는 걸로 바꿔야 한다.
        print("첫번째 수집 끝~!!!")
        #################################################첫번째 수집 끝~!!!############################################################################

        data_2 = []
        #################################################두번째 수집 시작~!!############################################################################
        for p1 in range(0, 2):
            for i1 in range(1, 40):
                url = f'https://finance.naver.com/sise/sise_market_sum.nhn?sosok={p1}&page={i1}'
                driver.get(url)
                # 아래에서 맨 첫번째 페이지면 불필요한 checkbox를 해제 후 필요한거 선택
                if p1 == 0 and i1 == 1:
                    # check box에서 해당 부분 우클릭 '검사' 후 copy --> selector 하면 아래 selector를 얻을 수 있다.
                    existing_checked_selector = ['#option25', '#option11', '#option6', '#option12', '#option18', '#option24']
                    new_checked_selector = ['#option1', '#option3', '#option15', '#option4', '#option22', '#option26']
                    for selector in existing_checked_selector:
                        selected_tab = driver.find_element_by_css_selector(selector)
                        selected_tab.click()
                    for selector_2 in new_checked_selector:
                        selected_tab = driver.find_element_by_css_selector(selector_2)
                        selected_tab.click()
                    # 아래는 적용하기 버튼을 누르는 과정이다.
                    selected_tab_3 = driver.find_element_by_css_selector(
                        '#contentarea_left > div.box_type_m > form > div > div > div > a:nth-child(1) > img')
                    selected_tab_3.click()
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')

                if i1 == 1:
                    col = list(soup.select_one('table.type_2 tr').stripped_strings)

                for row in soup.select('table.type_2 tr:not(:has(th, [colspan]))'):
                    data_2.append([x.text for x in row.select('td:not(.title)')])
                # break

        # 아래를 해준 이유는 만약에 webpage에서 col이 바꼈을 때 알려줘야 하기 때문이다. mail로 보내줘야 한다~!!!
        if col != ['N', '종목명', '현재가', '전일비', '등락률', '액면가', '거래량', '거래대금', '시가총액', '매출액', '보통주배당금', '외국인비율', '토론실']:
            na.send_email(na.smtp_info, na.msg_2)     # 여기를 자동 mail 보내주는 걸로 바꿔야 한다.
        print("두번째 수집 끝~!!!")
        #################################################첫번째 수집 끝~!!!############################################################################


        ## 종목명: code_name / 현재가: current_price / 매출액증가율:revenue_increase / 영업이익증가율: income_increase 로 바꿨다.
        col = ['N', 'code_name', 'current_price', 'compared_yes', 'variance', 'par_value', 'revenue_increase', 'income_increase', 'PER', 'ROE', 'ROA', 'PBR', 'discussion']
        df = pd.DataFrame(data, columns=col)
        df2 = df.loc[:,['N', 'code_name', 'current_price', 'par_value', 'revenue_increase', 'income_increase', 'PER', 'ROE', 'ROA', 'PBR']]  # 위의 col에서 '전일비', '등락률', '토론실'을 빼고 slicing
        col_2 = ['N', 'code_name', 'current_price', 'par_value', 'revenue_increase', 'income_increase', 'PER', 'ROE', 'ROA', 'PBR']

        ## 종목명: code_name / 현재가: current_price / 거래량: volume / 거래대금: transaction_amount / 시가총액: market_cap / 매출액: revenue / 보통주배당금: dividend / 외국인비율: foreigner 로 바꿨다.
        col_3 = ['N', 'code_name', 'current_price', 'compared_yes', 'variance', 'par_value', 'volume', 'transaction_amount', 'market_cap', 'revenue', 'dividend', 'foreigner', 'discussion']
        df3 = pd.DataFrame(data_2, columns=col_3)
        df4 = df3.loc[:,['code_name', 'current_price', 'volume', 'transaction_amount', 'market_cap', 'revenue', 'dividend', 'foreigner']]  # 위의 col에서 '전일비', '등락률', '토론실'을 빼고 slicing
        col_4 = ['code_name', 'current_price', 'volume', 'transaction_amount', 'market_cap', 'revenue', 'dividend', 'foreigner']


        df2 = df2.replace('N/A', np.nan, regex=True)      # naver에서 받다오니 N/A가 있는데 이게 string이라서 numpy의 nan으로 수정해야 numeric로 변경이 가능하더라.
        for col_name in col_2:
            df2[f"{col_name}"] = df2[f"{col_name}"].str.replace(',', '', regex=True)
        df4 = df4.replace('N/A', np.nan, regex=True)      # naver에서 받다오니 N/A가 있는데 이게 string이라서 numpy의 nan으로 수정해야 numeric로 변경이 가능하더라.
        for col_name in col_4:
            df4[f"{col_name}"] = df4[f"{col_name}"].str.replace(',', '', regex=True)

        df5 = pd.merge(df2, df4, how='outer', on='code_name')
        print(df5.columns)


        today = datetime.datetime.today().strftime("%Y%m%d")
        # df5.drop('code_name_y', inplace=True, axis=1)
        # df5 = df5.rename(columns={'code_name_x': 'code_name'})
        df5.drop('current_price_y', inplace=True, axis=1)
        df5 = df5.rename(columns={'current_price_x': 'current_price'})
        df5[['current_price','revenue_increase', 'income_increase', "PER", "ROE", "ROA", "PBR", 'volume','transaction_amount', 'market_cap', 'revenue', 'dividend', 'foreigner']] = df5[['current_price','revenue_increase', 'income_increase', "PER", "ROE", "ROA", "PBR", 'volume','transaction_amount', 'market_cap', 'revenue', 'dividend', 'foreigner']].apply(pd.to_numeric)


        df5['date'] = today
        df5['EPS'] = df5['current_price'] / df5['PER']
        df5['AppPrice'] = df5['EPS'] * df5['ROE']       # 적정주가
        df5['margin'] = df5['AppPrice'] - df5['current_price']    # 적정주가 - 현재가
        df5['margin_rate'] = df5['AppPrice'] / df5['current_price']

        # 아오 EPS 구할 때 PER이 0인 경우 inf로 나오는 경우가 있어 이걸 nan으로 바꿔주는 아래 code를 추가했다.
        df5 = df5.replace([np.inf, -np.inf], np.nan)
        print(df5)
        # database 이름은 lower case table names를 써야 한다.
        recipe_name = "navercrawling_2"

        #####################여기 아래는 db에 넣기 위해서 작업 ########################################################

        db_url = URL(
            drivername="mysql+mysqldb",
            username=cf.db_id,
            password=cf.db_passwd,
            host=cf.db_ip,
            port=cf.db_port,
            database='daily_buy_list'
        )

        db_engine = create_engine(db_url)

        ###여기는 db에 df 넣기 전에 data가 이미 존재하는지 확인~!####
        sql_bong = "SELECT date from daily_buy_list.navercrawling_2 order by date desc limit 1"
        exist_check = db_engine.execute(sql_bong).fetchall()[0][0]
        if today == exist_check:
            quit()

        df5.to_sql(
            recipe_name,
            db_engine, if_exists='append',
            dtype={
                'N': VARCHAR(length=6),
                'code_name': VARCHAR(length=128),
                'current_price': Float,
                'par_value': Float,
                'revenue_increase': Float,
                'income_increase': Float,
                'PER': Float,
                'ROE': Float,
                'ROA': Float,
                'PBR': Float,
                'volume': Float,
                'transaction_amount': Float,
                'market_cap': Float,
                'revenue': Float,
                'dividend': Float,
                'foreigner': Float,
                'date': Text,
                'EPS': Float,
                'AppPrice': Float,
                'margin': Float,
                'margin_rate': Float,
            }
        )
        print(f"봉현아 {today}자 naver_crawling_완료 후 db에 update 완료했다~!!!")
        na.send_email(na.smtp_info, na.msg)


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