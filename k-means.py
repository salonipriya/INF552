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
	def __repr__(self):
		return repr((self.X_cordinate, self.Y_cordinate))

#Algorithm terminate condition
def AlgorithmStop(oldCentroid_dict,new_centroid_dict):
	if not bool(oldCentroid_dict):
		return False
	for val in new_centroid_dict:
		if val not in new_centroid_dict:
			return False
	return True
			#return False
	#return True

def Insert_Key(get_mean_for_set,new_centroid_dict):
	#Algo:
	#Get mean of datapoins and set the respective key
	#Avoiding the use of Numpy
	for value in get_mean_for_set:
		total_sum_X = value.X_cordinate
		total_sum_Y = value.Y_cordinate
	average_X = float(total_sum_X/len(get_mean_for_set))
	average_Y = float(total_sum_Y/len(get_mean_for_set))
	key = Datapoints(average_X,average_Y)
	new_centroid_dict[key] = list()
		#Based on the logic chance of having same keys is minimialized
		#Confirm with Shiva
	return new_centroid_dict

def Update_Centroid_Location(Cluster_map):
	new_centroid_dict = {}
	for key in Cluster_map:
		#Steps:
		##Get the entire list of values for each Key
		##Evaluate average to assign new key
		new_centroid_dict = Insert_Key (Cluster_map[key],new_centroid_dict)
	return new_centroid_dict

def Randomize_Centroid_Iteration_1(dataSet,K):
	new_centroid_dict = {}
	#Error Check
	if len(dataSet) < K:
		print ("To form clusters for K=3 kMeans you need a minimum of three points")
		exit()
	#Create 3 subset of sorted python list
	no_of_sets_needed = int(len(dataSet)/3)
	chunks=[dataSet[x:x+no_of_sets_needed] for x in range(0, len(dataSet), no_of_sets_needed)]
	total_chunk_len = len(chunks[0]) + len(chunks[1]) + len(chunks[2])
	#print (len(dataSet))
	#print (total_chunk_len)
	while (total_chunk_len < len(dataSet)):
		chunks[2].append(dataSet[total_chunk_len])
		total_chunk_len = total_chunk_len + 1
	#print (chunks[2])
	for i in range(0,K):
		new_centroid_dict = copy.deepcopy(Insert_Key (chunks[i],new_centroid_dict))
	return new_centroid_dict

def attach_To_Centroid(dataSet,cluster_map,type_distance):
	for each_dataPoint in dataSet:
		#Create an empty class type object
		store_CentroidLabel = type('', (), {})()
		min_dist = float(sys.maxsize)
		#print ("Considering Point",each_dataPoints,X_cordinate)
		for Key in cluster_map:
			#print ("Considering Key",Key.X_cordinate)
			for Key in cluster_map:
				#Euclidean Distance
				if (type_distance == "L1"):
					dist = math.sqrt((Key.X_cordinate - float(each_dataPoint.X_cordinate))**2 + (Key.Y_cordinate - float(each_dataPoint.Y_cordinate))**2)
				elif(type_distance == "L2"):
					dist = math.fabs(Key.X_cordinate - float(each_dataPoint.X_cordinate)) + math.fabs(Key.Y_cordinate - float(each_dataPoint.Y_cordinate))

				if(dist < min_dist):
					min_dist =dist
					store_CentroidLabel = Key
		try:
			cluster_map[store_CentroidLabel].append(Datapoints(each_dataPoint.X_cordinate,each_dataPoint.Y_cordinate))
		except KeyError:
			print ("There was an Error with Cluster map centroid key")
	return cluster_map

def kmeans(dataSet,K):
	#Initialize centroid Randomly - Iteration_#1
	#Get the range for Centroid
	Sorted_dataSet = []
	Sorted_dataSet = sorted(dataSet, key=lambda x: x.X_cordinate)
	newVersion_Centroids = copy.deepcopy(Randomize_Centroid_Iteration_1(Sorted_dataSet,K))
	newCentroid_dict = {}
	for i in range(2):
		if not bool(newCentroid_dict):
			newCentroid_dict.clear()
		newCentroid_dict = copy.deepcopy(newVersion_Centroids)
		type_distance = "L"+str(i+1)

		#Initialize book keeping variables
		oldCentroid_dict = None

		#start the kMeans Algorithm
		while not AlgorithmStop(oldCentroid_dict,newCentroid_dict):

			#Assign Clustering label to each Datapoints
			Cluster_Map = attach_To_Centroid(dataSet,newCentroid_dict,type_distance)

			#Book keeping
			oldCentroid_dict = copy.deepcopy(Cluster_Map)

			#Recalculate Centroids
			newCentroid_dict = Update_Centroid_Location(Cluster_Map)

		#Print the Cluster Set
		i = 1
		##IMPLEMENTATION COMMENT
		#Remove after you have finished algorithm
		print ("Cluster based on ",type_distance," distance",sep="")
		for key in Cluster_Map:
			print ("Cluster C",i," location:",key.X_cordinate,",",key.Y_cordinate,sep="",end="\n")
			print ("Clustered Set:")
			for value in Cluster_Map[key]:
				print (value.X_cordinate,",",value.Y_cordinate,sep="",end="\n")
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
		cordinate_split = line.strip().split(",")
		dataSet.append(Datapoints(float(cordinate_split[0]),float(cordinate_split[1])))
	#print (dataSet)
	#print (dataSet[0].X_cordinate)
	# Given: K = 3
	kmeans(dataSet,3)

def main():	
	read_file()

main()