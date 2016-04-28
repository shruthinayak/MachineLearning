import sys
import utilities
import core_functions

# ./k-means	<numberOfClusters> <input-file-name> <output-file-name>
if len(sys.argv) == 4:
    k = int(sys.argv[1])
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    values = utilities.read_from_file(input_file)
    datapoints = core_functions.create_datapoints(values)
    centroids, clusters = core_functions.kmeans(k, datapoints, False)
    sse = core_functions.validate_clusters(centroids, clusters, False)

    with open(output_file, "a") as myfile:
        for k in clusters:
            myfile.write(str(k) + ":")
            for i in clusters[k]:
                myfile.write(str(i.label)+", ")
            myfile.write("\n")
else:
    print "Usage: "
    print "python kmeans.py <number_of_clusters> <input_file> <output_file>"
