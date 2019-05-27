# coding:utf-8
import json
import time
import random
import datetime
import requests
import psycopg2
import pandas as pd
from lxml import etree
from sqlalchemy import create_engine

import sys
sys.path.insert(0,'../Proxy')
import config as cfg
from buff import get_proxy


def get_data(ip_lst):
  circles = [50] # 依次循环次数
  # circles = [1] # test
  # print('current circles \ndota2:sales-{},buying-{}; \nH1Z1:sales-{},buying-{};'.format(*circles))
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
  # dota2
  url = "https://www.v5fox.com/dota2"
  appid = 570
  for i in range(circles[0]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"keyword":"","min_price":"5.00","max_price":"2000.00","sort_key":"1","sort_type":"2",
        "only_flag":"","pageNum":"{}".format(i+1),"pageSize":"25"} # 出售&求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_v5fox2db(appid,r.text)
    print('current page is:{}\tgoods num:{}'.format(i+1,total))

  # csgo
  url = "https://www.v5fox.com/csgo"
  appid = 730
  for i in range(85):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"keyword":"","min_price":"10.00","max_price":"","rarity_id":"","exterior_id":"","quality_id":"","sort_key":"1",
      "sort_type":"2","only_flag":"","pageNum":"{}".format(i+1),"pageSize":"25"} # 出售&求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_v5fox2db(appid,r.text)

def save_v5fox2db(appid,html):
  tree = etree.HTML(html)

  goods_names = tree.xpath('/html/body/div[6]/div[2]/div[2]/a/@title')
  amounts= tree.xpath('/html/body/div[6]/div[2]/div[2]/a/div[1]/div[2]/p/span/text()')
  good_statuses = tree.xpath('/html/body/div[6]/div[2]/div[2]/a/div[2]/div[2]/text()')

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

    engine = create_engine('postgresql+psycopg2://postgres:root@localhost:5432/linzi')
    df.to_sql(name='game_v5fox_goods',con=engine,schema='jiake',index=False,if_exists='append')
  except:
    print('error!',df.shape,lst)
  return len(lst)


if __name__ == '__main__':
  conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
  cursor = conn.cursor()
  sql = "DELETE FROM jiake.game_v5fox_goods"
  cursor.execute(sql) # 删除当前数据
  conn.commit()
  cursor.close()
  conn.close()

  ip_list = get_proxy()
  get_data(ip_list)

