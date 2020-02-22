import sys
import random

# Opening data file and converting it to list of list
datafile = open(sys.argv[1])
data = []
line = datafile.readline()

while(line != ''):
    array = line.split()
    array_list = []
    for i in range(len(array)):
        array_list.append(float(array[i]))
    # array_list.append(1)
    data.append(array_list)
    line = datafile.readline()

row = len(data)
col = len(data[0])
datafile.close()

# aSSIGNING THE VALUE OF CLUSTERS
k = int(sys.argv[2])


def random_clusters(data, k):
    clusters = {}

    for i in range(0, k):
        clusters[i] = []
    for point in data:
        arg = random.randint(0, k-1)
        clusters[arg].append(point)

    return clusters


def compute_mean(clusters):

    centroid = {}

    for C in clusters.keys():

        cluster_list = list(zip(*clusters[C]))

        center_point = []

        for colm in cluster_list:
            mean = sum(colm)/len(colm)
            center_point.append(mean)

        centroid[C] = center_point

    return centroid


def obj_fn(clusters, centroids):

    obj = 0

    for C in clusters.keys():

        for point in clusters[C]:

            for val, center in zip(point, centroids[C]):
                obj += (val - center) ** 2

    return obj


def final_clusters(data, centroids):

    clusters = {}

    for key in centroids.keys():
        clusters[key] = []

    for val in data:

        dist_list = []

        for k, centroid in centroids.items():
            eucli_dist = 0
            for a, b in zip(val, centroid):
                eucli_dist += (a - b) ** 2

            eucli_dist = eucli_dist ** 0.5
            dist_list.append(eucli_dist)

        min_dist = min(dist_list)
        cluster_num = dist_list.index(min_dist)
        clusters[cluster_num].append(val)

    return clusters


theta = 0.001
error = 1
clusters = random_clusters(data, k)
centroid = compute_mean(clusters)
prev_obj = obj_fn(clusters, centroid)
while (error > theta):
    recompute_clusters = final_clusters(data, centroid)

    recompute_centroid = compute_mean(recompute_clusters)

    new_obj = obj_fn(recompute_clusters, recompute_centroid)

    error = prev_obj - new_obj

    prev_obj = new_obj

final_cluster = recompute_clusters

predictions = {}
for cluster_lab, points in final_cluster.items():
    for point in points:
        index = data.index(point)
        predictions[index] = cluster_lab
for i, j in sorted(predictions.items()):
    print(j, i)
