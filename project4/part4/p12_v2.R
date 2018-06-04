library(igraph)

g = read.graph("movie_edge_weight.txt", format="ncol", directed=FALSE)

movie_name = file("movie_actors.txt", open="r")
r_line = readLines(movie_name, 1, encoding="latin1")
Name = rep("", vcount(g))
while(length(r_line) != 0)
{
    rline = strsplit(r_line, "\t\t")
    nodeId = (1:vcount(g))[V(g)$name == rline[[1]][2]]
    Name[nodeId] = rline[[1]][1]
    r_line = readLines(movie_name, 1, encoding="latin1")
} 
close(movie_name)

V(g)$movie_name = Name

#generate rating
File_rate = file("movie_rating.txt", open="r")
r_line = readLines(File_rate, 1, encoding="latin1")
nodeId1 = 0
Rate = rep("0", vcount(g))
while(length(r_line) != 0)
{
    rline = strsplit(r_line, "\t\t")
    nodeId1 = (1:vcount(g))[V(g)$movie_name == rline[[1]][1]]
    Rate[nodeId1] = rline[[1]][2]
    r_line = readLines(File_rate, 1, encoding="latin1")
} 
close(File_rate)

V(g)$rate = Rate