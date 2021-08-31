# coding=utf-8
# python3

"""
Name: connect.py
Author: zhengxiangwei
Time: 2021-08-30 17:45
Desc:
"""

# coding=utf-8
# python3

"""
Name: connect.py
Author: zhengxiangwei
Time: 2021-08-26 10:46
Desc:
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库数据
HOSTNAME = '1.117.213.193'
PORT = '3306'
DATABASE = 'wedding'
USERNAME = 'root'
PASSWORD = ''


# 连接数据连接 URL
db_url_prod = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME,
    PASSWORD,
    HOSTNAME,
    PORT,
    DATABASE,
)


engine = create_engine(db_url_prod, echo=True)


Base = declarative_base(engine)  # 基类
Session = sessionmaker(engine)
session = Session()
