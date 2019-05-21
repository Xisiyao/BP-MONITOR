from patient import ColdTime
from qlearning import q_learning_model
from environment import Environment
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import csv

def update(days):
    Reward = 0
    max=np.zeros((days, 24), int)
    increas=np.zeros((days, 24), int)
    bp = np.zeros(240)
    rewardmax = 0
    energy_sumb = 0.5 * days * 24
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
        bool_flag_1 = False
        bool_flag_2 = False
        delaytime = 0
        timeofill = 0
        energy_change = 0
        energy_sum = 0
        delay = 0
        for n in range(0, 15):
            s[n] = [n//5-1, n % 5, 5, 0]
        for days_number in range(days):
            for n in range(0,24):
                s_[0] = [0,-1,0,0]
                s_[0][0]=increas[days_number][n]
                s_[0][1]=max[days_number][n]

                now=(s_[0][0]+1)*5+s_[0][1]
                energy_sum = energy_sum + s[now][2]/(s[now][2]+s[now][3])

                while True:
                    while True:
                        action = RL.choose_action(str(s[now]),episode)
                        s_[0][2],s_[0][3],is_pass= env.change(s[now][2],s[now][3],action) # 执行这个动作得到反馈（下一个状态s 奖励r ）
                        if is_pass==1:
                            break
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
                        timeofill+=1

                    if days_number == days - 1 and n == 22:
                        next = (s_[0][0] + 1) * 5 + s_[0][1]
                        energy_sum = energy_sum+s[next][2]/(s[next][2]+s[next][3])
                        energy_change = 100*(energy_sum - days*24)/(days*24)
                        energy_sumb = energy_sum
                    else:
                        if n == 23:
                            r,d = env.reward(days_number+1,0, s_[0][1], s_[0][2], s_[0][3], energy_change,illpoint)
                        else:
                            r,d = env.reward(days_number,n+1, s_[0][1], s_[0][2], s_[0][3], energy_change,illpoint)
                    Reward=Reward+r
                    RL.rl(str(s[now]), action, r, str(s_[0])) # 更新状态
                    if d > 4:
                        delaytime += 1
                        bool_flag_2 = True
                        break
                    next = (s_[0][0]+1) * 5 + s_[0][1]
                    s[next][2] = s_[0][2]
                    s[next][3] = s_[0][3]
                    break
                if days_number == days - 1 and n == 22:
                    break
                if bool_flag_2 == True:
                    bool_flag_1 = True
                    break
            if  bool_flag_1 == True:
                y[episode]=5
                break
            y[episode] = energy_sum
        if y[episode]>rewardmax:
            rewardmax = y[episode]
        print(episode,",",y[episode])

    for episode in range(0, episode_number):
        y[episode]=y[episode]/rewardmax
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
    days=60
    episode_number=6000
    coti = ColdTime(days-30)
    getilltime=coti.getilltime()
    env=Environment()
    illtime=np.zeros((1,(days-30)*24*3600))
    x=np.zeros(episode_number)
    y = np.zeros(episode_number)
    for i in range(episode_number):
        x[i]=i

    RL= q_learning_model(actions=list(range(env.n_actions)))
    for n in range(days-30):
        for m in range(24*3600):
            illtime[0][n*24*3600+m]= getilltime[n][m]
    s = np.zeros((15, 4),int)
    update(days-30)
#显示所有列
    pd.set_option('display.max_columns', None)
#显示所有行
    pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth',100)
    print(RL.q_table)






