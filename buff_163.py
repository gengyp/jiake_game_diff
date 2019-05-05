# coding:utf-8
import json
import time
import random
import datetime
import requests
import psycopg2
import pandas as pd
import sys
sys.path.insert(0,'../Proxy')
import config as cfg

'''
CREATE TABLE "jiake"."game_buff_goods" (
"index" serial,
"steam_price" text COLLATE "default",
"steam_price_cny" text COLLATE "default",
"market_hash_name" text COLLATE "default",
"buy_max_price" text COLLATE "default",
"sell_num" int8,
"sell_min_price" text COLLATE "default",
"sell_reference_price" text COLLATE "default",
"quick_price" text COLLATE "default",
"name" text COLLATE "default",
"buy_num" int8,
"game" text COLLATE "default",
"goods_id" int8,
"appid" int8,
"create_time" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)WITH (OIDS=FALSE);

COMMENT ON COLUMN "jiake"."game_buff_goods"."steam_price" IS 'Steam美元价';
COMMENT ON COLUMN "jiake"."game_buff_goods"."steam_price_cny" IS 'Steam人名币价';
COMMENT ON COLUMN "jiake"."game_buff_goods"."buy_max_price" IS '求购最大单价';
COMMENT ON COLUMN "jiake"."game_buff_goods"."sell_num" IS '当前在售数';
COMMENT ON COLUMN "jiake"."game_buff_goods"."sell_min_price" IS '当前最小售价';
COMMENT ON COLUMN "jiake"."game_buff_goods"."name" IS '商品中文名称';
COMMENT ON COLUMN "jiake"."game_buff_goods"."buy_num" IS '当前求购数量';
COMMENT ON COLUMN "jiake"."game_buff_goods"."game" IS '游戏名称';
COMMENT ON COLUMN "jiake"."game_buff_goods"."appid" IS '游戏代码';
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
    # website https://buff.163.com/market/?game=dota2#tab=buying&page_num=1
    url = "https://buff.163.com/api/market/goods/buying"
    headers = {
      'Accept': 'application/json, text/javascript, */*; q=0.01',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'Connection': 'keep-alive',
      'Cookie': '_ntes_nnid=5095810d461811f7dc838877a17f425e,1537173746258; _ntes_nuid=5095810d461811f7dc838877a17f425e; vjuids=-99dfec9a3.166959e011a.0.4235fdae1b734; vjlast=1540108452.1540108452.30; __oc_uuid=517f3650-ebf0-11e8-8522-790aadc56740; __utma=187553192.28276556.1539135868.1542630585.1542632967.4; __utmz=187553192.1542632967.4.3.utmcsr=open.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/special/cuvocw/qiyecaiwu.html; vinfo_n_f_l_n3=906020b7a134d80f.1.3.1540108449670.1545901070101.1552872008117; _ga=GA1.2.28276556.1539135868; usertrack=ezq0ZVzC/jM0QTkRBF0VAg==; _gid=GA1.2.442229967.1556376581; csrf_token=17b123f4549af663a251cb77dcfe57b56d1251a0; game=dota2; NTES_YD_SESS=LehxiEaGpZbw5rGP55KXBpeGDWxYqfI5OZs0yIjWTTzDv4jcvh2dqALszP7FAa2a.Vg1D14Xx3.CTQ1xMJN8jJ1b.X3mgw6qyhQzlbihLxuhYZOrUEOH0XR5SHikJ3Azra7UwAzSsiNiAQyIpI3X.QKM9.E9maADxUYguN8qSqqwGE5e0m.FsPwAO_r2hGwQQg5TY0ZG8o63GBQTKZjIP5Zxw0FysOtwl1OMw.Ec9ciQK; S_INFO=1556434091|0|3&80##|17826853236; P_INFO=17826853236|1556434091|0|netease_buff|00&99|null&null&null#zhj&330100#10#0#0|&0|null|17826853236; session=1-exfqRmFc-LlCuZ0E5GNLuQoR2f6q6jzNtHcWzX_JkMsb2046372339',
      'Host': 'buff.163.com',
      'Referer': 'https://buff.163.com/market/?game=dota2',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
      'X-Requested-With': 'XMLHttpRequest'
        }
    # DOTA2 数据量较大，只爬取求购数据
    for i in range(300):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"game":"dota2","page_num":"{}".format(2+i),"sort_by":"price.desc","_":"1556434296404"} # dota2 求购
      try:
        r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
        save_data2db(json.loads(r.text))
      except Exception as e:
        raise e
      time.sleep(0.2)

    # H1Z1 求购数据较少，故爬取出售数据
    time.sleep(5)
    for i in range(15):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"game":"h1z1","page_num":"{}".format(2+i),"sort_by":"price.desc","_":"1556461440132"}
      try:
        r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
        save_data2db(json.loads(r.text))
      except Exception as e:
        raise e
      time.sleep(0.2)

    # # CS:GO 求购数据较少，故爬取出售数据
    # time.sleep(5)
    # for i in range(450):
    #   proxy = {'http': 'http://' + random.choice(ip_lst)}
    #   querystring = {"game":"csgo","page_num":"{}".format(30+i),"sort_by":"price.desc","_":"1556548044595"}
    #   try:
    #     r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
    #     save_data2db(json.loads(r.text))
    #   except Exception as e:
    #     raise e
    #   time.sleep(0.2)

def save_data2db(dts):
  page_num = dts['data']['page_num']
  page_size = dts['data']['page_size']
  total_count = dts['data']['total_count']
  total_page = dts['data']['total_page']
  print('当前页数：{}商品数量：{}商品总数：{}网页数：{}'.format(page_num,page_size,total_count,total_page))

  # col_name = ['steam_price','steam_price_cny','market_hash_name','buy_max_price'
  #   ,'sell_num','sell_min_price','sell_reference_price','quick_price','name','buy_num','game']

  lst = []
  for dt in dts['data']['items']:
    steam_price = dt['goods_info']['steam_price']
    steam_price_cny = dt['goods_info']['steam_price_cny']
    market_hash_name = dt['market_hash_name'].replace("'",'')
    buy_max_price = dt['buy_max_price']
    sell_num = dt['sell_num']
    sell_min_price = dt['sell_min_price']
    sell_reference_price = dt['sell_reference_price']
    quick_price = dt['quick_price']
    name = dt['name'].replace("'",'')
    buy_num = dt['buy_num']
    game = dt['game']
    goods_id = dt.get('id',0)
    appid = dt.get('appid',0)

    lst.append([steam_price,steam_price_cny,market_hash_name,buy_max_price,sell_num
      ,sell_min_price,sell_reference_price,quick_price,name,buy_num,game,goods_id,appid])
  # df = pd.DataFrame(lst)
  # df.columns = col_name

  # store valid proxies into db.
  print ("\n>>>>>>>>>>>>>>>>>>>> Insert to database Start  <<<<<<<<<<<<<<<<<<<<<<")
  try:
    conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
    cursor = conn.cursor()
    for i,t in enumerate(lst):
      sql = '''INSERT INTO jiake.game_buff_goods(steam_price,steam_price_cny,market_hash_name,buy_max_price,sell_num,sell_min_price,
        sell_reference_price,quick_price,name,buy_num,game,goods_id,appid) VALUES('{}','{}', '{}','{}', '{}','{}', '{}','{}', '{}', {},'{}',{},{})'''.format(*t)
      cursor.execute(sql)
      conn.commit()
      print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"insert successfully."+str(i+1),end='\r')
  except Exception as e:
    raise e
  finally:
    cursor.close()
    conn.close()
  print( ">>>>>>>>>>>>>>>>>>>> Insert to database Ended  <<<<<<<<<<<<<<<<<<<<<<")

if __name__ == '__main__':
  conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
  cursor = conn.cursor()
  sql = "DELETE FROM jiake.game_buff_goods"
  cursor.execute(sql) # 删除当前数据
  conn.commit()
  cursor.close()
  conn.close()

  ip_list = get_proxy()
  get_data(ip_list)