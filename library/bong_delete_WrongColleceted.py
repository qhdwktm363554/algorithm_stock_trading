# from collections import OrderedDict
#
# from sqlalchemy import Integer, Text, String, Float
#
# ver = "#version 1.5.0"
# print(f"collector_api Version: {ver}")
#
import numpy
# import pathlib
# from library.open_api import *
import os
import time
# from PyQt5.QtWidgets import *
# from library.daily_buy_list import *
# from pandas import DataFrame
from kind_crawling import *
import cf
t = time.time()
today =  time.strftime("%Y%m%d", time.gmtime(t))
db_schema = "daily_craw"
print(today)
Base_engine = create_engine(
                "mysql+mysqldb://" + cf.db_id + ":" + cf.db_passwd + "@" + cf.db_ip + ":" + cf.db_port + "/daily_craw",
                encoding='utf-8')
Connected_engine = Base_engine.connect()

sql = "select table_name from information_schema.TABLES where TABLE_SCHEMA = 'daily_craw'"
table_name = Connected_engine.execute(sql).fetchall()
# print(table_name)


for n,i in enumerate(table_name):
    del_sql = f"""delete from `{i[0]}` where date = '{today}'"""
    Connected_engine.execute(del_sql)
    print(f"{n}.{i[0]}'s delete has completed")




