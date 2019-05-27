'''
This script takes multiple clustering result .json files and merges them into a single file.
'''

#imports
import os
import json

#load config
result_file_paths = []
output_file_path = ""
with open('../config/cluster_results_merge_config.json') as json_file:  
    data = json.load(json_file)
    result_file_paths = data["resultFiles"]
    output_file_path = data["output"]

output = {"results": []}

for x in result_file_paths:
    with open(x) as json_file:  
        d = json.load(json_file)
        output["results"] = output["results"] + d["results"]
        
with open(output_file_path, 'w') as outfile:
    json.dump(output, outfile)