import json
import sys
import core_functions
import utilities


class Tweet(object):
    text = ""
    id_str = ""
    cluster = -1
    label = ""


def as_tweet(line):
    p = Tweet()
    p.__dict__.update(line)
    return p


def read_tweets(filepath):
    local_tweets = []
    f = open(filepath)
    lines = f.readlines()
    f.close()

    for line in lines:
        o = json.loads(line, object_hook=as_tweet)
        o.label = o.id_str
        local_tweets.append(o)
    return local_tweets


if len(sys.argv) == 4:
    initial_seeds = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    tweets = read_tweets(input_file)

    k = 25

    centroids, clusters = core_functions.kmeans(k, tweets, True, initial_seeds)
    l = 0
    sse = core_functions.validate_clusters(centroids, clusters, True)
    print "K: ", k, "SSE: ", sse
    with open(output_file, "a") as myfile:
        for k in clusters:
            myfile.write(str(k) + ":")
            for i in clusters[k]:
                myfile.write(str(i.label)+", ")
            myfile.write("\n")
            myfile.write("\n")
else:
    print 'Usage: '
    print 'python kmeans.py <initial_seeds> <input_file> <output_file>'
