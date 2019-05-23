import matplotlib.pyplot as plt
import numpy as np
import time
import math
import csv
import pandas as pd
import matplotlib as mpl
from qlearning import q_learning_model
from environment import Environment

x_axix=np.zeros(1000)
co=['green','red','blue']
for i in range(1000):
    x_axix[i]=i
for m in range(3):
    y =np.zeros(1000)
    for i in range(1000):
        y[i]=x_axix[i]/(x_axix[i]+100*(m+2))
    plt.plot(x_axix, y, color=co[m], label='value is %s' % (100*(m+2)))
sub_axix = filter(lambda x: x % 200 == 0, x_axix)
plt.title('Result Analysis')
plt.legend()  # 显示图例

plt.xlabel('iteration times')
plt.ylabel('rate')
plt.show()
# python 一个折线图绘制多个曲线






