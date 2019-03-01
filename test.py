from patient import ColdTime
from qlearning import q_learning_model
from environment import Environment
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import time

number=180
seconds=6
np.random.seed(0)
mu = 0
sigma = 1
xl = np.zeros((number, seconds*24))
time=np.zeros(24*seconds)
for i in range(24*seconds):
    time[i]=i/seconds

def oneday(x,variation):
    y=5.819e-06*math.pow(x,7)- 0.0004894*math.pow(x,6)+ 0.0158*math.pow(x,5)  - 0.2419 *math.pow(x,4)+ 1.713 *math.pow(x,3)  - 4.118 *math.pow(x,2)- 1.086 *math.pow(x,1)  +  132+variation
    return y

def daybyday(number):
    x=number/30
    y = 0.04236* math.pow(x, 6)- 0.6854* math.pow(x, 5) + 3.934 * math.pow(x,4) - 9.281  * math.pow(x, 3)+ 7.024 * math.pow(x, 2)+ 1.967  * math.pow(x, 1)- 2.578e-13
    return y

data=0
for m in range(number):
    data = np.random.normal(mu, sigma, 1)
    variation=daybyday(m)+data/2
    for n in range(24):
        for i in range(seconds):
            data = np.random.normal(mu, sigma, 1)
            xl[m][n*seconds+i]=oneday(n+i/seconds,variation)+data*2.5

i = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
y_=np.zeros(25)
for x in range(25):
    y_[x] = 0 * math.pow(x, 8) + 5.819e-06 * math.pow(x, 7) - 0.0004894 * math.pow(x, 6) + 0.0158 * math.pow(x,5) - 0.2419 * math.pow(x, 4) + 1.713 * math.pow(x, 3) - 4.118 * math.pow(x, 2) - 1.086 * math.pow(x, 1) + 132
plt.plot(i,y_)

plt.title("Change of Blood Pressure")
plt.xlim(right=24, left=0)
plt.ylim(top=180, bottom=100)
plt.xlabel("Time")
plt.ylabel("Systolic BP")
for i in range(number):
    plt.plot(time, xl[i])
plt.show()

