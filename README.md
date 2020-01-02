游戏平台数据采集
===============
各个游戏平台游戏求购与在售等信息

### Construct your database
linux
step1: install Anaconda3-5.2.0-Linux-x86_64.sh and postgresql-10.
step2: 执行 ./else/game.sql 文件，其中 代理ip 非空

### Demo on how to use these program.
```python
# run script
python schedule.py
```

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