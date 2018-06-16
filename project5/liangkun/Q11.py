import sys
import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

file_uberGraph_info = open("./data/uber/origin_graph.txt", "r")
locations = list()
id_list = list()

for line in file_uberGraph_info.readlines():
    line = line.split("\t\t")
    node_id = line[0]
    x = line[1]
    y = line[2]
    y=y.strip("\n")
    tmp = list([x, y])
    locations.append(tmp)
    id_list.append(node_id)

file_uberGraph_info.close()
    
locations_np = np.array(locations)
tri = Delaunay(locations_np)

import matplotlib.pyplot as plt
print(locations_np)
plt.triplot(locations_np[:,0], locations_np[:,1], tri.simplices.copy())
plt.plot(locations_np[:,0], locations_np[:,1], 'o')
plt.show()

# file_Delaunay = open("./data/uber/Delaunay.txt", "w")
# for array in tri.simplices:
#     file_Delaunay.write("{:d}\t\t{:d}\t\t{:d}\n".format(int(id_list[array[0]]), int(id_list[array[1]]), 1))
#     file_Delaunay.write("{:d}\t\t{:d}\t\t{:d}\n".format(int(id_list[array[1]]), int(id_list[array[2]]), 1))
#     file_Delaunay.write("{:d}\t\t{:d}\t\t{:d}\n".format(int(id_list[array[0]]), int(id_list[array[2]]), 1))

# file_Delaunay.close()