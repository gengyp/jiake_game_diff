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
  circles = [100,78,13,6] # 依次循环次数
  print('current circles \ndota2:sales-{},buying-{}; \nH1Z1:sales-{},buying-{};'.format(*circles))
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
  # dota2
  url = "https://www.c5game.com/dota.html"
  appid = 570
  for i in range(circles[0]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"min":"3","max":"300","k":"","rarity":"","quality":"","hero":"","tag":"","sort":"price.desc",
        "locale":"zh","page":"{}".format(i+1)} # 出售
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_data2db(appid,r.text)
    print('current page is:{}\t商品总数:{}'.format(i+1,total))
    time.sleep(0.2)

  for i in range(circles[1]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"min":"2","max":"300","only":"on","k":"","rarity":"","quality":"","hero":"","tag":"",
        "sort":"price.desc","page":"{}".format(i+1),"locale":"zh"} # 求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_data2db(appid,r.text)
    print('current page is:{}\t商品总数:{}'.format(i+1,total))
    time.sleep(0.5)

  # H1Z1
  url = "https://www.c5game.com/market.html"
  appid = 433850
  for i in range(circles[2]): # 21
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"min":"3","max":"300","k":"","rarity":"","quality":"","hero":"","tag":"","sort":"price.desc",
        "appid":"433850","locale":"zh","page":"{}".format(i+1)} # 出售
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_data2db(appid,r.text)
    print('current page is:{}\t商品总数:{}'.format(i+1,total))
    time.sleep(0.5)

  for i in range(circles[3]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"min":"3","max":"300","only":"on","k":"","rarity":"","quality":"","hero":"","tag":"",
         "sort":"price.desc","appid":"433850","locale":"zh","page":"{}".format(i+1)} # 求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    total = save_data2db(appid,r.text)
    print('current page is:{}\t商品总数:{}'.format(i+1,total))
    time.sleep(0.5)

def save_data2db(appid,html):
  tree = etree.HTML(html)

  goods_names = tree.xpath('//*[@id="yw0"]/div[1]/ul/li/a/img/@alt')
  good_statuses = tree.xpath('//*[@id="yw0"]/div[1]/ul/li/p[2]/span[1]/text()')
  amounts = tree.xpath('//*[@id="yw0"]/div[1]/ul/li/p[2]/span[1]/span/text()')
  good_nums = tree.xpath('//*[@id="yw0"]/div[1]/ul/li/p[2]/span[2]/text()')

  lst = []
  for i in range(len(goods_names)):
    goods_name = goods_names[i].replace("'",'')
    amount = eval(amounts[i].split(' ')[1])
    good_status = good_statuses[i].split(':')[0].replace("求购价","求购").replace("售价","在售")
    good_num = eval(good_nums[i].split('件')[0])
    # 以下为英文 解析
    # if ' ' in good_statuses[i].split(':')[0]:
    #   good_status = '求购'
    # else:
    #   good_status = '在售'
    # good_num = eval(good_nums[i].split(' ')[0])
    lst.append([appid,goods_name,amount,good_status,good_num])

  # store valid proxies into db.
  # print ("\n>>>>>>>>>>>>>>>>>>>> Insert to database Start  <<<<<<<<<<<<<<<<<<<<<<")
  try:
    conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
    cursor = conn.cursor()
    for i,t in enumerate(lst):
      sql = '''INSERT INTO jiake.game_c5game_goods(appid,good_name,amount,good_status,good_num) VALUES({},'{}',{},'{}',{})'''.format(*t)
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
  sql = "DELETE FROM jiake.game_c5game_goods"
  cursor.execute(sql) # 删除当前数据
  conn.commit()
  cursor.close()
  conn.close()

  ip_list = get_proxy()
  get_data(ip_list)

