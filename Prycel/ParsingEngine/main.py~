import json

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

def parsePost(post, phone):
	# Takes as input a craigDb[i] post and a blank phone dictionary
	# No output, but the phone field should be filled in with values
	# e.g. phone['brand'], phone['device'] etc. should all be filled in
	pass


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
	allPhones = list()

	for i in range(0, len(craigData)):
		thisPhone = dict()

		

		allPhones.append(thisPhone)
	

if __name__ == "__main__":
	main()
