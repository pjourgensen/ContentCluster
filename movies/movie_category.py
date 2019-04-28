'''
This script reads raw movie data (in a .csv file) as well as a predefined set of genres
Outputs JSON where each movie has a bit vector corresponding to its genres per the predefined list
'''

#imports
import os
import csv
import json

genres = {}
movies = {}

#helper method to load predefined genres properly
def load_genres(file_path):
    output = {}
    count = 0
    with open(file_path) as json_file:  
        gs = json.load(json_file)
        for x in gs:
            output[x] = count
            count = count + 1
    return output

#helper method to initialize movie output object
def initialize_movie(movie_id, movie_name):
    if not movie_id in movies:
        movies[movie_id] = {}
        movies[movie_id]["name"] = movie_name
        movies[movie_id]["genres"] = []
        for x in range(len(genres.keys())):
            movies[movie_id]["genres"].append(0)

#load config
csv_file_path = ""
output_file_path = ""
genre_file_path = ""
with open('../config/movie_category_config.json') as json_file:  
    data = json.load(json_file)
    csv_file_path = data["csv"]
    output_file_path = data["output"]
    genre_file_path = data["genre"]

genres = load_genres(genre_file_path)

#read in CSV
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='\'')
    for row in reader:
        try:
            #extract movie relevant information
            gs = row[2].split('|')
            movie_name = row[5]
            movie_id = int(row[0])
            initialize_movie(movie_id, movie_name)
            for g in gs:
                #clean up text
                g = g.lower().replace(" ", "")
                if g in genres:
                    movies[movie_id]["genres"][genres[g]] = 1
        except Exception as e:
            print (e)
    
with open(output_file_path, 'w') as outfile:
    json.dump(movies, outfile)