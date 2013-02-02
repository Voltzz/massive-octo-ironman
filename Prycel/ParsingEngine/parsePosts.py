import json
import Levenshtein
import unicodedata
import os
from util import loadJSONData

# TODO: Fix this latent bug...
APPL_ROOT=os.path.join(os.path.dirname(__file__), '..')

CRAIGSLIST_SCRAPED_FILEPATH = os.path.join(APPL_ROOT,"data_sets","scraped","craigslist_TO_scraped.json")


def getCraigDb(craigData):
	# Takes as input the raw JSON file
	# Output needs to be a ilst of dictionaries
	# E.g. craigDb[0] corresponds to the first posting
	# craigDb[0]["title"] = "SELLING COOL PHONE!!!"
	# craigDb[0]["desc"] = "OMG i love this phone but dont want it\nSo please keep it love you thx"

	craigDb = [dict() for x in range(len(craigData))]
	for i,craigItem in enumerate(craigData):
		title = craigItem["title"][0]
		desc = ''	
		rawDesc = craigItem["desc"]

		for d in rawDesc:
			desc = desc + d

		craigDb[i]["title"] = title
		craigDb[i]['desc'] = desc

	return craigDb


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
	currBest = -1
	for brand in phoneDb.iterkeys():
		for device in phoneDb[brand]:
			for word in post['title'].split():
				thisRatio = Levenshtein.ratio(str(word), str(device))
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

