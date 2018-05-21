# -*- coding: utf-8 -*-
"""
Created on Sat May 19 17:57:21 2018
@author: Yufei Hu
"""


from cvxopt import matrix, solvers
from env4rl import MDPenv
import numpy as np
import matplotlib.pyplot as plt
import seaborn


def compute_reward(lamb, gamma, Pa1, Pa, R_max):
    
    C = [1] * 100
    C.extend([-lamb] * 100)
    C.extend([0] * 100)
    C = np.array(C)
    C = C.reshape((300, 1))
    
    I = np.identity(100)
    M = I - gamma * Pa1
    M = np.linalg.inv(M)
    
    D0 = np.concatenate((np.identity(100), np.zeros((100, 100))), axis=1)
    D0 = np.concatenate((D0, D0, D0), axis=0)
    D0_R = list()
    for i in range(Pa.shape[2]):
        for j in range(Pa.shape[0]):
            vec_left = Pa1[j] - Pa[j, :, i]
            vec_left = vec_left.reshape((1, vec_left.shape[0]))
            vec_ans = -vec_left.dot(M)
            D0_R.append(vec_ans[0])
    D0_R = np.array(D0_R)
    D0 = np.concatenate((D0, D0_R), axis=1)
    
    D1 = np.zeros((300, 200))
    D1_R0 = -(Pa1 - Pa[:, :, 0])
    D1_R0 = D1_R0.dot(M)
    D1_R1 = -(Pa1 - Pa[:, :, 1])
    D1_R1 = D1_R1.dot(M)
    D1_R2 = -(Pa1 - Pa[:, :, 2])
    D1_R2 = D1_R2.dot(M)
    D1_R = np.concatenate((D1_R0, D1_R1, D1_R2), axis=0)
    D1 = np.concatenate((D1, D1_R), axis=1)
    
    D2_0 = np.concatenate((np.zeros((100, 100)), -np.identity(100), -np.identity(100)), axis=1)
    D2_1 = np.concatenate((np.zeros((100, 100)), -np.identity(100), np.identity(100)), axis=1)
    D2 = np.concatenate((D2_0, D2_1), axis=0)
    
    D3_0 = np.concatenate((np.zeros((100, 200)), np.identity(100)), axis=1)
    D3_1 = np.concatenate((np.zeros((100, 200)), -np.identity(100)), axis=1)
    D3 = np.concatenate((D3_0, D3_1), axis=0)
    
    D = np.concatenate((D0, D1, D2, D3), axis=0)
    
    b = np.zeros((1, 1000))
    b[0, 800:] = R_max
    b = np.array(b)
    
    C_cvx = matrix(-C)
    A_cvx = matrix(D)
    b_cvx = matrix(b.T)
    sol = solvers.lp(C_cvx, A_cvx, b_cvx)
    ans = list(sol['x'])
    R_hat = np.array(ans[200:])
    R_hat = R_hat.reshape((10, 10)).T
    
    return R_hat
    

rf1 = np.array([[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.]])



rf2 = np.array([[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
                [ 0.,  0.,  0.,  0.,  -100.0,  -100.0,  -100.0,  0.,  0.,  0.],
                [ 0.,  0.,  0.,  0.,  -100.0,  0.,  -100.0,  0.,  0.,  0.],
                [ 0.,  0.,  0.,  0.,  -100.0,  0.,  -100.0,  -100.0,  -100.0,  0.],
                [ 0.,  0.,  0.,  0.,  -100.0,  0.,  0.,  0.,  -100.0,  0.],
                [ 0.,  0.,  0.,  0.,  -100.0,  0.,  0.,  0.,  -100.0,  0.],
                [ 0.,  0.,  0.,  0.,  -100.0,  0.,  0.,  0.,  -100.0,  0.],
                [ 0.,  0.,  0.,  0.,  0.,  0.,  -100.0,  -100.0,  -100.0,  0.],
                [ 0.,  0.,  0.,  0.,  0.,  0.,  -100.0,  0.,  0.,  0.],
                [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  10.]])


# Question 11/18:

lamb_list = np.linspace(0, 5, 500)
gamma = 0.8


env1 = MDPenv(reward_function=rf1)
_, policy_optimal = env1.value_iter(epsilon=0.01)
Pa1, Pa = env1.compute_probability_matrix()


acc_total = list()
for lamb in lamb_list:
    reward_cur = compute_reward(lamb, gamma, Pa1, Pa, 1)
    env_cur = MDPenv(reward_function=reward_cur)
    _, policy_cur = env_cur.value_iter(epsilon=0.01)
    compare = 0
    for i in range(10):
        for j in range(10):
            if list(policy_cur[i, j]) == list(policy_optimal[i, j]):
                compare += 1
    acc_cur = compare / 100.0
    acc_total.append(acc_cur)
plt.figure()
plt.title("Accuracy - λ Plot")
plt.xlabel("λ")
plt.ylabel("Accuracy")
plt.plot(lamb_list, acc_total)
plt.show()


# Question 12/19:
lamb_list = np.array(lamb_list)
lamb_max = lamb_list[acc_total == np.max(acc_total)]
print("lambda_max is", lamb_max)

# lambda_max 1 is [3.26653307 3.30661323 3.31663327 3.40681363 3.43687375 3.46693387 3.48697395]
# lambda_max is [1.75350701 1.76352705 1.77354709 1.78356713 1.79358717 1.80360721
#  1.81362725 1.82364729 2.08416834 2.09418838 2.10420842 2.3747495
#  2.38476954 2.39478958 2.40480962 2.41482966 2.4248497  2.43486974
#  2.44488978 2.45490982 2.46492986 2.4749499  2.48496994 2.49498998
#  2.50501002 2.51503006]
#
# # Question 13/20:
# lamb_max = 1.75350701
# reward_cur = compute_reward(lamb_max, gamma, Pa1, Pa, 100)
# env_cur = MDPenv(reward_function=reward_cur)
# env_cur.draw_rewardmap()
#
# # Question 14 & 16/21 & 23:
# env_cur.value_iter(0.01)
# env_cur.draw_map()

