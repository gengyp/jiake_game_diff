
-- 查询出符合条件的商品
-- 版本一
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
WHERE a.sell_num>0
)a WHERE diff >1
ORDER BY 4 desc

-- 版本二
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
WHERE max_buy>0 and min_sell>0 and max_buy-min_sell>2
ORDER BY 5 desc

-- 查询出活跃的商品
SELECT *
from jiake.game_buff_goods
WHERE buy_num>10 and sell_num>10
and buy_max_price::NUMERIC>10 and sell_min_price::NUMERIC<=60

# buff&igxe 市场 中饰品名含有 多普勒 商品评级差价表
SELECT a.name,a.grade,max_buy,min_sell,max_buy - min_sell diff,b.platform max_p,a.platform min_p
from
(
    SELECT name,grade,price min_sell,platform
    from (
    SELECT *,"row_number"() over(partition by name,grade order by price) num
    from jiake.buff_igxe_grade
    where good_status='selling')a where num=1
)a
INNER JOIN
(
    SELECT name,grade,price max_buy,platform
    from (
    SELECT *,"row_number"() over(partition by name,grade order by price desc) num
    from jiake.buff_igxe_grade
    where good_status='buy')a where num=1
)b on a."name"=b.name and a.grade=b.grade
where max_buy - min_sell>-50
ORDER BY 5 desc