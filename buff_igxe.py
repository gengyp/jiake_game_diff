# coding:utf8
import json
import random
import psycopg2
import pandas as pd
import requests
from lxml import etree
from sqlalchemy import create_engine

from buff import get_proxy
import sys
sys.path.insert(0,'./else')
import config as cfg

'''
爬取含有 多普勒 的csgo 商品评级详情
'''
buff_url_search = "https://buff.163.com/api/market/goods"
buff_url_sell = "https://buff.163.com/api/market/goods/sell_order"
buff_url_buy = "https://buff.163.com/api/market/goods/buy_order"

igxe_url_search = "https://www.igxe.cn/csgo/730"
igxe_url_sell = "https://www.igxe.cn/product/trade/730/{}"
igxe_url_buy = "https://www.igxe.cn/purchase/get_product_purchases"

global ip_lst

ip_lst = get_proxy()

def output_csgo(df=None):
  delete_data()
  goods_name = list(df['market_name'].values)
  # goods_name = ['M9 刺刀（★） | 伽玛多普勒 (崭新出厂)'
  #   ,'爪子刀（★） | 多普勒 (崭新出厂)'
  #   ,'蝴蝶刀（★） | 多普勒 (崭新出厂)'
  #   ,'刺刀（★） | 伽玛多普勒 (崭新出厂)'
  #   ,'刺刀（★） | 多普勒 (崭新出厂)'
  #   ,'折叠刀（★） | 伽玛多普勒 (崭新出厂)']
  for good in goods_name:
    try:
      if '多普勒' in good:
          print('crawl good is:{}'.format(good))
          lst_buff = buff_data(good)
          lst_igxe = igxe_data(good)
          save2db(lst_buff)
          save2db(lst_igxe)
    except:
      print('error goods',good)

def save2db(lst):
    # store valid proxies into db.
    try:
        df = pd.DataFrame(lst)
        col_name = ['name','grade','price','good_status','platform']
        df.columns = col_name

        engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(cfg.user,cfg.passwd,cfg.host,cfg.port,cfg.DB_NAME))
        df.to_sql(name='buff_igxe_grade',con=engine,schema='jiake',index=False,if_exists='append')
    except:
        print('error!',df.shape,lst)

def buff_data(good):
    # 查询商品 id
    # 搜索是通过模糊匹配的，不准
    querystring = {"game":"csgo","page_num":"1","search":"{}".format(good),"_":"1562241624231"}
    dts = buff_request(buff_url_search,querystring)
    good_ids = [lst['id'] for lst in dts['data']['items'] if good==lst['name']]
    # print(len(good_ids)==1)

    lst = []

    for good_id in good_ids:

      # 获取 在售 信息
      querystring = {"game":"csgo","goods_id":"{}".format(good_id),"page_num":"1","sort_by":"default","mode":""
        ,"allow_tradable_cooldown":"1","_":"1562251948206"}
      dts = buff_request(buff_url_sell,querystring)
      page_num = dts['data']['total_page']


      for i in range(page_num):
        querystring = {"game":"csgo","goods_id":"{}".format(good_id),"page_num":"{}".format(i+1),"sort_by":"default","mode":""
          ,"allow_tradable_cooldown":"1","_":"1562251948206"}
        dts = buff_request(buff_url_sell,querystring)
        for dt in dts['data']['items']:
          try:
              grade = dt['asset_info']['info']['metaphysic']['data']['name']
          except:
              grade = ''
          price = float(dt['price'])
          good_status= 'selling'
          platform = 'buff'
          lst.append([good,grade,price,good_status,platform])
      # 获取 求购 信息
      querystring = {"game":"csgo","goods_id":"{}".format(good_id),"page_num":"1","_":"1562251948208"}
      dts = buff_request(buff_url_buy,querystring)
      page_num = dts['data']['total_page']

      for i in range(page_num):
        querystring = {"game":"csgo","goods_id":"{}".format(good_id),"page_num":"{}".format(i+1),"_":"1562251948208"}
        dts = buff_request(buff_url_buy,querystring)
        for dt in dts['data']['items']:
          try:
              grade = dt['specific'][0]['simple_text'].replace('hase','')
          except:
              grade = ''
          price = float(dt['price'])
          good_status= 'buy'
          platform = 'buff'
          lst.append([good,grade,price,good_status,platform])
    return lst

def igxe_data(good):
    # 查询商品 id
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    querystring = {"keyword":"{}".format(good)}
    try:
        r = requests.get(igxe_url_search,headers=headers, params=querystring)
        tree = etree.HTML(r.text)
        goods = tree.xpath('//div[@class="dataList"]/a/div[@class="name"]/@title')
        goods_url = tree.xpath('//div[@class="dataList"]/a/@href')
        for g,u in zip(goods,goods_url):
          if g==good:
            product_id = u.split('/')[-1]
    except Exception as e:
        raise e

    # 获取 在售 信息
    querystring = {"product_id":"{}".format(product_id)}
    r = requests.get(igxe_url_sell.format(product_id),params=querystring)
    dts = json.loads(r.text)
    page_num = dts['page']['page_count']

    lst = []
    for i in range(page_num):
      try:
        proxy = {'http': 'http://' + random.choice(ip_lst)}
        querystring = {"sort_rule":"0","buy_method":"0","status_locked":"0","is_sticker":"0","gem_attribute_id":""
        ,"gem_id":"","paint_seed_type":"0","paint_seed_id":"0","page_no":"{}".format(i+1),"cur_page":"1","product_id":"{}".format(product_id)}

        dts = json.loads(requests.get(igxe_url_sell.format(product_id),params=querystring, proxies=proxy).text)
        for dt in dts['d_list']:
          grade = dt.get('paint_name',0)
          price = float(dt['unit_price'])
          good_status= 'selling'
          platform = 'igxe'
          lst.append([good,grade,price,good_status,platform])
      except:
        print('error',dts)
    # 获取 求购 信息
    querystring = {"product_id":"{}".format(product_id)}
    dts = json.loads(requests.get(igxe_url_buy,params=querystring).text)
    for dt in dts['datas']['datas']:
        grade = dt.get('paint_name',0)
        price = float(dt['unit_price'])
        good_status= 'buy'
        platform = 'igxe'
        lst.append([good,grade,price,good_status,platform])
    return lst

def buff_request(url,querystring):
    proxy = {'http': 'http://' + random.choice(ip_lst)}
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

    response = requests.request("GET", url, headers=headers, params=querystring, proxies=proxy)

    dts = json.loads(response.text)
    return dts

def delete_data():
  conn = psycopg2.connect(host=cfg.host, port=cfg.port, user=cfg.user, password=cfg.passwd,database=cfg.DB_NAME)
  cursor = conn.cursor()
  sql = "DELETE FROM jiake.buff_igxe_grade"
  cursor.execute(sql) # 删除当前数据
  conn.commit()
  cursor.close()
  conn.close()

if __name__ == '__main__':
  output_csgo()