# coding:utf-8

"""
该文件配置了数据库连接的信息、以及创建的表名
确保数据存储正确
Page number that you crawl from those websites.
* if your crawl task is not heavy, set page_num=2~5
* if you'd like to keep a proxies pool, page_num=10 can meet your need.
"""
page_num = 2

# ip test timeout.
timeout = 5

# database host
host = 'localhost'

# database host
port = 5432

# db user
user = 'postgres'

# db password
passwd = 'root'

# db name
DB_NAME = 'postgres'

# schema name
SCHEMA_NAME = 'jiake'

# table name
TABLE_NAME = 'proxy_ips_games'
# TABLE_NAME = 'proxy_ips'

# max failure times of an ip, if exceed, delete it from db.
USELESS_TIME = 4

# lowest success rate of an ip, if exceed, delete it from db.
SUCCESS_RATE = 0.7

# timeout punishment
TIME_OUT_PENALTY = 5

# ip quality assessment time interval. (currently once per day.)
CHECK_TIME_INTERVAL = 24*3600
