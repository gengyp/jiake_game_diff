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
sys.path.insert(0,'../Proxy')
import config as cfg
from buff import get_proxy


def get_data(ip_lst):
    # crawl website: https://www.stmbuy.com/dota2
    url = "https://api2.stmbuy.com/gameitem/list.json"
    headers = {'Origin': "https://www.stmbuy.com",
      'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}

    circles = [250,18] # 依次循环次数
    start_page = [3,1]
    # circles = [1,1] # test
    # start_page = [1,1]
    # dota2
    for i in range(circles[0]):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      # querystring = {"row":"20","page":"{}".format(i+9),"appid":"570","category_id":"","showseek":"1","filter":"{}",
      #   "sort":"-on_seek_price_max"} # dota2 求购
      querystring = {"row":"20","page":"{}".format(i + start_page[0]),"appid":"570","category_id":"","filter":"{}",
        "sort":"-market_price,-on_sale_count"} # dota2 出售
      r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
      total = save_stmbuy2db(json.loads(r.text))
      print('current page is:{}\tgoods num:{}'.format(i+1,total))

    # H1Z1
    for i in range(circles[1]):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"row":"20","page":"{}".format(i + start_page[1]),"appid":"433850","category_id":"","filter":"{}",
        "sort":"-market_price,-on_sale_count"} # H1Z1 出售
      r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
      total = save_stmbuy2db(json.loads(r.text))
      print('current page is:{}\tgoods num:{}'.format(i+1,total))


def save_stmbuy2db(dts):
  count = dts['count']
  page = dts['page']
  # print('next page:{}\ttotal num:{}'.format(page,count))


  lst = []
  for dt in dts['data']:
    on_seek_price_max = dt.get('on_seek_price_max',0)
    on_seek_price_min = dt.get('on_seek_price_min',0)
    market_name = dt.get('market_name','unknown').replace("'",'')
    on_sale_price_max = dt.get('on_sale_price_max',0)
    on_sale_price_min = dt.get('on_sale_price_min',0)
    sale_count = dt.get('sale_count',0)
    market_price = dt.get('market_price',0)
    on_sale_count = dt.get('on_sale_count',0)
    on_seek_count = dt.get('on_seek_count',0)
    last_price = dt.get('last_price',0)
    itime =  datetime.datetime.fromtimestamp(dt.get('itime',0))
    utime = datetime.datetime.fromtimestamp(dt.get('utime',0))
    market_hash_name = dt.get('market_hash_name','unknown').replace("'",'')
    class_id = dt.get('_id','')
    appid = dt.get('appid',0)

    lst.append([on_seek_price_max,on_seek_price_min,market_name,on_sale_price_max,on_sale_price_min,sale_count,
                market_price,on_sale_count,on_seek_count,last_price,itime,utime,market_hash_name,class_id,appid])

  # store valid proxies into db.
  try:
    df = pd.DataFrame(lst)
    col_name = ['on_seek_price_max','on_seek_price_min','market_name','on_sale_price_max','on_sale_price_min','sale_count'
      ,'market_price','on_sale_count','on_seek_count','last_price','itime','utime','market_hash_name','class_id','appid']
    df.columns = col_name

    engine = create_engine('postgresql+psycopg2://postgres:root@localhost:5432/linzi')
    df.to_sql(name='game_stmbuy_goods',con=engine,schema='jiake',index=False,if_exists='append')
  except:
    print('error!',df.shape,lst)
  return len(lst)

if __name__ == '__main__':
  conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
  cursor = conn.cursor()
  sql = "DELETE FROM jiake.game_stmbuy_goods"
  cursor.execute(sql) # 删除当前数据
  conn.commit()
  cursor.close()
  conn.close()

  ip_list = get_proxy()
  get_data(ip_list)

