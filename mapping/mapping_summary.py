'''
This script takes a mapping result and outputs a reader-friendly ranking of all mappings.
'''

#imports
import os
import json

def sort_results(a):
    return a["error"]

#load config
result_file_path = ""
with open('../config/mapping_summary_config.json') as json_file:  
    data = json.load(json_file)
    result_file_path = data["resultFile"]

results = []
with open(result_file_path) as json_file:  
    d = json.load(json_file)
    results = d["results"]
    
unsorted = []
for x in results:
    unsorted.append({"customerKValue": x["customerKValue"], "movieKValue": x["movieKValue"], "error": x["analysis"]["normalized_error"]})
    
unsorted.sort(key=sort_results)
sorted_results = unsorted

for y in range(len(sorted_results)):
    msg = "Ranking: " + str(y+1) + "\tCustomer K-Value: " + str(sorted_results[y]["customerKValue"]) + "\tMovie K-Value: " + str(sorted_results[y]["movieKValue"]) + "\tNormalized Error: " + str(sorted_results[y]["error"])
    print (msg)