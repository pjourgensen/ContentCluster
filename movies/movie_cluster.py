'''
This script uses a generated movie data set (from a .json file) and runs a specified clustering algorithm on it
Results can be fed into some visualization library
'''

#imports
import os
import json

#Input functions for clustering algorithms

def direct_compare(datapoint, mean):
    cost = 0
    for x in range(len(datapoint)):
        if not datapoint[x] == mean[x]:
            cost = cost + 1
    return cost

def direct_diff(datapoint, mean):
    cost = 0
    for x in range(len(datapoint)):
        cost = cost + (abs(datapoint[x] - mean[x]))
    return cost

def arith_mean(datapoints, default_length=25):
    mean = []
    if len(datapoints) == 0:
        for x in range(default_length):
            mean.append(0)
        return mean
    else:
        length = len(datapoints[0])
        for x in range(length):
            total = 0
            for datapoint in datapoints:
                total = total + datapoint[x]
            mean.append(total / len(datapoints))
        return mean
    
def intra_error_only(intra_error, inter_error):
    return intra_error

def diff_error(intra_error, inter_error):
    return intra_error - inter_error

func_list = {"directCompare": direct_compare, "directDiff": direct_diff, "arithMean": arith_mean, "intraErrorOnly": intra_error_only, "interErrorOnly": inter_error_only}

#load config
data_file_path = ""
algorithm = ""
alg_options = {}
with open('../config/movie_category_config.json') as json_file:  
    data = json.load(json_file)
    data_file_path = data["data"]
    algorithm = data["algorithm"]
    alg_options = data["alg_options"]
    
#import kmeans library
sys.path.insert(0, r'..\utils')
from kmeans import KMeans

dataset = json.loads(data_file_path)

if algorithm == "kmeans":
    results = {}
    cost_func = func_list[alg_options["kmeans"]["costFunc"]]
    mean_func = func_list[alg_options["kmeans"]["meanFunc"]]
    error_func = func_list[alg_options["kmeans"]["errorFunc"]]
    for k in xrange(alg_options["kmeans"]["minK"], alg_options["kmeans"]["maxK"]):
        run = KMeans(dataset, k, cost_func, mean_func, error_func)
        results[k] = run
else:
    print ("The algorithm specified has not been implemented yet!")