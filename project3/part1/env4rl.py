import numpy as np
import matplotlib.pyplot as plt
import seaborn


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
        plt.show()
        ax2 = seaborn.heatmap(self.space, annot=marks, fmt='s', linecolor='black', linewidth=1, cmap='viridis')
        plt.show()


    def transition_prob(self, current_state, action, next_state):
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

