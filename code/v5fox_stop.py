# coding:utf-8
import json
import time
import random
import datetime
import requests
import psycopg2
import pandas as pd
from lxml import etree


from buff import get_proxy
import config as cfg
from config import mod_data_pg

'''
注: 该平台已倒闭
dota2 商品数量少 销售和求购可以放到一起 商品起价10
csgo 商品数量少 销售和求购可以放到一起 商品起价100
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
    save_v5fox2db(appid,r.text)
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
    save_v5fox2db(appid,r.text)
    print('csgo current page:{}'.format(i),end='\r')
    # 爬取销售商品 停止条件
    tree = etree.HTML(r.text)
    if '下一页' not in tree.xpath('//div[@class="page-con"]/div/a/text()'):
      break
  print('csgo crawl finished!')






if __name__ == '__main__':
  # clear table
  sql = "DELETE FROM {}.game_v5fox_goods".format(cfg.SCHEMA_NAME)
  mod_data_pg(sql)

  ip_list = get_proxy()
  get_data(ip_list)

