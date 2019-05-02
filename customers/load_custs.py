import os
import json
import csv 

def extract_movie_ids(file_path):
    output = set()
    with open(file_path, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            output.add(int(row[1]))
    return output

def read_nf_data(file_path,cust_dict,movie_set):
    movie_id = -1
    include_movie = False
    with open(file_path) as fp:
        line = fp.readline()
        while line:
            parsed_line = [x.strip() for x in line.split(',')]
            if len(parsed_line) == 1:
                movie_id = int(parsed_line[0][:-1])
                if movie_id in movie_set:
                    include_movie = True
                else:
                    include_movie = False
            elif include_movie:
                cust_id = parsed_line[0]
                if cust_id not in cust_dict:
                    cust_dict[cust_id] = []
                cust_rating = int(parsed_line[1])
                cust_dict[cust_id].append((movie_id,cust_rating))
            line = fp.readline()
    return cust_dict

#load config
merge_movie_path = ""
cust_data1_path = ""
cust_data2_path = ""
cust_data3_path = ""
cust_data4_path = ""
output_file_path = ""
with open('../config/load_custs_config.json') as json_file:  
    data = json.load(json_file)
    merge_movie_path = data["mmp"]
    cust_data1_path = data["cust1"]
    cust_data2_path = data["cust2"]
    cust_data3_path = data["cust3"]
    cust_data4_path = data["cust4"]
    output_file_path = data["output"]

movie_ids = extract_movie_ids(merge_movie_path)

cust_dict = {}
cust_dict = read_nf_data(cust_data1_path,cust_dict,movie_ids)
cust_dict = read_nf_data(cust_data2_path,cust_dict,movie_ids)
cust_dict = read_nf_data(cust_data3_path,cust_dict,movie_ids)
cust_dict = read_nf_data(cust_data4_path,cust_dict,movie_ids)

with open(output_file_path,'w') as outfile:
    json.dump(cust_dict,outfile)
