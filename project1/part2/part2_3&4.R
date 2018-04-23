library(igraph)
# 3a

g = barabasi.game(n=1000, m=4,  directed=T)
pr1 <- page_rank(g, directed = TRUE, damping = 1)$vector
d1<-degree(g)
d2<-degree(g, mode = "in")
plot(pr1, xlab="index", ylab="probability",  main = "probability distrubution",type="o", col="blue")
plot(d1, xlab="index", ylab="degree",  main = "degree distrubution",type="o", col="blue")

sum(pr1*d1)/sqrt(sum(pr1^2)*sum(d1^2)) #consine similarity
sum(pr1*d2)/sqrt(sum(pr1^2)*sum(d2^2)) #consine similarity

# 3b
pr2 <- page_rank(g, directed = TRUE, damping = 0.85)$vector
plot(pr2, xlab="index", ylab="probability",  main = "probability distrubution",type="o", col="blue")
sum(pr2*d1)/sqrt(sum(pr2^2)*sum(d1^2)) #consine similarity
sum(pr2*d2)/sqrt(sum(pr2^2)*sum(d2^2)) #consine similarity

# 4a
pr3 <- page_rank(g, directed = TRUE, damping = 0.85, personalized=pr1)$vector
plot(pr3, xlab="index", ylab="probability", main = "probability distrubution",type="o", col="blue")
sum(pr3*pr2)/sqrt(sum(pr3^2)*sum(pr2^2)) #consine similarity
#compare the top values
head(pr2,10)
head(pr3,10)
# 4b

index<-head(which(pr2==median(pr2,2)),2)
op = array(0,1000)
for( i in index){
  op[i] = 1/2
}
index
pr2[index[1]]
pr2[index[2]]
pr4<-page_rank(g, directed = TRUE, damping = 0.85, personalized=op)$vector
plot(pr4, xlab="index", ylab="probability", type="o",  main = "probability distrubution",col="blue")
pr4[index[1]]
pr4[index[2]]
