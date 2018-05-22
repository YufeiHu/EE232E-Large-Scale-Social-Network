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


def compute_reward(lamb, gamma, Pa1, Pa, Rmax):
    
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
    b[0, 800:] = Rmax
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


lamb_list = np.linspace(0, 5, 50)
gamma_list = np.linspace(0.8, 0.95, 20)


env1 = MDPenv(reward_function=rf2)
_, policy_optimal = env1.value_iter(epsilon=0.01)
Pa1, Pa = env1.compute_probability_matrix()


acc_max_list = list()
for gamma in gamma_list:
    acc_total = list()
    for lamb in lamb_list:
        reward_cur = compute_reward(lamb, gamma, Pa1, Pa, 100)
        env_cur = MDPenv(reward_function=reward_cur)
        _, policy_cur = env_cur.value_iter(epsilon=0.01)
        compare = 0
        for i in range(10):
            for j in range(10):
                if list(policy_cur[i, j]) == list(policy_optimal[i, j]):
                    compare += 1
        acc_cur = compare / 100.0
        acc_total.append(acc_cur)
        
    acc_max_list.append(max(acc_total))
#plt.figure()
#plt.plot(lamb_list, acc_total)
#plt.show()
#print(max(acc_total))