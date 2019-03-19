from patient import ColdTime
from qlearning import q_learning_model
from environment import Environment
import numpy as np
import matplotlib.pyplot as plt
import math
import csv

def update(days):
    s_ = np.zeros((1, 4), int)

    delay=0
    for episode in range(0,episode_number):
        Reward = 0
        for n in range(0, 15):
            s[n] = [n//5, n%5 , 5, 5]
        for days_number in range(days):
            for n in range(0,24):
                s_[0] = [0,-1,0,0]
                max=0
                for second in range((days_number*24+n)*3600,(days_number*24+n+1)*3600):
                    if illtime[0][second]>max:
                        max=illtime[0][second]
                if max<90:
                    s_[0][1]=0
                else:
                    if 90<=max<120:
                        s_[0][1] = 1
                    else:
                        if 120<=max<130:
                            s_[0][1] = 2
                        else:
                            if 130<=max<140:
                                s_[0][1] = 3
                            else:
                                if 140<=max<180:
                                    s_[0][1] = 4
                with open('bloodpressure.csv', 'r', encoding='UTF-8') as csvfile:
                    reader = csv.reader(csvfile)
                    bp = np.zeros(240)
                    column = [row[1+days_number] for row in reader]
                    for i in range(240):
                        bp[i] = column[n * 3600 + (i + 1) * 15]
                    m=mk(bp)
                    if m<-2.32:
                        s_[0][0]=-1
                    else:
                        if m > 2.32:
                            s_[0][0] = 1
                        else:
                            s_[0][0] = 0
                x=s_[0][0]*5+s_[0][1]

                while True:
                    if days_number == days-1 and n == 23:
                        break
                    action = RL.choose_action(str(s[x]),episode)
                    s_[0][2],s_[0][3],is_pass= env.change(s[x][2],s[x][3],action) # 执行这个动作得到反馈（下一个状态s 奖励r ）
                    max = 0
                    illpoint = 0
                    for second in range((days_number * 24 + n+1) * 3600, (days_number * 24 + n + 2) * 3600):
                        if illtime[0][second] > max:
                            max = illtime[0][second]
                    if max < 90:
                        s_[0][1] = 0
                    else:
                        if 90 <= max < 120:
                            s_[0][1] = 1
                        else:
                            if 120 <= max < 130:
                                s_[0][1] = 2
                            else:
                                if 130 <= max < 140:
                                    s_[0][1] = 3
                                else:
                                    if 140 <= max < 180:
                                        s_[0][1] = 4
                    if s_[0][1] == 4:
                        for second in range((days_number * 24 + n+1) * 3600, (days_number * 24 + n + 2) * 3600):
                            if illtime[0][second] >= 140:
                                illpoint = second
                                break

                    with open('bloodpressure.csv', 'r', encoding='UTF-8') as csvfile:
                        reader = csv.reader(csvfile)
                        bp = np.zeros(240)
                        if n==23:
                            column = [row[1 + days_number+1] for row in reader]
                            for i in range(240):
                                bp[i] = column[(i + 1) * 15]
                        else:
                            column = [row[1 + days_number] for row in reader]
                            for i in range(240):
                                bp[i] = column[(n + 1) * 3600 + (i + 1) * 15]
                        m = mk(bp)
                        if m<-2.32:
                            s_[0][0]=-1
                        else:
                            if m> 2.32:
                                s_[0][0] = 1
                            else:
                                s_[0][0] = 0
                    if is_pass == 1:
                        r = 0
                    else:
                        if n == 23:
                            r,d = env.reward(days_number+1,0, s_[0][1], s_[0][2], s_[0][3], illpoint)
                        else:
                            r,d = env.reward(days_number,n+1, s_[0][1], s_[0][2], s_[0][3], illpoint)
                    Reward=Reward+r
                    delay=delay+d
                    RL.rl(str(s[x]), action, r, str(s_[0])) # 更新状态
                    x = s_[0][0] * 5 + s_[0][1]
                    s[x][2] = s_[0][2]
                    s[x][3] = s_[0][3]
                    break
        y[0][episode] =Reward#/(episode+1)
        print(episode,",",y[0][episode])
    plt.plot(x[0], y[0])
    plt.xlim(right=301, left=0)
    plt.ylim(top=200, bottom=0)
    plt.xlabel('Episode')
    plt.ylabel('Average Delay')
    plt.title('Number of Episode=300')
    plt.show()

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
    days=35
    episode_number=100
    coti = ColdTime(days-30)
    getilltime=coti.getilltime()
    env=Environment()
    illtime=np.zeros((1,(days-30)*24*3600))
    x=np.zeros((1,episode_number))
    y = np.zeros((1, episode_number))
    for i in range(episode_number):
        x[0][i]=i+1

    RL= q_learning_model(actions=list(range(env.n_actions)))
    for n in range(days-30):
        for m in range(24*3600):
            illtime[0][n*24*3600+m]= getilltime[n][m]
    s = np.zeros((15, 4),int)
    update(days-30)






