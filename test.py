from patient import ColdTime
from qlearning import q_learning_model
from environment import Environment
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import csv

a=ColdTime(180)

'''def mk(inputdata):
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
        print(m)'''


'''with open('bloodpressure.csv', 'r', encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile)
    bp = np.zeros(24*3600)
    column = [row[1] for row in reader]
    for i in range(24*3600):
        bp[i] = column[i+1]

time=np.zeros(3600*24)
y_=np.zeros(3600*24)
for i in range(3600*24):
    time[i]=i

x = time
y = bp

coef7 = np.polyfit(x,y, 7)
poly_fit7 = np.poly1d(coef7)
plt.plot(x, poly_fit7(x), 'r:',label="7")
print(poly_fit7)

for i in range(24*3600):
    y_[i] = 7.537e-31*math.pow(i/3600,7)- 2.27e-25*math.pow(i/3600,6)+ 2.624e-20*math.pow(i/3600,5) - 1.437e-15 *math.pow(i/3600,4)+ 3.635e-11 *math.pow(i/3600,3)  - 3.085e-07 *math.pow(i/3600,2)- 0.000447*math.pow(i/3600,1)  + 132.9-y[i]

plt.scatter(time,y_, s=1,color='black')
plt.legend(loc=2)
print(y_[i])
plt.show()'''

'''def get_auto_corr(timeSeries,k):
           Descr:输入：时间序列timeSeries，滞后阶数k
            输出：时间序列timeSeries的k阶自相关系数
        l：序列timeSeries的长度
        timeSeries1，timeSeries2:拆分序列1，拆分序列2
        timeSeries_mean:序列timeSeries的均值
        timeSeries_var:序列timeSeries的每一项减去均值的平方的和''''''
    l = len(timeSeries)
#取出要计算的两个数组
    timeSeries1 = timeSeries[0:l-k]
    timeSeries2 = timeSeries[k:]
    timeSeries_mean = timeSeries.mean()
    timeSeries_var = np.array([i**2 for i in timeSeries-timeSeries_mean]).sum()
    auto_corr = 0
    for i in range(l-k):
        temp = (timeSeries1[i]-timeSeries_mean)*(timeSeries2[i]-timeSeries_mean)/timeSeries_var
    auto_corr = auto_corr + temp
    return auto_corr

with open('bloodpressure.csv', 'r', encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile)
    bp = np.zeros(24*3600)
    column = [row[1] for row in reader]
    for i in range(24*3600):
        bp[i] = column[i+1]
    result=get_auto_corr(bp,3)
    print(result)'''

