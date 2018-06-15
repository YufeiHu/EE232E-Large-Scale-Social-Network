# @author: Yufei Hu


import sys
import csv
import json
import numpy as np
from collections import OrderedDict


def progressBar(start, end, bar_length=20):
    percent = float(start) / end
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write("\r[{0}] {1}% [{2}/{3}]".format(arrow + spaces, int(round(percent * 100)), start, end))
    sys.stdout.flush()


def readCSV(filename):
    lines = []
    with open(filename, "rt") as f:
        csvreader = csv.reader(f)
        for line in csvreader:
            lines.append(line)
    return lines


def readJson(fn):
    if len(fn) == 0:
        return dict()
    with open(fn, 'rt') as f:
        return json.load(f)


def triangle_inequality_satisfy(w1, w2, w3):
    if (w1 + w2 > w3 and w1 + w3 > w2 and w2 + w3 > w1):
        return True
    else:
        return False


verticeList = set()
weights = OrderedDict()
edgeNums = OrderedDict()
data = readCSV('./data/uber/san_francisco-censustracts-2017-4-All-MonthlyAggregate.csv')


print("Filling weights...")
for row in data[1:]:
    if row[2] == '12':
        verticeList.add(row[0])
        verticeList.add(row[1])

        key_forward = row[0] + '-' + row[1]
        key_backward = row[1] + '-' + row[0]
        weight = float(row[3])
        if key_forward in weights and key_backward in weights:
            raise ValueError('Error: Both kinds of keys are in weights!')
        elif key_forward in weights and key_backward not in weights:
            weights[key_forward] = (weights[key_forward] * edgeNums[key_forward] + weight) / (edgeNums[key_forward] + 1)
            edgeNums[key_forward] = edgeNums[key_forward] + 1
        elif key_forward not in weights and key_backward in weights:
            weights[key_backward] = (weights[key_backward] * edgeNums[key_backward] + weight) / (edgeNums[key_backward] + 1)
            edgeNums[key_backward] = edgeNums[key_backward] + 1
        else:
            weights[key_forward] = weight
            edgeNums[key_forward] = 1


print("Finding satisfied triangles...")
i = 0
num_sample = 1000
memo = list()
verticeList = list(verticeList)
num_satisfied = 0

while(i < num_sample):

    progressBar(i, num_sample)
    idxsList = np.random.choice(verticeList, 3, replace=False)
    idxsSet = set()
    idxsSet.add(idxsList[0])
    idxsSet.add(idxsList[1])
    idxsSet.add(idxsList[2])

    if idxsSet not in memo:
        memo.append(idxsSet)
        v1 = idxsList[0]
        v2 = idxsList[1]
        v3 = idxsList[2]

        e1_forward = v1 + '-' + v2
        e1_backward = v2 + '-' + v1
        e2_forward = v1 + '-' + v3
        e2_backward = v3 + '-' + v1
        e3_forward = v2 + '-' + v3
        e3_backward = v3 + '-' + v2

        if e1_forward in weights or e1_backward in weights:
            e1 = e1_forward if e1_forward in weights else e1_backward
            if e2_forward in weights or e2_backward in weights:
                e2 = e2_forward if e2_forward in weights else e2_backward
                if e3_forward in weights or e3_backward in weights:
                    e3 = e3_forward if e3_forward in weights else e3_backward
                    i += 1
                    w1 = weights[e1]
                    w2 = weights[e2]
                    w3 = weights[e3]
                    if triangle_inequality_satisfy(w1, w2, w3):
                        num_satisfied += 1
print('\n{:.3f}% of the {} sampled triangles satisfy the triangle inequality'.format(num_satisfied * 100.0 / i, i))