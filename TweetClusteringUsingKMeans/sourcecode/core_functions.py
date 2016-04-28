import random
import math
import collections
import utilities


class DataPoint(object):
    cluster = -1

    def __init__(self, label, x, y):
        self.label = label
        self.x = x
        self.y = y

    def print_obj(self):
        print self.label, ":", self.x, ", ", self.y, ", ", self.cluster


def create_datapoints(parsed):
    data_points = []
    for line in parsed:
        data_points.append(DataPoint(int(line[0]), float(line[1]), float(line[2])))
    return data_points


def kmeans(k, data_points, is_tweet, initial_seeds_path=""):
    if is_tweet:
        centroids = get_initial_centroids_for_tweet(k, initial_seeds_path, data_points)
    else:
        centroids = get_initial_centroids(data_points, k)
    s = 0
    for s in range(0, 25):
        data_points = assign_dp_to_clusters(centroids, data_points, is_tweet)
        clusters = group_by_clusters(data_points)
        if is_tweet:
            pseudo_centroids = recompute_centroids_tweet(clusters)
        else:
            pseudo_centroids = recompute_centroids(clusters)
        if utilities.check_equality(centroids, pseudo_centroids, is_tweet):
            break
        else:
            centroids = pseudo_centroids

    print "K-means converged at: ", s, "th iteration", "for k: ", k
    return centroids, group_by_clusters(data_points)


def get_initial_centroids(data_points, k):
    seeds = random.sample(range(1, len(data_points)), k)
    centroids = []
    # initialize seeds
    j = k
    for i in seeds:
        data_points[i].cluster = j
        j -= 1
        centroids.append(data_points[i])
    return centroids


def get_initial_centroids_for_tweet(k, file_path, tweets):
    f = open(file_path)
    j = k
    lines = f.readlines()
    centroids = []
    for line in lines:
        line = line.replace(",", "").strip()
        for i in tweets:
            if i.id_str == line:
                i.cluster = j
                centroids.append(i)
                j -= 1
        if j == 0:
            break
    return centroids


def recompute_centroids(clusters):
    centroids = []
    for i in clusters.keys():
        val = clusters[i]
        sumx = 0.0
        sumy = 0.0
        for dp in val:
            sumx = sumx + dp.x
            sumy = sumy + dp.y
        size = (len(val) * 1.0)
        newdp = DataPoint(-1, round(sumx / size, 3), round(sumy / size, 3))
        newdp.cluster = i
        centroids.append(newdp)

    return centroids


def recompute_centroids_tweet(clusters):
    centroid_with_cluster_label = {}
    for tweet_list in clusters.values():
        min_dist = 999
        for tweetA in tweet_list:
            sum_of_tweet_distances = 0
            for tweetB in tweet_list:
                sum_of_tweet_distances += jaccard(tweetA, tweetB)
            if sum_of_tweet_distances < min_dist:
                centroid_with_cluster_label[tweetA.cluster] = tweetA
    return centroid_with_cluster_label.values()


def assign_dp_to_clusters(centroids, data_points, is_tweet):
    for dp in data_points:
        if dp not in centroids:
            min_dist = 999
            for centroid in centroids:
                if is_tweet:
                    new_dist = jaccard(centroid, dp)
                else:
                    new_dist = euclidean(centroid, dp)
                if new_dist < min_dist:
                    min_dist = new_dist
                    dp.cluster = centroid.cluster
    return data_points


def euclidean(dp1, dp2):
    dist = math.sqrt((dp1.x - dp2.x) ** 2 + (dp1.y - dp2.y) ** 2)
    return dist


def jaccard(tweeta, tweetb):
    l_tweeta = tweeta.text.split(" ")
    l_tweetb = tweetb.text.split(" ")
    set_a = set(l_tweeta)
    set_b = set(l_tweetb)

    common_words = len(set_a.intersection(set_b))
    all_words = len(set_a.union(set_b))
    dist = 1 - (common_words / (all_words * 1.0))
    return dist


def group_by_clusters(data_points):
    clusters = collections.defaultdict(list)
    for dp in data_points:
        clusters[dp.cluster].append(dp)
    dict(clusters)
    return clusters


def print_clusters(clusters):
    for k in clusters:
        print k, ":",
        for i in clusters[k]:
            print i.label


def validate_clusters(centroids, clusters, is_tweet):
    i = 1
    ss_error = 0
    for centroid in centroids:
        for point in clusters[i]:
            if is_tweet:
                d = jaccard(centroid, point) ** 2
            else:
                d = euclidean(centroid, point) ** 2
            ss_error += d
        i += 1
    return ss_error
