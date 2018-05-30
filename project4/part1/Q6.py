# @author: Yufei Hu
import sys


# initializations
file_movie_edge_weight = open("movie_edge_weight.txt", 'w')
file_movie_actors = open("movie_actors.txt", "r")
file_merge = open("actor_movies_merged.txt", 'r')

movie_actorlist = dict()  # movie_id, actorlist
movie_name_map = dict()
movie_edge_list = dict()
actor_movielist = dict()  # actorid, movie_id_list


# main
def progressBar(start, end, bar_length=20):
    percent = float(start) / end
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write("\r[{0}] {1}% [{2}/{3}]".format(arrow + spaces, int(round(percent * 100)), start, end))
    sys.stdout.flush()


print("Start filling movie_actorlist...")
for line in file_movie_actors.readlines():
    line = line[:-1]
    line_list = line.split("\t\t")
    movie_actorlist[line_list[1]] = line_list[2:]
    movie_name_map[line_list[0]] = line_list[1]


print("Start filling actor_movielist...")
for line in file_merge.readlines():
    line = line[:-1]
    line_list = line.split("\t\t")
    movie_list_cur = list()
    for item in line_list[1:]:
        if item in movie_name_map and movie_name_map[item] in movie_actorlist:
            movie_list_cur.append(movie_name_map[item])
    actor_movielist[line_list[0]] = movie_list_cur


print("Start filling movie_edge_list...")
for row in actor_movielist.items():
    movie_list = row[1]
    index = len(movie_list)
    if index > 1:
        for i in range(0, index - 1):
            for j in range(i + 1, index):
                key = (int(movie_list[i]), int(movie_list[j]))
                key_rev = (int(movie_list[j]), int(movie_list[i]))
                if key in movie_edge_list:
                    movie_edge_list[key] += 1
                elif key_rev in movie_edge_list:
                    movie_edge_list[key_rev] += 1
                else:
                    movie_edge_list[key] = 1


i = 0
error = 0
print("Start writing to movie_edge_weight.txt...")
for item in movie_edge_list.items():
    progressBar(i, len(movie_edge_list))
    i += 1
    union = len(movie_actorlist[str(item[0][0])]) + len(movie_actorlist[str(item[0][1])]) - int(item[1])
    if union <= 0:
        error += 1
        continue
    weight = float(item[1]) / union
    file_movie_edge_weight.write(str(item[0][0]) + "\t\t" + str(item[0][1]) + "\t\t" + str(weight) + "\n")
print("\nNumber of abnormal edge weight: {}".format(error))


# close all files
file_movie_edge_weight.close()
file_movie_actors.close()
file_merge.close()