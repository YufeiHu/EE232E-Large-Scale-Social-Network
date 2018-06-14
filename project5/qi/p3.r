library('igraph')

#reference: Younan Liang
#get stock list
Name_sector = read.csv("finance_data_cleaned/Name_sector.csv", stringsAsFactors=FALSE) 

#get ids
stock_ids = Name_sector$Symbol
ri = matrix(list(), length(stock_ids), 2)
P = data.frame(A=character(), B=character(), C=numeric(), stringsAsFactors=FALSE) 
colnames(P) = c("Node1", "Node2", "weight")

#look into each stock
idx = 1
dirty = 0
for(i in stock_ids){
    ri[[idx,1]] = i

    #get close price for each stock
    close = read.csv(paste('finance_data/data/', i, '.csv', sep=""), 
        stringsAsFactors = FALSE)$Close 
    ri_tmp = numeric(0)
    for (j in 2:length(close)){
        #ri
        ri_tmp[j-1] = log(close[j]) - log(close[j-1])
    }
    ri[[idx,2]] = ri_tmp

    #check length and discard some data
    if (length(ri_tmp) != 764){
      cat("to be cleaned", i,  "\n")
      dirty = dirty + 1
    }

    idx = idx + 1
}

dirty

#graph
edge_idx = 1
w_ij = numeric()
for(i in 1 : (length(stock_ids) - 1)){
    for(j in (i+1) : length(stock_ids)){
        P[edge_idx, 1] = stock_ids[i] 
        P[edge_idx, 2] = stock_ids[j]

        mean_i = mean(ri[[i,2]])
        mean_j = mean(ri[[j,2]])
        sqr_mean_i = mean(ri[[i,2]]^2) 
        sqr_mean_j = mean(ri[[j,2]]^2)

        #correlation
        p_ij = (mean(ri[[i,2]] * ri[[j,2]]) - mean_i * mean_j) / sqrt((sqr_mean_i - mean_i^2) * (sqr_mean_j - mean_j^2))
        wij_curr = sqrt(2 * (1 - p_ij))

        P[edge_idx, 3] = wij_curr
        
        w_ij = c(w_ij, wij_curr)
        edge_idx = edge_idx + 1
    }
}

g1 = graph.data.frame(P, directed = FALSE)

#get stock names
sector = Name_sector$Sector
color = rep(0, length(sector))

#assign color for different sectors
color_idx = 1
for(i in unique(sector)){
    color[which(sector == i)] = color_idx 
    color_idx = color_idx + 1
}

#plot MST
plot(mst(g1, weights = P$weight), vertex.color = color, vertex.label = NA, vertex.size = rep(5, length(sector)), main = "MST")
