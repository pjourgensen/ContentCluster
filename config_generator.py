'''
This script can be used to generate config files for all other python scripts used in this project.
The script is interactive.
'''

import re
import json

file_pattern = re.compile(r"[a-zA-Z]:\\((?:[a-zA-Z0-9() ]*\\)*).*")

#helper method to retrieve Boolean user input
def get_bool (prompt):
    while True:
        try:
            t = {"y": True,"n": False}
            return t[input(prompt).lower()]
        except KeyError:
            print ("Invalid input! Please enter Y or N!")
            
#helper method to retrieve integer user input
def get_int (prompt):
    while True:
        try:
            check = input(prompt)
            return int(check)
        except Exception:
            print ("Invalid input! Please enter an integer!")
            
#helper method to retrieve float user input
def get_float (prompt):
    while True:
        try:
            check = input(prompt)
            return float(check)
        except Exception:
            print ("Invalid input! Please enter a number!")

#helper method to retrieve Boolean user input
def get_file_path (prompt):
    while True:
        try:
            path = input(prompt)
            check = file_pattern.match(path)
            if check is None:
                m = get_bool("The file path you have entered did not match the Windows file path regex. Is this OK? (Y/N) ")
                if m == False:
                    raise KeyError()
            return path
        except KeyError:
            print ("Invalid input! Please enter a valid file path!")
            
#helper method to retrieve clustering algorithm
def get_algorithm (prompt, need_options=True):
    while True:
        t = {"kmeans": True}
        a = input(prompt).lower()
        if a in t:
            if need_options == True:
                return (a, get_alg_options(a))
            else:
                return (a, None)
        else:
            print ("Invalid algorithm name!")
            
#helper method to retrieve mapping cost function
def get_cost_function (prompt, need_options=True):
    while True:
        t = {"directdiff": True}
        a = input(prompt).lower()
        if a in t:
            if need_options == True:
                return (a, get_alg_options(a))
            else:
                return (a, None)
        else:
            print ("Invalid cost function name!")
        
                
#helper method to retrieve algorithm options
def get_alg_options(alg_name):
    output = {}
    if alg_name == "kmeans":
        output["minK"] = get_int("Please enter a minimum k value: ")
        output["maxK"] = get_int("Please enter a maximum k value: ")
        output["costFunc"] = input("Please enter the name of the cost function to use: ")
        output["meanFunc"] = input("Please enter the name of the mean function to use: ")
        output["errorFunc"] = input("Please enter the name of the error function to use: ")
        if output["errorFunc"] == "diffError":
            output["intraScale"] = get_float("Please enter a scale factor for within cluster error: ")
            output["interScale"] = get_float("Please enter a scale factor for cross cluster error: ")
        elif "clusterError" in output["errorFunc"]:
            output["clusterPenalty"] = get_float("Please enter a penalty factor for large/small clusters: ")
    elif alg_name == "directdiff":
        output["scale"] = get_float("Please enter a scale factor for mapping error: ")
    return output

            
#genre_parse.py
q1 = get_bool("Would you like to generate a config file for genre_parse.py (Y/N)? ")
if q1 == True:
    csv_path = get_file_path("Please enter the path to the .csv data file: ")
    out_path = get_file_path("Please enter a path for the output .json file: ")
    
    o = {}
    o["csv"] = csv_path
    o["output"] = out_path
    
    with open("genre_parse_config.json", 'w') as outfile:
        json.dump(o, outfile)
        
#movie_category.py
q2 = get_bool("Would you like to generate a config file for movie_category.py (Y/N)? ")
if q2 == True:
    csv_path = get_file_path("Please enter the path to the .csv data file: ")
    genre_path = get_file_path("Please enter a path for the genre .json file: ")
    out_path = get_file_path("Please enter a path for the output .json file: ")
    
    o = {}
    o["csv"] = csv_path
    o["genre"] = genre_path
    o["output"] = out_path
    
    with open("movie_category_config.json", 'w') as outfile:
        json.dump(o, outfile)
        
#movie_cluster.py
q3 = get_bool("Would you like to generate a config file for movie_cluster.py (Y/N)? ")
if q3 == True:
    data_path = get_file_path("Please enter the path to the input .json data file: ")
    out_path = get_file_path("Please enter the path for the output results .json data file: ")
    alg = get_algorithm("Which clustering algorithm would you like to use (kmeans): ")
    
    o = {}
    o["data_file_path"] = data_path
    o["output"] = out_path
    o["algorithm"] = alg[0]
    o["alg_options"] = alg[1]
    
    with open("movie_cluster_config.json", 'w') as outfile:
        json.dump(o, outfile)
        
#movie_summary.py
q4 = get_bool("Would you like to generate a config file for movie_summary.py (Y/N)? ")
if q4 == True:
    data_path = get_file_path("Please enter the path to the results .json file: ")
    genre_path = get_file_path("Please enter a path for the genre .json file: ")
    alg = get_algorithm("Which clustering algorithm was used to generate these results (kmeans): ", False)
    
    o = {}
    o["data_file_path"] = data_path
    o["genre_file_path"] = genre_path
    o["algorithm"] = alg[0]
    
    with open("movie_summary_config.json", 'w') as outfile:
        json.dump(o, outfile)
        
#merge_movie_data.py
q5 = get_bool("Would you like to generate a config file for merge_movie_data.py (Y/N)? ")
if q5 == True:
    csv_path_nf = get_file_path("Please enter the path to the .csv nf data file: ")
    csv_path_mdb = get_file_path("Please enter a path for the .csv mdb data file: ")
    out_path = get_file_path("Please enter a path for the output .csv file: ")
    
    o = {}
    o["nf"] = csv_path_nf
    o["mdb"] = csv_path_mdb
    o["output"] = out_path
    
    with open("merge_movie_data_config.json", 'w') as outfile:
        json.dump(o, outfile)

#load_custs.py
q6 = get_bool("Would you like to generate a config file for load_custs.py (Y/N)? ")
if q6 == True:
    csv_path_merged = get_file_path("Please enter the path to the .csv merged data file: ")
    cust_data1_path = get_file_path("Please enter a path for the .txt data file: ")
    cust_data2_path = get_file_path("Please enter a path for the .txt data file: ")
    cust_data3_path = get_file_path("Please enter a path for the .txt data file: ")
    cust_data4_path = get_file_path("Please enter a path for the .txt data file: ")
    out_path = get_file_path("Please enter a path for the output .json file: ")
    
    o = {}
    o["mmp"] = csv_path_merged
    o["cust1"] = cust_data1_path
    o["cust2"] = cust_data2_path
    o["cust3"] = cust_data3_path
    o["cust4"] = cust_data4_path
    o["output"] = out_path
    
    with open("load_custs_config.json", 'w') as outfile:
        json.dump(o, outfile)
        
#map_custs_movies.py
q7 = get_bool("Would you like to generate a config file for map_custs_movies.py (Y/N)? ")
if q7 == True:
    cust_clusters = get_file_path("Please enter the path for the customer clustering results .json file: ")
    movie_clusters = get_file_path("Please enter a path for the movie clustering results .json file: ")
    cost_func = get_cost_function("Which cost function would you like to use? ", True)
    out_path = get_file_path("Please enter a path for the output .json file: ")
    
    o = {}
    o["customers"] = cust_clusters
    o["movies"] = movie_clusters
    o["costFunc"] = cost_func[0]
    o["costFuncOpts"] = cost_func[1]
    o["output"] = out_path
    
    with open("map_custs_movies_config.json", 'w') as outfile:
        json.dump(o, outfile)
        
#cluster_results_merge.py
q8 = get_bool("Would you like to generate a config file for cluster_results_merge.py (Y/N)? ")
if q8 == True:
    result_files = []
    c = True
    while c == True:
        r = get_file_path("Please enter the path for a clustering result .json file to merge: ")
        result_files.append(r)
        c = get_bool("Would you like to merge another result (Y/N)? ")
    out_path = get_file_path("Please enter a path for the output .json file: ")
    
    o = {}
    o["resultFiles"] = result_files
    o["output"] = out_path
    
    with open("cluster_results_merge_config.json", 'w') as outfile:
        json.dump(o, outfile)