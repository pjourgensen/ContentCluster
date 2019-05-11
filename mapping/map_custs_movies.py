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

#### TODO: once we know what the customer clusters look like ####

func_list = {}

### General Helper Methods

#write formatted results of ideal mapping
#TODO: how to express mapped clusters?
#TODO: what other info to include?
def write_mapping_results(results, output_path):
    output = {}
    
    with open(output_path, 'w') as outfile:
        json.dump(output, outfile)
        
### Main Execution Methods ###

#find the best movie cluster for each customer cluster
#by applying the cost function specified in the config
def evaluate_mapping(cust_cluster_result, movie_cluster_result):
    results = {"total_error": None, "mappings": {}}
    cust_count = 0
    for cust_cluster in cust_cluster_result: #TODO: fix cust_cluster
        min_error = None
        best_mapping = None
        for movie_cluster in movie_cluster_result["groupings"]:
            cost = cost_func(cust_cluster, movie_cluster["mean"]) #TODO: fix cust_cluster
            if (min_error is None) or (cost < min_error):
                min_error = cost
                best_mapping = movie_cluster["groupNumber"]
        results["total_error"] = results["total_error"] + min_cost
        results["mappings"][cust_count] = {"movie_cluster": best_mapping, "error": min_cost}
        cust_count = cust_count + 1
    return results
    

#load config
customer_cluster_file_path = ""
movie_cluster_file_path = ""
output_path = ""
cost_func = None
cost_func_options = {}
with open('../config/cluster_mapping.json') as json_file:  
    data = json.load(json_file)
    customer_cluster_file_path = data["customers"]
    movie_cluster_file_path = data["movies"]
    cost_func = data["costFunc"]
    cost_func_options = data["costFuncOpts"]

#load clustering results
cust_clusters = None
with open(customer_cluster_file_path) as json_file:
    cust_clusters = json.load(json_file)
    #TODO: extract array of cluster results
    
movie_clusters = None
with open(movie_cluster_file_path) as json_file:
    movie_clusters = json.load(json_file)
    movie_clusters = movie_clusters["results"]

cost_func = func_list[cost_func]
#TODO: bind arguments as a partial based on cost function (from cost_func_options)

min_err = None
best_mapping = None
all_results = {}
for cust_cluster_result in cust_clusters:
    for movie_cluster_result in movie_clusters:
        cost = evaluate_mapping(cust_cluster_result, movie_cluster_result)
        m = "TODO" + ":" + movie_cluster_result["kValue"] #TODO: set m to be some unique identifier of the given mapping test
        if (min_err is None) or (cost["total_error"] < min_err):
            min_err = cost["total_error"]
            best_mapping = m
        all_results[m] = cost
        
write_mapping_results(all_results, min_err, best_mapping, output_path)