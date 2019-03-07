import matplotlib.pyplot as plt
import numpy as np
import time
from math import *
import csv

def mk(inputdata):
#输入numpy数组
    n=inputdata.shape[0]
    var=n*(n-1)*(2*n+5)/18
    sv=np.sqrt(var)
    #sv为标准差
    s=0
    z=0
    for i in np.arange(n):
        if i <=(n - 1):
            for j in np.arange(i+1,n):
                if inputdata[j]> inputdata[i]:
                    s=s+1
                elif inputdata[j]< inputdata[i]:
                    s=s-1
                else:
                    s=s
    if s > 0:
        z= (s - 1) / sv
    elif s < 0:
        z= (s+ 1) / sv
    return z

if __name__ == "__main__":
    with open('bloodpressure.csv','r', encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile)
        bp=np.zeros(240)
        column = [row[1] for row in reader]
        for i in range(240):
            bp[i]=column[8*3600+(i+1)*15]
        m=mk(bp)
        print(m)



