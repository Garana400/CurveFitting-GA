from random import random, uniform, randint
from bisect import bisect
import matplotlib.pyplot as plt
from time import time


def intializePOP():
    pop = [ [ uniform(-10,10) for _ in range(d+1) ] for _ in range(popSize) ]
    return pop


def calcFitness(chromo):
    #return meanSq = sum( (sum(point[0]**i * chromo[i] for i in range(len(chromo))) - point[1]) ** 2 for point in points  ) * 1/n   ## momken tsheel al function kolha w tseb al satr da, bs RIP readability and efficiency tehehehehehe 
    meanSq = 0
    for point in points:
        yCALC = 0
        for i in range(len(chromo)):
            yCALC += point[0]**i * chromo[i]
        meanSq += (yCALC-point[1])**2
    meanSq *= (1/n)
    return meanSq


def calcCumFitness():
    total = 0
    fitness = [calcFitness(i) for i in pop]
    cumFitness = []
    newCumFitness = []
    newTotal = 0
    cumFitness.append(0)
    for i in fitness:
        total+=i
        cumFitness.append(total)
    for i in range(len(cumFitness)):
        newCumFitness.append(total - cumFitness[i])
    del cumFitness
    return fitness, newCumFitness, total


def selection():
    ln = len(cumFitness)
    cumFitness.sort()
    for i in range(int(len(pop)/2)):
        x = randint(0,int(total))
        y = randint(0,int(total))
        yield ln - bisect(cumFitness, x)-1, ln - bisect(cumFitness, y)-1
          

def xoverNmutation(selected, g):
    for elem in selected:
        if random() <= 0.7:
            x = randint(1,d-1)
            a = pop[elem[0]][:x] + pop[elem[1]][x:]
            b = pop[elem[1]][:x] + pop[elem[0]][x:]
            if (calcFitness(a) + calcFitness(b)) < (fitness[elem[0]] + fitness[elem[1]]):
                pop[elem[0]] = a
                pop[elem[1]] = b
                
    for i in range(len(pop)):
        temp = pop[i].copy()
        for j in range(len(pop[i])):
            if random() <= 0.5:
                y = temp[j] -10
            else:
                y = 10 + temp[j]
            deltaI =  y * ( 1-random()**(1-g/gen)**uniform(0.5,5) )
            temp[j] += deltaI
            
        if calcFitness(temp) < fitness[i]:
            pop[i] = temp

        
if  __name__  ==  "__main__":
    popSize = 10000
    gen = 500
    t = int(input())
    for j in range(t):
        n, d = map(int, input().split())
        points = []
        for i in range(n):
            x, y = map(float, input().split())
            points.append((x, y))
        pop = intializePOP()
        mini = 1e9
        mini_index = -1
        z = time()
        for k in range(gen):
            fitness, cumFitness, total = calcCumFitness()
            m = min(fitness)
            if m < mini:
                mini = m
                mini_index = fitness.index(m)
            xoverNmutation(selection(), k)
        print(pop[mini_index])
        print("Error = ", mini)
        print(time()-z)
            
        
        
