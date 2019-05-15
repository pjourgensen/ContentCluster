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
    scaler_st = StandardScaler()
    ratings = scaler_st.fit_transform(ratings)
    ratings = np.exp(ratings)
    ratings = ratings/len(ratings)
    return ratings

#load config
movie_info_file_path = ""
cust_data_file_path = ""
genre_order_file_path = ""
output_file_path = ""
with open('../config/process_cust_config.json') as json_file:
    data = json.load(json_file)
    movie_info_file_path = data["mi"]
    cust_data_file_path = data["cd"]
    genre_order_file_path = data["go"]
    output_file_path = data["out"]

#generate merged movie dataframe
movie_info = pd.read_csv(movie_info_file_path, header=None, index_col=False)

#generate customer dictionary
with open(cust_data_file_path, 'r') as json_file:
    cust_data = json.load(json_file)


#generate genre dictionary
genre_dict = {}
unique_genres = []
for i in range(len(movie_info)):
    mid = movie_info.iloc[i,1]
    genres = movie_info.iloc[i,7].lower().split('|')
    for j in genres:
        if j not in unique_genres:
            unique_genres.append(j)
    genre_dict[mid] = genres

#initialize customer-genre dataframe
cust_df = pd.DataFrame(data = np.zeros((len(cust_data),len(unique_genres))),
                       index = cust_data.keys(), columns= unique_genres)

#process each custmer -
for i in cust_data.keys():
    mids, rats = extract_mids_ratings(i)
    rats = transform_ratings(rats)
    for j in range(len(mids)):
        movie = mids[j]
        for k in genre_dict[movie]:
            cust_df.loc[i,k] += rats[j]

#make sure column order matches that of movie clustering
with open(genre_order_file_path) as json_file:
    genre_order = json.load(json_file)

cust_df.columns = ['documentary', 'animation', 'comedy', 'thriller', 'mystery', 'romance',
       'horror', 'sciencefiction', 'action', 'crime', 'drama', 'music',
       'foreign', 'adventure', 'history', 'tvmovie', 'family', 'fantasy',
       'war', 'western']

cust_df = cust_df[genre_order]

#Convert to dictionary to be used in clustering algorithm
cd = []
for i in cust_df.index:
    datapoint = {}
    datapoint['id'] = i
    datapoint['genres'] = cust_df.loc[i,:].tolist()
    cd.append(datapoint)

with open(output_file_path, 'w') as outfile:
    json.dump(cd, outfile)
