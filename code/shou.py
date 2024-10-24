# coding:utf-8
import json
import time
import random
import datetime
import requests
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

from buff import get_proxy
import sys
sys.path.insert(0,'./else')
import config as cfg

import warnings
warnings.filterwarnings("ignore")

def get_data(ip_lst):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}

    # csgo
    url = "https://www.50shou.cn/api/store/inventory/730"
    querystring = {"price_sort":"0","page":"1","count":"10"}
    response = requests.request("GET", url, headers=headers, params=querystring,verify=False)
    dts = json.loads(response.text)
    total_pages = dts['pages']
    total_num = dts['total']
    print('current game pages is:{}\tgoods num is:{}'.format(total_pages,total_num))
    for i in range(total_pages):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"price_sort":"0","page":"{}".format(i+1),"count":"10"}
      r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring,verify=False)
      total = save_shou2db(json.loads(r.text),appid=730)
      print('csgo sell current page is:{}'.format(i+1),end='\r')

    # data2
    url = "https://www.50shou.cn/api/store/inventory/570"
    querystring = {"price_sort":"0","page":"1","count":"10"}
    response = requests.request("GET", url, headers=headers, params=querystring,verify=False)
    dts = json.loads(response.text)
    total_pages = dts['pages']
    total_num = dts['total']
    print('\ncurrent game pages is:{}\tgoods num is:{}'.format(total_pages,total_num))
    for i in range(total_pages):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"price_sort":"0","page":"{}".format(i+1),"count":"10"}
      r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring,verify=False)
      total = save_shou2db(json.loads(r.text),appid=570)
      print('csgo sell current page is:{}'.format(i+1),end='\r')

def save_shou2db(dts,appid):
  lst = []
  for dt in dts['data']:
      # appid = dt.get('appid',0)
      stickerNum = dt.get('stickerNum',0)
      coolingTime = datetime.datetime.fromtimestamp(dt.get('coolingTime',0))
      price = dt.get('price',0)
      hero = dt.get('hero','0')
      englishName = dt.get('englishName','0')
      type = dt.get('type','0')
      exterior = dt.get('exterior','0')
      artifactId = dt.get('artifactId','0')
      name = dt.get('name','0')
      lst.append([appid,stickerNum,coolingTime,price,hero,englishName,type,exterior,artifactId,name])

  # store data into db.
  try:
    df = pd.DataFrame(lst)
    col_name = ['appid','stickerNum','coolingTime','price','hero','englishName','type','exterior','artifactId','name']
    df.columns = col_name

    engine = engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(cfg.user,cfg.passwd,cfg.host,cfg.port,cfg.DB_NAME))
    df.to_sql(name='game_shou_goods',con=engine,schema='{}'.format(cfg.SCHEMA_NAME),index=False,if_exists='append')
  except:
    print('error!',df.shape,lst)
  return len(lst)

if __name__ == '__main__':
  conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
  cursor = conn.cursor()
  sql = "DELETE FROM {}.game_shou_goods".format(cfg.SCHEMA_NAME)
  cursor.execute(sql) # 删除当前数据
  conn.commit()
  cursor.close()
  conn.close()

  ip_list = get_proxy()
  get_data(ip_list)

