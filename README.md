游戏平台数据采集
===============
各个游戏平台游戏求购与在售等信息

### Construct your database(Mac version) and use these program step by step
1. 下载 [Anaconda3镜像](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/) 安装
2. 下载 [postgresql镜像](https://www.postgresql.org/) 安装，建各平台数据采集表及代理ip入库
   1. 终端进入postgresql安装目录，执行`\i /path/to/your/sql/proxy_ips_games.sql`,`game.sql`
   2. 查看表`\dt games.*`.如果 数据库 postgres 里面有表 games.proxy_ips_games 说明运行成功
3. [config.py](./else/config.py) line50 换 [buff 平台](https://buff.163.com/market/?game=csgo#tab=selling&page_num=1)登陆进去，任一网页请求 cookies
4. [config.py](./else/config.py) line54 更换钉钉机器人加签密钥、webhook
5. `buff.py c5game.py csgo.py igxe.py shou.py stmbuy.py v5fox.py`均可 cmd 输入`python buff.py`单独测试,其他平台类似
6. 各个平台单独测试通过后，运行`python schedule.py`即可

备注：需要更换的可以写到配置文件中[config.py](./else/config.py)，缺点不方便调试

### crawl one good link
通过单个商品名称，爬取各个平台的价格
1. stmbuy：https://api2.stmbuy.com/game/item/onsale.json?appid=730&class_id=4c2b57013a8dc5d0
2. c5game:https://www.c5game.com/api/product/sale.json?id=553395655

### 代码更新纪要
1. 使用 Proxy 的逐条插入法
    1. buff:    16min 400 pages v=25
    2. stmbuy:  6min  270 pages v=45
    3. c5game:  5min  180 pages v=36
    4. igxe:    510s  300 pages v=35 pages/min
    5. v5fox:   70s   50  pages v=42.5
2. 使用 df.to_sql 法: