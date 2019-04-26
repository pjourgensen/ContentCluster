'''
This script reads raw movie data (in a .csv file) and extracts all genre information from that file
The output is a json file containing unique genres
'''

#imports
import os
import csv
import json

#load config
csv_file_path = ""
output_file_path = ""
with open('../config/genre_parse_config.json') as json_file:  
    data = json.load(json_file)
    csv_file_path = data["csv"]
    output_file_path = data["output"]

genres = {}

#read in CSV
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='\'')
    for row in reader:
        try:
            #extract genres
            gs = row[2].split('|')
            for g in gs:
                #clean up text and check for special cases
                g = g.lower().replace(" ", "")
                if g != "" and g != "genres":
                    #only capture unique genres
                    if not g in genres:
                        genres[g] = True
        except Exception as e:
            print (e)

#dump genres into output JSON file
o = []
for key, value in genres.items():
    o.append(key)
    
with open(output_file_path, 'w') as outfile:
    json.dump(o, outfile)