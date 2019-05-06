'''
This script uses a generated movie data set (from a .json file) and runs a specified clustering algorithm on it
Results can be fed into some visualization library
'''

#imports
import sys
import json
import time
from functools import partial

### Input functions for clustering algorithms ###

#### KMeans input functions ####

#cost function => directly compare each genre bit
def direct_compare(datapoint, mean):
    cost = 0
    for x in range(len(datapoint["genres"])):
        if not datapoint["genres"][x] == mean[x]:
            cost = cost + 1
    return cost

#cost function => compute positive difference of each genre bit
def direct_diff(datapoint, mean):
    cost = 0
    for x in range(len(datapoint["genres"])):
        cost = cost + (abs(datapoint["genres"][x] - mean[x]))
    return cost

#mean function => simple arithmetic mean for each genre bit
def arith_mean(datapoints, default_length=20):
    mean = []
    if len(datapoints) == 0:
        for x in range(default_length):
            mean.append(0)
        return mean
    else:
        length = len(datapoints[0]["genres"])
        for x in range(length):
            total = 0
            for datapoint in datapoints:
                total = total + datapoint["genres"][x]
            mean.append(total / len(datapoints))
        return mean
    
#error function => only consider error within each cluster
def intra_error_only(intra_error, inter_error=None, cluster_info=None):
    return intra_error

#error function => consider both error with each cluster and error across clusters
#within => want to be small
#across => want to be large
def diff_error(intra_scale, inter_scale, intra_error, inter_error, cluster_info=None):
    return (intra_scale * intra_error) + (inter_scale * inter_error)

#error function => consider both error within each cluster and cluster size
#within => want to be small
#size => want to be close to some ideal size
def intra_cluster_size(penalty, intra_error, inter_error, cluster_info):
    return intra_error + pow(cluster_info[0] - cluster_info[1], 2) * penalty

func_list = {"directCompare": direct_compare, "directDiff": direct_diff, "arithMean": arith_mean, "intraErrorOnly": intra_error_only, "diffError": diff_error, "clusterError": intra_cluster_size}

### General Helper Methods

#write formatted results of kmeans clustering analysis
def write_kmeans_results(results, dataset_size, start_time, end_time, output_path):
    output = {"dataset_size": dataset_size, "start_time": start_time, "end_time": end_time, "results": []}
    for key,value in results.items():
        tmp = {"kValue": key, "totalError": value[0], "groupings": []}
        for k,v in value[1].items():
            tmp["groupings"].append({"groupNumber": k, "mean": v["mean"], "intraError": v["intra_error"], "interError": v["inter_error"], "clusterSize": len(v["datapoints"])})
        output["results"].append(tmp)
    
    with open(output_path, 'w') as outfile:
        json.dump(output, outfile)
    

#load config
data_file_path = ""
output_path = ""
algorithm = ""
alg_options = {}
with open('../config/movie_cluster_config.json') as json_file:  
    data = json.load(json_file)
    data_file_path = data["data_file_path"]
    output_path = data["output"]
    algorithm = data["algorithm"]
    alg_options = data["alg_options"]
    
#import kmeans library
sys.path.insert(0, r'..\utils')
from kmeans import KMeans

dataset = None
with open(data_file_path) as json_file:
    dataset = json.load(json_file)

start_time = time.time()
    
if algorithm == "kmeans":
    results = {}
    cost_func = func_list[alg_options["costFunc"]]
    mean_func = func_list[alg_options["meanFunc"]]
    
    error_func = None
    if alg_options["errorFunc"] == "diffError":
        intra_scale = alg_options["intraScale"] if "intraScale" in alg_options else 1
        inter_scale = alg_options["interScale"] if "interScale" in alg_options else -1
        error_func = partial(func_list[alg_options["errorFunc"]], intra_scale, inter_scale)
    elif alg_options["errorFunc"] == "clusterError":
        penalty = alg_options["clusterPenalty"] if "clusterPenalty" in alg_options else 1
        error_func = partial(func_list[alg_options["errorFunc"]], penalty)
    else:
        error_func = func_list[alg_options["errorFunc"]]
    
    for k in range(alg_options["minK"], alg_options["maxK"] + 1):
        r = KMeans(dataset, k, cost_func, mean_func, error_func)
        results[k] = r.run()
    
    end_time = time.time()
    write_kmeans_results(results, len(dataset), start_time, end_time, output_path)
else:
    print ("The algorithm specified has not been implemented yet!")