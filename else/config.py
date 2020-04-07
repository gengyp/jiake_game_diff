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
buff_cookies = '_ntes_nnid=a0b7340d264da0230b132d3464878dfc,1580284684086; _ntes_nuid=a0b7340d264da0230b132d3464878dfc; __utma=187553192.1124055066.1580284686.1580284686.1580284686.1; __utmz=187553192.1580284686.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Device-Id=dYfH1DSLSx8bUal6EcGC; _ga=GA1.2.1124055066.1580284686; _gid=GA1.2.1236140270.1585415225; Locale-Supported=zh-Hans; game=csgo; NTES_YD_SESS=URkTaHDx4qfEOb9nxL4dsH7qLFj660eAbYmn_ySB77.915ST1ltocJUm.L0zJjtju2QN9N5CFfue7wNFAdkhSdNquCfZQMWc_lw.XqDlUFIYWkA.eWwjQEMr1NXyBnjSuj0xMJ.6mDkDJw_yOyfCuwrAEupEZjJ9Fx3QIkhc6ccXkNfzkubkgDV1RwJEM_ADPA6jDIulK3BzgvZ8pSW7a6OFMnz_mgiMXNgAMupTETDwr; S_INFO=1585460206|0|3&80##|17826853236; P_INFO=17826853236|1585460206|0|netease_buff|00&99|zhj&1585405858&netease_buff#zhj&330200#10#0#0|&0|null|17826853236; session=1-tzP_zqkPz0Gpgvy5xW9xbRSy-c6eJ9jd4V6dnPGN-wZU2046372339; csrf_token=ImMxYjIyYmY1ZWQwZDk5ODExYmI3NTI0YjRmYjIxMDdkNDUyOTUwMzAi.EWHFjA.498CxGM44_aQX3wvCt8OryMimSQ'

# dingding robot parms
# 设置钉钉机器人时，选择--加签--复制密钥 放入 secret 中
secret = 'SECda6dbd05930a5ae9e0c6c14359811f14012ba38c38b9baa0ba64c61cce4d8fdb'
# webhook 复制到下方
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=2e1da23001b398c06162ca9c8ad91467d835cf7c9f29e93a4cc9ef68d376490f'

