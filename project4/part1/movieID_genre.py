# @author: Yufei Hu
import sys
from collections import OrderedDict


# initializations
file_movie_genre = open("movie_genre.txt", "r")
file_movie_actors = open("movie_actors.txt", "r")
file_movieID_genre = open("movieID_genre.txt", "w")

movieID_dict = OrderedDict()
movieGenre_dict = dict()


# main
def progressBar(start, end, bar_length=20):
    percent = float(start) / end
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write("\r[{0}] {1}% [{2}/{3}]".format(arrow + spaces, int(round(percent * 100)), start, end))
    sys.stdout.flush()


for line1 in file_movie_actors.readlines():
    line1 = line1[:-1]
    line1_list = line1.split("\t\t")
    movie1_name = line1_list[0]
    movie1_ID = line1_list[1]
    movieID_dict[movie1_name] = movie1_ID


for line2 in file_movie_genre.readlines():
    line2 = line2[:-1]
    line2_list = line2.split("\t\t")
    movie2_name = line2_list[0]
    movie2_genre = line2_list[1]
    movieGenre_dict[movie2_name] = movie2_genre


i = 0
for row in movieID_dict.items():

    progressBar(i, 203562)
    i += 1

    movie_name = row[0]
    movie_ID = row[1]

    if movie_name in movieGenre_dict:
        file_movieID_genre.write(movie_name + "\t\t" + movie_ID + "\t\t" + movieGenre_dict[movie_name] + "\n")
    else:
        file_movieID_genre.write(movie_name + "\t\t" + movie_ID + "\t\t" + "None" + "\n")


# close all files
file_movie_genre.close()
file_movie_actors.close()
file_movieID_genre.close()