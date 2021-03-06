import math

class Environment:
    def __init__(self,delaylimit):
        self.action_space = ['（-1，-1）', '（+1，-1）', '（-1，+1）','（+1，+1）','(0,0)']
        self.n_actions = len(self.action_space)
        self.delaylimit=delaylimit

    #奖赏函数
    def reward(self,day,T,s,n_on,n_off,n_onb,n_offb,illtime):
        illtime=illtime-day*3600*24
        delay = 0
        energy_change=n_on/(n_on+n_off)-n_onb/(n_onb+n_offb)
        re=-energy_change
        if s==4:
            for m in range(3600):
                if (n_on+n_off)*m<=illtime-T*3600<(n_on+n_off)*(m+1):
                    if (n_on+n_off)*m<=illtime-T*3600<(n_on+n_off)*m+n_on:
                        delay=0
                    else:
                        delay=(n_on+n_off)*(m+1)-(illtime-T*3600)
                        if delay >self.delaylimit:
                            re=-10
                    break
        return re,delay

    #根据动作改变状态
    def change(self, n_on,n_off,action):
        a=n_on
        b=n_off
        if action == 0:n_on=n_on-1;n_off =n_off - 1
        if action == 1:n_on = n_on+1;n_off =n_off - 1
        if action == 2:n_on = n_on -1;n_off =n_off+ 1
        if action == 3:n_on=n_on+1;n_off =n_off+1
        if action == 4: n_on = n_on ;n_off = n_off
        return n_on,n_off
