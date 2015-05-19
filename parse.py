#!/usr/bin/env python
"""
echo "$el" | sed -e 's/ \+- //; s/INT/BIGINT/; s/STR/STRING/; s/ --/, --/; s/PK/PRIMARY KEY/; s/TST/DATETIME/; s/BOL/BOOLEAN/; s/FLT/DOUBLE/'


Data file description:

* commodities.json (Array)
  - DIC category
    - id INT PK
    - name STR
  
  - id INT PK
  - average_price INT
  - category_id INT
  - name STR

* systems.json (Array)
  - id INT PK -- 1,
  - allegiance STR -- "Empire",
  - faction STR -- "Empire League",
  - government STR -- "Patronage",
  - name STR -- "1 G. Caeli",
  - needs_permit BOL -- 0,
  - population INT -- 6544826,
  - primary_economy STR -- "Industrial",
  - security STR -- "Medium",
  - state STR -- "None",
  - updated_at TST -- 1430931668,
  - x FLT -- 80.90625,
  - y FLT -- -83.53125,
  - z FLT -- -30.8125

CREATE TABLE systems (
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

* stations.js (Array)
  - ARR STR economies --[], ? list of strings, convert to int
  - ARR STR export_commodities --[], list of strings, convert to int
  - ARR STR import_commodities --[], list of strings, convert to int

  - DIC listings -- these are the commodities informations
    - id INT PK --87,
    - buy_price INT --223,
    - collected_at INT --1431043003,
    - commodity_id INT --1,
    - demand INT --0,
    - sell_price INT --207,
    - station_id INT --3,
    - supply INT --46197,
    - update_count INT --"2"
  
  - id INT PK --1,
  - allegiance STR --null,
  - distance_to_star INT --16253,
  - faction STR --"",
  - government STR --null,
  - has_blackmarket BOL --0,
  - has_commodities BOL --1,
  - has_outfitting BOL --null,
  - has_rearm BOL --null,
  - has_refuel BOL --null,
  - has_repair BOL --null,
  - has_shipyard BOL --null,


-- commodities
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

-- systems
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

-- stations
create table listing ( -- commodities available on the market
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
	has_shipyard BOOLEAN --null
);

CREATE TABLE economy (
	id BIGINT PRIMARY KEY, 
	name STRING
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

"""

import json, config

class parse():
	_con = None
	_cur = None
	
	@staticmethod
	def _dbconn():
		if (parse._con == None):
			import sqlite3
			parse._con = sqlite3.connect(config.db)
			parse._cur = parse._con.cursor()
		
		return (parse._con, parse._cur)
		
	@staticmethod
	def _listexpand(list, size):		
		l = len(list)
		#print "%d, %d" % (l, size)
		while (len(list) <= size):
			list.append(None)
	
	@staticmethod
	def commodities():
		# load data to memory
		fp = open("commodities.json", "r")
		data = json.load(fp)
		fp.close()
		
		# loop over properties
		categories = []
		for e in data:
			#print e["category"]["id"]
			parse._listexpand(categories, e["category"]["id"])
			categories[e["category"]["id"]] = e["category"]["name"]
			
		# return modified data
		(con, cur) = parse._dbconn()
		
		# create a list of tuples containing all values
		categories_sqldata = []
		count = 0
		for x in range(0, len(categories)):
			categories_sqldata.append((x, categories[x]))
			count += 1
		
		cur.executemany("INSERT INTO category (id, name) VALUES (?, ?)", categories_sqldata)
		con.commit()
		
		print categories_sqldata

def main():
	"""
	parse downlaoded files
	"""
	parse.commodities()
	
if __name__ == "__main__":
	main()
