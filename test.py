from patient import ColdTime
from qlearning import q_learning_model
from environment import Environment
import pandas as pd
import numpy as np
import math

def update(days):
    s_ = np.zeros((1, 4), int)
    for episode in range(0,number):
        s[0] = [9, 5, 5, 0]
        for days_number in range(days-1):
            s_[0] = [9,0,0,0]
            if 9<=illtime[0][days_number]<10:
                s[0][3]=1
            while True:
                action = RL.choose_action(str(s[0]))
                s_[0][1],s_[0][2],is_pass= env.change(s[0][1],s[0][2],action) # 执行这个动作得到反馈（下一个状态s 奖励r ）
                if 9 <= illtime[0][days_number+1] < 10:
                    s_[0][3] = 1
                if is_pass==1:
                    r=0
                else:
                    r=env.reward(9,s_[0][1],s_[0][2],s_[0][3],illtime[0][days_number+1])
                RL.rl(str(s[0]), action, r, str(s_[0])) # 更新状态表
                s[0][1] = s_[0][1]
                s[0][2] = s_[0][2]
                s[0][3] = s_[0][3]
                break
        print(episode)

if __name__ == "__main__":
    days=60
    number=500
    coti = ColdTime(days)
    env = Environment()
    illtime = np.zeros((1, number * (days - 30)))
    RL = q_learning_model(actions=list(range(env.n_actions)))
    for n in range(days-30):
        for m in range(number):
            illtime[0][n+m] = coti.getilltime_m()[n]
    testtime=np.zeros((1,30))
    for n in range(30):
        testtime[0][n]=coti.getilltime_m()[30+n]
    s = np.zeros((1, 4),int)
    update(days-30)

    Delay = 0
    Energy = 0
    Energy += s[0][1] / (s[0][1] + s[0][2])
    for n in range(30):
        if s[0][0] <= testtime[0][n] < s[0][0] + 1:
            for i in range(3600):
                if (s[0][1] + s[0][2]) * i <= (testtime[0][n] - 9) * 3600 < (s[0][1] + s[0][2]) * (i + 1):
                    if (s[0][1] + s[0][2]) * i <= (testtime[0][n] - 9) * 3600 < (s[0][1] + s[0][2]) * i + s[0][
                        1]:
                        Delay = Delay + 0
                    else:
                        Delay += (s[0][1] + s[0][2]) * (i + 1) - (testtime[0][n] - 9) * 3600
    result = math.sqrt(Energy + Delay / 10)
    print(result)