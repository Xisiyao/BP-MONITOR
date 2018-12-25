import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

class ColdTime:
    def __init__(self,number):
        self.number=number
        np.random.seed(0)
        #上午
        self.mu = 12
        self.sigma = 1
        self.xl_mor=[0]*self.number
        for n in range(self.number):
            while True:
                data = np.random.normal(self.mu, self.sigma, 1)
                if 9 <= data[0] <15:
                    data[0]=round(data[0], 4)
                    if data[0] != 15:
                        self.xl_mor[n] = data[0]
                        break
        #下午
        self.mu1 = 18  # mean of distribution
        self.sigma1 = 1  # standard deviation of distribution
        self.xl_aft = [0] * self.number
        for n in range(self.number):
            while True:
                data = np.random.normal(self.mu1, self.sigma1, 1)
                if 15 <= data[0] < 21:
                    data[0] = round(data[0], 4)
                    if data[0]!=21:
                        self.xl_aft[n] = data[0]
                        break

    def getilltime_m(self):
        return self.xl_mor

    def getilltime_a(self):
        return self.xl_aft

    #画发病统计图像
    def drawing(self):
        num_bins = 12
        fig, ax = plt.subplots(2)
        xl=[0]*self.number*2
        xl=self.xl_mor+self.xl_aft
        n, bins, patches = ax[0].hist(xl, num_bins, normed=0)
        ax[0].set_xlabel('time')
        ax[0].set_ylabel('Number of episodes')
        ax[0].set_title(r'Incidence of a patient')
        y = mlab.normpdf(bins, self.mu, self.sigma)
        y1 = mlab.normpdf(bins, self.mu1, self.sigma1)
        yy=y+y1
        ax[1].plot(bins, yy, '--')
        ax[1].set_xlabel('time')
        ax[1].set_ylabel('Probability density')
        ax[1].set_title(r'Curve Fitting')
        fig.tight_layout()

