#sublist: [sum, total calls, mean]
import random
import math

def bandit(testNum, armIdx, pullVal):
    global TENARM, UCB, EPSILON
    if testNum == 0:
        TENARM = [[0.0,1.0,0.0] for i in range(10)]
        UCB = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
        EPSILON = 0.1
        return 0
    if testNum<10:
        TENARM[armIdx][0]+=pullVal
        TENARM[armIdx][1]+=1
        TENARM[armIdx][2]=TENARM[armIdx][0]/TENARM[armIdx][1]
        for i in range(len(UCB)):
            UCB[i] = TENARM[i][2] + .8 * math.sqrt(((math.log(testNum)) / (TENARM[i][1])))
        return (armIdx+1)%10
    else: 
        TENARM[armIdx][0]+=pullVal
        TENARM[armIdx][1]+=1
        TENARM[armIdx][2]=TENARM[armIdx][0]/(TENARM[armIdx][1])
        for i in range(len(UCB)):
            UCB[i] = TENARM[i][2] + .8 * math.sqrt(((math.log(testNum)) / (TENARM[i][1])))
        return UCB.index(max(UCB))

#Abhisheik Sharma 7 2024
