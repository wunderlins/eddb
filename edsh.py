#!/usr/bin/env python
"""
Elite Dangerous DataBase Shell - short edsh (eddb is the name of the database)



"""

import sys
import cmd
import sqlite3
import config
import os
import reload

con = sqlite3.connect(config.db)
cur = con.cursor()

addresses = [
    'here@blubb.com',
    'foo@bar.com',
    'whatever@wherever.org',
]

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
	
	def do_system(self, line):
		# FIXME: validate system name, only use it if found
		self.prompt = colorize(line.title(), "Light Blue") + " > : "

	def do_station(self, line):
		pass
	
	def do_reload(self, line):
		# FIXME: reloading base class does not work
		reload.recompile("edsh")
	
	def do_find(self, line):
		systems = find(line)
		for s in systems:
			sys.stdout.write("%-15s" % s)
		#print systems
	
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
					ret.append(e[srchstr_l+1:])
				
				return ret
			
		else:
			return []

if __name__ == '__main__':
	print os.getenv("COLUMNS")
	my_cmd = MyCmd()
	my_cmd.cmdloop()