import json

def loadJSONData(filepath):
	jsonFile = open(filepath).read()
	jsonData = json.loads(jsonFile)

	return jsonData


