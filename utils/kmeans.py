'''
This script implements K-Means Clustering using generic cost functions
'''

#imports
import random

class KMeans:
    def __init__(self, dataset, k, cost_func, mean_func, error_func, compute_inter_error=True):
        self.dataset = dataset
        self.k = k
        self.cost_func = cost_func
        self.mean_func = mean_func
        self.error_func = error_func
        self.compute_inter_error = compute_inter_error
        
        self.means = []
        self.groupings = {}
        for x in range(k):
            self.groupings[x] = {"mean": None, "datapoints": [], "intra_error": None, "inter_error": None}
        
    #generate initial set of means
    #use a pseudorandom number generator for assignment
    def _initial_partition(self):
        for datapoint in self.dataset:
            assignment = random.randint(0, self.k - 1)
            self.groupings[assignment]["datapoints"].append(datapoint)
            
    #find closest mean to given datapoint
    #group that datapoint per the closest mean
    def _find_best_grouping(self, datapoint, ind):
        min_cost = None
        min_mean = None
        mean_costs = []
        ideal_size = ind / self.k
        for mean in self.means:
            mean_costs.append(self.cost_func(datapoint, mean))
        for index in range(len(mean_costs)):
            tmp = None
            if self.compute_inter_error == True:
                tmp = self.__compute_two_costs(mean_costs, index)
            else:
                tmp = (mean_costs[index], None)
            tmp_cost = self.error_func(tmp[0], tmp[1], (len(self.groupings[index]["datapoints"])+1, ideal_size))
            if min_cost is None or tmp_cost < min_cost:
                min_cost = tmp_cost
                min_mean = index
        self.groupings[min_mean]["datapoints"].append(datapoint)
        
    #helper method to return a tuple of (intracost, intercost)
    #where intracost is at the specified index
    #intercost is the sum of the remaining indices
    def __compute_two_costs(self, mean_costs, index):
        intra = None
        inter = 0
        for x in range(len(mean_costs)):
            if x == index:
                intra = mean_costs[x]
            else:
                inter = inter + mean_costs[x]
        return (intra, inter)
        
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
        ideal_size = len(self.dataset) / self.k
        self._initial_partition()
        for group, data in self.groupings.items():
            self._compute_group_mean(group)
            self._compute_group_error(group)
        for group, data in self.groupings.items():
            if self.compute_inter_error == True:
                self._compute_cross_cluster_error(group)
            min_error = min_error + self.error_func(self.groupings[group]["intra_error"], self.groupings[group]["inter_error"], (len(self.groupings[group]["datapoints"]), ideal_size))
            
        #main loop
        while (current_error is None) or (current_error < min_error):
            #update self.mean, grouping datapoints, and min_error
            min_error = current_error if not current_error is None else min_error
            self.means = []
            for group, data in self.groupings.items():
                self.means.append(self.groupings[group]["mean"])
                self.groupings[group]["datapoints"] = []
                
            #map dataset into new groups
            process_count = 0
            for datapoint in self.dataset:
                process_count = process_count + 1
                self._find_best_grouping(datapoint, process_count)
                
            #update grouping stats - mean, errors
            current_error = 0
            for group, data in self.groupings.items():
                self._compute_group_mean(group)
                self._compute_group_error(group)
            for group, data in self.groupings.items(): 
                if self.compute_inter_error == True:
                    self._compute_cross_cluster_error(group)
                current_error = current_error + self.error_func(self.groupings[group]["intra_error"], self.groupings[group]["inter_error"], (len(self.groupings[group]["datapoints"]), ideal_size))
            print (current_error)
                
        #return all relevant data
        return (min_error, self.groupings)