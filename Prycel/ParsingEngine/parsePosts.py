import json
import Levenshtein
import unicodedata
import os
import pymongo
import unittest
import sys
from util import loadJSONData
import time

# TODO: Fix this latent bug...
APPL_ROOT=os.path.join(os.path.dirname(__file__), '..')

CRAIGSLIST_SCRAPED_FILEPATH = os.path.join(APPL_ROOT,"data_sets","scraped","craigslist_TO_scraped.json")


SPAM_KEYWORDS_LIST= ['case','cover','protector','jailbreak','cases','unlocking','fixing','repair','charger'
			   ,'cable','bumper','repairs' ,'cutter','dock','sim','service','headset','sd card','battery'
			   ,'keyboard', 'fix', 'holster']

#PROFILE
timeList = list()


def getCraigDb(craigData):
	# Takes as input the raw JSON file
	# Output needs to be a list of dictionaries
	# E.g. craigDb[0] corresponds to the first posting
	# craigDb[0]["title"] = "SELLING COOL PHONE!!!"
	# craigDb[0]["desc"] = "OMG i love this phone but dont want it\nSo please keep it love you thx"

	craigDb = [dict() for x in range(len(craigData))]
	for i,craigItem in enumerate(craigData):
		title = craigItem["title"][0].decode("utf-8")
		desc = ''	
		rawDesc = craigItem["desc"]

		for d in rawDesc:
			desc = desc + d.encode("ascii", errors="ignore")

		craigDb[i]["title"] = title
		craigDb[i]['desc'] = desc

	return craigDb


def getManufacturers(device, phoneDb):
	# Returns a list of manufacturers for given device
	manufacturers = list()

	for phone in phoneDb:
		if phone['device'] == device:
			manufacturers.append(phone['manufacturer'])
	
	return manufacturers

def pickBestManufacturer(ratios, listOfPossibleManufacturers):
	bestRatio = -1
	bestPick = 0
	for i in range(0, len(listOfPossibleManufacturers)):
		ratio = ratios[listOfPossibleManufacturers[i]]
		if ratio > bestRatio:
			bestRatio = ratio
			bestPick = i
	
	return listOfPossibleManufacturers[bestPick]

def cleanPosts(postDb):
	hashTable = dict()

	maxRange = len(postDb)

	i = 0

	while i < maxRange:
		desc = postDb[i]['description']
		if desc in hashTable.keys() or postDb[i]['price'] == - 1 or postDb[i]['device'] == "Unknown":
			del postDb[i]
			i = i - 1
			maxRange = maxRange - 1
		else:
			hashTable[desc] = True
		i = i + 1
	return postDb


def parsePost(post, phoneDb):
	global timeList
	# Takes as input a craigDb[i] post, and the phone database
	# Output is the dictionary
	# e.g. phone['manufacturer'], phone['device'] etc. should all be filled in

	#PROFILE
	startTime = time.time()

	phone = dict()

	# Initial Values
	phone['manufacturer'] = "Unknown"
	phone['device'] = "Unknown"
	phone['unlocked'] = False
	phone['refurbished'] = False
	phone['new'] = False
	phone['description'] = "UNDEFINED"
	phone['price'] = -1

	#Early exit if post title is irrelevant
	if checkDiscard(post) == 'true':
	
		phone['description'] = post['desc']
		return phone

	# First lets get device and manufacturer
	topManufacturer = "Unknown"
	topDevice = "Unknown"
	manufacturerRatios = dict() # We keep track of the ratio for each manufacturer, incase we detect an invalid one
	currManuBest = -1
	currDeviBest = -1

	#PROFILE
	firstIteration = True
	for thisPhone in phoneDb:
		#PROFILE
		if firstIteration:
			beginTime = time.time()
		manufacturer = thisPhone['manufacturer']
		device = thisPhone['device']
		#print "(" + manufacturer + ") " + device
		# Find the closest Manufacturer, if exists
		# Search the title n words at a time, where n is length of manufacturer
		numOfWordsInManu = len(manufacturer.split(" "))
		splitTitle = post['title'].split()
		
		try: # We will run out of words since we access i + len(manufacturer)
			for i in range(0, len(manufacturer)):
				if splitTitle[i][0].lower() != manufacturer[0].lower():
					# Quick hack to make it faster. Ignore word if first letter doesn't match
					# Who the heck spells it as 'Pihone 5' or 'aGlaxy S3'
					manuRatio = 0
				else:
					manuRatio = Levenshtein.ratio(str(" ".join(splitTitle[i:i+numOfWordsInManu])).lower(), str(manufacturer).lower())
					manuRatio = manuRatio + ((numOfWordsInManu-1) * 0.0001) # We need to add a bonus for length so we give preference to longer matches
					#print "Comparison: " + str(" ".join(splitTitle[i:i+numOfWordsInManu])).lower() + " vs. " + str(manufacturer).lower()
					#print "Ratio: " + str(manuRatio)
				if manuRatio > currManuBest:
					currManuBest = manuRatio
					topManufacturer = manufacturer
				manufacturerRatios[manufacturer] = manuRatio
		except:
			pass # Finished searching title

		#PROFILE
		if firstIteration:
			manuSearchTime = time.time()
			manuSearchTimeDelta = manuSearchTime - beginTime
			print "Time taken to check the manufacturer: " + str(manuSearchTimeDelta)
		
		# Now lets find the closest device
		# Same strategy as before
		numOfWordsInDevi = len(device.split(" "))
		try:
			for i in range(0, len(device)):
				if splitTitle[i][0].lower() != device[0].lower():
					deviRatio = 0
				else:
					deviRatio = Levenshtein.ratio(str(" ".join(splitTitle[i:i+numOfWordsInDevi])).lower(), str(device).lower())
					deviRatio = deviRatio + ((numOfWordsInDevi-1) * 0.0001)
					#print "Comparison: " + str(" ".join(splitTitle[i:i+numOfWordsInDevi])).lower() + " vs. " + str(device).lower()
					#print "Ratio: " + str(deviRatio)
				if deviRatio > currDeviBest:
					currDeviBest = deviRatio
					topDevice = device
		except:
			pass

		#PROFILE
		if firstIteration:
			deviSearchTime = time.time()
			deviSearchTimeDelta = deviSearchTime - manuSearchTime
			print "Time taken to check the device: " + str(deviSearchTimeDelta)
			firstIteration = False

	# At this point, we may have a match for manufacturer that doesn't match the device
	# e.g. Samsung iPhone 4S
	# We always give precedence to the device
	copyOfDb = phoneDb.clone() # So cursor doesn't mess up
	possibleManufacturers = getManufacturers(topDevice, copyOfDb)
	if not(topManufacturer in possibleManufacturers):
		topManufacturer = pickBestManufacturer(manufacturerRatios, possibleManufacturers)
	phone['manufacturer'] = topManufacturer
	phone['device'] = topDevice

	#Unlocked?
	if post['desc'].lower().find('unlocked') != -1:
		phone['unlocked'] = True
	
	#New?
	if post['desc'].lower().find('new') != -1:
		phone['new'] = True
	
	#Refurb?
	if post['desc'].lower().find('refurb') != -1 or post['desc'].lower().find('refurbished') != -1:
		phone['refurbished'] = True
	
	phone['description'] = post['desc']

	# Price
	try: # Not all posts have set price (OBO, etc.)
		splitTitle = post['title'].split(' - ')
		# We assume it to be "HI SELLING PHONE - $200"
		splitTitle = splitTitle[1].split()
		splitTitle = splitTitle[0].split('$')
		splitTitle = splitTitle[1]
		priceString = "" # Some prices are "$300obo"
		for x in range(0,len(splitTitle)):
			if splitTitle[x] >= '0' and splitTitle[x] <= '9':
				priceString = priceString + splitTitle[x]
			else:
				break


		phone['price'] = int(priceString)
	except IndexError:
		# If price is not given, or is invalid
		pass

	endTime = time.time()
	totalTimeTaken = endTime - startTime

	timeList.append(totalTimeTaken)

	return phone


def parsePostsTester():
	pass

def checkDiscard(post):
	#Takes as input craigDB post as input
	#Checks if the post title is irrelevant
	#Eg. 'iPhone,iPad jailbreak is here!' , 'Samsung Galaxy S3 leather hoster case'

	postTitle = post['title'].lower()
	discard  = 'false'
	for word in SPAM_KEYWORDS_LIST:
		if word in postTitle and '+' not in postTitle and 'with' not in postTitle:
			discard = 'true'

	return discard

def main(args):
	global timeList
	print "[Main] Welcome to the post parsing script!"

	wipeDatabase = False

	# Check flags
	for arg in args[1:]:
		if arg == "--fresh":
			wipeDatabase = True
			break
		else:
			print "[Main] WARNING: Option '"+arg+"' was unrecognized and has been ignored"

	print "[Main] Loading JSON data from file...",
	craigData = loadJSONData(CRAIGSLIST_SCRAPED_FILEPATH)
	print "done."

	print "[Main] Parsing JSON data...",
	craigDb = getCraigDb(craigData)
	print "done."

	print "[Main] Connecting to database...",
	phonesCollection = pymongo.MongoClient().phones_db.phones_collection
	print "done."

	print "[Main] Retrieving phone database...",
	phoneDb = phonesCollection.find()
	if phoneDb.count() == 0:
		print "FAIL!"
		print "The phone database is empty. Please initialize the database before using it."
		exit()
	print "done."

	print "[Main] There are " + str(phonesCollection.count()) + " phones in the database"

	print "[Main] Opening post collection database",
	postsCollection = pymongo.MongoClient().posts_db.posts_collection
	print "done."

	if wipeDatabase:
		print "[Main] Fresh flag was passed, wiping out database...",
		postsCollection.remove()
		print "done."

	print "[Main] Beginning to parse posts"
	i = 1
	postList = list()
	for post in craigDb:
		copyOfDb = phoneDb.clone() # So the cursor doesn't mess up
		print "Phone #" + str(i)
		phone = parsePost(post, copyOfDb)
		
		print "Subject: " + post['title']

		postList.append(phone)

		print "\n"
		i = i + 1

		if i > 100:
			break
	
	#PROFILE
	avgTime = sum(timeList)/len(timeList)

	print "Average time taken: " + str(avgTime)

	exit()

	postList = cleanPosts(postList)
	
	print "[Main] Writing collection to database...",
	postsCollection.ensure_index( [("description",pymongo.ASCENDING)], unique=True)
	postsCollection.insert(postList)
	print "done."
	
	print "[Main] Done script."

if __name__ == "__main__":
	main(sys.argv)
