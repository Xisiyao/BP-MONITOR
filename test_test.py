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

if __name__ == "__main__":
    bp = np.zeros(240)
    bp[0]=0
    for i in range(240):
        bp[i] = 3*bp[i-1]
    result=get_auto_corr(bp,1)
    print(result)


