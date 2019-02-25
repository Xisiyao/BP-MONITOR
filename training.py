from patient import ColdTime
from qlearning import q_learning_model
from environment import Environment
import numpy as np
import matplotlib.pyplot as plt
import math

def update(days):
    s_ = np.zeros((1, 4), int)
    Reward = 0
    for episode in range(0,episode_number):
        for n in range(0, 24):
            s[n] = [n , 5, 5, -1]
        for days_number in range(days):
            for n in range(0,24):
                s_[0] = [n,0,0,-1]
                max=0
                for second in range((days_number*24+n)*3600,(days_number*24+n+1)*3600):
                    if illtime[0][second]>max:
                        max=illtime[0][second]
                if max<90:
                    s_[0][3]=0
                else:
                    if 90<=max<120:
                        s_[0][3] = 1
                    else:
                        if 120<=max<130:
                            s_[0][3] = 2
                        else:
                            if 130<=max<140:
                                s_[0][3] = 3
                            else:
                                if 140<=max<180:
                                    s_[0][3] = 4
                s[n][3] = s_[0][3]

                while True:
                    if days_number == days-1 and n == 23:
                        break
                    action = RL.choose_action(str(s[n]),episode)
                    s_[0][1],s_[0][2],is_pass= env.change(s[n][1],s[n][2],action) # 执行这个动作得到反馈（下一个状态s 奖励r ）
                    max = 0
                    illpoint = 0
                    for second in range((days_number * 24 + n+1) * 3600, (days_number * 24 + n + 2) * 3600):
                        if illtime[0][second] > max:
                            max = illtime[0][second]
                    if max < 90:
                        s_[0][3] = 0
                    else:
                        if 90 <= max < 120:
                            s_[0][3] = 1
                        else:
                            if 120 <= max < 130:
                                s_[0][3] = 2
                            else:
                                if 130 <= max < 140:
                                    s_[0][3] = 3
                                else:
                                    if 140 <= max < 180:
                                        s_[0][3] = 4
                    if s_[0][3] == 4:
                        for second in range((days_number * 24 + n+1) * 3600, (days_number * 24 + n + 2) * 3600):
                            if illtime[0][second] >= 140:
                                illpoint = second
                                break
                    if is_pass == 1:
                        r = 0
                    else:
                        if n == 23:
                            r = env.reward(days_number,0, s_[0][1], s_[0][2], s_[0][3], illpoint)
                        else:
                            r = env.reward(days_number,n+1, s_[0][1], s_[0][2], s_[0][3], illpoint)
                    Reward=Reward+r
                    RL.rl(str(s[n]), action, r, str(s_[0])) # 更新状态
                    if n==23:
                        n=-1
                    s[n+1][1] = s_[0][1]
                    s[n+1][2] = s_[0][2]
                    s[n+1][3] = s_[0][3]
                    break
        print(episode)
    Reward=Reward/episode_number
    print(Reward)

if __name__ == "__main__":
    days=60
    episode_number=200
    coti = ColdTime(days)
    getilltime=coti.getilltime()
    env=Environment()
    illtime=np.zeros((1,(days-30)*24*3600))
    RL= q_learning_model(actions=list(range(env.n_actions)))
    for n in range(days-30):
        for m in range(24*3600):
            illtime[0][n*24*3600+m]= getilltime[n][m]
    testtime=np.zeros((1,30*24*3600))
    for n in range(30):
        for m in range(24 * 3600):
            testtime[0][n*24*3600+m]=coti.getilltime()[n+days-30][m]
    s = np.zeros((24, 4),int)
    update(days-30)

    '''
    s_ = np.zeros((1, 4), int)
    for n in range(0, 24):
        s[n] = [n, 5, 5, -1]
    for days_number in range(days-30):
        for n in range(0, 24):
            s_[0] = [n, 0, 0, -1]
            max = 0
            for second in range((days_number * 24 + n) * 3600, (days_number * 24 + n + 1) * 3600):
                if illtime[0][second] > max:
                    max = illtime[0][second]
            if max < 90:
                s_[0][3] = 0
            else:
                if 90 <= max < 120:
                    s_[0][3] = 1
                else:
                    if 120 <= max < 130:
                        s_[0][3] = 2
                    else:
                        if 130 <= max < 140:
                            s_[0][3] = 3
                        else:
                            if 140 <= max < 180:
                                s_[0][3] = 4
            s[n][3] = s_[0][3]

            while True:
                if days_number == days - 31 and n == 23:
                    break
                action = RL.choose_action(str(s[n]))
                s_[0][1], s_[0][2], is_pass = env.change(s[n][1], s[n][2], action)  # 执行这个动作得到反馈（下一个状态s 奖励r ）
                max = 0
                illpoint = 0
                for second in range((days_number * 24 + n + 1) * 3600, (days_number * 24 + n + 2) * 3600):
                    if illtime[0][second] > max:
                        max = illtime[0][second]
                if max<90:
                    s_[0][3]=0
                else:
                    if 90<=max<120:
                        s_[0][3] = 1
                    else:
                        if 120<=max<130:
                            s_[0][3] = 2
                        else:
                            if 130<=max<140:
                                s_[0][3] = 3
                            else:
                                if 140<=max<180:
                                    s_[0][3] = 4
                if s_[0][3] == 4:
                    for second in range((days_number * 24 + n + 1) * 3600, (days_number * 24 + n + 2) * 3600):
                        if illtime[0][second] >= 140:
                            illpoint = second
                            break
                if is_pass == 1:
                    R = 0
                else:
                    if n == 23:
                        R = env.reward(days_number,0, s_[0][1], s_[0][2], s_[0][3], illpoint)
                    else:
                        R = env.reward(days_number,n + 1, s_[0][1], s_[0][2], s_[0][3], illpoint)
                Reward+=R
                if n == 23:
                    n = -1
                s[n + 1][1] = s_[0][1]
                s[n + 1][2] = s_[0][2]
                s[n + 1][3] = s_[0][3]
                break
    print(Reward)'''


    #画学习结果
    '''x= np.zeros((1, 12))
    y = np.zeros((1, 12))
    for n in range(0,12):
        x[0][n]=s[n][0]
        y[0][n]=s[n][1]/(s[n][1]+s[n][2])
    plt.plot(x[0],y[0])
    plt.xlabel('Ti')
    plt.ylabel('Duty Cycle')
    plt.title('Number of Episode=60')

    #画病人发病时间
    coti.drawing()
    plt.show()'''





