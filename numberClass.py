from numpy import *

"""
This class represents a number along
with the parameters that every class
requires.
classValue = The numeric value of the class
prior = The prior probability of this class 
        based on empirical frequencies
empirical_likelihood = matrix of likelihoods
        for every pixel location to be a 
        forground pixel
training_data = list of 2d arrays where each
		2d array is the training image that
		belongs to this class
"""
class numberClass(object):

	def __init__(self, value):
		self.classValue = value
		self.prior= .1
		self.empirical_likelihood = zeros((28,28))
		self.training_data = []

	def addTrainingData(self, training_value):
		self.training_data.append(training_value)

	def setPrior(self, priorValue):
		self.prior = priorValue


if __name__ == '__main__':
	main()


