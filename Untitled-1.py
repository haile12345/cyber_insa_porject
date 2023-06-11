#   Created by Elshad Karimov 
#   Copyright © AppMillers. All rights reserved.

# House Robber Problem  in Python

def houseRobber(val,i=0,k=0): 
    if val[i][k] == 1:
        return
    if i<2:
        val[i][k]=1
        houseRobber(val,i+1,k) 
    if k<2:
        val[i][k]=1
        houseRobber(val,i,k-1)
    if k>=1:
        val[i][k]=1
        houseRobber(val,i,k-1)
    if i>=1:
        val[i][k]=1
        houseRobber(val,i-1,k)

lists =[[0,0,0],
       [0,1,1],
       [0,1,0]]
houseRobber(lists)
print(lists)

