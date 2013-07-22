from math import log
from collections import Counter

class Data:    
    def __init__(self):   
        self._params = None
        
    def load_from_file(self, file_name, nr_params):
        """Load training data set from a file in which every line        
        represent a instance and has values for every parameter 
        separated by a comma. Last value is the label: unacc,acc,good or vgood.
        """
        self.n = nr_params + 1
        self.data = [[] for _ in range(self.n)]  # empty list for each param + 1 one for label        
        f = open(file_name, 'r')
        lines = f.readlines()
        f.close()        
        self.nr = len(lines)
        for line in lines:
            line = line[:-1]
            tokens = line.split(',')
            for i in range(self.n):
                self.data[i].append(tokens[i])    
        self.compute_basic()
        
    
        
    def entropy(self, results, nr):
        """Apply entropy formula
        results - lists of counts for each possible value 
        """
        e = 0.0
        for r in results:
            r = float(r)
            e -= (r / nr) * log(r / nr, 2) if r != 0.0 else 0
        return e
    
    
    def compute_basic(self):        
        """Count the evaluation result (unacc,acc,good,vgood)
        and the data's overall entropy
        """
        self.counter = Counter(self.data[-1])
        self.data_entropy = self.entropy(self.counter.values() , self.nr) 
        
    def get_entropy(self, o):
        """Get the entropy for parameter o"""
        counts = Counter(self.data[o]) #count for each value of parameter
        entropy = self.data_entropy
        for k,v in counts.items():
            count_result = Counter([self.data[-1][i] for i in range(self.nr) if self.data[o][i] == k])
            entropy -= (v / self.nr) * self.entropy(count_result.values(), v)
        return entropy  
                   
            
    def get_all_entropy(self):
        return [(i, self.get_entropy(i)) for i in range(self.n - 1)]
    
    def get_best_param(self):
        return sorted(self.get_all_entropy(), key=lambda e: e[1], reverse=True)[0][0]
        
    def is_final(self):
        """Final state if all instance are the same
        or there is no parameter left
        """
        return self.nr in self.counter.values() or self.n == 1
    
    def _set_debug(self, p):
        self._params = p
    
    def debug(self):
        s = ""
        for i in range(self.nr):
            
            for j in range(self.n):
                s += "\t" + self.data[j][i]
        print s
        

def create_from_other(other, param, value):
    """Load training data set from other data set while eliminating
    the parameter param and keeping only the instances where param 
    had the specificated value. 
    """
    data = Data()    
    data.data = [[] for _ in range(other.n)]
    data.nr = 0
    for i in range(other.nr):
        if other.data[param][i] == value:
            data.nr += 1
            for j in range(other.n):
                data.data[j].append(other.data[j][i])
    del data.data[param]
    data.n = other.n - 1
    data.compute_basic()
    
    
    if other._params:  # debug only
        data._params = [p for p in other._params]
        del data._params[param]
        
    return data

            
            
