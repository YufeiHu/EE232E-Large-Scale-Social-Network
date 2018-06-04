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


creat_edgelist <- function(movie_id_list) {
    # build the edgelist for bipartite graph
    movie_actors_file = file("movie_actors.txt", open="r")
    line = readLines(movie_actors_file, 1, encoding="latin1")

    # index of movie_id_list
    idx = 1

    # edgelist
    movie_id_edge = c()
    actor_id_edge = c()

    while(length(line) != 0) {    
        line = strsplit(line,"\t\t")
        movie_id = line[[1]][2]
    
        if (movie_id == movie_id_list[idx]) {
            actor_id = line[[1]][3:length(line[[1]])]
            movie_id_edge = c(movie_id_edge, rep(paste("m_id",movie_id),
                                              length(actor_id)))
            actor_id_edge = c(actor_id_edge, actor_id)
            idx = idx + 1
        }

        if (idx > length(movie_id_list)) {
            break
        }
        line = readLines(movie_actors_file, 1, encoding="latin1")
    } 
    close(movie_actors_file)
    list(actor_id_edge, movie_id_edge)
}


build_bipartite_graph <- function(actor_id_edge, movie_id_edge) {
    # build the bipartite graph
    edge_df = data.frame(actor_id_edge, movie_id_edge)
    g.bi = graph_from_data_frame(edge_df)
    V(g.bi)$type = V(g.bi)$name %in% actor_id_edge
    g.bi
}

plot_bipartite_graph <- function(bipartite_graph, vsize=6) {
    l = layout_as_bipartite(bipartite_graph)
    plot(bipartite_graph, layout=l[, c(2,1)], vertex.size= vsize, asp=0, 
         vertex.label=NA)    
}

c(2541, 61140, 86386)
edgelist = creat_edgelist(c(2541, 61140, 86386))
actor_id_edge = edgelist[[1]]
movie_id_edge = edgelist[[2]]

g.bi = build_bipartite_graph(actor_id_edge, movie_id_edge)
plot_bipartite_graph(g.bi)

find_actors_movies <- function(actor_list){
    score = rep(0, length(actor_list))
    for (i in length(actor_list)){
        movies = file("actor_movies_merged.txt", open="r")
        r_line = readLines(movies, 1, encoding="latin1")
        while (length(r_line) != 0){
            rline = strsplit(r_line, "\t\t")
            if (actor_list[i] == rline[[1]][1]){
                rline_len = length(rline[[1]])
                tmp = rline[[1]][2:rline_len]
                for (j in tmp){
                    nodeId_now = (1:vcount(g))[V(g)$movie_name == j]
                    score[i] = score[i] + as.numeric(Rate[nodeId_now])/rline_len
                }
                break
            }
            r_line = readLines(movies, 1, encoding="latin1")
        }
        close(movies)
    }    
}

edgelist1 = creat_edgelist(c(2541))
actor_id_edge1 = edgelist1[[1]]

edgelist2 = creat_edgelist(c(61140))
actor_id_edge2 = edgelist1[[1]]

edgelist3 = creat_edgelist(c(86386))
actor_id_edge3 = edgelist1[[1]]


pre1 = mean(find_actors_movies(actor_id_edge_1))
pre2 = mean(find_actors_movies(actor_id_edge_2))
pre3 = mean(find_actors_movies(actor_id_edge_3))