'''
This script implements K-Means Clustering using generic cost functions
'''

#imports
import random

class KMeans:
    def __init__(self, dataset, k, cost_func, mean_func, error_func):
        self.dataset = dataset
        self.k = k
        self.cost_func = cost_func
        self.mean_func = mean_func
        self.error_func = error_func
        
        self.means = []
        self.groupings = {}
        for x in range(k):
            self.groupings[k] = {"mean": None, "datapoints": [], "intra_error": None, "inter_error": None}
        
    #generate initial set of means
    #use a pseudorandom number generator for assignment
    def _initial_partition(self):
        for datapoint in self.dataset:
            assignment = random.randint(0, self.k)
            self.groupings[assignment]["datapoints"].append(datapoint)
            
    #find closest mean to given datapoint
    #group that datapoint per the closest mean
    def _find_best_grouping(self, datapoint):
        min_cost = None
        min_mean = None
        count = 0
        for mean in self.means:
            tmp_cost = self.cost_func(datapoint, mean)
            if min_cost is None or tmp_cost < min_cost:
                min_cost = tmp_cost
                min_mean = count
            count = count + 1
        self.groupings[min_mean]["datapoints"].append(datapoint)
        
    #compute the mean for a given cluster assignment
    #just wraps user-provided mean computation function
    def _compute_group_mean(self, group_id):
        self.groupings[group_id]["mean"] = self.mean_func(self.groupings[group_id]["datapoints"])
    
    #compute total error for a given cluster assignment
    #by checking aggregate distance of points within the cluster to its mean
    def _compute_group_error(self, group_id):
        total_error = 0
        mean = self.groupings[group_id]["mean"]
        for datapoint in self.groupings[group_id]["datapoints"]:
            total_error = total_error + self.cost_func(datapoint, mean)
        self.groupings[group_id]["intra_error"] = total_error
        
    #compute total error for a given cluster assignment
    #by checking aggregate distance of points within the cluster to all other cluster means
    def _compute_cross_cluster_error(self, group_id):
        total_error = 0
        for group, data in self.groupings.items():
            if not group == group_id:
                mean = self.groupings[group]["mean"]
                for datapoint in self.groupings[group_id]["datapoints"]:
                    total_error = total_error + self.cost_func(datapoint, mean)
        self.groupings[group_id]["inter_error"] = total_error
        
    def run(self):
        #initial with random partition
        current_error = None
        min_error = 0
        _initial_partition()
        for group, data in self.groupings.items():
            _compute_group_mean(group)
            _compute_group_error(group)
            _compute_cross_cluster_error(group)
            min_error = min_error + self.error_func(self.groupings[group]["intra_error"], self.groupings[group]["inter_error"])
            
        #main loop
        while (not current_error is None) or (current_error < min_error):
            #update self.mean, grouping datapoints, and min_error
            min_error = current_error if not current_error is None else min_error
            self.means = []
            for group, data in self.groupings.items():
                self.means.append(self.groupings[group]["mean"])
                self.groupings[group]["datapoints"] = []
                
            #map dataset into new groups
            for datapoint in self.dataset:
                _find_best_grouping(datapoint)
                
            #update grouping stats - mean, errors
            current_error = 0
            for group, data in self.groupings.items():
                _compute_group_mean(group)
                _compute_group_error(group)
                _compute_cross_cluster_error(group)
                current_error = current_error + self.error_func(self.groupings[group]["intra_error"], self.groupings[group]["inter_error"])
                
        #return all relevant data
        return (current_error, self.groupings)

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