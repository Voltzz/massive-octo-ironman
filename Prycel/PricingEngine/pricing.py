from sklearn import linear_model
from sklearn.externals import joblib
import pylab as pl
import numpy as np

'''

	Data Set assumption:
	JSON of form

	[
		{"unlocked":1,"refurbished":0,"new":1,"price":300},
		{"unlocked":0,"refurbished":0,"new":1,"price":600}
	]

'''


def predictPrices(regr,inputVector):
	return regr.predict(inputVector)

def convertPostToVector(post):
#Converts input vector to NumPy array 
	inputList = []

	inputList.append(post['unlocked'])
	inputList.append(post['refurbished'])
	inputList.append(post['new'])

	return np.array(inputList)

def main():
	regr = joblib.load('TrainingData/appleiphone5.pkl')


	#Create fake post
	#convertPostToVector(fakePost)

	inputVector = np.array([1,0,1])
	outputValue = predictPrices(regr,inputVector)

	print "Output Value",outputValue

if __name__ == '__main__':
	main()