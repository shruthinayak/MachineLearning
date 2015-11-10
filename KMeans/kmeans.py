import random
import math
import collections
import matplotlib.pyplot as plt
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
	graphplot(centroids, groupByClusters(datapoints).values())
	for s in range(0,25):
		print "Iteration: ", s
		datapoints = assignDPtoClusters(centroids, datapoints)
		clusters = groupByClusters(datapoints)
		pseudoCentroids = getCentroids(clusters)
		if(checkEquality(centroids, pseudoCentroids)):
			break;
		else:
			centroids = pseudoCentroids
	print "K-means converged at: ", s, "th iteration"
	print "Final clusters: "
	groupByClusters(datapoints)
		
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
	for key in clusters.keys():
		print key,": ", 
		for dp in clusters[key]:
			print dp.label, ",",
		print 
		print
	return clusters

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

def graphplot(centroids, dp):
	x=[]
	y=[]
	count=0
	for d in dp:
		for v in d:
			count+=1
			print v.x, v.x
			x.append(v.x)
			y.append(v.y)
	plt.plot(x, y, 'ro')
	plt.axis([0, max(x)+0.5, 0, max(y)+0.5])
	x=[]
	y=[]
	for d in centroids:
		print d.x, d.x
		x.append(d.x)
		y.append(d.y)
	plt.plot(x, y, 'bo')
	plt.axis([0, max(x)+0.5, 0, max(y)+0.5])
	print len(centroids), count
	global fig
	fig += 1
	plt.savefig(str(fig)+".png")

datapoints = readFromFile("test_data.txt")
k = 5
kmeans(k, datapoints)


	
