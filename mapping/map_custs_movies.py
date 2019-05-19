'''
This script uses clustered customers and movies and performs a brute-force search such that
the best mapping of customers to movies is identified per some cost function
'''

#imports
import sys
import json
import scipy.stats
from functools import partial

### Possible cost functions to evaluate mappings ###

#cost function for deviation between customer and movie cluster
#linearly scale the sum of the positive differences between each vector component
def direct_diff(scale, cust_mean, movie_mean):
    error = 0
    ran = len(cust_mean) if len(cust_mean) <= len(movie_mean) else len(movie_mean)
    for x in range(ran):
        d = abs(cust_mean[x] - movie_mean[x])
        error = error + d
    return (error * scale)

func_list = {"directdiff": direct_diff}

### General Helper Methods

#write formatted results of ideal mapping
def write_mapping_results(results, min_error, best_mapping, output_path):
    output = {"bestMapping": best_mapping, "minError": min_error, "results": results}
    
    with open(output_path, 'w') as outfile:
        json.dump(output, outfile)
        
### Main Execution Methods ###

#find the best movie cluster for each customer cluster
#by applying the cost function specified in the config
def evaluate_mapping(cust_cluster_result, movie_cluster_result):
    results = {"total_error": None, "normalized_error": None, "mappings": {}}
    for cust_cluster in cust_cluster_result["groupings"]:
        min_error = None
        best_mapping = None
        for movie_cluster in movie_cluster_result["groupings"]:
            cost = cost_func(cust_cluster["mean"], movie_cluster["mean"])
            if (min_error is None) or (cost < min_error):
                min_error = cost
                best_mapping = movie_cluster["groupNumber"]
        results["total_error"] = results["total_error"] + min_error if not results["total_error"] is None else min_error 
        results["mappings"][cust_cluster["groupNumber"]] = {"movie_cluster": best_mapping, "error": min_error}
    results["normalized_error"] = results["total_error"] / cust_cluster_result["kValue"]
    return results
    

#load config
customer_cluster_file_path = ""
movie_cluster_file_path = ""
output_path = ""
cost_func = None
cost_func_options = {}
with open('../config/map_custs_movies_config.json') as json_file:  
    data = json.load(json_file)
    customer_cluster_file_path = data["customers"]
    movie_cluster_file_path = data["movies"]
    cost_func = data["costFunc"]
    cost_func_options = data["costFuncOpts"]
    output_path = data["output"]

#load clustering results
cust_clusters = None
with open(customer_cluster_file_path) as json_file:
    cust_clusters = json.load(json_file)
    cust_clusters = cust_clusters["results"]
    
movie_clusters = None
with open(movie_cluster_file_path) as json_file:
    movie_clusters = json.load(json_file)
    movie_clusters = movie_clusters["results"]

cost_func = func_list[cost_func]
if cost_func == direct_diff:
    cost_func = partial(cost_func, cost_func_options["scale"])

min_err = None
best_mapping = None
all_results = []
for cust_cluster_result in cust_clusters:
    for movie_cluster_result in movie_clusters:
        cost = evaluate_mapping(cust_cluster_result, movie_cluster_result)
        m = {"customerKValue": cust_cluster_result["kValue"], "movieKValue": movie_cluster_result["kValue"]}
        if (min_err is None) or (cost["normalized_error"] < min_err):
            min_err = cost["normalized_error"]
            best_mapping = m
        all_results.append({"customerKValue": cust_cluster_result["kValue"], "movieKValue": movie_cluster_result["kValue"], "analysis": cost})
        
write_mapping_results(all_results, min_err, best_mapping, output_path)