import codecs
#fileName = "data_sets/scraped/craigslist_TO_scraped.json"
fileName = "data_sets/scraped/arena_scraped.json"

f = codecs.open(fileName, 'r', encoding="utf-8")
allLines = f.readlines()
f.close()
for i in range(0, len(allLines)):
	allLines[i] = allLines[i].replace("\u0410", "")
f = codecs.open(fileName, 'w', encoding="ascii", errors="ignore")
for i in range(0, len(allLines)):
	f.write(allLines[i])
f.close()
