import pandas as pd
import numpy as np
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, VARCHAR, DATE, Float, Text
from library import cf
import pymysql
pymysql.install_as_MySQLdb()

df = pd.read_csv("220109_kospi_index.csv")
df['Date'] = df['Date'].str.replace('-', '', regex=True)
# df['Date'] = df['Date'].astype(str)
# # df = df.astype({'Date':'text'})
print(df.dtypes)
print(df)

db_url = URL(
    drivername="mysql+mysqldb",
    username=cf.db_id,
    password=cf.db_passwd,
    host=cf.db_ip,
    port=cf.db_port,
    database='daily_buy_list'
)

db_engine = create_engine(db_url)

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