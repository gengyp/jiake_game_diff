# coding:utf-8
import json
import time
import random
import datetime
import requests
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

from buff import save_buff2db
from c5game import save_c5game2db
from igxe import save_igxe2db
from stmbuy import save_stmbuy2db
from v5fox import save_v5fox2db

from buff import get_proxy
import sys
sys.path.insert(0,'./else')
import config as cfg


def get_data(ip_lst):
    circles = [498,100,75,319,60,200,77] # 依次循环次数
    # circles = [1,1,1,1,1,1,1] # 测试

    # buff 求购数据
    url = "https://buff.163.com/api/market/goods/buying"
    print(url)
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
    for i in range(circles[0]):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"game":"csgo","page_num":"{}".format(1+i),"sort_by":"price.desc","min_price":"5","max_price":"2000","_":"1557652874396"}
      try:
        r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
        save_buff2db(json.loads(r.text))
      except Exception as e:
        raise e

    # c5game
    total_flag = 0
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    url = "https://www.c5game.com/csgo/default/result.html"
    print(url)
    appid = 730
    for i in range(circles[1]):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"min":"5","max":"2000","k":"","csgo_filter_category":"","rarity":"","quality":"",
        "exterior":"","sort":"price.desc","type":"","tag":"","locale":"zh","page":"{}".format(i+1)}
      r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
      total = save_c5game2db(appid,r.text)
      if total_flag==total:
        print('current page is:{}\t goods num:{}'.format(i+1,total),end='\r')
      else:
        total_flag = total
        print('current page is:{}\t goods num:{}'.format(i+1,total))

    for i in range(circles[2]):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"min":"5","max":"2000","only":"on","k":"","csgo_filter_category":"","rarity":"",
        "quality":"","exterior":"","sort":"price.desc","type":"","tag":"","locale":"zh","page":"{}".format(i+1)}
      r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
      total = save_c5game2db(appid,r.text)
      if total_flag==total:
        print('current page is:{}\t goods num:{}'.format(i+1,total),end='\r')
      else:
        total_flag = total
        print('current page is:{}\t goods num:{}'.format(i+1,total))

    # igxe
    url = "https://www.igxe.cn/csgo/730"
    print(url)
    appid = eval(url.split('/')[-1])
    for i in range(circles[3]):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"is_buying":"0","is_stattrak[]":["0","0"],"price_from":"5","price_to":"2000","sort":"2","ctg_id":"0","type_id":"0",
        "page_no":"{}".format(i+1),"page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557660313335",
        "is_stattrak%5B%5D":["0","0"]} # 出售
      r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
      total = save_igxe2db(appid,r.text)
      if total_flag==total:
        print('current page is:{}\t goods num:{}'.format(i+1,total),end='\r')
      else:
        total_flag = total
        print('current page is:{}\t goods num:{}'.format(i+1,total))

    for i in range(circles[4]):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"is_buying":"1","is_stattrak[]":["0","0"],"price_from":"5","price_to":"2000","sort":"2","ctg_id":"0","type_id":"0",
        "page_no":"{}".format(i+1),"page_size":"20","rarity_id":"0","exterior_id":"0","quality_id":"0","capsule_id":"0","_t":"1557660068590",
        "is_stattrak%5B%5D":["0","0"]} # 求购
      r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
      total = save_igxe2db(appid,r.text)
      if total_flag==total:
        print('current page is:{}\t goods num:{}'.format(i+1,total),end='\r')
      else:
        total_flag = total
        print('current page is:{}\t goods num:{}'.format(i+1,total))

    # stmbuy 出售
    url = "https://api2.stmbuy.com/gameitem/list.json"
    print(url)
    for i in range(circles[5]):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"row":"20","page":"{}".format(i + 9),"appid":"730","category_id":"","filter":"{}","sort":"-market_price,-on_sale_count"}
      r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
      total = save_stmbuy2db(json.loads(r.text))
      if total_flag==total:
        print('current page is:{}\t goods num:{}'.format(i+1,total),end='\r')
      else:
        total_flag = total
        print('current page is:{}\t goods num:{}'.format(i+1,total))

    # v5fox
    url = "https://www.v5fox.com/csgo"
    print(url)
    appid = 730
    for i in range(circles[6]):
      proxy = {'http': 'http://' + random.choice(ip_lst)}
      querystring = {"keyword":"","min_price":"5.00","max_price":"","rarity_id":"","exterior_id":"","quality_id":"","sort_key":"1",
        "sort_type":"2","only_flag":"","pageNum":"{}".format(i+1),"pageSize":"25"} # 出售&求购
      r = requests.request("GET", url, headers=headers, proxies=proxy, params=querystring)
      total = save_v5fox2db(appid,r.text)
      if total_flag==total:
        print('current page is:{}\t goods num:{}'.format(i+1,total),end='\r')
      else:
        total_flag = total
        print('current page is:{}\t goods num:{}'.format(i+1,total))

def output2dingding():
  engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(cfg.user,cfg.passwd,cfg.host,cfg.port,cfg.DB_NAME))
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

if __name__ == '__main__':
  while True:
    ip_list = get_proxy()
    get_data(ip_list)
    output2dingding()

    if datetime.datetime.now().hour>=6:
      sleep_hour = 29-datetime.datetime.now().hour
      sleep_minute = 60-datetime.datetime.now().minute
      print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'sleep:{}\thour {}\tminutes!~~'.format(sleep_hour,sleep_minute))
      time.sleep(sleep_hour*3600)
      time.sleep(sleep_minute*60)