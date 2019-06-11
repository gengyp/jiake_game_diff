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


def output2dingding(dfs):
  # 这个 url 从 PC 端钉钉群组->管理机器人里获得
  dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=3f4585affb8636bf1e1d090d1cf09621128c137de2deec3357661ef3351c735b"
  headers = {"Content-Type": "application/json; charset=utf-8"}

  for df in dfs:
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

def sql2data():
  engine = create_engine('postgresql+psycopg2://postgres:root@localhost:5432/linzi')
  sql = '''
      DROP TABLE jiake.game_total;
      CREATE TABLE jiake.game_total as
      SELECT appid,market_name,on_sale_price_min/100.0 amount,'在售' good_status,'stmbuy' platform
      from jiake.game_stmbuy_goods
      WHERE on_sale_count>0
      union
      SELECT appid,market_name,on_seek_price_max/100.0 amount,'求购' good_status,'stmbuy' platform
      from jiake.game_stmbuy_goods
      WHERE on_seek_count>0
      union
      SELECT appid,good_name,amount,good_status,'c5game' platform
      from jiake.game_c5game_goods
      union
      SELECT appid,name,sell_min_price::NUMERIC,'在售' good_status,'buff' platform
      from jiake.game_buff_goods a
      WHERE sell_num>0
      union
      SELECT appid,name,a.buy_max_price::NUMERIC,'求购' good_status,'buff' platform
      from jiake.game_buff_goods a
      union
      SELECT appid,name,price,'在售' good_status,'shou' platform
      from jiake.game_shou_goods
      union
      SELECT appid,good_name,amount::NUMERIC,good_status,'igxe' platform
      from jiake.game_igxe_goods;

      SELECT a.appid,a.market_name,max_buy,min_sell,max_buy-min_sell diff
      ,b.platform max_platform,c.platform min_platform
      from
      (
          SELECT appid,market_name,max(case when good_status='求购' then amount else 0 end) max_buy
          ,min(case when good_status='在售' then amount end) min_sell
          from jiake.game_total a
          GROUP BY 1,2
      )a
      LEFT JOIN jiake.game_total b on a.appid=b.appid and a.market_name=b.market_name and a.max_buy=b.amount and b.good_status='求购'
      LEFT JOIN jiake.game_total c on a.appid=c.appid and a.market_name=c.market_name and a.min_sell=c.amount and c.good_status='在售'
      WHERE max_buy>0 and min_sell>0 and max_buy-min_sell>100 and a.appid=730
      ORDER BY 5 desc
    '''
  sql2 = '''
    SELECT a.appid,a.market_name,max_buy,min_sell,max_buy-min_sell diff
      ,b.platform max_platform,c.platform min_platform
    from
    (
      SELECT appid,market_name,max(case when good_status='求购' then amount else 0 end) max_buy
      ,min(case when good_status='在售' then amount end) min_sell
      from jiake.game_total a
      GROUP BY 1,2
    )a
    LEFT JOIN jiake.game_total b on a.appid=b.appid and a.market_name=b.market_name and a.max_buy=b.amount and b.good_status='求购'
    LEFT JOIN jiake.game_total c on a.appid=c.appid and a.market_name=c.market_name and a.min_sell=c.amount and c.good_status='在售'
    WHERE max_buy>0 and min_sell>0 and max_buy-min_sell>5 and a.appid=433850
    ORDER BY 5 desc'''

  sql3 = '''
    SELECT a.appid,a.market_name,max_buy,min_sell,max_buy-min_sell diff
      ,b.platform max_platform,c.platform min_platform
    from
    (
      SELECT appid,market_name,max(case when good_status='求购' then amount else 0 end) max_buy
      ,min(case when good_status='在售' then amount end) min_sell
      from jiake.game_total a
      GROUP BY 1,2
    )a
    LEFT JOIN jiake.game_total b on a.appid=b.appid and a.market_name=b.market_name and a.max_buy=b.amount and b.good_status='求购'
    LEFT JOIN jiake.game_total c on a.appid=c.appid and a.market_name=c.market_name and a.min_sell=c.amount and c.good_status='在售'
    WHERE max_buy>0 and min_sell>0 and max_buy-min_sell>5 and a.appid=570
    ORDER BY 5 desc'''

  df = pd.read_sql(sql,engine)
  df2 = pd.read_sql(sql2,engine)
  df3 = pd.read_sql(sql3,engine)

  return df,df2,df3


def main():
  time_interval = 5
  while True:
    os.system('rm ./else/*.log')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' 爬取 buff 平台数据...')
    os.system('python buff.py > ./else/buff.log')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' 爬取 stmbuy 平台数据...')
    os.system('python stmbuy.py > ./else/stmbuy.log')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' 爬取 c5game 平台数据...')
    os.system('python c5game.py > ./else/c5game.log')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' 爬取 igxe 平台数据...')
    os.system('python igxe.py > ./else/igxe.log')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' 爬取 shou 平台数据...')
    os.system('python shou.py > ./else/shou.log')
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' 输出结果到钉钉...')
    dfs = sql2data()
    output2dingding(dfs)
    # 是否夜间运行
    if datetime.datetime.now().hour==0 or (datetime.datetime.now().hour==23 and (60-datetime.datetime.now().minute)<=time_interval/2):
      print('It is time to sleep!!!')
      time.sleep(8*3600-600)
    elif datetime.datetime.now().hour==23 and (60-datetime.datetime.now().minute)>time_interval/2:
      print('Preparing to sleep!~~')
      time.sleep((58 - datetime.datetime.now().minute)*60)
    else:
      print('Today is new day,move on!~~',end='\r')
      time.sleep(time_interval*60)


if __name__ == '__main__':
  main()

  # dfs = sql2data()
  # output2dingding(dfs)