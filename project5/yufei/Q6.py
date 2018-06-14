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


weights = OrderedDict()
edgeNums = OrderedDict()
file_uberGraph = open("./data/uber/uberGraph.txt", "w")
file_uberGraph_info = open("./data/uber/uberGraph_info.txt", "w")
data = readCSV('./data/uber/san_francisco-censustracts-2017-4-All-MonthlyAggregate.csv')
info = readJson('./data/uber/san_francisco_censustracts.json')
info = info['features']


print("Writing to uberGraph_info.txt...")
idx = 0
for row in info:
    progressBar(idx, len(info))
    idx += 1
    ID = int(row['properties']['MOVEMENT_ID'])
    streetName = row['properties']['DISPLAY_NAME']
    coordinates = np.array(row['geometry']['coordinates'][0][0])
    coordinate = np.mean(coordinates, axis=0)
    file_uberGraph_info.write("{:d}\t\t{:s}\t\t{:f}\t\t{:f}\n".format(ID, streetName, coordinate[0], coordinate[1]))
file_uberGraph_info.close()


print("\nFilling weights...")
idx = 0
for row in data[1:]:
    progressBar(idx, len(data) - 1)
    idx += 1
    if row[2] == '12':
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


print("\nWriting to uberGraph.txt...")
idx = 0
for row in weights.items():
    progressBar(idx, len(weights) - 1)
    idx += 1
    key = row[0].split('-')
    source = int(key[0])
    dest = int(key[1])
    weight = float(row[1])
    file_uberGraph.write("{:d}\t\t{:d}\t\t{:f}\n".format(source, dest, weight))
file_uberGraph.close()
