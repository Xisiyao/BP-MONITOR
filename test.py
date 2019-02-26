from patient import ColdTime
from qlearning import q_learning_model
from environment import Environment
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

avg=np.array([-4,3,1,3,4,4,4,3,-2,-2,-4,-2,-2,0,-1,3,3,3,3,-3,-2,-4,-5,-3])
time= np.zeros(24*3600)
for h in range(24):
    for sec in range(3600):
        time[h*3600+sec] = h+sec/3600
number = 60
np.random.seed(0)
mu = 0
sigma = 1
xl= np.zeros((number, 24*3600))
for m in range(number):
    for n in range(24):
        for i in range(3600):
            data = np.random.normal(mu,sigma, 1)
            if m==0 and n+i==0:
                xl[m][n] = 130 + 1*data
            else:
                if n+i==0:
                    if avg[n] >= 0:
                        v = 5 * (160 - xl[m-1][24*3600-1]) / (160*3600)
                    else:
                        v = 3 * (xl[m-1][24*3600-1] - 110) / (110*3600)
                    xl[m][n] = xl[m-1][24*3600-1]+avg[n]*v +1*data/30
                else:
                    if avg[n] >= 0:
                        v = 5 * (160 - xl[m][n*3600-1+i]) / (160*3600)
                    else:
                        v = 3 * (xl[m][n*3600-1+i] - 110) /(110*3600)
                    xl[m][n*3600+i] = xl[m][n*3600-1+i]+avg[n]*v +  1*data/30
plt.title("Change of Blood Pressure")
plt.xlim(right=24,left=0)
plt.ylim(top=160,bottom=110)
plt.xlabel("Time")
plt.ylabel("Systolic BP")
for i in range(number):
     plt.plot(time,xl[i])
plt.show()

