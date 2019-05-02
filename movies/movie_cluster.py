'''
This script uses a generated movie data set (from a .json file) and runs a specified clustering algorithm on it
Results can be fed into some visualization library
'''

#imports
import sys
import json

#Input functions for clustering algorithms

def direct_compare(datapoint, mean):
    cost = 0
    for x in range(len(datapoint["genres"])):
        if not datapoint["genres"][x] == mean[x]:
            cost = cost + 1
    return cost

def direct_diff(datapoint, mean):
    cost = 0
    for x in range(len(datapoint["genres"])):
        cost = cost + (abs(datapoint["genres"][x] - mean[x]))
    return cost

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
    
def intra_error_only(intra_error, inter_error):
    return intra_error

def diff_error(intra_error, inter_error):
    return intra_error - inter_error

func_list = {"directCompare": direct_compare, "directDiff": direct_diff, "arithMean": arith_mean, "intraErrorOnly": intra_error_only, "diffError": diff_error}

#load config
data_file_path = ""
algorithm = ""
alg_options = {}
with open('../config/movie_cluster_config.json') as json_file:  
    data = json.load(json_file)
    data_file_path = data["data_file_path"]
    algorithm = data["algorithm"]
    alg_options = data["alg_options"]
    
#import kmeans library
sys.path.insert(0, r'..\utils')
from kmeans import KMeans

dataset = None
with open(data_file_path) as json_file:
    dataset = json.load(json_file)

if algorithm == "kmeans":
    results = {}
    cost_func = func_list[alg_options["costFunc"]]
    mean_func = func_list[alg_options["meanFunc"]]
    error_func = func_list[alg_options["errorFunc"]]
    for k in range(alg_options["minK"], alg_options["maxK"] + 1):
        r = KMeans(dataset, k, cost_func, mean_func, error_func)
        results[k] = r.run()
else:
    print ("The algorithm specified has not been implemented yet!")