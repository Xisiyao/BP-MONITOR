from patient import ColdTime
from qlearning import q_learning_model
from environment import Environment
import numpy as np
import matplotlib.pyplot as plt
import math
import csv

def update(days):
    max=np.zeros((days, 24), int)
    increas=np.zeros((days, 24), int)
    bp = np.zeros(240)
    rewardmax=0
    for days_number in range(days):
        for n in range(0, 24):
            for second in range((days_number * 24 + n) * 3600, (days_number * 24 + n + 1) * 3600):
                if illtime[0][second] > max[days_number][n]:
                    max[days_number][n] = illtime[0][second]
            if max[days_number][n] < 90:
                max[days_number][n] = 0
            else:
                if 90 <= max[days_number][n] < 120:
                    max[days_number][n] = 1
                else:
                    if 120 <= max[days_number][n] < 130:
                        max[days_number][n] = 2
                    else:
                        if 130 <= max[days_number][n] < 140:
                            max[days_number][n] = 3
                        else:
                            if 140 <= max[days_number][n] < 180:
                                max[days_number][n] = 4

            for i in range(240):
                bp[i] = illtime[0][(days_number * 24+n) * 3600 + (i +1) * 15-1]
            m = mk(bp)
            if m < -2.32:
                increas[days_number][n] = -1
            else:
                if m > 2.32:
                    increas[days_number][n] = 1
                else:
                    increas[days_number][n] = 0

    s_ = np.zeros((1, 4), int)


    for episode in range(0,episode_number):
        Reward = 0
        delay = 0
        for n in range(0, 15):
            s[n] = [n//5-1, n % 5, 5, 5]
        for days_number in range(days):
            for n in range(0,24):
                s_[0] = [0,-1,0,0]
                s_[0][0]=increas[days_number][n]
                s_[0][1]=max[days_number][n]

                next=(s_[0][0]+1)*5+s_[0][1]

                while True:
                    if days_number == days-1 and n == 23:
                        break
                    action = RL.choose_action(str(s[next]),episode)
                    s_[0][2],s_[0][3],is_pass= env.change(s[next][2],s[next][3],action) # 执行这个动作得到反馈（下一个状态s 奖励r ）
                    illpoint = 0
                    if n==23:
                        s_[0][0] = increas[days_number+1][0]
                        s_[0][1] = max[days_number+1][0]
                    else:
                        s_[0][0] = increas[days_number][n + 1]
                        s_[0][1] = max[days_number][n+1]

                    if s_[0][1] == 4:
                        for second in range((days_number * 24 + n+1) * 3600, (days_number * 24 + n + 2) * 3600):
                            if illtime[0][second] >= 140:
                                illpoint = second
                                break

                    if is_pass == 1:
                        r = 0
                    else:
                        if n == 23:
                            r,d = env.reward(days_number+1,0, s_[0][1], s_[0][2], s_[0][3], s[next][2],s[next][3],illpoint)
                        else:
                            r,d = env.reward(days_number,n+1, s_[0][1], s_[0][2], s_[0][3], s[next][2],s[next][3],illpoint)
                    Reward=Reward+r
                    if d>delay:
                        delay=d
                    RL.rl(str(s[next]), action, r, str(s_[0])) # 更新状态
                    next = (s_[0][0]+1) * 5 + s_[0][1]
                    s[next][2] = s_[0][2]
                    s[next][3] = s_[0][3]
                    break
        y[episode] =delay
        if y[episode]>rewardmax:
            rewardmax=y[episode]
        print(episode,",",y[episode])
    for i in range(episode_number):
        y[i]=y[i]/rewardmax
    plt.plot(x, y)
    plt.xlim(right=601, left=0)
    plt.ylim(top=1.1, bottom=0)
    plt.xlabel('Episode')
    plt.ylabel('Average Reward')
    plt.title('Number of Episode=600')
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
    days=150
    episode_number=600
    coti = ColdTime(days-30)
    getilltime=coti.getilltime()
    env=Environment()
    illtime=np.zeros((1,(days-30)*24*3600))
    x=np.zeros(episode_number)
    y = np.zeros(episode_number)
    for i in range(episode_number):
        x[i]=i+1

    RL= q_learning_model(actions=list(range(env.n_actions)))
    for n in range(days-30):
        for m in range(24*3600):
            illtime[0][n*24*3600+m]= getilltime[n][m]
    s = np.zeros((15, 4),int)
    update(days-30)






