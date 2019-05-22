import matplotlib.pyplot as plt
import numpy as np
import time
import math
import csv
import pandas as pd

o = pd.Series([1,3,4,7])
m=[1]
m.append(3)
o=o.drop(m)
action = np.random.choice(o.index)
print(action)



