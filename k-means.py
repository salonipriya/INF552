#!/usr/bin/env python3.4
#LOGIC: To Assign atleast one datapoint to each centroid 
#LOGIC: To change the centroid location based on Datapoint
import sys
import random
import math
import copy
from decimal import Decimal

INPUT_FILE = "input.txt"

class Datapoints(object):
	def __init__(self, X_cord,Y_cord):
		self.X_cordinate = X_cord
		self.Y_cordinate = Y_cord

# Fetch the range for the datapoints 
# Code Optimization: Can be performed during input read
def getRange(dataSet):
	#New in Python3
	min_valX = sys.maxsize
	min_valY = sys.maxsize
	max_valX = -sys.maxsize-1
	max_valY = -sys.maxsize-1
	if not dataSet:
		#ERROR CHECK HERE
		return ((0,0),(0,0))
	for val in dataSet:
		X = float(val.X_cordinate)
		Y = float(val.Y_cordinate)
		if(X<min_valX):
			min_valX = X
		if(X>max_valX):
			max_valX = X
		if(Y<min_valY):
			min_valY = Y
		if(Y>max_valY):
			max_valY = Y
	Range_X = (min_valX,max_valX)
	Range_Y = (min_valY,max_valY)
	return (Range_X,Range_Y)

def Insert_Key(Range_X, Range_Y,new_centroid_dict):
	#Check: The random location should not coincide
	while True:
		get_random_X = random.uniform(Range_X[0],Range_X[1])
		get_random_Y = random.uniform(Range_Y[0],Range_Y[1])

		key = Datapoints(get_random_X,get_random_Y)
		if key not in new_centroid_dict:
			new_centroid_dict[key] = list()
			break
	return new_centroid_dict


# To get the random location for initial K Centroid - ITERATION #1
#ERROR CHECK: For now taking the location of all three centroid at Random
def Randomize_Centroid_Iteration_1(Range_X,Range_Y,K):
	new_centroid_dict = {}
	for i in range(0, K):
		new_centroid_dict = Insert_Key (Range_X,Range_Y,new_centroid_dict)
	return new_centroid_dict

#To fetch new location for Centroid
def Update_Centroid_Location(Cluster_map,dataSet):
	new_centroid_dict = {}
	#Steps:
	##Get the list of points for each key from the map
	##Evaluate range
	for key in Cluster_map:
		Range_X,Range_Y = getRange(Cluster_map[key])
		new_centroid_dict = Insert_Key (Range_X,Range_Y,new_centroid_dict)
	return new_centroid_dict

#Algorithm terminating condition
def AlgorithmStop(oldCentroid_dict,new_centroid_dict):
	if not bool(oldCentroid_dict):
		return False
	return set(oldCentroid_dict) == set(new_centroid_dict)

def attach_To_Centroid(dataSet,Cluster_map,type_distance):
	for each_dataPoint in dataSet:
		#Create an empty class type object
		store_CentroidLabel = type('', (), {})()
		min_dist = float(sys.maxsize)
		###print ("Considering Pont",each_dataPoint.X_cordinate)
		for Key in Cluster_map:
			###print ("Considering Key",Key.X_cordinate)
			#Euclidean Distance
			if(type_distance == "L1"):
				dist = math.sqrt((Key.X_cordinate - float(each_dataPoint.X_cordinate))**2 + (Key.Y_cordinate - float(each_dataPoint.Y_cordinate))**2)
			elif(type_distance == "L2"):
				dist = math.fabs(Key.X_cordinate - float(each_dataPoint.X_cordinate)) + math.fabs(Key.Y_cordinate - float(each_dataPoint.Y_cordinate))
		
			if (dist < min_dist):
				min_dist = dist
				store_CentroidLabel = Key
		###print (store_CentroidLabel.X_cordinate,"Label_X")
		try:
			Cluster_map[store_CentroidLabel].append(Datapoints(each_dataPoint.X_cordinate,each_dataPoint.Y_cordinate))
		except KeyError:
			print ("There was an Error with Cluster map centroid key")
			exit()

	#If any cluster is empty
	#Assign one point at random from dataSet to empty cluster 
	#Avoid empty clusters and 0 means

	

	return Cluster_map



def kmeans(dataSet,K):
	#Initialize centroid Randomly - Iteration_#1
	#Get the range for Centroid
	Range_X,Range_Y = getRange(dataSet)

	newVersion_Centroids = copy.deepcopy(Randomize_Centroid_Iteration_1(Range_X,Range_Y,K))
	newCentroid_dict = {}
	for i in range(2):
		if not bool(newCentroid_dict):
			newCentroid_dict.clear()
		newCentroid_dict = copy.deepcopy(newVersion_Centroids)
		type_distance = "L"+str(i+1)

		#Initialize book keeping variables
		oldCentroid_dict = None

		#Start the kMeans Algorithm
		while not AlgorithmStop(oldCentroid_dict,newCentroid_dict):
		
			#Assign Clustering label to each datapoints
			Cluster_Map = attach_To_Centroid(dataSet,newCentroid_dict,type_distance)

			#Book Keeping
			oldCentroid_dict = copy.deepcopy(Cluster_Map)

			#Recaluculate Centroids
			newCentroid_dict = Update_Centroid_Location(Cluster_Map,dataSet)
			break

		#Print the Cluster Set
		i = 1
		#Remove after who have finished the algorithm
		print ("Cluster based on ",type_distance," distance",sep="")
		for key in Cluster_Map:
			print ("Cluster C",i," location:",key.X_cordinate,",",key.Y_cordinate,sep="")
			for value in Cluster_Map[key]:
				print (value.X_cordinate,",",value.Y_cordinate,sep="",end="")
			i +=1
			print ("")


def read_file():
	try:
		global f
		f = open(INPUT_FILE,"r")
	except IOError:
		print ("Error reading the file")
		exit()
	# Fetch the dataSet as list of Datapoints
	dataSet = []
	for line in f:
		cordinate_split = line.split(",")
		dataSet.append(Datapoints(cordinate_split[0],cordinate_split[1]))
	#print (dataSet[0].X_cordinate)
	# Given: K = 3
	kmeans(dataSet,3)

def main():	
	read_file()

main()