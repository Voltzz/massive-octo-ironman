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
import pylab as pl
import numpy as np

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

	X,y = createVectors(dataSet)
	regr = generateLinearModel(X,y)

	inputVector = np.array([1,1,0])
	outputValue = predictPrices(regr,inputVector)


if __name__ == "__main__":
	main()	
