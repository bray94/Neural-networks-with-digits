from numpy import *
from numberClass import *
import time
import csv
import random as r

def readTrainingLabels():
	# Open The File
	file = open("digitdata/traininglabels" , "r")

	# Count each digit in training set
	list = [0,0,0,0,0,0,0,0,0,0]
	labels = []

	# Total num of digits
	counter = 0

	for line in file:
		list[int(line.strip())]+=1
		counter+=1
		labels.append(int(line.strip()))

	file.close()

	return [float(x)/counter for x in list],labels

def readTrainingImages():
	# Open the Training Images
	file = open("digitdata/trainingimages", "r")

	# The List to store the images
	list = []

	curr_image = []
	i = 0


	for line in file:
		# Remove the \n
		line = line[0:28]

		j = 0

		for character in line:
			if character != ' ':
				curr_image.append(1)
			else: curr_image.append(0)
			j+=1

		i+=1

		if (i%28) == 0:
			list.append(array(curr_image))
			curr_image = []

	return list

def readTestingLabels():
	# Open The File
	file = open("digitdata/testlabels" , "r")

	# Count each digit in training set
	list = [0,0,0,0,0,0,0,0,0,0]
	labels = []

	# Total num of digits
	counter = 0

	for line in file:
		list[int(line.strip())]+=1
		counter+=1
		labels.append(int(line.strip()))

	file.close()

	return list,labels

def readTestingImages():
	# Open the Training Images
	file = open("digitdata/testimages", "r")

	# The List to store the images
	list = []

	curr_image = zeros((28,28))
	i = 0


	for line in file:
		# Remove the \n
		line = line.rstrip()

		j = 0

		for character in line:
			if line[j] != ' ':
				curr_image[(i)%28][j] = 1
			j+=1

		i+=1

		if (i%28) == 0:
			list.append(curr_image)
			curr_image = zeros((28,28))

	return list

def	makeWeights(a):
	if(a == 0): return zeros(28*28)
	else: return random.rand(28*28)

def classify(weightList, imagesList, labels, epochs = 200, bias = 0, randomIteration = True):

	rightPercentages = []

	images = zip(imagesList, labels)

	for x in xrange(epochs):
		if randomIteration: r.shuffle(images)
		alpha = float(1)/(1 + x) # learning rate decay function
		right = 0

		for curr in xrange(5000): #iterate over all training images
			totalList = [] #make an empty list to pick the argmax from

			for x in xrange(10):
				total = dot(weightList[x],images[curr][0]); # dots weight and image vector

				total += bias # add the bias
				totalList.append(total) # append to list

			classifiedImage = totalList.index(max(totalList)) # get argmax from total list

			if classifiedImage == images[curr][1]:
				right += 1
				continue
			else:
				
					weightList[images[curr][1]] += alpha * (images[curr][0])
					weightList[classifiedImage] -= alpha * (images[curr][0])

		rightPercentages.append(float(right)/5000)
		if float(right)/5000 >= 1.0: break

	return rightPercentages




def main():
	start_time = time.time() 
	#priorList = readTrainingLabels()
	imagesList = readTrainingImages()
	labelsList, labels = readTrainingLabels()
	weightList = [] # list of weights for 0-9

	classesList = []

	for x in xrange(0,10):
		classesList.append(numberClass(x))
		classesList[x].setPrior(labelsList[x])

	for x in xrange(0,len(imagesList)):
		classesList[labels[x]].addTrainingData(imagesList[x])

	for x in xrange(0,10):
		weightList.append(makeWeights(1)); # 0 intilizes all of them to 0, anything else is random

	rightPercentages = classify(weightList, imagesList, labels)

	with open('data.csv' , 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

		for x in rightPercentages:
			writer.writerow([x])

	print(" --- %s seconds ---" % (time.time() - start_time))





if __name__ == '__main__':
	main()

