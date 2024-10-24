-- CREATE SCHEMA
CREATE SCHEMA if not exists games;
-- buff_igxe_grade table
CREATE TABLE if not exists "games"."buff_igxe_grade" (
"index" serial,
"name" text COLLATE "default",
"grade" text COLLATE "default",
"price" float8,
"good_status" text COLLATE "default",
"platform" text COLLATE "default",
"create_time" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)WITH (OIDS=FALSE);

-- buff_163 table
CREATE TABLE if not exists "games"."game_buff_goods" (
"index" serial,
"steam_price" text COLLATE "default",
"steam_price_cny" text COLLATE "default",
"market_hash_name" text COLLATE "default",
"buy_max_price" float8,
"sell_num" int8,
"sell_min_price" float8,
"sell_reference_price" text COLLATE "default",
"quick_price" text COLLATE "default",
"name" text COLLATE "default",
"buy_num" int8,
"game" text COLLATE "default",
"goods_id" int8,
"appid" int8,
"create_time" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)WITH (OIDS=FALSE);

COMMENT ON COLUMN "games"."game_buff_goods"."steam_price" IS 'Steam美元价';
COMMENT ON COLUMN "games"."game_buff_goods"."steam_price_cny" IS 'Steam人名币价';
COMMENT ON COLUMN "games"."game_buff_goods"."buy_max_price" IS '求购最大单价';
COMMENT ON COLUMN "games"."game_buff_goods"."sell_num" IS '当前在售数';
COMMENT ON COLUMN "games"."game_buff_goods"."sell_min_price" IS '当前最小售价';
COMMENT ON COLUMN "games"."game_buff_goods"."name" IS '商品中文名称';
COMMENT ON COLUMN "games"."game_buff_goods"."buy_num" IS '当前求购数量';
COMMENT ON COLUMN "games"."game_buff_goods"."game" IS '游戏名称';
COMMENT ON COLUMN "games"."game_buff_goods"."appid" IS '游戏代码';

-- c5game table
CREATE TABLE if not exists "games"."game_c5game_goods" (
  "index" SERIAL PRIMARY KEY,
  "appid" int8,
  "good_name" text COLLATE "default",
  "amount" float8,
  "good_status" text COLLATE "default",
  "good_num" int8,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP
  )WITH (OIDS=FALSE);


-- igxe table
CREATE TABLE if not exists "games"."game_igxe_goods" (
  "index" SERIAL PRIMARY KEY,
  "appid" int8,
  "good_name" text COLLATE "default",
  "amount" text COLLATE "default",
  "good_status" text COLLATE "default",
  "good_num" int8,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP
  )WITH (OIDS=FALSE);


-- stmbuy table
CREATE TABLE if not exists "games"."game_stmbuy_goods" (
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

COMMENT ON COLUMN "games"."game_stmbuy_goods"."on_seek_price_max" IS '最大求购单价';
COMMENT ON COLUMN "games"."game_stmbuy_goods"."on_seek_price_min" IS '最小求购单价';
COMMENT ON COLUMN "games"."game_stmbuy_goods"."market_name" IS '商品中文名称';
COMMENT ON COLUMN "games"."game_stmbuy_goods"."on_sale_price_max" IS '当前最大售价';
COMMENT ON COLUMN "games"."game_stmbuy_goods"."on_sale_price_min" IS '当前最小售价';
COMMENT ON COLUMN "games"."game_stmbuy_goods"."sale_count" IS '累计出售';
COMMENT ON COLUMN "games"."game_stmbuy_goods"."market_price" IS '市场参考价';
COMMENT ON COLUMN "games"."game_stmbuy_goods"."on_sale_count" IS '当前在售数量';
COMMENT ON COLUMN "games"."game_stmbuy_goods"."on_seek_count" IS '当前求购数量';
COMMENT ON COLUMN "games"."game_stmbuy_goods"."last_price" IS '最近成交价';
COMMENT ON COLUMN "games"."game_stmbuy_goods"."appid" IS '游戏代码';

-- v5fox table
CREATE TABLE if not exists "games"."game_v5fox_goods" (
  "index" SERIAL PRIMARY KEY,
  "appid" int8,
  "good_name" text COLLATE "default",
  "amount" float8,
  "good_status" text COLLATE "default",
  "good_num" int8,
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP
  )WITH (OIDS=FALSE);

-- 50shou table
CREATE TABLE if not exists "games"."game_shou_goods" (
  "id" SERIAL PRIMARY KEY,
  "appid" int8,
  "stickerNum" int8,
  "coolingTime" timestamp(6),
  "price" float8,
  "hero" text COLLATE "default",
  "englishName" text COLLATE "default",
  "type" text COLLATE "default",
  "exterior" text COLLATE "default",
  "artifactId" text COLLATE "default",
  "name" text COLLATE "default",
  "create_time" timestamp(6) DEFAULT CURRENT_TIMESTAMP
)WITH (OIDS=FALSE);
