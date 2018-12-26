import math

class Environment:
    def __init__(self):
        self.action_space = ['（-1，-1）', '（+1，-1）', '（-1，+1）','（+1，+1）']
        self.n_actions = len(self.action_space)

    #奖赏函数
    def reward(self,T,n_on,n_off,is_ill,illtime):
        energy=n_on/(n_on+n_off)
        if is_ill==1:
            for m in range(3600):
                if (n_on+n_off)*m<=(illtime-T)*3600<(n_on+n_off)*(m+1):
                    if (n_on+n_off)*m<=(illtime-T)*3600<(n_on+n_off)*m+n_on:
                        delay=0
                        r=1-energy
                    else:
                        delay=(n_on+n_off)*(m+1)-(illtime-T)*3600
                        if delay <=2:
                            r = 0
                        else:
                            r = -delay+2+energy
                    break
        else:
            r=0.5-energy
        return r

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
