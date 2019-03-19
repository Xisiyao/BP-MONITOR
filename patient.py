import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math
import pandas as pd
import csv

class ColdTime:
    def __init__(self,number):
        self.number = number
        self.seconds = 3600
        np.random.seed(0)
        self.mu = 0
        self.sigma = 1
        self.xl = np.zeros((self.number, self.seconds * 24))
        time = np.zeros(24 * self.seconds)
        for i in range(24 * self.seconds):
            time[i] = i / self.seconds
        self.data = 0
        for m in range(self.number):
            if m % 4 == 0:
                variation = self.daybyday(m)
            for n in range(24):
                data = np.random.normal(self.mu, self.sigma, 1)
                variation = variation + data / 5
                for i in range(self.seconds):
                    if i % 60 == 0:
                        data = np.random.normal(self.mu, self.sigma, 1)
                    self.xl[m][n * self.seconds + i] = self.oneday(n + i / self.seconds, variation) + data * 2.5

        '''i = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
        y_ = np.zeros(25)
        for x in range(25):
            y_[x] = 0 * math.pow(x, 8) + 5.819e-06 * math.pow(x, 7) - 0.0004894 * math.pow(x, 6) + 0.0158 * math.pow(x,5) - 0.2419 * math.pow(x, 4) + 1.713 * math.pow(x, 3) - 4.118 * math.pow(x, 2) - 1.086 * math.pow(x, 1) + 132
        plt.plot(i, y_)

        plt.title("Change of Blood Pressure")
        plt.xlim(right=24, left=0)
        plt.ylim(top=180, bottom=100)
        plt.xlabel("Time")
        plt.ylabel("Systolic BP")
        for i in range(number):
            plt.plot(time, self.xl[i])
        plt.show()'''

        dataframe = pd.DataFrame()
        csvfile = open('bloodpressure.csv', 'a', newline='')  # 打开方式还可以使用file对象
        writer = csv.writer(csvfile)
        for i in range(number):
            dataframe['DAY %s' % (i + 1)] = self.xl[i]
        # 将DataFrame存储为csv,index表示是否显示行名，default=True
        dataframe.to_csv("bloodpressure.csv", index=True, sep=',')
        csvfile.close()

    def oneday(self,x, variation):
        y = 5.819e-06 * math.pow(x, 7) - 0.0004894 * math.pow(x, 6) + 0.0158 * math.pow(x, 5) - 0.2419 * math.pow(x,4) + 1.713 * math.pow(x, 3) - 4.118 * math.pow(x, 2) - 1.086 * math.pow(x, 1) + 132 + variation
        return y

    def daybyday(self,number):
        x = number / 30
        y = 0.04236 * math.pow(x, 6) - 0.6854 * math.pow(x, 5) + 3.934 * math.pow(x, 4) - 9.281 * math.pow(x,3) + 7.024 * math.pow(x, 2) + 1.967 * math.pow(x, 1) - 2.578e-13
        return y

    def getilltime(self):
        return self.xl

    #画发病统计图像
    def drawing(self):
        plt.title("Change of Blood Pressure")
        plt.xlim(right=24, left=0)
        plt.ylim(top=180, bottom=100)
        plt.xlabel("Time")
        plt.ylabel("Systolic BP")
        for i in range(self.number):
            plt.plot(self.time, self.xl[i])
        plt.show()

