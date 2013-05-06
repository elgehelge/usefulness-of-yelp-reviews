# Clear memory
rm(list=ls())

library("Matrix")
library("glmnet")

data = readMM("/Users/utdiscant/github/usefulness-of-yelp-reviews/data-exploration/python code/finalMatrix.mtx")

rows = dim(data)[1]
cols = dim(data)[2]

model1 = glmnet(data[,2:cols], data[,1], family="poisson", nlambda=5)

# 09:10