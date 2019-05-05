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

'''
CREATE TABLE "jiake"."game_v5fox_goods" (
  "index" SERIAL PRIMARY KEY,
  "appid" int8,
  "good_name" text COLLATE "default",
  "amount" float8,
  "good_status" text COLLATE "default",
  "good_num" int8,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP
  )WITH (OIDS=FALSE);
'''
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
  circles = [60] # 依次循环次数
  # print('current circles \ndota2:sales-{},buying-{}; \nH1Z1:sales-{},buying-{};'.format(*circles))
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
  # dota2
  url = "https://www.v5fox.com/dota2"
  appid = 570
  for i in range(circles[0]):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
    querystring = {"keyword":"","min_price":"1.00","max_price":"1000.00","sort_key":"1","sort_type":"2",
        "only_flag":"","pageNum":"{}".format(i+1),"pageSize":"25"} # 出售&求购
    r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    save_data2db(appid,r.text)
    print(i+1,">>>>>>>>>>>>>>>>>>>> Insert to database Ended  <<<<<<<<<<<<<<<<<<<<<<",end='\r')
    time.sleep(0.5)

def save_data2db(appid,html):
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
  # print ("\n>>>>>>>>>>>>>>>>>>>> Insert to database Start  <<<<<<<<<<<<<<<<<<<<<<")
  try:
    conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
    cursor = conn.cursor()
    for i,t in enumerate(lst):

      sql = '''INSERT INTO jiake.game_v5fox_goods(appid,good_name,amount,good_status,good_num) VALUES({},'{}',{},'{}',{})'''.format(*t)

      cursor.execute(sql)
      conn.commit()
      # print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"insert successfully."+str(i+1),end='\r')
  except Exception as e:
    raise e
  finally:
    cursor.close()
    conn.close()


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

