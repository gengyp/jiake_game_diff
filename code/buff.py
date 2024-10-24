# coding:utf-8
import json
import time
import random
import datetime
import requests
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

import sys
sys.path.insert(0,'./else')
import config as cfg


def get_proxy():
  conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
  cursor = conn.cursor()

  ip_list = []
  try:
      cursor.execute("SELECT content FROM {}.{}".format(cfg.SCHEMA_NAME,cfg.TABLE_NAME))
      result = cursor.fetchall()
      for i in result:
          ip_list.append(i[0])
  except Exception as e:
      print (e)
  finally:
      cursor.close()
      conn.close()
  return ip_list

def get_data(ip_lst):
    # website https://buff.163.com/market/?game=dota2#tab=buying&page_num=1
    # url = "https://buff.163.com/api/market/goods/buying"
    url = "https://buff.163.com/api/market/goods"
    headers = {
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
'Connection': 'keep-alive',
'Cookie': cfg.buff_cookies,
'Host': 'buff.163.com',
'Referer': 'https://buff.163.com/market/?game=dota2',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
'X-Requested-With': 'XMLHttpRequest'
        }
    # DOTA2 数据量较大，只爬取求购数据
    i = 0
    while True:
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"game":"dota2","page_num":"{}".format(1+i),"sort_by":"price.desc","min_price":"10","max_price":"4000","_":"1556434296404"} # dota2 求购
      i += 1
      try:
        r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
        dts = json.loads(r.text)
        # buff 开始解析的 页数并不是真正的页数
        page_num = dts['data']['page_num']
        total_page = dts['data']['total_page']
        if page_num<=total_page:
          total = save_buff2db(dts)
        else:
          break
        print('dota2 current page:{}'.format(page_num),end='\r')
      except Exception as e:
        raise e
    print('dota2 crawl finished!')

    # # H1Z1 求购数据较少，故爬取出售数据
    # for i in range(5):
    #   proxy = {'http': 'http://' + random.choice(ip_lst)}
    #   querystring = {"game":"h1z1","page_num":"{}".format(1+i),"sort_by":"price.desc","min_price":"10","max_price":"2000","_":"1556461440132"}
    #   try:
    #     r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    #     total = save_buff2db(json.loads(r.text))
    #   except Exception as e:
    #     raise e

    # csgo 求购数据较少，故爬取出售数据
    i = 0
    while True:
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"game":"csgo","page_num":"{}".format(1+i),"sort_by":"price.desc","min_price":"50","_":"1557652874396"}
      i += 1
      try:
        r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
        # buff 开始解析的 页数并不是真正的页数
        dts = json.loads(r.text)
        page_num = dts['data']['page_num']
        total_page = dts['data']['total_page']
        if page_num<=total_page:
          total = save_buff2db(dts)
        else:
          break
        print('csgo current page:{}'.format(page_num),end='\r')
      except Exception as e:
        raise e
    print('csgo crawl finished!')

def save_buff2db(dts):
  lst = []
  for dt in dts['data']['items']:
    steam_price = dt['goods_info']['steam_price']
    steam_price_cny = dt['goods_info']['steam_price_cny']
    market_hash_name = dt['market_hash_name'].replace("'",'')
    buy_max_price = eval(dt['buy_max_price'])
    sell_num = dt['sell_num']
    sell_min_price = eval(dt['sell_min_price'])
    sell_reference_price = dt['sell_reference_price']
    quick_price = dt['quick_price']
    name = dt['name'].replace("'",'')
    buy_num = dt['buy_num']
    game = dt['game']
    goods_id = dt.get('id',0)
    appid = dt.get('appid',0)

    lst.append([steam_price,steam_price_cny,market_hash_name,buy_max_price,sell_num
      ,sell_min_price,sell_reference_price,quick_price,name,buy_num,game,goods_id,appid])

  # store valid proxies into db.
  try:
    df = pd.DataFrame(lst)
    col_name = ['steam_price','steam_price_cny','market_hash_name','buy_max_price','sell_num'
      ,'sell_min_price','sell_reference_price','quick_price','name','buy_num','game','goods_id','appid']
    df.columns = col_name
    conn_info = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(cfg.user,cfg.passwd,cfg.host,cfg.port,cfg.DB_NAME)
    engine = create_engine(conn_info)
    # print(conn_info)

    df.to_sql(name='game_buff_goods',con=engine,schema='{}'.format(cfg.SCHEMA_NAME),index=False,if_exists='append')
  except:
    print('error!',df.shape)
  return len(lst)

if __name__ == '__main__':
  conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
  cursor = conn.cursor()
  sql = "DELETE FROM {}.game_buff_goods".format(cfg.SCHEMA_NAME)
  cursor.execute(sql) # 删除当前数据
  conn.commit()
  cursor.close()
  conn.close()

  ip_list = get_proxy()
  get_data(ip_list)