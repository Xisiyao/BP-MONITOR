import math

class Environment:
    def __init__(self):
        self.action_space = ['（-1，-1）', '（+1，-1）', '（-1，+1）','（+1，+1）']
        self.n_actions = len(self.action_space)

    #奖赏函数
    def reward(self,day,T,s,n_on,n_off,n_onb,n_offb,illtime):
        illtime=illtime-day*3600*24
        delay = 0
        energy=n_on/(n_on+n_off)
        energyb = n_onb / (n_onb + n_offb)
        if energy>=energyb:
            re=0
        else:
            re=1
        if s==4:
            for m in range(3600):
                if (n_on+n_off)*m<=illtime-T*3600<(n_on+n_off)*(m+1):
                    if (n_on+n_off)*m<=illtime-T*3600<(n_on+n_off)*m+n_on:
                        delay=0
                        '''re=1-energy'''
                    else:
                        delay=(n_on+n_off)*(m+1)-(illtime-T*3600)
                        if delay <=2:
                            re = 0
                        else:
                            re = -delay-100
                            '''+energy'''
                    break
        '''else:
            re = 1 - energy'''
        return re,delay

    #根据动作改变状态
    def change(self, n_on,n_off,action):
        a=n_on
        b=n_off
        is_pass=0
        if action == 0:n_on=n_on-1;n_off =n_off - 1
        if action == 1:n_on = n_on+1;n_off =n_off - 1
        if action == 2:n_on = n_on -1;n_off =n_off+ 1
        if action == 3:n_on=n_on+1;n_off =n_off+1
        if n_on <= 0 or n_on >=11 or n_off <= 0 or n_off >= 11:
            n_on=a
            n_off=b
            is_pass=1
        return n_on,n_off,is_pass
