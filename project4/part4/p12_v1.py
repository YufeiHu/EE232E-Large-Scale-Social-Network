import os
import random
import numpy as np
from sklearn import svm


movie_id = []
movie_random_actors = []        
with open('movie_actors.txt', 'r', encoding='gb18030', errors='ignore') as fr:
    for line in fr:
        line = line.split()
        for i in range(len(line)):
            if line[i][-1] == ")":
                movie_id.append(int(line[i+1]))
                tmp = line[i+2:]
                tmp_sample = random.sample(tmp, 6)
                for j in range(5):
                    tmp_sample[j] = int(tmp_sample[j])
                movie_random_actors.append(tmp_sample)
                break
movie_id = np.array(movie_id)
movie_random_actors = np.array(movie_random_actors)
print("finish extract")
print(movie_id)
print(movie_random_actors)

X_raw = movie_random_actors
y_raw = np.load('movie_rating.npy')

X = []
y = []

for i in range(len(X_raw)):
    if y_raw[i] != 0:
        X.append(X_raw[i])
        y.append(y_raw[i])
X = np.array(X)
y = np.array(y)

#training set (0.9)
X_train = X[0:int(np.floor(0.9*len(X)))]
y = y[[0:int(np.floor(0.9*len(X)))]]

clf = svm.SVR()
clf.fit(X, y) 

#Batman v Superman: Dawn of Justice (2016):
clf.predict([[17205, 48028, 51023, 84675, 49172]])
#Mission: Impossible - Rogue Nation (2015):
clf.predict([[42152, 52558, 66684, 24628, 73205]])
#Minions (2015):
clf.predict([[16095, 43221, 51476, 55121, 94815]])
