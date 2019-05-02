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

#helper method to retrieve Boolean user input
def get_file_path (prompt):
    while True:
        try:
            path = input(prompt)
            check = file_pattern.match(path)
            if check is None:
                raise KeyError()
            return path
        except KeyError:
            print ("Invalid input! Please enter a valid file path!")

            
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
        
#merge_movie_data.py
q3 = get_bool("Would you like to generate a config file for merge_movie_data.py (Y/N)? ")
if q3 == True:
    csv_path_nf = get_file_path("Please enter the path to the .csv nf data file: ")
    csv_path_mdb = get_file_path("Please enter a path for the .csv mdb data file: ")
    out_path = get_file_path("Please enter a path for the output .csv file: ")
    
    o = {}
    o["nf"] = csv_path_nf
    o["mdb"] = csv_path_mdb
    o["output"] = out_path
    
    with open("merge_movie_data_config.json", 'w') as outfile:
        json.dump(o, outfile)
