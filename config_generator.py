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