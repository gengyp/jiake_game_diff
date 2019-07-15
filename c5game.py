# coding:utf-8
import re
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

'''
c5game 最多显示 100 页，销售和求购 混在一起
1. 爬取所有 dota2 商品价格大于10的 销售 和 求购 商品
2. 爬取所有 csgo 商品价格大于100的 销售 和 求购 商品
'''
def get_data(ip_lst):
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
  # dota2
  url = "https://www.c5game.com/dota.html"
  appid = 570
  i = 0
  while True:
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"min":"10","max":"","k":"","rarity":"","quality":"","hero":"","tag":"","sort":"price","page":"{}".format(i+1),"locale":"zh"} # 销售
    i += 1
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_c5game2db(appid,r.text)
    print('dota2 sell current page is:{}'.format(i),end='\r')
    # 爬取销售商品 停止条件
    tree = etree.HTML(r.text)
    if 'purchaseing' in tree.xpath('//div[@class="tab-pane active"]/ul/li/@class'):
      break
  print('dota2 sell crawl finished!')

  i = 0
  while True:
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"min":"10","max":"","only":"on","k":"","rarity":"","quality":"","hero":"","tag":"","sort":"price","locale":"zh","page":"{}".format(i+1)} # 求购
    i += 1
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_c5game2db(appid,r.text)
    print('dota2 buy current page is:{}'.format(i),end='\r')
    # 爬取求购商品 停止条件
    tree = etree.HTML(r.text)
    if 'next disabled' in tree.xpath('//ul[@class="pagination clearfix"]/li/@class'):
      break
  print('dota2 buy crawl finished!')
  # # H1Z1
  # url = "https://www.c5game.com/market.html"
  # appid = 433850
  # for i in range(12):
  #   proxy = {'http': 'http://' + random.choice(ip_lst)}
  #   querystring = {"min":"5","max":"","k":"","rarity":"","quality":"","hero":"","tag":"","sort":"price.desc",
  #       "appid":"433850","locale":"zh","page":"{}".format(i+1)} # 出售&求购
  #   r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
  #   total = save_c5game2db(appid,r.text)
  #   print('current page is:{}\t goods num:{}'.format(i+1,total))

  # csgo
  url = "https://www.c5game.com/csgo/default/result.html"
  appid = 730
  i = 0
  while True:
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"min":"100","max":"","k":"","csgo_filter_category":"","rarity":"","quality":""
      ,"exterior":"","sort":"price","type":"","tag":"","locale":"zh","page":"{}".format(i+1)} # 出售
    i += 1
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_c5game2db(appid,r.text)
    print('csgo sell current page is:{}'.format(i),end='\r')
    # 爬取销售商品 停止条件
    tree = etree.HTML(r.text)
    if 'purchaseing' in tree.xpath('//div[@class="tab-pane active"]/ul/li/@class'):
      break
  print('csgo sell crawl finished!')

  i = 0
  while True:
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"min":"100","max":"","only":"on","k":"","csgo_filter_category":"","rarity":"","quality":""
      ,"exterior":"","sort":"price","type":"","tag":"","locale":"zh","page":"{}".format(i+1)} # 求购
    i += 1
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_c5game2db(appid,r.text)
    print('csgo buy current page is:{}'.format(i),end='\r')
    # 爬取求购商品 停止条件
    tree = etree.HTML(r.text)
    if 'next disabled' in tree.xpath('//ul[@class="pagination clearfix"]/li/@class'):
      break
  print('csgo buy crawl finished!')

def save_c5game2db(appid,html):
  tree = etree.HTML(html)

  goods_names = tree.xpath('//*[@id="yw0"]/div[1]/ul/li/a/img/@alt')
  good_statuses = tree.xpath('//*[@id="yw0"]/div[1]/ul/li/p[2]/span[1]/text()[1]')
  amounts = tree.xpath('//*[@id="yw0"]/div[1]/ul/li/p[2]/span[1]/span/text()')
  good_nums = tree.xpath('//*[@id="yw0"]/div[1]/ul/li/p[2]/span[2]/text()')

  lst = []
  for i in range(len(goods_names)):
    goods_name = goods_names[i].replace("'",'')
    amount = eval(re.search(r'\d.*',amounts[i]).group())
    good_status = good_statuses[i].strip().split(':')[0].replace("求购价","求购").replace("售价","在售")
    good_num = eval(good_nums[i].strip().split('件')[0])
    lst.append([appid,goods_name,amount,good_status,good_num])

  # store valid proxies into db.
  try:
    df = pd.DataFrame(lst)
    col_name = ['appid','good_name','amount','good_status','good_num']
    df.columns = col_name

    engine = create_engine('postgresql+psycopg2://postgres:root@localhost:5432/linzi')
    df.to_sql(name='game_c5game_goods',con=engine,schema='jiake',index=False,if_exists='append')
  except:
    print('error!',df.shape,lst)

  return len(goods_names)


if __name__ == '__main__':
  conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
  cursor = conn.cursor()
  sql = "DELETE FROM jiake.game_c5game_goods"
  cursor.execute(sql) # 删除当前数据
  conn.commit()
  cursor.close()
  conn.close()

  ip_list = get_proxy()
  get_data(ip_list)

