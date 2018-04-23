library('igraph')
library('Matrix')
library('pracma')

create_transition_matrix = function (g){
  
  # WARNING: make sure your graph is connected (you might input GCC of your graph)
  
  vs = V(g)
  n = vcount(g)
  adj = as_adjacency_matrix(g)
  adj[diag(rowSums(adj) == 0)] = 1  # handle if the user is using the function for networks with isolated nodes by creating self-edges
  z = matrix(rowSums(adj, , 1))
  
  transition_matrix = adj / repmat(z, 1, n)  # normalize to get probabilities
  
  return(transition_matrix)
}

random_walk = function (g, num_steps, start_node, transition_matrix = NULL){
  if(is.null(transition_matrix))
    transition_matrix = create_transition_matrix(g)
  
  v = start_node
  for(i in 1:num_steps){
    #fprintf('Step %d: %d\n', i, v)  # COMMENT THIS
    PMF = transition_matrix[v, ]
    v = sample(1:vcount(g), 1, prob = PMF)        
  }
  
  return(v)
}

g = barabasi.game(n=1000, m=4,  directed=T)
plot(degree(g,mode ="in"), xlab="index", ylab="in_degree",  col="blue")
m = create_transition_matrix(g)
num = 100000
steps = 200
prob = array(0,1000)
for (i in (1:num)){
  node_start = sample((1:1000), 1)
  v_last = random_walk(g, steps, node_start, m)
  prob[v_last]=prob[v_last]+1
}
prob = prob/num
plot(prob)
