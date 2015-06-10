#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Elite Dangerous DataBase Shell - short edsh (eddb is the name of the database)

interesting example code can be foudn here:
https://bitbucket.org/kfsone/tradedangerous/src

command line ideas:
$ set station <nameofstation> # wil lset the active station
$ set system <name of system> # dito system
$ search <search term> # will find stations and systems
$ search commodity <commdoity name> # will find commodieies in a certain radius
$ set option <name> <value>
...          commodity <commdoity name>
...          radius <distance in ly>
...          <sell|buy>
$ distance <target system> # calculate distance from selected to target
$ distance <source system> <target system> # calculate distance from source to target
"""

import sys
import cmd
import sqlite3
import config
import os
import reload
import math

con = sqlite3.connect(config.db)
cur = con.cursor()

def get_systems(text):
	# do a database query, find all available systems
	sql = "SELECT name FROM system WHERE name LIKE '"+text+"%'"
	cur.execute(sql)
	res = cur.fetchall()
	options = []
	for name in res:
		#print "  %d, %s" % (id, val)
		options.append(name[0])
	return options

def find(token):
	# do a database query, find all available systems
	sql = "SELECT name FROM system WHERE name LIKE '%"+token+"%'"
	cur.execute(sql)
	res = cur.fetchall()
	options = []
	for name in res:
		#print "  %d, %s" % (id, val)
		options.append(name[0])
	return options

bash_colors = {
	"Black"       :"0;30",     "Dark Gray"     :"1;30",
	"Blue"        :"0;34",     "Light Blue"    :"1;34",
	"Green"       :"0;32",     "Light Green"   :"1;32",
	"Cyan"        :"0;36",     "Light Cyan"    :"1;36",
	"Red"         :"0;31",     "Light Red"     :"1;31",
	"Purple"      :"0;35",     "Light Purple"  :"1;35",
	"Brown"       :"0;33",     "Yellow"        :"1;33",
	"Light Gray"  :"0;37",     "White"         :"1;37"
}

def colorize(string, color):
	return "\033[" + bash_colors[color] + "m" + string + "\033[0m"
	

class MyCmd(cmd.Cmd):
	colwidth = 18
	intro = colorize("""Welcome to edsh
""", "Purple")
	
	prompt = colorize("None", "Light Blue") + " > : "
	
	"""
	def parseline(self, line):
		print 'parseline(%s) =>' % line,
		ret = cmd.Cmd.parseline(self, line)
		print ret
		return ret
	"""

	def cmdloop(self):
		try:
			cmd.Cmd.cmdloop(self)
		except KeyboardInterrupt as e:
			#print "CTRL-C detected"
			print "" # exiting readline mode probably, add a newline
			sys.exit(127)
	
	def do_EOF(self, line):
		"""catch CTRL-D, exit"""
		print "" # must add a newline
		return True
        	
	def do_system(self, line):
		# FIXME: validate system name, only use it if found
		self.prompt = colorize(line.title(), "Light Blue") + " > : "

	def do_station(self, line):
		pass
	
	def do_reload(self, line):
		# FIXME: reloading base class does not work
		reload.recompile("edsh")
	
	def do_colwidth(self, line):
		self.colwidth = int(line)
		print colorize("Column width set to %d characters" % self.colwidth, "Cyan")
	
	def do_set(self, line):
		print "i should do something with this data now"
		
	def complete_set(self, text, line, start_index, end_index):
		print line
	
	def do_find(self, line):
		width = int(os.getenv("COLUMNS"))
		colwidth = self.colwidth
		nlat = math.floor(width * 1.0 / colwidth)
		#print "colwidth: %d, width: %d, nlat: %d" % (colwidth, width, nlat)
		systems = find(line)
		counter=1
		for s in systems:
			l = len(s)
			mask = "%-"+str(colwidth-1)+"s "
			out = s
			if l+1 > colwidth:
				out = out[0:colwidth-2] + u"…"
			sys.stdout.write(mask % out)
			if counter % nlat == 0:
				sys.stdout.write("\n")
			counter += 1
		#print systems
		return None
	
	def complete_system(self, text, line, start_index, end_index):
		search = line[7:]
		tmp_tokens = line.split(' ')
		tokens = []
		for e in tmp_tokens:
			if e == "":
				continue
			tokens.append(e)
		
		#print tokens
		#print ""
		#print "%s, %s, %d, %d, %d" % (line, search, start_index, end_index, len(tokens))
		
		#print len(line)
		if line and len(line) > 2+7:
			if len(tokens) == 2:
				return get_systems(search)
			else:
				#print " ".join(tokens[1:len(tokens)-1])
				srchstr = " ".join(tokens[1:len(tokens)-1])
				srchstr_l = len(srchstr)
				ret = []
				sy = get_systems(search)
				#print sy
				for e in sy:
					"""
					start = len(tokens[1])+1
					ret.append(e[start:])
					"""
					# FIXME: if system name is equal to the whole line, return
					ret.append(e[srchstr_l+1:])
				
				return ret
			
		else:
			return []
def start():
	my_cmd = MyCmd()
	my_cmd.cmdloop()
	
if __name__ == '__main__':
	my_cmd = MyCmd()
	my_cmd.cmdloop()
