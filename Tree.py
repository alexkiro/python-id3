from Data import create_from_other
from copy import deepcopy

class Node:
    def __init__(self):
        self.name = None
        self.param = None
        self.children = {}  # pair value : child
        
    def decide(self, instance):
        if self.children:   #is not a leaf
            i = deepcopy(instance)
            for k, v in self.children.items():
                if instance[self.param] == k:                    
                    break
            del i[self.param]
            return v.decide(i)
        else:
            return self.value
        
    
    def debug(self, lvl):
        if self.children == None:
            return "|" + ("-"*lvl) + str(self.value) + "\n"
        else:
            s = ""
            for k, v in self.children.items():
                s += "|" + ("-"*lvl) + str(self.name) + "=" + str(k) + ":\n" + v.debug(lvl + 1) 
            return s
                
        
        
def learn(data):        
    node = Node()
    if data.is_final():
        node.children = None
        node.value = sorted(data.counter.items(), key=lambda c: [1], reverse=True)[0][0]
    else:
        node.param = data.get_best_param()
        node.name = data._params[node.param]          
        for value in sorted(set(data.data[node.param])):
            node.children[value] = learn(create_from_other(data, node.param, value))             
    return node
        
    
