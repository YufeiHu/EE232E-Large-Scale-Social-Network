# @author: Yufei Hu


# user definition
min_actor = 5


# initializations
file_edge_weight = open("edge_weight.txt", "w")
file_movie_actors = open("movie_actors.txt", "w")
file_merge = open("actor_movies_merged.txt", "r")

movie_id = 0
edge_weight = dict()
movie_actors = dict()
actor_numOfMovie = dict()


# start fill in movie_actor and actor_num_movie
print("Filling movie_actors and actor_numOfMovie...")
for line in file_merge.readlines():

    line = line[:-1]
    name_movies = line.split("\t\t")
    name_actor = name_movies[0]

    actor_numOfMovie[name_actor] = len(name_movies) - 1
    for name_movie in name_movies[1:]:
        if name_movie in movie_actors:
            if name_actor not in movie_actors[name_movie]:
                movie_actors[name_movie].append(name_actor)
        else:
            movie_actors[name_movie] = list()
            movie_actors[name_movie].append(movie_id)
            movie_actors[name_movie].append(name_actor)
            movie_id += 1


# start fill in edge_weight and write to movie_actors.txt
print("Filling edge_weight and writing to movie_actors.txt...")
for row in movie_actors.items():

    key_movie_actors = row[0]
    value_movie_actors = row[1]
    actor_num = len(value_movie_actors) - 1

    if actor_num >= min_actor:
        file_movie_actors.write(key_movie_actors)
        for val in value_movie_actors:
            file_movie_actors.write("\t\t" + str(val))
        file_movie_actors.write("\n")

    if actor_num > 1:
        for i in range(1, actor_num):
            for j in range(i + 1, actor_num + 1):
                key1 = (int(value_movie_actors[i]), int(value_movie_actors[j]))
                key2 = (int(value_movie_actors[j]), int(value_movie_actors[i]))

                if key1 in edge_weight:
                    edge_weight[key1] += 1
                    edge_weight[key2] += 1
                else:
                    edge_weight[key1] = 1
                    edge_weight[key2] = 1


# start write to edge_weight.txt
print("Writing to edge_weight.txt...")
for row in edge_weight.items():
    weight = float(row[1]) / int(actor_numOfMovie[str(row[0][0])])
    if weight > 1:
        raise ValueError("Error: weight is bigger than 1")
    file_edge_weight.write(str(row[0][0]) + "\t\t" + str(row[0][1]) + "\t\t" + str(weight) + "\n")


# close all files
file_edge_weight.close()
file_movie_actors.close()
file_merge.close()