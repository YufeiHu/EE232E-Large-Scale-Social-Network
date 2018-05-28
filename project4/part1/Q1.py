# @author: Yufei Hu


# user definition
min_movie = 10


# initializations
id = 0
file_actress = open("actress_movies.txt", "r")
file_actor = open("actor_movies.txt", "r")
file_merge = open("actor_movies_merged.txt", "w")
file_actor_id = open("actor_id.txt", "w")
movie_list = set()


# start preprocessing actress_movies
print('Preprocessing actresses...')
for line in file_actress.readlines():

    # the last element '\n' is removed
    line = line[:-1]

    # the first element is actor/actress name, followed by movie names
    name_movies = line.split("\t\t")

    # skip when movies are fewer than threshold
    if len(name_movies) < min_movie + 1:
        continue

    # write to id-name mapping file
    name_actor = name_movies[0]
    name_actor.strip(" ")
    name_actor.strip("\t")
    file_actor_id.write(name_actor + "\t\t" + str(id))
    file_actor_id.write("\n")

    # write to merged file
    file_merge.write(str(id))
    memo = list()
    for name_movie in name_movies[1:]:
        end = name_movie.find(")")
        name_movie = name_movie[:end+1]
        name_movie.strip(" ")
        name_movie.strip("\t")
        if name_movie not in memo:
            memo.append(name_movie)
            file_merge.write("\t\t")
            file_merge.write(name_movie)
            movie_list.add(name_movie)
    file_merge.write("\n")
    id += 1


# start preprocessing actor_movies
print('Preprocessing actors...')
for line in file_actor.readlines():

    # the last element '\n' is removed
    line = line[:-1]

    # the first element is actor/actress name, followed by movie names
    name_movies = line.split("\t\t")

    # skip when movies are fewer than threshold
    if len(name_movies) < min_movie + 1:
        continue

    # write to id-name mapping file
    name_actor = name_movies[0]
    name_actor.strip(" ")
    name_actor.strip("\t")
    file_actor_id.write(name_actor + "\t\t" + str(id))
    file_actor_id.write("\n")

    # write to merged file
    file_merge.write(str(id))
    memo = list()
    for name_movie in name_movies[1:]:
        end = name_movie.find(")")
        name_movie = name_movie[:end+1]
        name_movie.strip(" ")
        name_movie.strip("\t")
        if name_movie not in memo:
            memo.append(name_movie)
            file_merge.write("\t\t")
            file_merge.write(name_movie)
            movie_list.add(name_movie)
    file_merge.write("\n")
    id += 1


# close all files
file_actress.close()
file_actor.close()
file_merge.close()
file_actor_id.close()
print("There are {} actors/actresses and {} unique movies".format(id, len(movie_list)))
# ans = 113132, 468150