# Genetic-Algorithm-Python-Implementation
This repo contains a python implementation of a genetic algorithm commonly known as GA

Requirements/Pre-requisites
Python3

Python Libraries needed
NumPy
scipy
math
heapq
tkinter
time


Run:
Just execute the file GA.py and it will show the best found path at the end in form of GUI.

Parameters to change 

m, n: to change the dimension of plane mxn (Kindly keep m and n similar) min value 5x5
popSize : to change the size of population
numberOfParentsForCrossover: number of parents to chose for crossover
obs: number of obstecles in path
crosspoint: single point crossover is implemented. One thing that done is to choose random point in single point crossover
iterations: number of itrations to go through. as limit condition is not implemented
mutationRate: mutation probability (0.0 - 1.0) two types of mutataion is implemeted but using one
candidatesToPick: how many candidated to pick for tournament selection
targetX: target coordinate X
targetY: target coordinate Y
