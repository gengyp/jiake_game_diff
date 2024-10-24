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
passwd = 'pgdb_passwd_gyp12*'

# db name
DB_NAME = 'linzi'

# schema name
SCHEMA_NAME = 'games'

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
secret = 'SEC943c310fe8ee595f6ab04f8958346d83afaadd908a0ab087bbabab346577227c'
# webhook 复制到下方
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=1fee784322cd65a5e4832dccb570660dd6c78ee3b986d2c2043a96ae15deef80'

import psycopg2
def mod_data_pg(sql):
    '''
    创建表、插入、删除、更新等无结果返回 sql
    '''
    try:
        conn = psycopg2.connect(user="postgres",password='{}'.format(passwd)
                                , host="{}".format(host), port=5432,dbname='linzi')
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)

from lxml import etree
from sqlalchemy import create_engine
def save_v5fox2db(appid,html):
  tree = etree.HTML(html)

  goods_names = tree.xpath('//div[@class="list-box clearfix"]/a/div[1]/div[2]/h5/text()')
  amounts= tree.xpath('//div[@class="list-box clearfix"]/a/div[1]/div[2]/p/span/text()')
  good_statuses = tree.xpath('//div[@class="list-box clearfix"]/a/div[2]/div[2]/text()')

  lst = []
  for i in range(len(goods_names)):
    goods_name = goods_names[i].replace("'",'')
    amount = eval(amounts[i])
    good_status = good_statuses[i].split('件 ')[1].replace("需求","求购")
    good_num = eval(good_statuses[i].split('件')[0])
    lst.append([appid,goods_name,amount,good_status,good_num])

  # store valid proxies into db.
  try:
    df = pd.DataFrame(lst)
    col_name = ['appid','good_name','amount','good_status','good_num']
    df.columns = col_name

    engine = engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(user,passwd,host,port,DB_NAME))
    df.to_sql(name='game_v5fox_goods',con=engine,schema='{}'.format(SCHEMA_NAME),index=False,if_exists='append')
  except:
    print('error!',df.shape,lst)
  return len(lst)