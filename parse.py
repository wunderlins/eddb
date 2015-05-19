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

import json, config, sys
import datetime

class parse():
	_con = None
	_cur = None

	@staticmethod
	def log(str):
		sys.stdout.write(str)
		sys.stdout.flush()
	
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
	def load_data(file):
		# load data to memory
		fp = open(file, "r")
		data = json.load(fp)
		fp.close()
		return data
	
	@staticmethod
	def commodities():
		# load data to memory
		f = "commodities.json"
		parse.log("Parsing file %s ... " % f)
		data = parse.load_data(f)
		
		# loop over properties
		categories = []
		commodities = []
		for e in data:
			#print e["category"]["id"]
			parse._listexpand(categories, e["category"]["id"])
			categories[e["category"]["id"]] = e["category"]["name"]
			
			commodities.append((
				e["id"],
				e["average_price"],
				e["category_id"],
				e["name"]
			))
		parse.log("done.\n")
		#print commodities
		
		# get connection
		(con, cur) = parse._dbconn()
		
		# create a list of tuples containing all values
		categories_sqldata = []
		count = 0
		for x in range(0, len(categories)):
			categories_sqldata.append((x, categories[x]))
			count += 1
		
		parse.log("Importing file %s ... " % f)
		
		# insert categories
		#print categories_sqldata
		cur.execute("DELETE FROM category")
		cur.executemany("INSERT INTO category (id, name) VALUES (?, ?)", categories_sqldata)
		con.commit()
		
		# insert commodities
		cur.execute("DELETE FROM commodity")
		sql = "INSERT INTO commodity (id, average_price, category_id, name) VALUES (?,?,?,?)"
		cur.executemany(sql, commodities)
		con.commit()
		
		parse.log("done.\n")
		
		#print categories_sqldata

	@staticmethod
	def system():
		# load data to memory
		f = "systems.json"
		parse.log("Parsing file %s ... " % f)
		data = parse.load_data("systems.json")
		
		# get connection
		(con, cur) = parse._dbconn()
		
		systems = []
		for r in data:
			systems.append((
				r["allegiance"], # : "Federation",
				r["faction"], # : "Values Party of 1 Hydrae",
				r["government"], # : "Democracy",
				r["id"], # : 3,
				r["name"], # : "1 Hydrae",
				r["needs_permit"], # : 0,
				r["population"], # : 4294967295,
				r["primary_economy"], # : "Agriculture",
				r["security"], # : "High",
				r["state"], # : "None",
				datetime.datetime.fromtimestamp(int(r["updated_at"])), # : 1430938502,
				r["x"], # : 60.90625,
				r["y"], # : 28.53125,
				r["z"] # : -54.90625
			))
			
			if len(systems[len(systems)-1]) != 14:
				print systems[len(systems)-1]
			
		parse.log("done.\n")
		
		"""
		for l in systems:
			print l
		"""
		
		# get connection
		(con, cur) = parse._dbconn()
		
		parse.log("Importing file %s ... " % f)
		
		# insert systems
		cur.execute("DELETE FROM system")
		cur.executemany("""INSERT INTO system (
			allegiance, 
			faction, 
			government, 
			id, 
			name, 
			needs_permit, 
			population, 
			primary_economy, 
			security, 
			state, 
			updated_at, 
			x, 
			y, 
			z) 
		VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
		""", systems)
		con.commit()
		
		parse.log("done.\n")
		
def main():
	"""
	parse downlaoded files
	"""
	parse.commodities()
	parse.system()
	
if __name__ == "__main__":
	main()
