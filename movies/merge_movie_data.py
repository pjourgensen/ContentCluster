import os
import csv
import json
import pandas as pd

#load config
nf_file_path = ""
mdb_file_path = ""
output_file_path = ""
with open('../config/merge_movie_data_config.json') as json_file:
    data = json.load(json_file)
    nf_file_path = data["nf"]
    mdb_file_path = data["mdb"]
    output_file_path = data["output"]

#Read NF data
nf_df = pd.read_csv(nf_file_path, encoding="ISO-8859-1", header=None, names=['Movie_Id', 'Year', 'Name'])

#Read mdb data
mdb_df = pd.read_csv(mdb_file_path, sep=";")

#Normalize title
nf_df['title'] = nf_df['Name'].apply(lambda x: x.lower())
mdb_df['title'] = mdb_df['original_title'].apply(lambda x: str(x).lower())

#Join datasets on "title"
movies_df = pd.merge(nf_df, mdb_df, on='title', how='inner')

#Check year
movies_df['release_date'].fillna('0000', inplace=True)
movies_df['release_year'] = movies_df['release_date'].apply(lambda x: int(x[:4]) if '-'in x else int(x[-4:]))
to_drop = []
for i in range(len(movies_df)):
    if (movies_df.loc[i,'Year'] != movies_df.loc[i,'release_year']) and (movies_df.loc[i,'Year'] - 1 != movies_df.loc[i,'release_year']):
        to_drop.append(i)
movies_df.drop(to_drop,inplace=True)

#Check id
movies_df.sort_values('Movie_Id',inplace=True)
movies_df.reset_index(inplace=True)
to_drop = []
for i in range(1,len(movies_df)):
    if (movies_df.loc[i,'Movie_Id'] == movies_df.loc[i-1,'Movie_Id']):
        to_drop.append(i)
movies_df.drop(to_drop,inplace=True)

#Drop movies that don't have genre data
movies_df.dropna(subset=['genres'],inplace=True)

#Write to output file
movies_df.to_csv(output_file_path, index=False, encoding="utf-8")
