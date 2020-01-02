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

# buff.py cookies
buff_cookies = 'Device-Id=CO6MHUM3HLENoI4mYuwV; Locale-Supported=zh-Hans; game=csgo; _ga=GA1.2.1221107236.1577941304; _gid=GA1.2.1296564522.1577941304; NTES_YD_SESS=oTV4qYnpPvySsJnGQAq2ufCoaP_q8I2DtOYQUo2v7ZdIceKDcQzbiWonkdENW5z5sFaTITeM1XsA9jT16B7gKBTtsMX8aSHiYQjkwtuQo1mhx9gqk3OZ16UcobrFyjmDEnkOMIWjDGzGXQ6C2mH9IzlzyMBk0R3vDMWwbjwFOL0GqBkCg11R_myhiUzDk64dVjDqd.Wu01oIEp64_fHNQ4z64Y7cPAJqC_X5.qcHi.PCL; S_INFO=1577943192|0|3&80##|17826853236; P_INFO=17826853236|1577943192|0|netease_buff|00&99|null&null&null#zhj&330200#10#0#0|&0||17826853236; session=1-138mZct5yZdm5e8qgzD6UNZDnkS6Wq0lEPrpDkQFZIOI2046372339; csrf_token=ImNmYzg5Y2JlZTBmNmViOGYwMzIyYTM2ZWM5YTdkMGM5MWIyMjY2NGMi.EO8SHg.E0zBf8_dGywpZwswDVZmCVOJQ2U; _gat_gtag_UA_109989484_1=1'

# dingding robot parms
# 设置钉钉机器人时，选择--加签--复制密钥 放入 secret 中
secret = 'SECda6dbd05930a5ae9e0c6c14359811f14012ba38c38b9baa0ba64c61cce4d8fdb'
# webhook 复制到下方
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=2e1da23001b398c06162ca9c8ad91467d835cf7c9f29e93a4cc9ef68d376490f'

