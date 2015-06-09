#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import config
import sqlite3

con = None
cur = None

row_width = (9, 18, 5, 8, 8, 4)

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
		__display(e[0].decode('utf-8'), row_width[0])
		__display(e[1].decode('utf-8'), row_width[1])
		__display(str(e[2]).decode('utf-8'), row_width[2], "r")
		__display(e[5].decode('utf-8'), row_width[3])
		__display(e[4].decode('utf-8'), row_width[4])
		
		
		xyz = str(e[7]).rjust(row_width[5]) + "/" + str(e[8]).rjust(row_width[5]) + "/" + str(e[9]).rjust(row_width[5])
		
		__display(xyz, 14)
		#__display(, row_width[5])
		sys.stdout.write("\n")


def __display(string, length, direction="l", fillchar=" ", last=False):
	"""
		string (str): the string to format
		direction (char): eighter r|R or l|L
		lenght (int): number of maximum length of string
	"""
	
	# check if this is an array
	
	# handle delimiters
	if len(string) == 0:
		sys.stdout.write(string.ljust(length, fillchar) + fillchar + "+")
		if (not last):
			sys.stdout.write(fillchar)
		return
	
	# if streing does not exceed max string, pad it and return it
	if len(string)-1 < length:
		if direction == "l" or direction == "L":
			sys.stdout.write(string.ljust(length, fillchar) + " | ")
		else:
			sys.stdout.write(string.rjust(length, fillchar) + " | ")
		return
	
	# if string is longer, clip it and add "…"
	if len(string) > 0:
		tmp = string[0:length-1] + u"…"
		sys.stdout.write(tmp + " | ")


sql = "SELECT sy.name system, s.name station, s.distance_to_star, s.faction, \
              s.government, s.allegiance, \
       julianday('now')-julianday(datetime(s.updated_at, \
                                  'unixepoch', 'localtime')) last_upd_days_ago \
       , CAST(sy.x as INT), CAST(sy.y as INT), CAST(sy.z as INT) \
FROM station s LEFT JOIN system sy ON (s.system_id = sy.id) \
WHERE s.faction like 'Sirius Corp%' \
  AND s.max_landing_pad_size = 'L' \
  AND s.distance_to_star < 2000;"

print
__display("System", row_width[0])
__display("Station", row_width[1])
__display("d2star", row_width[2], "r")
__display("Allegiance", row_width[3])
__display("Government", row_width[4])
__display("  x /  y /  z ", 14)

sys.stdout.write("\n")
__display("", row_width[0], fillchar="-")
__display("", row_width[1], fillchar="-")
__display("", row_width[2], fillchar="-")
__display("", row_width[3], fillchar="-")
__display("", row_width[4], fillchar="-")
__display("", 14, fillchar="-", last=True)
sys.stdout.write("\n")
query(sql)


