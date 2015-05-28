CREATE TABLE category (
	id BIGINT PRIMARY KEY, 
	name STRING
);
CREATE TABLE commodity (
	id BIGINT PRIMARY KEY, 
	average_price BIGINT, 
	category_id BIGINT, 
	name STRING
);
CREATE TABLE economy (
	id BIGINT PRIMARY KEY, 
	name STRING
);
CREATE TABLE listing ( -- commodities available on the market
	id BIGINT PRIMARY KEY, --87,
	buy_price BIGINT, --223,
	collected_at BIGINT, --1431043003,
	commodity_id BIGINT, --1,
	demand BIGINT, --0,
	sell_price BIGINT, --207,
	station_id BIGINT, --3,
	supply BIGINT, --46197,
	update_count BIGINT --"2"
);
CREATE TABLE station (
	id BIGINT PRIMARY KEY, --1,
	allegiance STRING, --null,
	distance_to_star BIGINT, --16253,
	faction STRING, --"",
	government STRING, --null,
	has_blackmarket BOOLEAN, --0,
	has_commodities BOOLEAN, --1,
	has_outfitting BOOLEAN, --null,
	has_rearm BOOLEAN, --null,
	has_refuel BOOLEAN, --null,
	has_repair BOOLEAN, --null,
	has_shipyard BOOLEAN, --null

  state STRING, --"None",
  system_id BIGINT, --: 7358,
  type STRING, -- "Commercial Outpost",
  updated_at BIGINT, -- 1431043155
  max_landing_pad_size STRING, -- : "M",
  name STRING -- "Gehry Dock",

);
CREATE TABLE station2economy (
	economy_id BIGINT, 
	station_id BIGINT
);
CREATE TABLE station2export (
	commodity_id BIGINT, 
	station_id BIGINT
);
CREATE TABLE station2import (
	commodity_id BIGINT, 
	station_id BIGINT
);
CREATE TABLE station2prohibited (
	commodity_id BIGINT, 
	station_id BIGINT
);
CREATE TABLE system (
	id BIGINT PRIMARY KEY, -- 1,
	allegiance STRING, -- "Empire",
	faction STRING, -- "Empire League",
	government STRING, -- "Patronage",
	name STRING, -- "1 G. Caeli",
	needs_permit BOOLEAN, -- 0,
	population BIGINT, -- 6544826,
	primary_economy STRING, -- "Industrial",
	security STRING, -- "Medium",
	state STRING, -- "None",
	updated_at DATETIME, -- 1430931668,
	x DOUBLE, -- 80.90625,
	y DOUBLE, -- -83.53125,
	z DOUBLE -- -30.8125
);
