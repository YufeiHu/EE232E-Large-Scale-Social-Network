import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn

matplotlib.rcParams.update({'font.size': 6})

class MDPenv(object):
    def __init__(self, greedy_prob=0.1, discount_factor=0.8, reward_function=None):
        # space map
        #self.space_idx = np.zeros([10, 10])
        self.space = np.zeros([10, 10])
        # action set (up, down, left, right)
        self.action_set = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
        # epsilon-greedy
        self.greedy_prob = greedy_prob
        # discount factor
        self.discount_factor = discount_factor
        # reward function
        self.reward_function = reward_function
        # policy
        self.policy = np.array([[None] * 10] * 10)
        # arrow set
        self.mark_set = ['\u2191', '\u2193', '\u2190', '\u2192']


    def draw_rewardmap(self):
        ax1 = seaborn.heatmap(self.reward_function, annot=True, linecolor='black', linewidth=1, cmap='viridis')
        ax1.set_title("Reward map")
        plt.show()


    def draw_map(self):
        marks = np.array([[''] * 10] * 10)
        mark_set = self.mark_set
        for i in range(10):
            for j in range(10):
                if list(self.policy[i][j]) == [-1, 0]:
                    marks[i][j] = mark_set[0]
                elif list(self.policy[i][j]) == [1, 0]:
                    marks[i][j] = mark_set[1]
                elif list(self.policy[i][j]) == [0, -1]:
                    marks[i][j] = mark_set[2]
                elif list(self.policy[i][j]) == [0, 1]:
                    marks[i][j] = mark_set[3]

        ax1 = seaborn.heatmap(self.space, annot=True, linecolor='black', linewidth=1, cmap='viridis')
        ax1.set_title("Optimal state value")
        plt.show()

        ax2 = seaborn.heatmap(self.space, annot=marks, fmt='s', linecolor='black', linewidth=1, cmap='viridis')
        ax2.set_title("Optimal policy")
        plt.show()



    def transition_prob(self, current_state, action, next_state):
        # impossible leap
        if ((current_state[0] == next_state[0] and current_state[1] == next_state[1]) or
           (current_state[0] == next_state[0] + 1 and current_state[1] == next_state[1]) or
           (current_state[0] == next_state[0] - 1 and current_state[1] == next_state[1]) or
           (current_state[0] == next_state[0] and current_state[1] == next_state[1] + 1) or
           (current_state[0] == next_state[0] and current_state[1] == next_state[1] - 1)) == False:
            return 0.0
        
        # intended state
        intended_state = current_state + action

        # normal case:
        if current_state[0] > 0 and current_state[0] < 9 and current_state[1] > 0 and current_state[1] < 9:
            if list(next_state) == list(current_state):
                return 0
            if list(next_state) == list(intended_state):
                return (1 - self.greedy_prob + self.greedy_prob / 4)
            else:
                return self.greedy_prob / 4

        # corner 1:
        elif list(current_state) == [0, 0]:
            if intended_state[0] < 0 or intended_state[1] < 0:
                if list(next_state) == list(current_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4 + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4
            else:
                if list(next_state) == list(current_state):
                    return self.greedy_prob / 4 + self.greedy_prob / 4
                elif list(next_state) == list(intended_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4

        # corner 2:
        elif list(current_state) == [0, 9]:
            if intended_state[0] < 0 or intended_state[1] > 9:
                if list(next_state) == list(current_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4 + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4
            else:
                if list(next_state) == list(current_state):
                    return self.greedy_prob / 4 + self.greedy_prob / 4
                elif list(next_state) == list(intended_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4

        # corner 3:
        elif list(current_state) == [9, 0]:
            if intended_state[0] > 9 or intended_state[1] < 0:
                if list(next_state) == list(current_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4 + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4
            else:
                if list(next_state) == list(current_state):
                    return self.greedy_prob / 4 + self.greedy_prob / 4
                elif list(next_state) == list(intended_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4


        # corner 4:
        elif list(current_state) == [9, 9]:
            if intended_state[0] > 9 or intended_state[1] > 9:
                if list(next_state) == list(current_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4 + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4
            else:
                if list(next_state) == list(current_state):
                    return self.greedy_prob / 4 + self.greedy_prob / 4
                elif list(next_state) == list(intended_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4

        # edge 1:
        elif current_state[0] == 0 and list(current_state) != [0, 0] and list(current_state) != [0, 9]:
            if intended_state[0] < 0:
                if list(next_state) == list(current_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4
            else:
                if list(next_state) == list(intended_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4

        # edge 2:
        elif current_state[0] == 9 and list(current_state) != [9, 0] and list(current_state) != [9, 9]:
            if intended_state[0] > 9:
                if list(next_state) == list(current_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4
            else:
                if list(next_state) == list(intended_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4

        # edge 3:
        elif current_state[1] == 0 and list(current_state) != [0, 0] and list(current_state) != [9, 0]:
            if intended_state[1] < 0:
                if list(next_state) == list(current_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4
            else:
                if list(next_state) == list(intended_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4

        # edge 4:
        elif current_state[1] == 9 and list(current_state) != [0, 9] and list(current_state) != [9, 9]:
            if intended_state[1] > 9:
                if list(next_state) == list(current_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4
            else:
                if list(next_state) == list(intended_state):
                    return 1 - self.greedy_prob + self.greedy_prob / 4
                else:
                    return self.greedy_prob / 4
        
        # out of bound:
        else:
            return 0.0


    def optimal_state_value(self, current_state):
        # initial
        current_value = -float('inf')
        current_policy = np.array([0, 0])
        # computation
        for action in self.action_set:
            value_tmp = 0
            for move in np.array([[-1,0], [1,0], [0,-1], [0,1], [0,0]]):
                next_state = current_state + move
                if next_state[0] < 0 or next_state[0] > 9 or next_state[1] < 0 or next_state[1] > 9:
                    continue 
                prob = self.transition_prob(current_state, action, next_state)
                value_tmp += prob * (self.reward_function[next_state[0]][next_state[1]] + self.discount_factor * self.space[next_state[0]][next_state[1]])
            if value_tmp > current_value:
                current_policy = action
                current_value = value_tmp
        return current_value, current_policy

    
    def one2two(self, idx):
        y = int(idx % 10)
        x = int(idx / 10)
        return np.array([y, x])
        
        
    def compute_probability_matrix(self):
        optimal_action = self.policy
        Pa1 = np.zeros((100, 100))
        Pa = np.zeros((100, 100, 3))
        for idx0 in range(100):
            current_state = self.one2two(idx0)
            a1 = optimal_action[current_state[0], current_state[1]]
            for idx1 in range(100):
                next_state = self.one2two(idx1)
                Pa1[idx0, idx1] = self.transition_prob(current_state, a1, next_state)
                idx2 = 0
                for action in self.action_set:
                    if action[0] != a1[0] and action[1] != a1[1]:
                        Pa[idx0, idx1, idx2] = self.transition_prob(current_state, action, next_state)
                        idx2 += 1
        return Pa1, Pa


    def value_iter(self, epsilon):
        self.space = np.zeros([10, 10])
        delta = float('inf')
        while delta > epsilon:
            delta = 0
            for i in range(10):
                for j in range(10):
                    curr = self.space[i][j]
                    self.space[i][j], self.policy[i][j] = self.optimal_state_value(np.array([i, j]))
                    delta = max(delta, abs(curr - self.space[i][j]))
        return self.space, self.policy

