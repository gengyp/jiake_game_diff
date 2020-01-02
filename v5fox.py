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

from buff import get_proxy
import sys
sys.path.insert(0,'./else')
import config as cfg

'''
dota2 商品数量少，销售和求购可以放到一起，商品起价10
csgo 商品数量少，销售和求购可以放到一起，商品起价100
'''

def get_data(ip_lst):
  # circles = [50] # 依次循环次数
  # circles = [1] # test
  # print('current circles \ndota2:sales-{},buying-{}; \nH1Z1:sales-{},buying-{};'.format(*circles))
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
  # dota2
  url = "https://www.v5fox.com/dota2"
  appid = 570
  i = 0
  while True:
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"keyword":"","min_price":"10.00","max_price":"","sort_key":"1","sort_type":"2"
      ,"only_flag":"","pageNum":"{}".format(i+1),"pageSize":"25"} # 出售&求购
    i += 1
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_v5fox2db(appid,r.text)
    print('dota2 current page:{}'.format(i),end='\r')
    # 爬取销售商品 停止条件
    tree = etree.HTML(r.text)
    if '下一页' not in tree.xpath('//div[@class="page-con"]/div/a/text()'):
      break
  print('dota2 crawl finished!')

  # csgo
  url = "https://www.v5fox.com/csgo"
  appid = 730
  i = 0
  while True:
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"keyword":"","min_price":"100.00","max_price":"","rarity_id":"","exterior_id":"","quality_id":"","sort_key":"1"
      ,"sort_type":"1","only_flag":"","pageNum":"{}".format(i+1),"pageSize":"25"} # 出售&求购
    i += 1
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_v5fox2db(appid,r.text)
    print('csgo current page:{}'.format(i),end='\r')
    # 爬取销售商品 停止条件
    tree = etree.HTML(r.text)
    if '下一页' not in tree.xpath('//div[@class="page-con"]/div/a/text()'):
      break
  print('csgo crawl finished!')



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

    engine = engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(cfg.user,cfg.passwd,cfg.host,cfg.port,cfg.DB_NAME))
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

