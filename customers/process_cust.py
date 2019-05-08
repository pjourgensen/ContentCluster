#Generates dataframe of customers and their "ratings" of each genre

import os
import csv
import json
import pandas as pd
import numpy as np

def extract_mids_ratings(cust_id):
    num_movies = len(cust_dict[cust_id])
    cust_mids = []
    cust_ratings = np.zeros(num_movies)
    for i in range(num_movies):
        curr_tuple = cust_dict[cust_id][i]
        curr_mid, curr_rating = curr_tuple[0], curr_tuple[1]
        cust_mids.append(curr_mid)
        cust_ratings[i] = curr_rating
    return cust_mids, cust_ratings

def transform_ratings(ratings):
    tfm_ratings = (ratings - ratings.mean())/ratings.std()
    tfm_ratings = np.exp(tfm_ratings)
    return tfm_ratings

#load config
movie_info_file_path = ""
cust_data_file_path = ""
output_file_path = ""
with open('../config/process_cust_config.json') as json_file:
    data = json.load(json_file)
    movie_info_file_path = data["mi"]
    cust_data_file_path = data["cd"]
    output_file_path = data["out"]
    
#generate merged movie dataframe
movie_info = pd.read_csv(movie_info_file_path)

#generate customer dictionary
json_file = json.open(cust_data_file_path)
json_list = json_file.read()
cust_data = json_list[0]

#generate genre dictionary
genre_dict = {}
unique_genres = []
for i in range(len(movie_info)):
    mid = movie_info.loc[i,'Movie_Id']
    genres = movie_info.loc[i,'genres'].lower().split('|')
    for j in genres:
        if j not in unique_genres:
            unique_genres.append(j)
    genre_dict[mid] = genres
    
#initialize customer-genre dataframe
cust_df = pd.DataFrame(data = np.zeros((len(cust_data),len(unique_genres))),
                       index = cust_data.keys(), columns= unique_genres)

#process each custmer - 
#split into movie list and ratings array 
#normalize and exp ratings
#scan through each movie of each customer and add appropriate score to appropriate genre
for i in cust_data.keys():
    mids, rats = extract_mids_ratings(i)
    rats = transform_ratings(rats)
    for j in range(len(mids)):
        gs = genre_dict[mids[j]]
        for k in gs:
            cust_df.loc[i,k] += rats[j]

cust_df.to_csv(output_file_path, index=False, encoding="utf-8")
