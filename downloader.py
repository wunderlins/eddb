#!/usr/bin/env python
"""
Parse json exports from eddb.io and store result in a mysql database.

"""

import urllib2, sys, json, os

"""
Json pretty print
>>> print json.dumps({'4': 5, '6': 7}, sort_keys=True,
...                  indent=4, separators=(',', ': '))
"""

import config

class HeadRequest(urllib2.Request):
	def get_method(self):
		return "HEAD"

def getHeadRequest(url):
	return urllib2.urlopen(HeadRequest(url))

# response = urllib2.urlopen(HeadRequest("http://google.com/index.html"))


def fetch(file):
	base_file = file[0:-5]
	#print base_file

	url = config.url + file
	sys.stdout.write("Downloading %s ... " % file)
	sys.stdout.flush()
	try:
		up = urllib2.urlopen(url)
	except Exception, e:
		sys.stdout.write("Failed\n")
		sys.stdout.flush()
		sys.stderr.write("Failed to open url %s" % file)
		sys.stderr.flush()
		return False
	
	try:
		# save file
		raw_file = base_file + ".raw"
		json_file = base_file + ".json"
		output = open(raw_file, 'wb')
		output.write(up.read())
		output.close()
		up.close()
	except:
		output.close()
		up.close()
		sys.stdout.write("Failed\n")
		sys.stdout.flush()
		sys.stderr.write("Failed to download and save %s" % file)
		sys.stderr.flush()
		return False
		
	if (config.pretty_print):
		try:
			# pretty print json code
			with open(raw_file) as data_file:    
				with open(json_file, 'wb') as outfile:
					json.dump(json.load(data_file), outfile, sort_keys=True,
						        indent=4, separators=(',', ': '))
			# remove raw file
			os.remove(raw_file)
			
		except:
			sys.stdout.write("Failed\n")
			sys.stdout.flush()
			sys.stderr.write("Failed to parse %s" % file)
			sys.stderr.flush()
			return False
	else:
		# rename files
		os.rename(raw_file, data_file)
		
	sys.stdout.write("Done\n")
	sys.stdout.flush()
	return True

def main():
	"""
	download files from http://eddb.io/api
	"""
	
	print config.url
	
	#Commodities
	ret = fetch("commodities.json")
	#Systems
	ret = fetch("systems.json")
	#Stations
	ret = fetch("stations.json")

if __name__ == "__main__":
	main()
