import pandas as pd
import numpy as np
import math


class q_learning_model:
    def __init__(self, actions,e_greedy=0.99,learning_rate=0.1, reward_decay=0.9):
        self.actions = actions
        self.learning_rate = learning_rate
        self.reward_decay = reward_decay
        self.e_greedy = e_greedy
        self.q_table = pd.DataFrame(columns=actions, dtype=np.float32)

    # 检查状态是否存在
    def check_state_exist(self, state):
        if state not in self.q_table.index:
            self.q_table = self.q_table.append(
                pd.Series(
                    [0] * len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )

    # 选择动作e
    def choose_action(self, s,p_actions,episode,values):
        self.check_state_exist(s)
        state_action = self.q_table.ix[s, :]
        if len(p_actions):
            state_action=state_action.drop(p_actions)
        if np.random.uniform() <(episode+1)/(episode+1+values):
            state_action = state_action.reindex(np.random.permutation(state_action.index))  # 防止相同列值时取第一个列，所以打乱列的顺序
            action = state_action.idxmax()
        else:
            action = np.random.choice(state_action.index)
        return action

    # 更新q表
    def rl(self, s, a, r, s_):
        self.check_state_exist(s_)
        q_predict = self.q_table.ix[s, a]  # q估计
        if s_ != 'terminal':
            q_target = r + self.reward_decay * self.q_table.ix[s_, :].max()  # q现实
        else:
            q_target = r

        self.q_table.ix[s, a] += self.learning_rate * (q_target - q_predict)
