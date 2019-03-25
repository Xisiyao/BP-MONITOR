import matplotlib.pyplot as plt
import numpy as np
import time
import math
import csv


def get_auto_corr(timeSeries,k):
    '''
    Descr:输入：时间序列timeSeries，滞后阶数k
            输出：时间序列timeSeries的k阶自相关系数
        l：序列timeSeries的长度
        timeSeries1，timeSeries2:拆分序列1，拆分序列2
        timeSeries_mean:序列timeSeries的均值
        timeSeries_var:序列timeSeries的每一项减去均值的平方的和
        
    '''
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
    bp = np.zeros(240)
    result=np.zeros(12)
    time=np.array([0,1,2,3,4,5,6,7,8,9,10,11])
    column = [row[1] for row in reader]
    for m in range(240):
        bp[m] = column[m*15+1]
    plt.title("Autocorrelation")
    plt.xlim(right=12, left=0)
    plt.ylim(top=1, bottom=0)
    plt.xlabel("Lag order")
    plt.ylabel("Autocorrelation")
    for i in range(12):
        result[i]= get_auto_corr(bp, i)
    print(result)
    plt.plot(time,result)
    plt.show()


