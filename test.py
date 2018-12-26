from patient import ColdTime
from qlearning import q_learning_model
from environment import Environment
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

def update(days):
    s_ = np.zeros((1, 4), int)
    for episode in range(0,number):
        s[0] = [T, 5, 5, 0]
        for days_number in range(days-1):
            s_[0] = [T,0,0,0]
            if T<=illtime[0][days_number]<T+1:
                s[0][3]=1
            while True:
                action = RL.choose_action(str(s[0]),0.8)
                s_[0][1],s_[0][2],is_pass= env.change(s[0][1],s[0][2],action) # 执行这个动作得到反馈（下一个状态s 奖励r ）
                if T <= illtime[0][days_number+1] < T+1:
                    s_[0][3] = 1
                if is_pass==1:
                    r=0
                else:
                    r=env.reward(T,s_[0][1],s_[0][2],s_[0][3],illtime[0][days_number+1])
                RL.rl(str(s[0]), action, r, str(s_[0])) # 更新状态表
                s[0][1] = s_[0][1]
                s[0][2] = s_[0][2]
                s[0][3] = s_[0][3]
                break
        print(episode)

def testresult():
    s[0]=[T,5,5,0]
    s_ = np.zeros((1, 4), int)
    Delay = 0
    Energy = 0
    for n in range(60):
        if T <= testtime[0][n] < T+1:
            s[0][3] = 1
        Energy += s[0][1] / (s[0][1] + s[0][2])
        if s[0][3]==1:
            for i in range(3600):
                if (s[0][1] + s[0][2]) * i <= (testtime[0][n] - T) * 3600 < (s[0][1] + s[0][2]) * (i + 1):
                    if (s[0][1] + s[0][2]) * i <= (testtime[0][n] - T) * 3600 < (s[0][1] + s[0][2]) * i + s[0][
                        1]:
                        Delay = Delay + 0
                    else:
                        Delay += (s[0][1] + s[0][2]) * (i + 1) - (testtime[0][n] - T) * 3600
        while True:
            action = RL.choose_action(str(s[0]),1)
            s[0][1],s[0][2], is_pass = env.change(s[0][1], s[0][2], action)  # 执行这个动作得到反馈
            break
    result = math.sqrt(Energy + Delay)
    return result

if __name__ == "__main__":
    days=120
    number=0
    T=11
    coti = ColdTime(days)
    env = Environment()
    illtime = np.zeros((1, (days - 60)))
    for n in range(days-60):
        illtime[0][n] = coti.getilltime_m()[n]
    testtime=np.zeros((1,61))
    for n in range(60):
        testtime[0][n]=coti.getilltime_m()[days-60+n]
    testtime[0][60]=0
    s = np.zeros((1, 4),int)
    V=[0]*6
    x=[1,2,3,4,5,6]
    for times in range(6):
        number=300*(times+1)
        RL = q_learning_model(actions=list(range(env.n_actions)))
        update(days-60)
        V[times]=testresult()
    plt.plot(x, V)
    plt.xlabel('times')
    plt.ylabel('Result')
    plt.title("Let's see what happens")
    plt.show()
