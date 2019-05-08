#! /usr/bin/env python
# coding: utf-8
import os
import time
import datetime
import requests
import json
import psycopg2
import pandas as pd
from sqlalchemy import create_engine


def output2dingding():
  sql = '''
    SELECT a.name,buy_max_price max_buy_price,sale_price_min min_sale_price,diff,lowplat
    from (
    SELECT a.market_hash_name,a.name,buy_max_price::NUMERIC,b.on_sale_price_min/100.0 sale_price_min,buy_max_price::NUMERIC - b.on_sale_price_min/100.0 diff,'stmbuy' lowplat
    from jiake.game_buff_goods a
    INNER JOIN jiake.game_stmbuy_goods b on a.market_hash_name=b.market_hash_name
    WHERE b.on_sale_count>0
    union all
    SELECT a.market_hash_name,a.name,b.on_seek_price_max/100.0 seek_price_max,a.sell_min_price::NUMERIC,b.on_seek_price_max/100.0 - a.sell_min_price::NUMERIC diff,'buff' lowplat
    from jiake.game_buff_goods a
    INNER JOIN jiake.game_stmbuy_goods b on a.market_hash_name=b.market_hash_name
    )a WHERE diff >0
    ORDER BY 4 desc
    '''
  engine = create_engine('postgresql+psycopg2://postgres:root@localhost:5432/linzi')
  df = pd.read_sql(sql,engine)

  # 这个 url 从 PC 端钉钉群组->管理机器人里获得
  dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=3f4585affb8636bf1e1d090d1cf09621128c137de2deec3357661ef3351c735b"
  headers = {"Content-Type": "application/json; charset=utf-8"}

  if len(df) != 0:
    post_data = {
        "msgtype": "text",
        "text": {
            "content": str(df)
        },
        "at": {
            "atMobiles": [],
            "isAtAll": True
        }
    }
  else:
    post_data = {
        "msgtype": "text",
        "text": {
            "content": "当前时段无符合标准的数据！~~"
        },
        "at": {
            "atMobiles": [],
            "isAtAll": False
        }
    }
  r = requests.post(dingding_url, headers=headers, data=json.dumps(post_data))
  print(r.content)

def main():
  while True:
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' 爬取 buff 平台数据...')
    os.system('python buff_163.py > buff_163.log')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' 爬取 stmbuy 平台数据...')
    os.system('python stmbuy.py > stmbuy.log')
    # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' 爬取 c5game 平台数据...')
    # os.system('python c5game.py > c5game.log')
    # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' 爬取 igxe 平台数据...')
    # os.system('python igxe.py > igxe.log')
    # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' 爬取 v5fox 平台数据...')
    # os.system('python v5fox.py > v5fox.log')
    output2dingding()
    if datetime.datetime.now().hour==0 or (datetime.datetime.now().hour==23 and (60-datetime.datetime.now().minute)<=20):
      print('It is time to sleep!!!')
      time.sleep(8*3600-600)
    elif datetime.datetime.now().hour==23 and (60-datetime.datetime.now().minute)>20:
      print('Preparing to sleep!~~')
      time.sleep((58 - datetime.datetime.now().minute)*60)
    else:
      print('Today is new day,move on!~~',end='\r')
      time.sleep(40*60)


if __name__ == '__main__':
  main()