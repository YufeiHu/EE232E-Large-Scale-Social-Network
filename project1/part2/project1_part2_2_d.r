library(igraph)

# (d) repeat (b) with 100 and 10000 nodes
num_node = 10000
m = 1
g = barabasi.game(num_node, m, directed=FALSE)

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
