# Intro to AI project 2
# Nathan Borkholder


# Cost function J tolerance: 0.1
# • Maximum population size: 500
# • Maximum number of generations: 1200
# • Maximum execution time: 7 min

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp


class Individual:
    def __init__(self, x, y, headAng, v, gamas, betas):
        self.x = x
        self.y = y
        self.headAng = headAng
        self.v = v
        self.gamas = gamas
        self.betas = betas
        self.stateHistory = []
        self.fitness = 0
        self.cost = 0
        self.infeasible = False

    def calcNewVals(self, gamma, beta, timestep):
        self.x = self.x + (self.v * np.cos(self.headAng)) * timestep
        self.y = self.y + (self.v * np.sin(self.headAng)) * timestep
        self.headAng = self.headAng + gamma * timestep
        self.v = self.v + beta * timestep

        if self.x <= -4 and not self.y > 3:
            self.infeasible = True
        elif (self.x > -4 and self.x < 4) and not self.y > -1:
            self.infeasible = True
        elif self.x >= 4 and not self.y > 3:
            self.infeasible = True

        state = [self.x, self.y, self.headAng, self.v]
        self.stateHistory.append(state)


POPSIZE = 200
GENS = 0
OPPARAM = 10
BINARYSIZE = 7
MUTATIONPROB = .005  # .5%
INFEASCONST = 200  # K


# function GENETIC-ALGORITHM(population, fitness) returns an individual
#   repeat
#       weights ← WEIGHTED-BY(population, fitness)
#       population2 ← empty list
#       for i = 1 to SIZE(population) do
#           parent1 , parent2 ← WEIGHTED-RANDOM-CHOICES(population,weights, 2)
#           child ← REPRODUCE(parent1, parent2 )
#           if (small random probability) then child ← MUTATE(child)
#           add child to population2
#       population ← population2
#   until some individual is fit enough, or enough time has elapsed
# return the best individual in population, according to fitness
#
# function REPRODUCE(parent1, parent2 ) returns an individual
#   n ← LENGTH(parent1)
#   c ← random number from 1 to n
#   return APPEND(SUBSTRING(parent1, 1, c), SUBSTRING(parent2, c + 1, n))

def GA(population):
    fitnessPercents = []
    fitnessTotal = 0
    for i in range(POPSIZE):
        fitnessTotal += population[i].fitness
    for i in range(POPSIZE):
        fitnessPercents.append((population[i].fitness / fitnessTotal))
    population2 = []
    population2.append(population[0])
    population2.append(population[1])
    population2.append(population[2])
    population2.append(population[3])
    halfPop = int(POPSIZE/2)
    for i in range(0, halfPop-2):
        parent1, parent2 = np.random.choice(population, 2, p=fitnessPercents)
        crossPoint = np.random.randint(1, 8)

        parent1LowG = parent1.gamas[0:crossPoint]
        parent1HighG = parent1.gamas[crossPoint:]
        parent1LowB = parent1.betas[0:crossPoint]
        parent1HighB = parent1.betas[crossPoint:]

        parent2LowG = parent2.gamas[0:crossPoint]
        parent2HighG = parent2.gamas[crossPoint:]
        parent2LowB = parent2.betas[0:crossPoint]
        parent2HighB = parent2.betas[crossPoint:]

        child1G = np.concatenate((parent1LowG, parent2HighG))
        child1B = np.concatenate((parent1LowB, parent2HighB))
        child2G = np.concatenate((parent2LowG, parent1HighG))
        child2B = np.concatenate((parent2LowB, parent1HighB))

        child1G = Mutation(child1G, True)
        child1B = Mutation(child1B, False)
        child2G = Mutation(child2G, True)
        child2B = Mutation(child2B, False)

        population2.append(Individual(0, 8, 0, 0, child1G, child1B))
        population2.append(Individual(0, 8, 0, 0, child2G, child2B))

    return population2



# passes in the list of gamma or beta values.
# if gamma then true, if beta than false
def Mutation(list, type):
    newList = []
    for i in list:
        if type:
            b = ConvertToBinaryG(i)
        else:
            b = ConvertToBinaryB(i)
        b2 = ""
        for j in b:
            mutate = np.random.choice([1, 2], 1, p = [.995, .005])
            if mutate == 2:
                if j == 0:
                    b2 += '1'
                else:
                    b2 += '0'
            else:
                b2 += j
        if type:
            d = ConvertFromBinaryB(b2)
        else:
            d = ConvertFromBinaryG(b2)
        newList.append(d)
    return newList


def EulerCalc(index, population):
    # interpolate math
    x = np.arange(10)
    gammas = population[index].gamas
    betas = population[index].betas
    betasCubic = sp.interpolate.CubicSpline(x, betas, bc_type='natural')
    gammasCubic = sp.interpolate.CubicSpline(x, gammas, bc_type='natural')
    betas_x = np.linspace(0, 10, 100)
    gammas_x = np.linspace(0, 10, 100)
    betas_y = betasCubic(betas_x)
    gammas_y = gammasCubic(gammas_x)

    # uses interpolated values for euler calculations
    timestep = .1
    for i in range(100):
        population[index].calcNewVals(gammas_y[i], betas_y[i], timestep)


# calculates the cost function for a given individual
# Final state is [0 0 0 0] so there is no need to subtract in the square root
def CostCalc(index, population):
    if population[index].infeasible:
        j = INFEASCONST
        population[index].cost = j
    else:
        x = np.square(population[index].x)
        y = np.square(population[index].y)
        headingAng = np.square(population[index].headAng)
        v = np.square(population[index].v)

        j = np.sqrt(x + y + headingAng + v)
        population[index].cost = np.abs(j)


def FitnessCost(index, population):
    j = population[index].cost
    population[index].fitness = 1 / (j + 1)


def ConvertToBinaryG(value):
    lb = -0.524
    R = .524 * 2
    d = ((value - lb) * (2 ** BINARYSIZE - 1)) / R
    d = int(d)
    binary = '{0:07b}'.format(d)
    return binary


def ConvertFromBinaryG(d):
    d = int(d, 2)
    lb = -0.524
    R = .524 * 2

    value = (d / (2 ** BINARYSIZE - 1)) * R + lb
    return value


def ConvertToBinaryB(value):
    lb = -5.0
    R = 5.0 * 2
    d = ((value - lb) * (2 ** BINARYSIZE - 1)) / R
    d = int(d)
    binary = '{0:07b}'.format(d)
    return binary


def ConvertFromBinaryB(d):
    d = int(d, 2)
    lb = -5.0
    R = 5.0 * 2

    value = (d / (2 ** BINARYSIZE - 1)) * R + lb
    return value


# the sort function to determine the lowest cost.
def sortFunc(i):
    return i.fitness


def main():
    generation = 0
    population = []
    for i in range(POPSIZE):
        gamas = np.random.uniform(low=-0.524, high=0.524, size=OPPARAM)
        betas = np.random.uniform(low=-5, high=5, size=OPPARAM)
        population.append(Individual(0, 8, 0, 0, gamas, betas))
        EulerCalc(i, population)
        CostCalc(i, population)
        FitnessCost(i, population)
    generation += 1
    population.sort(key=sortFunc, reverse=True)
    print("Generation ", generation, " : J = ", population[0].cost)
    while (population[0].cost >= .1):
        population = GA(population)
        generation += 1
        population.sort(key=sortFunc, reverse=True)
        print("Generation ", generation, " : J = ", population[0].cost)

    return None


if __name__ == '__main__':
    main()
