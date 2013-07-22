from Data import Data
from Tree import learn
import os

d = Data()

d.load_from_file("car.data", 6)
d._set_debug(["buying", "maint", "doors", "persons", "lug_boot", "safety"])

tree = learn(d)

print tree.debug(0)
print tree.decide(["low","high","2","4","med","low"])
print tree.decide(["low","low","2","more","small","high"])



#print d.get_all_entropy()