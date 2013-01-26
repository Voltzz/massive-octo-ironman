import json
import Levenshtein

CRAIGSLIST_SCRAPED_FILEPATH = "/Users/z/Prycel/data_sets/scraped/craigslist_TO_scraped.json")
SMARTPHONE_SCRAPED_FILEPATH = "/Users/z/Prycel/data_sets/scraped/sardb_scraped.json")

def loadJSONData(filepath):
	jsonFile = open(filepath).read()
	jsonData = json.loads(jsonFile)

	return jsonData

def getPhoneDb(phoneData):
	# Takes as input the raw JSON file
	# Output needs to be a dictionary with all phone brand/device filled
	# E.g. phoneDb["Apple"] = ["iPhone", "iPhone 2", "iPhone 3G", "iPhone 3GS" ... ]
	pass

def getCraigDb(craigData):
	# Takes as input the raw JSON file
	# Output needs to be a ilst of dictionaries
	# E.g. craigDb[0] corresponds to the first posting
	# craigDb[0]["title"] = "SELLING COOL PHONE!!!"
	# craigDb[0]["desc"] = "OMG i love this phone but dont want it\nSo please keep it love you thx"
	pass


def parsePost(post, phone, phoneDb):
	# Takes as input a craigDb[i] post and a blank phone object, and the phone database
	# No output, but the phone field should be filled in with values
	# e.g. phone['brand'], phone['device'] etc. should all be filled in

	# Initial Values
	phone['brand'] = "Unknown"
	phone['device'] = "Unknown"
	phone['unlocked'] = False
	phone['refurbished'] = False
	phone['new'] = False
	phone['description'] = "UNDEFINED"
	phone['price'] = -1

	# First lets get device and brand
	topBrand = "Unknown"
	topDevice = "Unknown"
	currBest = 0
	for brand in phoneDb:
		for device in phoneDb:
			for word in post['title']:
				thisRatio = ratio(word, device)
				if thisRatio > currBest:
					currBest = thisRatio
					topBrand = brand
					topDevice = device
	phone['brand'] = topBrand
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


def main():
	craigData = loadJSONData(CRAIGSLIST_SCRAPED_FILEPATH)
	phoneData = loadJSONData(SMARTPHONE_SCRAPED_FILEPATH)

	phoneDb = getPhoneDb(phoneData)
	craigDb = getCraigDb(craigData)

	# The full list of phones
	# Each phone has these fields:
	# Brand (String)
	# Device (String)
	# Unlocked (Bool)
	# Refurbished (Bool)
	# New (Bool)
	# Description (String)
	# Price (Integer)
	allPhones = list()

	for i in range(0, len(craigDb)):
		thisPhone = dict()

		parsePost(craigDb[i], thisPhone, phoneDb)

		allPhones.append(thisPhone)
	
	for i in range(0, len(allPhones)):
		print "Phone #"+str(i)
		print "Brand: " + allPhones[i]['brand']
		print "Device: " + allPhones[i]['device']
		print "Unlocked? " + allPhones[i]['unlocked']
		print "Refurbished? " + allPhones[i]['refurbished']
		print "New? " + allPhones[i]['new']
		print "Description"
		print allPhones[i]['description']
		print "\n"
	

if __name__ == "__main__":
	main()
