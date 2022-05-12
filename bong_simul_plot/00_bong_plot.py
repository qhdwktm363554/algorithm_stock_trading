import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from library import cf
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, VARCHAR, DATE, Float, Text
import re
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import event


def escape_percentage(conn, clauseelement, multiparams, params):
    # execute로 실행한 sql문이 들어왔을 때 %를 %%로 replace
    if isinstance(clauseelement, str) and '%' in clauseelement and multiparams is not None:
        while True:
            replaced = re.sub(r'([^%])%([^%s])', r'\1%%\2', clauseelement)
            if replaced == clauseelement:
                break
            clauseelement = replaced

    return clauseelement, multiparams, params
kospi_index_call = create_engine("mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/daily_buy_list",encoding='utf-8')
# Bong: 아래 listen 이런 것들은 나중에 추가된건데 pymysql에서 query문이 %로 들어간 건 error가 나는 경우가 있었다더라
#       이거는 escape_percentage 함수로 들어가서 % 하나가 있으면 두개로 바꿔주는 거란다.
event.listen(kospi_index_call, 'before_execute', escape_percentage, retval=True)

# Bong: 날짜 조회를 그냥 편의상 20180101로 했다.
################!@바꿔줄 부분######################################################
start_date = '20200101'
# simul_alg_list = [1,2,3,4,5,7,8,9,10,12,13,14,18,19,20,21,22,23,24,25,26]
# simul_alg_list = [13,25,26,27,28,29,30,31,32,33,34]
simul_alg_list = [25,26,27,31]
#################################################################################
for i in simul_alg_list:
    sql = "select * from kospi_index where Date > '%s'"
    kospi_index_list = kospi_index_call.execute(sql % (start_date)).fetchall()
    col = ['index', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    df = pd.DataFrame(kospi_index_list, columns = col)

    sql_2 = "select date, sum_valuation_profit from simulator%s.jango_data where Date > '%s'"
    jango_list = kospi_index_call.execute(sql_2 % (i, start_date)).fetchall()
    col_2 = ['date', 'sum_valuation_profit']
    df_2 = pd.DataFrame(jango_list, columns = col_2)


    # Date 열의 형식이 date string이라서 to_datetime으로 바꿔줬다.
    df['Date'] = pd.to_datetime(df['Date'])
    df_2['date'] = pd.to_datetime(df_2['date'])
    # df와 df_2의 'date'열의 이름이 달라져서 아래로 바꿔줬다.
    df_2.rename(columns = {'date':'Date'}, inplace = True)
    # df_2의 data type이 text라서 float으로 바꿔준다.
    df_2['sum_valuation_profit'] = df_2['sum_valuation_profit'].astype(float)


    df_3 = pd.merge(df, df_2, how = 'inner', on='Date')

    next_value = "my_value"

    fig, ax1 = plt.subplots()
    color_1 = 'tab:grey'
    ax1.set_title(f'Major index and alg{i}', fontsize = 10)
    ax1.set_xlabel('Date', fontsize = 5, color = 'black')
    ax1.set_ylabel('kospi', fontsize = 10, color = color_1)
    ax1.plot(df_3['Date'], df_3['Close'], label = 'Major index',color = color_1)
    ax1.tick_params(axis = 'y', labelcolor =color_1, labelsize = 7)
    ax1.legend(loc='upper left')
    plt.xticks(rotation = 45, fontsize = 7)
    ax1.set_yticks(list(range(2000,3500, 100)))
    ax1.set_ylim([2000, 3500])

    ax2 = ax1.twinx()
    color_2 = 'tab:red'
    ax2.set_ylabel(f'alg{i}', fontsize =10 ,color = color_2)
    ax2.plot(df_3['Date'], df_3['sum_valuation_profit'], label = f'Alg{i}',color = 'red', marker = '*', markersize = 5)
    ax2.tick_params(axis = 'y', labelcolor = color_2, labelsize = 7, pad = 10)
    ax2.legend(loc='upper right')
    # 바로 아래 code는 sub Y-axis 범위를 지정하느건데 fluctuation이 작은 경우 차이를 보기 힘들어서 그냥 생략했다.
    # ax2.set_yticks(list(range(-4000000, 30000000, 4000000)))
    # ax2.set_ylim([-4000000, 30000000])
    # ax2.yaxis.set_major_formatter('{x:1.1f}')

    #아래로 x/y축에 grid를 넣어준다.
    ax1.grid(axis = 'x', color = "grey", linestyle = ":")
    ax2.grid(axis = 'y', color = "grey", linestyle = ":")


    plt.show()





