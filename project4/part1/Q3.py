# @author: Yufei Hu


# initializations
parings_target = dict()
actorID_target = [53037, 36700, 51346, 65792, 70923, 55412, 101308, 33234, 55819, 91782]
file_edge_weight = open("edge_weight.txt", "r")
file_actor_id = open("actor_id.txt", "r")


# start analyzing edge_weight.txt
for line in file_edge_weight.readlines():
    line = line[:-1]
    paring = line.split("\t\t")
    paring[0] = int(paring[0])
    paring[1] = int(paring[1])
    paring[2] = float(paring[2])
    if paring[0] in actorID_target:
        if paring[0] in parings_target:
            if parings_target[paring[0]][1] < paring[2]:
                parings_target[paring[0]][0] = paring[1]
                parings_target[paring[0]][1] = paring[2]
        else:
            parings_target[paring[0]] = list()
            parings_target[paring[0]].append(paring[1])
            parings_target[paring[0]].append(paring[2])


# print results
actor_id = file_actor_id.readlines()
for paring in parings_target.items():
    in_name = actor_id[int(paring[0])].split("\t\t")[0]
    out_name = actor_id[int(paring[1][0])].split("\t\t")[0]
    weight = paring[1][1]
    print("{} prefers {} with edge cost of {.3f}".format(in_name, out_name, weight))
# Hanks, Tom prefers Allen, Tim (I) with edge cost of 0.10126582278481013
# Depp, Johnny prefers Bonham Carter, Helena with edge cost of 0.08163265306122448
# Streep, Meryl prefers De Niro, Robert with edge cost of 0.061855670103092786
# Clooney, George prefers Damon, Matt with edge cost of 0.11940298507462686
# DiCaprio, Leonardo prefers Scorsese, Martin with edge cost of 0.10204081632653061
# Johnson, Dwayne (I) prefers Austin, Steve (IV) with edge cost of 0.20512820512820512
# Pitt, Brad prefers Clooney, George with edge cost of 0.09859154929577464
# Cruise, Tom prefers Kidman, Nicole with edge cost of 0.1746031746031746
# Smith, Will (I) prefers Foster, Darrell with edge cost of 0.12244897959183673
# Watson, Emma (II) prefers Radcliffe, Daniel with edge cost of 0.52


# close all files
file_edge_weight.close()
file_actor_id.close()