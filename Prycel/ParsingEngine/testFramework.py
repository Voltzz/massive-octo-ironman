from parsePosts import parsePost
from parsePosts import getCraigDb
from util import loadJSONData
import os
import pymongo

APPL_ROOT=os.path.join(os.path.dirname(__file__), '..')
CRAIGSLIST_SCRAPED_FILEPATH = os.path.join(APPL_ROOT,"data_sets","scraped","craigslist_TO_scraped.json")


def generateGoldenList():
 	
 	f = open('output_tester.txt','r')
 	content = f.readlines()
 	f.close()

 	content = [line.strip() for line in content]

 
 	goldenList = []

 	for i,line in enumerate(content):
 		if 'Subject:' in line:

 			goldenSet = dict()
 			goldenSet['title'] = line.replace('Subject: ','')
 			goldenSet['new'] = content[i-2].replace('New? ','')
 			goldenSet['refurbished'] = content[i-3].replace('Refurb? ','')
 			goldenSet['unlocked'] = content[i-4].replace('Unlocked? ','')
 			goldenSet['device'] = content[i-5].replace('Device: ','')
 			goldenSet['manufacturer'] = content[i-6].replace('Manufacturer: ','')
 			goldenList.append(goldenSet)

 	return goldenList
	
def parsePostTester(goldenList,post,phone):

	c = 0
	for item in goldenList:
		if post['title'] == item['title']:
			print post['title']
			if str(phone['new']).strip() == str(item['new']).strip():
				print "New? correct ",
				print "Desired-",item['new']," ",
				print "Actual-", phone['new']
				c= c+1	
			else:
				print "New? wrong",
				print "Desired-",item['new']," ",
				print "Actual-", phone['new']
			if str(phone['refurbished']).strip() == str(item['refurbished']).strip():
				print "Refurb correct",
				print "Desired-",item['refurbished']," ",
				print "Actual-", phone['refurbished']
				c= c+1	
			else:
				print "Refurb wrong",
				print "Desired-",item['refurbished']," ",
				print "Actual-", phone['refurbished']	
			if str(phone['unlocked']).strip() == str(item['unlocked']).strip():
				print "Unlocked correct",
				print "Desired-",item['unlocked']," ",
				print "Actual-", phone['unlocked']
				c= c+1	
			else:
				print "Unlocked wrong",
				print "Desired-",item['unlocked']," ",
				print "Actual-", phone['unlocked']	
			if str(phone['device']).strip() == str(item['device']).strip():
				print "Device correct",
				print "Desired-",item['device']," ",
				print "Actual-", phone['device']
				c= c+1	
			else:
				print "Device wrong",
				print "Desired-",item['device']," ",
				print "Actual-", phone['device']	
			if str(phone['manufacturer']).strip() == str(item['manufacturer']).strip():
				print "Manufacturer correct",
				print "Desired-",item['manufacturer']," ",
				print "Actual-", phone['manufacturer']
				c= c+1	
			else:
				print "Manufacturer wrong",
				print "Desired-",item['manufacturer']," ",
				print "Actual-", phone['manufacturer']
				c= c+1
			print "Total: ",c,"/","5"	
			print '-----'
			return c

def generateTestPostTileList():

	f = open('output_tester.txt','r')
 	content = f.readlines()
 	f.close()

 	content = [line.strip() for line in content]

 	postTitleList = []

 	for i,line in enumerate(content):
 		if 'Subject:' in line:
 			postTitleList.append(line.replace('Subject: ',''))

 	return postTitleList


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

	testTitleList = generateTestPostTileList()
	goldenList = generateGoldenList()

	scoreCounter= 0
	iterationCounter = 0

	for post in craigDb:
		copyOfDb = phoneDb.clone() # So the cursor doesn't mess up
		#print "Phone #" + str(i)
		if(post['title'] in testTitleList):
			phone = parsePost(post,copyOfDb)
			scoreCounter = scoreCounter + parsePostTester(goldenList,post,phone)
			iterationCounter = iterationCounter + 1
		#phone = parsePost(post, copyOfDb)
		#parsePostTester(phone,post)
		#print "\n"
		i = i + 1
	iterationCounter = iterationCounter*5
	print "Total Score-" , scoreCounter,"/",iterationCounter 
	print "[Main] Done script."

if __name__ == '__main__':
	main()