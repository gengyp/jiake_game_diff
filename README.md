游戏平台数据采集
===============
各个游戏平台游戏求购与在售等信息

### Construct your database(Mac version) and use these program step by step
1. install [Anaconda3](https://www.anaconda.com/distribution/#download-section) and [postgresql](https://www.postgresql.org/download/).安装成功 cmd 可以输入`ipython`测试Anaconda3 是否安装成功。用数据库可视化工具连接 postgresql 测试是否成功。
2. 终端进入当前目录执行`psql -h localhost -p 5432 -U postgres -d postgres -t jiake.proxy_ips_games -f ./else/proxy_ips_games.sql`,[数据库连接参数按需修改](https://blog.csdn.net/weixin_42970378/article/details/90599970)。代理ip 入库，如果 数据库 postgres 里面有表 jiake.proxy_ips_games 说明运行成功
2. 终端进入当前目录执行`psql -h localhost -p 5432 -U postgres -d postgres -t jiake.proxy_ips_games -f ./else/game.sql`,[数据库连接参数按需修改](https://blog.csdn.net/weixin_42970378/article/details/90599970)。建表，如果数据库 postgres 目录下有很多 jiake.* 表说明成功。
3. [config.py](.else/config.py) line50 换 [buff 平台](https://buff.163.com/market/?game=csgo#tab=selling&page_num=1)登陆进去，任一网页请求 cookies
4. [config.py](.else/config.py) line54 更换钉钉机器人加签密钥、webhook
5. `buff.py c5game.py csgo.py igxe.py shou.py stmbuy.py v5fox.py`均可 cmd 输入`python buff.py`单独测试,其他平台类似
6. 各个平台单独测试通过后，运行`python schedule.py`即可

备注：需要更换的可以写到配置文件中[config.py](.else/config.py)，缺点不方便调试

### crawl one good link
通过单个商品名称，爬取各个平台的价格
1. stmbuy：https://api2.stmbuy.com/game/item/onsale.json?appid=730&class_id=4c2b57013a8dc5d0
2. c5game:https://www.c5game.com/api/product/sale.json?id=553395655
3. buff_163:
4. igxe:
5. v5fox:


### 代码更新纪要
1. 使用 Proxy 的逐条插入法
    1. buff:    16min 400 pages v=25
    2. stmbuy:  6min  270 pages v=45
    3. c5game:  5min  180 pages v=36
    4. igxe:    510s  300 pages v=35 pages/min
    5. v5fox:   70s   50  pages v=42.5
2. 使用 df.to_sql 法: