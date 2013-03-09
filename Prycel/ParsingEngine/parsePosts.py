import json
import Levenshtein
import unicodedata
import os
import pymongo
from util import loadJSONData

# TODO: Fix this latent bug...
APPL_ROOT=os.path.join(os.path.dirname(__file__), '..')

CRAIGSLIST_SCRAPED_FILEPATH = os.path.join(APPL_ROOT,"data_sets","scraped","craigslist_TO_scraped.json")


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


def parsePost(post, phoneDb):
	# Takes as input a craigDb[i] post and a blank phone object, and the phone database
	# No output, but the phone field should be filled in with values
	# e.g. phone['manufacturer'], phone['device'] etc. should all be filled in

	phone = dict()

	# Initial Values
	phone['manufacturer'] = "Unknown"
	phone['device'] = "Unknown"
	phone['unlocked'] = False
	phone['refurbished'] = False
	phone['new'] = False
	phone['description'] = "UNDEFINED"
	phone['price'] = -1

	# First lets get device and manufacturer
	topManufacturer = "Unknown"
	topDevice = "Unknown"
	manufacturerRatios = dict() # We keep track of the ratio for each manufacturer, incase we detect an invalid one
	currManuBest = -1
	currDeviBest = -1
	for thisPhone in phoneDb:
		manufacturer = thisPhone['manufacturer']
		device = thisPhone['device']
		#print "(" + manufacturer + ") " + device
		# Find the closest Manufacturer, if exists
		# Search the title n words at a time, where n is length of manufacturer
		numOfWordsInManu = len(manufacturer.split(" "))
		splitTitle = post['title'].split()
		try: # We will run out of words since we access i + len(manufacturer)
			for i in range(0, len(manufacturer)):
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
		
		# Now lets find the closest device
		# Same strategy as before
		numOfWordsInDevi = len(device.split(" "))
		try:
			for i in range(0, len(device)):
				deviRatio = Levenshtein.ratio(str(" ".join(splitTitle[i:i+numOfWordsInDevi])).lower(), str(device).lower())
				deviRatio = deviRatio + ((numOfWordsInDevi-1) * 0.0001)
				#print "Comparison: " + str(" ".join(splitTitle[i:i+numOfWordsInDevi])).lower() + " vs. " + str(device).lower()
				#print "Ratio: " + str(deviRatio)
				if deviRatio > currDeviBest:
					currDeviBest = deviRatio
					topDevice = device
		except:
			pass
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

	print "Manufacturer: " + phone['manufacturer']
	print "Device: " + phone['device']
	print "Unlocked? " + str(phone['unlocked'])
	print "Refurb? " + str(phone['refurbished'])
	print "New? " + str(phone['new'])
	print "---------"
	print "Subject: " + post['title']
	print phone['description']


def main():
	print "[Main] Welcome to the post parsing script!"

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

	print "[Main] Beginning to parse posts"
	i = 1
	for post in craigDb:
		copyOfDb = phoneDb.clone() # So the cursor doesn't mess up
		print "Phone #" + str(i)
		parsePost(post, copyOfDb)
		print "\n"
		i = i + 1
	
	print "[Main] Done script."

if __name__ == "__main__":
	main()
