from patient import ColdTime
from qlearning import q_learning_model
from environment import Environment
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import time
import csv

number=1
seconds=3600
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
    if m%4==0:
        variation = daybyday(m)
    for n in range(24):
        data = np.random.normal(mu, sigma, 1)
        variation = variation+ data / 5
        for i in range(seconds):
            if i%60==0:
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

'''dataframe=pd.DataFrame()
csvfile = open('bloodpressure.csv', 'a', newline='')  #打开方式还可以使用file对象
writer = csv.writer(csvfile)
for i in range(number):
    dataframe['DAY %s'%(i+1)]=xl[i]
#将DataFrame存储为csv,index表示是否显示行名，default=True
dataframe.to_csv("bloodpressure.csv",index=True,sep=',')
csvfile.close()'''

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

