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
  circles = [177,15,5,1] # 依次循环次数
  # circles = [1,1,1,1] # test
  print('current circles \ndota2:sales-{},buying-{}; \nH1Z1:sales-{},buying-{};'.format(*circles))
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
  # dota2
  url = "https://www.igxe.cn/dota2/570"
  appid = eval(url.split('/')[-1])
  for i in range(circles[0]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"is_buying":"0","is_stattrak[]":["0","0"],"price_from":"10","price_to":"2000","sort":"2","ctg_id":"0","type_id":"0","page_no":"{}".format(i+1),
      "page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557025475913"} # 出售
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_igxe2db(appid,r.text)
    print('current page is:{}\tgoods num:{}'.format(i+1,total))

  for i in range(circles[1]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"is_buying":"1","is_stattrak[]":["0","0"],"price_from":"10","price_to":"2000","sort":"2","ctg_id":"0","type_id":"0","page_no":"{}".format(i+1),
      "page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557026884738"} # 求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_igxe2db(appid,r.text)
    print('current page is:{}\tgoods num:{}'.format(i+1,total))

  # # H1Z1
  # url = "https://www.igxe.cn/h1z1/433850"
  # appid = eval(url.split('/')[-1])
  # for i in range(circles[2]): # 21
  #   proxy = {'http': 'http://' + random.choice(ip_lst)}
  #   querystring = {"is_buying":"0","is_stattrak[]":["0","0"],"price_from":"10","sort":"2","ctg_id":"0","type_id":"0","page_no":"{}".format(i+1),
  #     "page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557034298679"} # 出售
  #   r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
  #   total = save_igxe2db(appid,r.text)
  #   print('current page is:{}\tgoods num:{}'.format(i+1,total))

  # for i in range(circles[3]):
  #   proxy = {'http': 'http://' + random.choice(ip_lst)}
  #   querystring = {"is_buying":"1","is_stattrak[]":["0","0"],"price_from":"10","sort":"2","ctg_id":"0","type_id":"0","page_no":"{}".format(i+1),
  #     "page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557026884738"} # 求购
  #   r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
  #   total = save_igxe2db(appid,r.text)
  #   print('current page is:{}\tgoods num:{}'.format(i+1,total))

  # csgo
  url = "https://www.igxe.cn/csgo/730"
  appid = eval(url.split('/')[-1])
  for i in range(124):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"is_buying":"0","is_stattrak[]":["0","0"],"price_from":"100","sort":"2","ctg_id":"0","type_id":"0",
      "page_no":"{}".format(i+1),"page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557660313335",
      "is_stattrak%5B%5D":["0","0"]} # 出售
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_igxe2db(appid,r.text)
    print('current page is:{}\tgoods num:{}'.format(i+1,total))

  for i in range(40):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"is_buying":"1","is_stattrak[]":["0","0"],"price_from":"100","sort":"2","ctg_id":"0","type_id":"0",
      "page_no":"{}".format(i+1),"page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557660068590",
      "is_stattrak%5B%5D":["0","0"]} # 求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_igxe2db(appid,r.text)

def save_igxe2db(appid,html):
  tree = etree.HTML(html)

  goods_names = tree.xpath('//*[@id="center"]/div/div[3]/div/div[2]/a/div[@class="name"]/@title')
  amounts = tree.xpath('//*[@id="center"]/div/div[3]/div/div[2]/a/div[@class="inf clearfix"]/div[1]/span/text()')
  amount_subs = tree.xpath('//*[@id="center"]/div/div[3]/div/div[2]/a/div[@class="inf clearfix"]/div[1]/sub/text()')
  good_statuses = tree.xpath('//*[@id="center"]/div/div[3]/div/div[2]/a/div[@class="inf clearfix"]/div[2]/text()')

  lst = []
  for i in range(len(goods_names)):
    goods_name = goods_names[i].replace("'",'')
    good_status = good_statuses[i].split('：')[0]
    good_num = eval(good_statuses[i].split('：')[1])
    lst.append([appid,goods_name,amounts[i]+amount_subs[i],good_status,good_num])

  # store valid proxies into db.
  try:
    df = pd.DataFrame(lst)
    col_name = ['appid','good_name','amount','good_status','good_num']
    df.columns = col_name

    engine = create_engine('postgresql+psycopg2://postgres:root@localhost:5432/linzi')
    df.to_sql(name='game_igxe_goods',con=engine,schema='jiake',index=False,if_exists='append')
  except:
    print('error!',df.shape,lst)

  return len(goods_names)

if __name__ == '__main__':
  conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
  cursor = conn.cursor()
  sql = "DELETE FROM jiake.game_igxe_goods"
  cursor.execute(sql) # 删除当前数据
  conn.commit()
  cursor.close()
  conn.close()

  ip_list = get_proxy()
  get_data(ip_list)

