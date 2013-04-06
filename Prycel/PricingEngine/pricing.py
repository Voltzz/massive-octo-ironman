from sklearn import linear_model
from sklearn.externals import joblib
import pylab as pl
import numpy as np


def predictPrices(regr,inputVector):
	return regr.predict(inputVector)

def main():
	regr = joblib.load('trained.pkl')

	inputVector = np.array([1,1,0])
	outputValue = predictPrices(regr,inputVector)

	print "Output Value",outputValue

if __name__ == '__main__':
	main()