#!/usr/bin/env python
"""
echo "$el" | sed -e 's/ \+- //; s/INT/BIGINT/; s/STR/STRING/; s/ --/, --/; s/PK/PRIMARY KEY/; s/TST/DATETIME/; s/BOL/BOOLEAN/; s/FLT/DOUBLE/'


Data file description:

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
	has_shipyard BOOLEAN, --null
	
	state STRING, --"None",
	system_id BIGINT, --: 7358,
	type STRING, -- "Commercial Outpost",
	updated_at BIGINT, -- 1431043155
	max_landing_pad_size STRING, -- : "M",
	name STRING -- "Gehry Dock",
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
CREATE TABLE station2prohibited (
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
		data = parse.load_data(f)
		
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

	@staticmethod
	def get_id(name, arr, reverse):
		index = None
		try:
			index = arr.index(name)
		except:
			arr.append(name)
			index = arr.index(name)
			reverse[name] = index
		
		return index

	@staticmethod
	def get_index(el, obj):
		try:
			return obj[el]
		except:
			return None
	
	@staticmethod
	def station():
		# get connection
		(con, cur) = parse._dbconn()
		
		# get all commodities
		sql = "SELECT id, name FROM commodity"
		cur.execute(sql)
		res = cur.fetchall()
		commodities = {}
		for id, val in res:
			#print "  %d, %s" % (id, val)
			commodities[val] = id
		#print commodities
		#return
		
		# load data to memory
		f = "stations.json"
		parse.log("Parsing file %s ... " % f)
		data = parse.load_data(f)
		
		station = []
		economies = [None]
		economies_rev = {"None": 0}
		#commodities = []
		economies_arr = []
		commodities_export = []
		commodities_import = []
		commodities_prohibited = []
		
		listings = []
		
		for r in data:
			
			# insert commodities
			for e in r["economies"]:
				i = parse.get_id(e, economies, economies_rev)
				economies_arr.append((r["id"], i))
				#print "  %d, %s" % (i, e)
			
			# lookup all export/import commodities' ids
			for e in r["export_commodities"]:
				commodities_export.append((r["id"], parse.get_index(e, commodities)))
			for e in r["import_commodities"]:
				commodities_import.append((r["id"], parse.get_index(e, commodities)))
			# lookup prohibited commodities
			for e in r["prohibited_commodities"]:
				commodities_prohibited.append((r["id"], parse.get_index(e, commodities)))
			
			# insert station
			station.append((
				r["id"],
				r["allegiance"],
				r["distance_to_star"],
				r["faction"],
				r["government"],
				r["has_blackmarket"],
				r["has_commodities"],
				r["has_outfitting"],
				r["has_rearm"],
				r["has_refuel"],
				r["has_repair"],
				r["has_shipyard"],
				r["state"],
				r["system_id"],
				r["type"],
				r["updated_at"],
				r["max_landing_pad_size"],
				r["name"]
			))
			
			# build a list of commodities for later insertion
			"""
        "listings": [
            {
                "buy_price": 223,
                "collected_at": 1431043003,
                "commodity_id": 1,
                "demand": 0,
                "id": 87,
                "sell_price": 207,
                "station_id": 3,
                "supply": 46197,
                "update_count": "2"
            }
			"""
			for e in r["listings"]:
				listings.append((
					e["buy_price"], #: 223,
					e["collected_at"], #: 1431043003,
					e["commodity_id"], #: 1,
					e["demand"], #: 0,
					e["id"], #: 87,
					e["sell_price"], #: 207,
					e["station_id"], #: 3,
					e["supply"], #: 46197,
					e["update_count"] #: "2"
				))
		
		#print commodities_export
		
		eco = []
		for index, item in enumerate(economies):
			if index == 0:
				continue
			#print "%d, %s" % (index, item)
			eco.append((index, item))
		
		sql = """ INSERT INTO station (
			id,
			allegiance, -- STRING, --null,
			distance_to_star, -- STRING, --null, BIGINT, --16253,
			faction, -- STRING, --null, STRING, --"",
			government, -- STRING, --null, STRING, --null,
			has_blackmarket, -- STRING, --null, BOOLEAN, --0,
			has_commodities, -- STRING, --null, BOOLEAN, --1,
			has_outfitting, -- STRING, --null, BOOLEAN, --null,
			has_rearm, -- STRING, --null, BOOLEAN, --null,
			has_refuel, -- STRING, --null, BOOLEAN, --null,
			has_repair, -- STRING, --null, BOOLEAN, --null,
			has_shipyard, -- STRING, --null, BOOLEAN, --null
			state, -- STRING, --null, STRING, --"None",
			system_id, -- STRING, --null, BIGINT, --: 7358,
			type, -- STRING, --null, STRING, -- "Commercial Outpost",
			updated_at, -- STRING, --null, BIGINT, -- 1431043155
			max_landing_pad_size, -- STRING, --null, STRING, -- : "M",
			name -- STRING, --null, STRING -- "Gehry Dock",
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
		
		cur.execute("DELETE FROM station")
		cur.execute("DELETE FROM listing")
		cur.execute("DELETE FROM economy")
		cur.execute("DELETE FROM station2economy")
		cur.execute("DELETE FROM station2export")
		cur.execute("DELETE FROM station2import")
		cur.execute("DELETE FROM station2prohibited")
		
		cur.executemany(sql, station)
		sql = "INSERT INTO station2economy (station_id, economy_id) VALUES (?, ?)"
		cur.executemany(sql, economies_arr)
		
		sql = "INSERT INTO economy (id, name) VALUES (?, ?)"
		cur.executemany(sql, eco)
		
		sql = "INSERT INTO station2export (station_id, commodity_id) VALUES (?, ?)"
		cur.executemany(sql, commodities_export)
		
		sql = "INSERT INTO station2import (station_id, commodity_id) VALUES (?, ?)"
		cur.executemany(sql, commodities_import)
		
		sql = "INSERT INTO station2prohibited (station_id, commodity_id) VALUES (?, ?)"
		cur.executemany(sql, commodities_import)
		
		sql = """INSERT INTO listing (
						buy_price, --": 223,
						collected_at, -- ": 1431043003,
						commodity_id, -- ": 1,
						demand, -- ": 0,
						id, -- ": 87,
						sell_price, -- ": 207,
						station_id, -- ": 3,
						supply, -- ": 46197,
						update_count -- ": "2"

			) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
		cur.executemany(sql, listings)
		con.commit()
		
		parse.log("done.\n")

		"""		
    {
        "id": 3,
        "state": "None",
        "system_id": 7358,
        "type": "Commercial Outpost",
        "updated_at": 1431043155
        "allegiance": "Empire",
        "faction": "Empire Consulate",
        "government": "Patronage",
        "has_blackmarket": 0,
        "has_commodities": 1,
        "has_outfitting": 0,
        "has_rearm": 0,
        "has_refuel": 0,
        "has_repair": 1,
        "has_shipyard": 0,
        "distance_to_star": 3908,
        "max_landing_pad_size": "M",
        "name": "Gehry Dock",
        
        "economies": [
            "High Tech",
            "Refinery"
        ],
        "export_commodities": [
            "Aluminium",
            "Copper",
            "Titanium"
        ],
        
        "import_commodities": [
            "Mineral Oil",
            "Bauxite",
            "Rutile"
        ],
        "prohibited_commodities": [
            "Narcotics",
            "Combat Stabilisers",
            "Slaves",
            "Personal Weapons",
            "Battle Weapons",
            "Toxic Waste"
        ],
        
        "listings": [
            {
                "buy_price": 223,
                "collected_at": 1431043003,
                "commodity_id": 1,
                "demand": 0,
                "id": 87,
                "sell_price": 207,
                "station_id": 3,
                "supply": 46197,
                "update_count": "2"
            }
        ],
    } """
			
		
def main():
	"""
	parse downlaoded files
	"""
	parse.commodities()
	parse.system()
	parse.station()
	
if __name__ == "__main__":
	main()
