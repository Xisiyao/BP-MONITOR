from patient import ColdTime
from qlearning import q_learning_model
from environment import Environment
import numpy as np
import matplotlib.pyplot as plt
import math

def update(days):
    s_ = np.zeros((1, 4), int)
    for episode in range(0,number):
        for n in range(0, 12):
            s[n] = [n + 9, 5, 5, 0]
        for days_number in range(days-1):
            #上午
            for n in range(0,6):
                s_[0] = [n+9,0,0,0]
                if n+9<=illtime[0][days_number]<n+10:
                    s[n][3]=1
                while True:
                    action = RL.choose_action(str(s[n]))
                    s_[0][1],s_[0][2],is_pass= env.change(s[n][1],s[n][2],action) # 执行这个动作得到反馈（下一个状态s 奖励r ）
                    if n + 9 <= illtime[0][days_number+1] < n + 10:
                        s_[0][3] = 1
                    if is_pass==1:
                        r=0
                    else:
                        r=env.reward(n+9,s_[0][1],s_[0][2],s_[0][3],illtime[0][days_number+1])
                    RL.rl(str(s[n]), action, r, str(s_[0])) # 更新状态表
                    s[n][1] = s_[0][1]
                    s[n][2] = s_[0][2]
                    s[n][3] = s_[0][3]
                    break
            #下午
            for n in range(6,12):
                s_[0] = [n+9,0,0,0]
                if n+9<=illtime[1][days_number]<n+10:
                    s[n][3]=1
                while True:
                    # 选择一个动作
                    action = RL.choose_action(str(s[n]))
                    s_[0][1],s_[0][2],is_pass= env.change(s[n][1],s[n][2],action)# 执行这个动作得到反馈（下一个状态s 奖励r ）
                    if n + 9 <= illtime[1][days_number+1] < n + 10:
                        s_[0][3] = 1
                    if is_pass==1:
                        r=0
                    else:
                        r=env.reward(n+9,s_[0][1],s_[0][2],s_[0][3],illtime[1][days_number+1])

                    # 更新状态表
                    RL.rl(str(s[n]), action, r, str(s_[0]))

                    s[n][1] = s_[0][1]
                    s[n][2] = s_[0][2]
                    s[n][3] = s_[0][3]
                    break
        print(episode)

if __name__ == "__main__":
    days=90
    number=60
    coti = ColdTime(days)
    env=Environment()
    illtime=np.zeros((2,number*(days-30)))
    RL= q_learning_model(actions=list(range(env.n_actions)))
    for n in range(days-30):
        for m in range(number):
            illtime[0][n+m] = coti.getilltime_m()[n]
            illtime[1][n+m] = coti.getilltime_a()[n]
    testtime=np.zeros((2,30))
    for n in range(30):
        testtime[0][n]=coti.getilltime_m()[30+n]
        testtime[1][n] = coti.getilltime_a()[30 + n]
    s = np.zeros((12, 4),int)
    update(days-30)

    Delay=0
    Energy=0
    for T in range(12):
        Energy+=s[T][1]/(s[T][1]+s[T][2])
        for n in range(30):
            for m in range(2):
                if s[T][0] <= testtime[m][n] < s[T ][0]+1:
                    for i in range(3600):
                        if (s[T][1]+s[T][2]) * i <= (testtime[m][n] - T+9) * 3600 < (s[T][1]+s[T][2]) * (i + 1):
                            if (s[T][1]+s[T][2]) * i <= (testtime[m][n] - T+9) * 3600 < (s[T][1]+s[T][2]) * i + s[T][1]:
                                Delay = Delay+0
                            else:
                                Delay += (s[T][1]+s[T][2]) * (i + 1) - (testtime[m][n] - T+9) * 3600
    result=math.sqrt(Energy+Delay/10)
    print(result)


    #画学习结果
    x= np.zeros((1, 12))
    y = np.zeros((1, 12))
    for n in range(0,12):
        x[0][n]=s[n][0]
        y[0][n]=s[n][1]/(s[n][1]+s[n][2])
    plt.plot(x[0],y[0])
    plt.xlabel('Ti')
    plt.ylabel('Duty Cycle')
    plt.title('Number of Train Set=60')

    #画病人发病时间
    coti.drawing()
    plt.show()





