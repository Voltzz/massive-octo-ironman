#This is the first iteration of the pricing engine
'''

	Data Set assumption:
	JSON of form

	[
		{"unlocked":1,"refurbished":0,"new":1,"price":300},
		{"unlocked":0,"refurbished":0,"new":1,"price":600}
	]
'''

from sklearn import linear_model
from sklearn.externals import joblib
import pylab as pl
import numpy as np
import pymongo

def createVectors(dataSet):
	
	#Numpy array order for X - 1) unlocked 2) refurbished 3) new 
	#Numpy array order for Y - 1) unlocked

	x_list = []
	y_list = []
	for element in dataSet:
		miniList = []
		miniList.append(element["unlocked"])
		miniList.append(element["refurbished"])
		miniList.append(element["new"])
		x_list.append(miniList)
		y_list.append(element["price"])
		#print type(element['price']),
		#print element

	X = np.array(x_list)
	y = np.array(y_list)

	return X,y

def generateLinearModel(X,y):

	regr = linear_model.LinearRegression()
	regr.fit(X,y)
	#print regr.coef_
	return regr

def predictPrices(regr,inputVector):
	return regr.predict(inputVector)


def main():
	

	dataSet = [{"unlocked":1,"refurbished":0,"new":1,"price":300},{"unlocked":0,"refurbished":0,"new":1,"price":600}]

	print "Training.py","[Main] Connecting to database...",
	postsCollection = pymongo.MongoClient().posts_db.posts_collection
	print "done."

	print "[Main] Retrieving phone database...",
	postsDb = postsCollection.find()
	if postsDb.count() == 0:
		print "FAIL!"
		print "The posts database is empty. Please initialize the database before using it."
		exit()
	print "done."

	copyOfdb = postsDb.clone() # So the cursor doesn't mess up
	listByPhoneNames = dict() # {'Samsung Galaxy S3': [{'unlocked': True, 'refurbished': True, 'new': False, 'price':300}],
						      #   'Apple iPhone 4':[{'unlocked': True, 'refurbished': True, 'new': False, 'price':300}]
						      # }

	for thisPost in copyOfdb:

		postInfoDict = dict()
		manufacturer = thisPost['manufacturer']
		device  = thisPost['device']
		postInfoDict['unlocked'] = thisPost['unlocked']
		postInfoDict['refurbished'] = thisPost['refurbished']
		postInfoDict['new'] = thisPost['new']
		postInfoDict['price'] = thisPost['price']

		dictKey = manufacturer+' '+device

		if dictKey not in listByPhoneNames.keys():
			listByPhoneNames[dictKey] = []
			listByPhoneNames[dictKey].append(postInfoDict)
		else:
			listByPhoneNames[dictKey].append(postInfoDict)


	#Converting 'True' to 1 and 'False' to 0
	for key in listByPhoneNames.keys():

		elementList = listByPhoneNames[key]

		elementsToPop = []
		for i,element in enumerate(elementList):

			if element['unlocked'] == True:
				element['unlocked'] = 1
			elif element['unlocked'] == False:
				element['unlocked'] = 0

			if element['refurbished'] == True:
				element['refurbished'] = 1
			elif element['refurbished']== False:
				element['refurbished']= 0

			if element['new'] == True:
				element['new'] = 1
			elif element['new']== False:
				element['new']= 0

			try:
				element['price'] = float(str(element['price']))
			except ValueError:
				elementsToPop.append(element)

		for i in elementsToPop:
			elementList.pop(elementList.index(i))

		listByPhoneNames[key] = elementList

	#Creating data-set of original form

	
	for key in listByPhoneNames.keys():

		dataSet = listByPhoneNames[key]
		X,y = createVectors(dataSet)
		regr = generateLinearModel(X,y)

		keyName =key.replace(' ','')
		if '/' in keyName:
			keyName = keyName.replace('/','_')
		filename = 'TrainingData/'+str(keyName).lower()+'.pkl'
		_ = joblib.dump(regr, filename, compress=9)


	#dataSet = [{'new': 0, 'price': u'700', 'refurbished': 0, 'unlocked': 1}, {'new': 1, 'price': u'595', 'refurbished': 0, 'unlocked': 0}, {'new': 1, 'price': u'650', 'refurbished': 0, 'unlocked': 0}, {'new': 0, 'price': u'380', 'refurbished': 0, 'unlocked': 0}, {'new': 1, 'price': u'560', 'refurbished': 0, 'unlocked': 1}, {'new': 1, 'price': u'1', 'refurbished': 0, 'unlocked': 0}, {'new': 0, 'price': u'420', 'refurbished': 0, 'unlocked': 0}, {'new': 1, 'price': u'580', 'refurbished': 0, 'unlocked': 1}, {'new': 0, 'price': u'400', 'refurbished': 0, 'unlocked': 0}, {'new': 1, 'price': u'650', 'refurbished': 0, 'unlocked': 0}, {'new': 1, 'price': u'650', 'refurbished': 0, 'unlocked': 1}, {'new': 1, 'price': u'650', 'refurbished': 0, 'unlocked': 1}, {'new': 1, 'price': u'575', 'refurbished': 0, 'unlocked': 0}, {'new': 1, 'price': u'400', 'refurbished': 0, 'unlocked': 0}, {'new': 1, 'price': u'600', 'refurbished': 0, 'unlocked': 0}]
	#X,y = X,y = createVectors(dataSet)
	#regr = generateLinearModel(X,y)

	#filename = 'trainedTest.pkl'
	#_ = joblib.dump(regr, filename, compress=9)

	#X,y = createVectors(dataSet)
	#regr = generateLinearModel(X,y)

	#filename = 'trained.pkl'
	#_ = joblib.dump(regr, filename, compress=9)

	#inputVector = np.array([1,1,0])
	#outputValue = predictPrices(regr,inputVector)


if __name__ == "__main__":
	main()	
