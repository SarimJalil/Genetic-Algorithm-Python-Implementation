import numpy as np
from scipy.spatial import distance as ED
from math import ceil
import heapq
from tkinter import *
import time


m = 10
n = 10
popSize = 500
numberOfParentsForCrossover = 20
obs = n*2
crosspoint = np.random.randint(1, m/2 -1)  
iterations = 200
obstacles = np.random.uniform(0,m,(1,obs,2))
population = np.random.uniform(0,m,(popSize,n,2))
mutationRate = 0.3
candidatesToPick = 20
targetX = n
targetY = m

for i in range(0,popSize):
    population[i][0] = [0,0]
    population[i][n-1] = [targetX,targetY]

def calculatePenalty(p1, p2):
    penalty = 0
    
    for i in range(0, n):
        crossproduct = (obstacles[0][i][1] - p1[1]) * (p2[0] - p1[0]) - (obstacles[0][i][0] - p1[0]) * (p2[1] - p1[1])
        if(abs(crossproduct) > sys.float_info.epsilon):
            penalty = penalty + 1
    

    return penalty


def internalMutation(childs):
    for i in range(0, len(childs)):
        value = np.random.uniform(0,1);
        if value < mutationRate:
            for j in range(1, m-1):
                # print(childs[i][j])
                childs[i][j][0] = np.random.uniform(0,m)
                childs[i][j][1] = np.random.uniform(0,m)
    
def externalMutation(childs):
    for i in range(0, len(childs)):
        value = np.random.uniform(0,1);
        if value < mutationRate:
            randIndex1 = np.random.randint(1,m-1)
            randIndex2 = np.random.randint(1,m-1)
            temp = childs[i][randIndex1]
            childs[i][randIndex1] = childs[i][randIndex2]
            childs[i][randIndex2] = temp 

def calculateFitness(pop, size, end):
    fitness = []
    distance = 0.0
    for i in range(0,size):
        for j in range(0,end-1):
            distance += ED.euclidean(pop[i][j],pop[i][j+1])
            distance = distance + calculatePenalty(pop[i][j],pop[i][j+1]) * 3
        # print("\n Row change: \n")
        fitness.append(ceil(distance))
        distance = 0
    return fitness

def singlePointCrossover(parents, point, replace, popFit):
    childs = []
    for j in  range(0, numberOfParentsForCrossover - 1):
        child_1 = []
        # child_2 = []
        # print("-----------------j----------------")
        # print(j)
        # print("-----------------i----------------")
        for i in range(0,m):
            # print(i)
            if(i <= point):
                child_1.append([parents[j][i][0], parents[j][i][1]])
                # child_2.append([parents[j+1][i][0], parents[j+1][i][1]])
            if(i > point):
                child_1.append([parents[j+1][i][0], parents[j+1][i][1]])
                # child_2.append([parents[j][i][0], parents[j][i][1]])
        childs.append(child_1)
        # internalMutation(childs)
        externalMutation(childs)
        # childs.append(child_2)
        # print("Child 1: ")
        # print(child_1)
        # print("Child 2: ")
        # print(child_2)
    
   
    
    childFitness = calculateFitness(childs, len(childs), m)
    # print("Childs")
    # print(childs)
    # print(childFitness)

    # print("Child 1 Fitness")
    # print(childFitness[0])
    # print("Child 2 Fitness")
    # print(childFitness[1])

    # print("Replace 1 Fitness")
    # print(popFit[replace[0]])

    # print("Replace 2 Fitness")
    # print(popFit[replace[1]])
    # print(len(replace))
    # print(childFitness)
    for i in range(0, len(childFitness)):
        if(childFitness[i] < popFit[replace[i]]):
            population[replace[i]] = childs[i]



def tournamentSelection(fitness, parents):
    for i in range(0, numberOfParentsForCrossover):
        temp = []
        indexes = []
        for j in range(0, candidatesToPick):
            num = np.random.randint(1, popSize-1)
            indexes.append(num)
            temp.append(fitness[num])
        parents.append(population[indexes[temp.index(min(temp))]])
        
    
# print(population)
for i in  range(0, iterations):
    fit = calculateFitness(population, popSize, m)
    parents = []
    tournamentSelection(fit, parents)
    # parents = heapq.nsmallest(numberOfParentsForCrossover, range(len(fit)), key=fit.__getitem__)
    replace = heapq.nlargest(numberOfParentsForCrossover, range(len(fit)), key=fit.__getitem__)
   
    print("Fitness")
    print(fit)

    # print("parent 1 Fitness")
    # print(fit[parents[0]])

    # print("Parent 2 Fitness")
    # print(fit[parents[1]])

    # crossoverParents = []
    # crossoverReplace = [] 
    # for i in range(0, numberOfParentsForCrossover):
    #     crossoverParents.append(population[parents[i]])

    # print("Parents: ")
    # print(parents)
    singlePointCrossover(parents, crosspoint, replace, fit)

fit = calculateFitness(population, popSize, m)
best = heapq.nsmallest(1, range(len(fit)), key=fit.__getitem__)

bestPath = population[best]
# print("Obstacles: ")
# print(obstacles)

root = Tk()
root.geometry('400x400')

c = Canvas(root, height= 400, width= 400, bg= "#49A")

multiplier = 400/n

for i in range(0, n):
    c.create_line(i*multiplier,0,i*multiplier,400)

for i in range(0, n):
    c.create_line(0,i*multiplier,400,i*multiplier)


c.create_rectangle((0) * multiplier,0 * multiplier,0.2 * multiplier,0.2 * multiplier, fill = "blue")
c.create_rectangle((targetX-0.2) * multiplier,(targetY-0.2) * multiplier,targetX * multiplier,targetY * multiplier, fill = "green")


for j in range(0, obs):
    c.create_rectangle((obstacles[0][j][1] -0.1) * multiplier,(obstacles[0][j][0] -0.1) * multiplier,obstacles[0][j][1] * multiplier,obstacles[0][j][0] * multiplier, fill = "red")

# print(obstacles[0][3][0])
# print(obstacles[0][3][1])

for i in range(0, m-1):
    c.create_line(bestPath[0][i][0] * multiplier ,bestPath[0][i][1] * multiplier , bestPath[0][i+1][0] * multiplier ,bestPath[0][i+1][1] * multiplier, fill = "white" )

# print("Population: ")
# print(population)
# time.sleep(5)

# c.delete('all')

c.pack()
root.mainloop()


# print("Obstacles: ")
# print(obstacles)
# print("Penalty: ")
# print(fitness)
# print(parents)
# print(fitness)

# input("Enter for exit: ")