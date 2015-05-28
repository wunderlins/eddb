#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import config
import sqlite3

con = None
cur = None

def connect(dbfile=None):
	global con, cur
	
	if dbfile == None:
		dbfile = config.db
	
	if (not con):
		#print "Connecting"
		con = sqlite3.connect(dbfile)
		cur = con.cursor()
	
	return (con, cur)

def close():
	con.close()

#def find(station=None, system=None, allegiance=None, faction=None):
def query(sql):
	global con, cur
	connect()
	
	res = cur.execute(sql)
	for e in res:
		#print e[0].ljust(10), e[1].ljust(25), str(e[2]).rjust(6), e[5].ljust(10)
		__display(e[0], 10)
		__display(e[1], 25)
		__display(str(e[2]), 6, "r")
		__display(e[5].decode('utf-8'), 10)
		sys.stdout.write("\n")


def __display(string, length, direction="l"):
	"""
		string (str): the string to format
		direction (char): eighter r|R or l|L
		lenght (int): number of maximum length of string
	"""
	
	length = length-1
	
	# if streing does not exceed max string, pad it and return it
	if len(string)-1 < length:
		if direction == "l" or direction == "L":
			sys.stdout.write(string.ljust(length) + " ")
		else:
			sys.stdout.write(string.rjust(length) + " ")
		return
	
	# if string is longer, clip it and add "…"
	if len(string) > 0:
		tmp = string[0:length-1] + "…"
		sys.stdout.write(tmp + " ")


sql = "SELECT sy.name system, s.name station, s.distance_to_star, s.faction, \
              s.government, s.allegiance, \
       julianday('now')-julianday(datetime(s.updated_at, \
                                  'unixepoch', 'localtime')) last_upd_days_ago \
FROM station s LEFT JOIN system sy ON (s.system_id = sy.id) \
WHERE s.faction like 'Sirius Corp%' \
  AND s.max_landing_pad_size = 'L' \
  AND s.distance_to_star < 2000;"
  
query(sql)


