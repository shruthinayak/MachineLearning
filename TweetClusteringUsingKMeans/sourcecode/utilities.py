import os

fig = 0


def read_from_file(filename):
    print "Entered"
    datapoints = []
    f = open(filename)
    line = f.readline()
    lines = line.split('\r')
    lines.pop(0)
    for line in lines:
        splt = line.split('\t')
        datapoints.append(splt)
    return datapoints


def print_clusters(clusters):
    for key in clusters.keys():
        print key, "\t ",
        for dp in clusters[key]:
            print dp.label, ",",
        print
    print "-" * 50


def check_equality(centroids1, centroids2, isTweet):
    if not isTweet:
        for i in range(0, len(centroids1)):
            if centroids1[i].x != centroids2[i].x or centroids1[i].y != centroids2[i].y:
                return False
    else:
        for i in range(0, len(centroids1)):
            #print centroids1[i].label, centroids2[i].label
            if centroids1[i].label != centroids2[i].label:
                return False
    return True
