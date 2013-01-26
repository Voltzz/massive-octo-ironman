import json

jsonFile = open("/Users/z/Prycel/data_sets/craigslist_TO_scraped.json").read()

jsonData = json.loads(jsonFile)

for i in range(0, len(jsonData)):
	print "Entry #"+str(i)
	print "Title: \""+jsonData[i]['title'][0]+"\""
	print "Description"
	print jsonData[i]['desc'][0]
	print "\n"
