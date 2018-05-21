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


# acc_total = list()
# for lamb in lamb_list:
#     reward_cur = compute_reward(lamb, gamma, Pa1, Pa, 100)
#     env_cur = MDPenv(reward_function=reward_cur)
#     _, policy_cur = env_cur.value_iter(epsilon=0.01)
#     compare = 0
#     for i in range(10):
#         for j in range(10):
#             if list(policy_cur[i, j]) == list(policy_optimal[i, j]):
#                 compare += 1
#     acc_cur = compare / 100.0
#     acc_total.append(acc_cur)
# plt.figure()
# plt.title("Accuracy - λ Plot")
# plt.xlabel("λ")
# plt.ylabel("Accuracy")
# plt.plot(lamb_list, acc_total)
# plt.show()


# Question 12/19:
# lamb_list = np.array(lamb_list)
# lamb_max = lamb_list[acc_total == np.max(acc_total)]
# print("lambda_max is", lamb_max)

# lambda_max 1 is [0.73146293 0.74148297 0.75150301 0.76152305 0.77154309 0.78156313
#  0.79158317 0.80160321 0.81162325 0.82164329 0.83166333 0.84168337
#  0.85170341 0.86172345 0.87174349 0.88176353 0.89178357 0.90180361
#  0.91182365 0.92184369 0.93186373 0.94188377 0.95190381 0.96192385
#  0.97194389 0.98196393 0.99198397 1.00200401 1.01202405 1.02204409
#  1.03206413 1.04208417 1.05210421 1.06212425 1.07214429 1.08216433
#  1.09218437 1.10220441 1.11222445 1.12224449 1.13226453 1.14228457
#  1.15230461 1.16232465 1.17234469 1.18236473 1.19238477 1.20240481
#  1.21242485 1.22244489 1.23246493 1.24248497 1.25250501 1.26252505
#  1.27254509 1.28256513 1.29258517 1.30260521 1.31262525 1.32264529
#  1.33266533 1.34268537 1.35270541 1.36272545 1.37274549 1.38276553
#  1.39278557 1.40280561 1.41282565 1.42284569 1.43286573 1.44288577
#  1.45290581 1.46292585 1.47294589 1.48296593 1.49298597 1.50300601
#  1.51302605 1.52304609 1.53306613 1.54308617 1.55310621 1.56312625
#  1.57314629 1.58316633 1.59318637 1.60320641 1.61322645 1.62324649
#  1.63326653 1.64328657 1.65330661 1.66332665 1.67334669 1.68336673
#  1.69338677 1.70340681 1.71342685 1.72344689 1.73346693 1.74348697
#  1.75350701 1.76352705 1.77354709 1.78356713 1.79358717 1.80360721
#  1.81362725 1.82364729 1.83366733 1.84368737 1.85370741 1.86372745
#  1.87374749 1.88376754 1.89378758 1.90380762 1.91382766 1.9238477
#  1.94388778 2.34468938 2.36472946 2.3747495  2.38476954 2.39478958
#  2.40480962 2.41482966 2.4248497  2.43486974 2.44488978 2.45490982
#  2.46492986 2.4749499  2.48496994 2.49498998 2.50501002 2.51503006
#  2.54509018 2.55511022 2.56513026 2.5751503  2.58517034 2.59519038
#  2.60521042 2.61523046 2.63527054 2.64529058 2.65531062 2.66533066
#  2.6753507  2.68537074 2.69539078 2.70541082 2.71543086 2.73547094
#  2.7755511  2.81563126 2.8256513  2.83567134 2.84569138 2.85571142
#  2.86573146 2.8757515  3.10621242]

# lambda_max 2 is [0.4008016  0.41082164 0.42084168 0.43086172 0.44088176 0.4509018
#  0.46092184 0.70140281 0.83166333 0.84168337 0.85170341 0.86172345
#  0.87174349]

# Question 13/20:
lamb_max = 0.73146293
reward_cur = compute_reward(lamb_max, gamma, Pa1, Pa, 1)
env_cur = MDPenv(reward_function=reward_cur)
env_cur.draw_rewardmap()

# Question 14 & 16/21 & 23:
env_cur.value_iter(0.01)
env_cur.draw_map()

