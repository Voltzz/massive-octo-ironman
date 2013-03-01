import json
import Levenshtein
import unicodedata
import os
import pymongo
import sys
from util import loadJSONData

# TODO: Fix this latent bug...
APPL_ROOT=os.path.join(os.path.dirname(__file__), '..')

SMARTPHONE_SCRAPED_FILEPATH = os.path.join(APPL_ROOT,"data_sets","scraped","arena_scraped.json")

def getPhoneDb(phoneData):
	# Takes as input the raw JSON file
	# Output needs to be a list of dictionaries, one dictionary for each phone
	# E.g. phoneDb = [ 	{'manufacturer' : 'Apple', 'device' : 'iPhone 3GS'},
	#			{'manufacturer' : 'Samsung', 'device' : 'Galaxy S3'},
	#			{'manufacturer' : 'Google', 'device' : 'Nexus S'}
	#		]
	phoneDb = list()

	for i, phoneItem in enumerate(phoneData):
		deviceList = phoneItem['device']
		if deviceList:
			manufacturer = phoneItem['brand'][0].strip()
			manufacturer = str(manufacturer.replace('phones','').strip())
			for device in deviceList:
				thisDict = {'manufacturer' : manufacturer, 'device' : device}
				phoneDb.append(thisDict)

	return phoneDb

def removeDuplicates(phoneDb):
	hashTable = dict()

	maxRange = len(phoneDb)

	i = 0

	while i < maxRange:
		device = phoneDb[i]['manufacturer'].replace("-","").replace(" ", "") + "." + phoneDb[i]['device'].replace("-","").replace(" ","")
		if device in hashTable.keys():
			#print "\t[removeDuplicates] Deleting duplicate"
			#print phoneDb[i]
			del phoneDb[i]
			i = i - 1
			maxRange = maxRange - 1
		else:
			hashTable[device] = True
		i = i + 1
	
	return phoneDb
	

def main(args):
	wipeDatabase = False

	print "[Main] Welcome to the phone parsing script!"
	
	
	# Check if the --fresh flag was passed
	for arg in args[1:]: # The first argument is always the python filename
		if arg == "--fresh":
			wipeDatabase = True
			break
		else:
			print "[Main] WARNING: Option '"+arg+"' was unrecognized and has been ignored"

	print "[Main] Loading JSON data from file...",
	phoneData = loadJSONData(SMARTPHONE_SCRAPED_FILEPATH)
	print "done."

	print "[Main] Parsing raw JSON data to generate dictionaries...",
	phoneDb = getPhoneDb(phoneData)
	print "done."

	print "[Main] All JSON data parsed successfully."

	print "[Main] Opening database connection...",
	phonesCollection = pymongo.MongoClient().phones_db.phones_collection
	print "done."

	print "[Main] Removing possible duplicates...",
	phoneDb = removeDuplicates(phoneDb)
	print "done."

	if wipeDatabase:
		print "[Main] Fresh flag was passed, wiping out database...",
		phonesCollection.remove()
		print "done."

	print "[Main] Writing collection to database...",
	phonesCollection.ensure_index( [("manufacturer",pymongo.ASCENDING),("device",pymongo.ASCENDING)], unique=True)

	phonesCollection.insert(phoneDb)
	print "done."

	print "\n[Main] Application has finished successfully."



if __name__ == "__main__":
	main(sys.argv)
