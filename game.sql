-- buff_163 table
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

-- c5game table
CREATE TABLE "jiake"."game_c5game_goods" (
  "index" SERIAL PRIMARY KEY,
  "appid" int8,
  "good_name" text COLLATE "default",
  "amount" float8,
  "good_status" text COLLATE "default",
  "good_num" int8,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP
  )WITH (OIDS=FALSE);


-- igxe table
CREATE TABLE "jiake"."game_igxe_goods" (
  "index" SERIAL PRIMARY KEY,
  "appid" int8,
  "good_name" text COLLATE "default",
  "amount" text COLLATE "default",
  "good_status" text COLLATE "default",
  "good_num" int8,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP
  )WITH (OIDS=FALSE);


-- stmbuy table
CREATE TABLE "jiake"."game_stmbuy_goods" (
  "index" SERIAL PRIMARY KEY,
  "on_seek_price_max" int8,
  "on_seek_price_min" int8,
  "market_name" text COLLATE "default",
  "on_sale_price_max" int8,
  "on_sale_price_min" int8,
  "sale_count" int8,
  "market_price" int8,
  "on_sale_count" int8,
  "on_seek_count" int8,
  "last_price" int8,
  "itime" timestamp(6),
  "utime" timestamp(6),
  "market_hash_name" text COLLATE "default",
  "class_id" text,
  "appid" int8,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP
  )WITH (OIDS=FALSE);

COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."on_seek_price_max" IS '最大求购单价';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."on_seek_price_min" IS '最小求购单价';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."market_name" IS '商品中文名称';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."on_sale_price_max" IS '当前最大售价';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."on_sale_price_min" IS '当前最小售价';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."sale_count" IS '累计出售';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."market_price" IS '市场参考价';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."on_sale_count" IS '当前在售数量';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."on_seek_count" IS '当前求购数量';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."last_price" IS '最近成交价';
COMMENT ON COLUMN "jiake"."game_stmbuy_goods"."appid" IS '游戏代码';

-- v5fox table
CREATE TABLE "jiake"."game_v5fox_goods" (
  "index" SERIAL PRIMARY KEY,
  "appid" int8,
  "good_name" text COLLATE "default",
  "amount" float8,
  "good_status" text COLLATE "default",
  "good_num" int8,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP
  )WITH (OIDS=FALSE);

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
)a WHERE diff >0
ORDER BY 4 desc

-- 版本二
DROP TABLE jiake.game_total;
CREATE TABLE jiake.game_total as
SELECT appid,good_name,amount,good_status,'v5fox' platform
from jiake.game_v5fox_goods
union
SELECT appid,market_name,on_sale_price_min/100.0,'在售','stmbuy'
from jiake.game_stmbuy_goods
WHERE on_sale_count>0
union
SELECT appid,good_name,amount,good_status,'c5game'
from jiake.game_c5game_goods
union
SELECT appid,market_name,on_seek_price_max/100.0,'求购','stmbuy'
from jiake.game_stmbuy_goods
WHERE on_seek_count>0
union
SELECT appid,name,sell_min_price::NUMERIC,'在售','buff'
from jiake.game_buff_goods a
WHERE sell_num>0
union
SELECT appid,name,a.buy_max_price::NUMERIC,'求购','buff'
from jiake.game_buff_goods a
WHERE buy_num>0;

SELECT a.appid,a.good_name,max_buy,min_sell,max_buy-min_sell diff
,b.platform max_platform,c.platform min_platform
from
(
    SELECT appid,good_name,max(case when good_status='求购' then amount else 0 end) max_buy
    ,min(case when good_status='在售' then amount end) min_sell
    from jiake.game_total a
    GROUP BY 1,2
)a
LEFT JOIN jiake.game_total b on a.appid=b.appid and a.good_name=b.good_name and a.max_buy=b.amount and b.good_status='求购'
LEFT JOIN jiake.game_total c on a.appid=c.appid and a.good_name=c.good_name and a.min_sell=c.amount and c.good_status='在售'
WHERE max_buy>0 and min_sell>0 and max_buy-min_sell>1
ORDER BY 5 desc