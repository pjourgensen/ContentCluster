'''
Config object for genre_parse python script
'''

class Config:
    def __init__(self):
        self.csv_file_path = r'C:\git\ContentCluster\data\350-000-movies-from-themoviedborg\AllMoviesDetailsCleaned.csv'
        self.output_file_path = r'C:\git\ContentCluster\data\genres.json'