import random
import math
import collections
import matplotlib.pyplot as plt
import os
fig = 0
class DataPoint(object):
	cluster=-1
	def __init__(self, label, x, y):
		self.label = label
		self.x = x
		self.y = y
	def printObj(self):
		print self.label, ":", self.x, ", ", self.y, ", ", self.cluster

def readFromFile(filename):
	print "Entered"
	datapoints = []
	f = open(filename)
	line = f.readline()
	lines = line.split('\r')
	lines.pop(0)
	for line in lines:
		splt = line.split('\t')
		datapoints.append(DataPoint(int(splt[0]), float(splt[1]), float(splt[2])))
	return datapoints

def kmeans(k, datapoints):
	seeds = random.sample(range(1, len(datapoints)), k)
	clusters = {}
	centroids = []
	#initialize seeds
	j = k
	for i in seeds:
		print i
		#SOME PROBLEM. CLUSTER MISSING SOMETIMES
		datapoints[i].cluster = j
		j = j-1
		centroids.append(datapoints[i])
	graph_plot(centroids, groupByClusters(datapoints))
	for s in range(0,25):
		print "Iteration: ", s
		datapoints = assignDPtoClusters(centroids, datapoints)
		clusters = groupByClusters(datapoints)
		pseudoCentroids = getCentroids(clusters)
		
		if(checkEquality(centroids, pseudoCentroids)):
			break;
		else:
			centroids = pseudoCentroids
		graph_plot(centroids, groupByClusters(datapoints))
	print "K-means converged at: ", s, "th iteration"
	print "Final clusters: "
	print_clusters(groupByClusters(datapoints))
		
def checkEquality(centroids1, centroids2):
	for i in range(0, len(centroids1)):
		if(centroids1[i].x != centroids2[i].x or centroids1[i].y != centroids2[i].y):
			return False
	return True
	
def getCentroids(clusters):
	centroids = []
	for i in clusters.keys():
		val = clusters[i]
		sumx = 0.0
		sumy = 0.0
		for dp in val:
			sumx = sumx + dp.x
			sumy = sumy + dp.y
		size = (len(val)*1.0)
		newdp = DataPoint(-1, round(sumx/size, 3), round(sumy/size, 3))
		newdp.cluster = i
		centroids.append(newdp)
		
	return centroids
	
def groupByClusters(datapoints):
	clusters = collections.defaultdict(list)
	for dp in datapoints: 
		clusters[dp.cluster].append(dp)
	dict(clusters)
	return clusters
	
def print_clusters(clusters):
	for key in clusters.keys():
		print key,": ", 
		for dp in clusters[key]:
			print dp.label, ",",
		print 
		print
def assignDPtoClusters(centroids, datapoints):
	for dp in datapoints:
		minDist = 999
		for centroid in centroids: 
			newDist = euclidean(centroid, dp)
			if(newDist < minDist):
				minDist = newDist
				dp.cluster = centroid.cluster
	return datapoints
		
def euclidean(dp1, dp2):
	dist = math.sqrt((dp1.x-dp2.x)**2 + (dp1.y-dp2.y)**2)
	return dist

def graph_plot(centroids, clusters):
    plt.close()
    for cluster in clusters:
        dp = clusters[cluster]
        x = []
        y = []
        for d in dp:
            x.append(d.x)
            y.append(d.y)
        if cluster == 1:
            plt.plot(x, y, 'ro')
        if cluster == 2:
            plt.plot(x, y, 'go')
        if cluster == 3:
            plt.plot(x, y, 'bo')
        if cluster == 4:
            plt.plot(x, y, 'yo')
        if cluster == 5:
            plt.plot(x, y, 'mo')

        plt.axis([0, 1.2, 0, 1.2])
   
    for d in centroids:
        x = []
        y = []
        x.append(d.x)
        y.append(d.y)
        if d.cluster == 1:
            plt.plot(x, y, 'r^', markersize=10)
        if d.cluster == 2:
            plt.plot(x, y, 'g^', markersize=10)
        if d.cluster == 3:
            plt.plot(x, y, 'b^', markersize=10)
        if d.cluster == 4:
            plt.plot(x, y, 'y^', markersize=10)
        if d.cluster == 5:
            plt.plot(x, y, 'm^', markersize=10)

    plt.axis([0, 1.2, 0, 1.2])
    print len(centroids)
    global fig
    fig += 1
    if not os.path.exists("plots"):
        os.makedirs("plots")
    plt.savefig("plots/" + str(fig) + ".png")

datapoints = readFromFile("test_data.txt")
k = 5
kmeans(k, datapoints)


	
