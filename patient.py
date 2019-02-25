import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

class ColdTime:
    def __init__(self,number):
        self.avg = np.array(
            [-4,3,1,3,4,4,4,3,-2,-2,-4,-2,-2,0,-1,3,3,3,3,-3,-2,-4,-5,-3])
        self.time = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
        self.number =number
        np.random.seed(0)
        self.mu = 0
        self.sigma = 1
        self.xl = np.zeros((self.number, 3600*24))
        for m in range(self.number):
            for n in range(24):
                for i in range(3600):
                    data = np.random.normal(self.mu, self.sigma, 1)
                    if m == 0 and n + i == 0:
                        self.xl[m][n] = 130 + 1 * data
                    else:
                        if n + i == 0:
                            if self.avg[n] >= 0:
                                v = 5 * (160 - self.xl[m - 1][24 * 3600 - 1]) / (160 * 3600)
                            else:
                                v = 3 * (self.xl[m - 1][24 * 3600 - 1] - 110) / (110 * 3600)
                            self.xl[m][n] = self.xl[m - 1][24 * 3600 - 1] + self.avg[n] * v + 1 * data / 50
                        else:
                            if self.avg[n] >= 0:
                                v = 5 * (160 - self.xl[m][n * 3600 - 1 + i]) / (160 * 3600)
                            else:
                                v = 3 * (self.xl[m][n * 3600 - 1 + i] - 110) / (110 * 3600)
                            self.xl[m][n * 3600 + i] = self.xl[m][n * 3600 - 1 + i] + self.avg[n] * v + 1 * data / 50

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

