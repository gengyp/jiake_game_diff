# coding:utf-8
import json
import time
import random
import datetime
import requests
import psycopg2
import pandas as pd
from lxml import etree
import sys
sys.path.insert(0,'../Proxy')
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
  circles = [274,22,7,1,319,60] # 依次循环次数
  # circles = [1,1,1,1,1,1] # test
  print('current circles \ndota2:sales-{},buying-{}; \nH1Z1:sales-{},buying-{};'.format(*circles))
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
  # dota2
  url = "https://www.igxe.cn/dota2/570"
  appid = eval(url.split('/')[-1])
  for i in range(circles[0]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"is_buying":"0","is_stattrak[]":["0","0"],"price_from":"5","price_to":"2000","sort":"2","ctg_id":"0","type_id":"0","page_no":"{}".format(i+1),
      "page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557025475913"} # 出售
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_data2db(appid,r.text)
    print('current page is:{}\tgoods num:{}'.format(i+1,total))
    # time.sleep(0.5)

  for i in range(circles[1]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"is_buying":"1","is_stattrak[]":["0","0"],"price_from":"5","price_to":"2000","sort":"2","ctg_id":"0","type_id":"0","page_no":"{}".format(i+1),
      "page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557026884738"} # 求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_data2db(appid,r.text)
    print('current page is:{}\tgoods num:{}'.format(i+1,total))
    time.sleep(0.5)

  # H1Z1
  url = "https://www.igxe.cn/h1z1/433850"
  appid = eval(url.split('/')[-1])
  for i in range(circles[2]): # 21
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"is_buying":"0","is_stattrak[]":["0","0"],"price_from":"5","price_to":"2000","sort":"2","ctg_id":"0","type_id":"0","page_no":"{}".format(i+1),
      "page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557034298679"} # 出售
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_data2db(appid,r.text)
    print('current page is:{}\tgoods num:{}'.format(i+1,total))
    time.sleep(0.5)

  for i in range(circles[3]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"is_buying":"1","is_stattrak[]":["0","0"],"price_from":"5","price_to":"2000","sort":"2","ctg_id":"0","type_id":"0","page_no":"{}".format(i+1),
      "page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557026884738"} # 求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_data2db(appid,r.text)
    print('current page is:{}\tgoods num:{}'.format(i+1,total))
    time.sleep(0.5)

  # csgo
  url = "https://www.igxe.cn/csgo/730"
  appid = eval(url.split('/')[-1])
  for i in range(circles[4]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"is_buying":"0","is_stattrak[]":["0","0"],"price_from":"5","price_to":"2000","sort":"2","ctg_id":"0","type_id":"0",
      "page_no":"{}".format(i+1),"page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557660313335",
      "is_stattrak%5B%5D":["0","0"]} # 出售

    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_data2db(appid,r.text)
    print('current page is:{}\tgoods num:{}'.format(i+1,total))
    time.sleep(0.5)

  for i in range(circles[5]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"is_buying":"1","is_stattrak[]":["0","0"],"price_from":"5","price_to":"2000","sort":"2","ctg_id":"0","type_id":"0",
      "page_no":"{}".format(i+1),"page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557660068590",
      "is_stattrak%5B%5D":["0","0"]} # 求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_data2db(appid,r.text)
    print('current page is:{}\tgoods num:{}'.format(i+1,total))
    time.sleep(0.5)

def save_data2db(appid,html):
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
  # print ("\n>>>>>>>>>>>>>>>>>>>> Insert to database Start  <<<<<<<<<<<<<<<<<<<<<<")
  try:
    conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
    cursor = conn.cursor()
    for i,t in enumerate(lst):
      sql = '''INSERT INTO jiake.game_igxe_goods(appid,good_name,amount,good_status,good_num) VALUES({},'{}','{}','{}',{})'''.format(*t)
      cursor.execute(sql)
      conn.commit()
      # print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"insert successfully."+str(i+1),end='\r')
  except Exception as e:
    raise e
  finally:
    cursor.close()
    conn.close()
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

