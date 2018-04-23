library(igraph)

# (a) create network
num_node = 1000
p = 0.01
g = random.graph.game(num_node, p, directed=FALSE)
plot(g)

# (b) random walk
netrw = function(g, steps, node_start){
    curr = node_start
    distance = c()
    if (length(neighbors(g, curr)) == 0){
        distance = c(distance, 0)
        return (distance)
    }
    while (length(distance) < steps){
        if (length(neighbors(g, curr)) == 1){
            curr = neighbors(g,curr)
            distance = c(distance, distances(g, v=node_start, to=curr))
        } 
        else{
            curr = sample(neighbors(g,curr), 1)
            distance = c(distance, distances(g, v=node_start, to=curr))
        }
    }
    return (distance)
}

len_max = 0
num = 250
steps = 200
dist_list = array(0, c(num, steps))

for (i in (1:num)){
    node_start = sample((1:num_node), 1)
    distance = netrw(g, steps, node_start)
    dist_len = length(distance)
    len_max = max(len_max, dist_len)
    if (dist_len != 0){
        dist_list[i, 1:dist_len] = distance
    }
}

avg = rep(NA, len_max)
std = rep(NA, len_max)
for (t in (1:len_max)){
    s = dist_list[, t]
    s = s[s!=0]
    avg[t] = mean(s)
    std[t] = sd(s)
}

plot((1:length(avg)), avg, xlab="Number of Steps", ylab="Average Distance", type="o", col="blue")

plot((1:length(std)), std, xlab="Number of Steps", ylab="Standard Deviation", type="o", col="blue")

# (c) degree distribution
netrw_degree = function(g, steps, node_start){
    curr = node_start
    distance = c()
    if (length(neighbors(g, curr)) == 0){
        return (curr)
    }
    while (length(distance) < steps){
        if (length(neighbors(g, curr)) == 1){
            curr = neighbors(g,curr)
            distance = c(distance, distances(g, v=node_start, to=curr))
        } 
        else{
            curr = sample(neighbors(g,curr), 1)
            distance = c(distance, distances(g, v=node_start, to=curr))
        }
    }
    return (curr)
}

deg = c()
for (i in (1:num)){
    node_start = sample((1:num_node), 1)
    node_end = netrw_degree(g, steps, node_start)
    deg = c(deg, degree(g, node_end))
}

h = hist(deg, breaks=seq(-0.5, by=1 , length.out=max(deg)+3), xlab="Degree", ylab="Frequency", main="End node degree")
plt = data.frame(x = h$mids, y = h$density)
plot(plt, xlab = "Degree", ylab = "Frequency", type="o", col="blue", main="End node degree")
plot(degree.distribution(g), xlab = "Degree", ylab = "Frequency", type="o", col="blue", main="Graph degree")

#deg_g = degree(g, c(1:num_node))
#h_g = hist(deg_g, breaks=seq(-0.5, by=1 , length.out=max(deg_g)+3), xlab='Degree', ylab='Frequency', main='Graph degree')


# (d) repeat (b) with 100 and 10000 nodes
# see next .r file