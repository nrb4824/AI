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
MUTATIONPROB = .005  #.5%
INFEASCONST = 200  #K
INDIVIDUALS = []

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
    fitness = []
    for i in range(POPSIZE):
        fitness.append(population[i].fitness)
    population2 = []
    for i in range(1,POPSIZE):
        parent1, parent2 = np.random.choices(population, fitness, k = 2)
        crossPoint = np.random.randint(1, 8)

        parent1LowG = parent1.gamas[0:crossPoint]
        parent1HighG = parent1.gamas[crossPoint:]
        parent1LowB = parent1.betas[0:crossPoint]
        parent1HighB = parent1.betas[crossPoint:]

        parent2LowG = parent2.gamas[0:crossPoint]
        parent2HighG = parent2.gamas[crossPoint:]
        parent2LowB = parent2.betas[0:crossPoint]
        parent2HighB = parent2.betas[crossPoint:]

        child1G = parent1LowG + parent2HighG
        child1B = parent1LowB + parent2HighB
        child2G = parent2LowG + parent1HighG
        child2B = parent2LowB + parent1HighB

        Mutation(child1G)
        Mutation(child1B)
        Mutation(child2G)
        Mutation(child2B)

        population2.append(Individual(0, 8, 0, 0, child1G, child1B))
        population2.append(Individual(0, 8, 0, 0, child2G, child2B))

        # TODO add elitism.

    return population2

def Mutation(list):
    for i in list:
        for j in i:
            mutate = np.random.choice([1,2],[95.5,.5], k=1)
            if mutate == 2:
                if j == 0:
                    j = 1
                else:
                    j = 0

def EulerCalc(index):

    #interpolate math
    x = np.arange(10)
    gammas = INDIVIDUALS[index].gamas
    betas = INDIVIDUALS[index].betas
    betasCubic = sp.interpolate.CubicSpline(x, betas, bc_type='natural')
    gammasCubic = sp.interpolate.CubicSpline(x, gammas, bc_type='natural')
    betas_x = np.linspace(0,10,100)
    gammas_x = np.linspace(0,10,100)
    betas_y = betasCubic(betas_x)
    gammas_y = gammasCubic(gammas_x)

    #uses interpolated values for euler calculations
    timestep = .1
    for i in range(100):
        INDIVIDUALS[index].calcNewVals(gammas_y[i], betas_y[i], timestep)

#calculates the cost function for a given individual
#Final state is [0 0 0 0] so there is no need to subtract in the square root
def CostCalc(index):
    if INDIVIDUALS[index].infeasible:
       j = INFEASCONST
       INDIVIDUALS[index].cost = j
    else:
        x = np.square(INDIVIDUALS[index].x)
        y = np.square(INDIVIDUALS[index].y)
        headingAng = np.square(INDIVIDUALS[index].headAng)
        v = np.square(INDIVIDUALS[index].v)

        j = np.sqrt(x + y + headingAng + v)
        INDIVIDUALS[index].cost = np.abs(j)

def FitnessCost(index):
    j = INDIVIDUALS[index].cost
    INDIVIDUALS[index].fitness = 1/(j+1)

def ConvertToBinaryG(value):
    lb = -0.524
    R = .524*2
    d = ((value - lb)*(2**BINARYSIZE - 1))/R
    d = int(d)
    binary = '{0:07b}'.format(d)
    return binary


def ConvertFromBinaryG(d):
    print(d)
    d = int(d,2)
    lb = -0.524
    R = .524*2

    value = (d/(2**BINARYSIZE - 1))*R + lb
    return value

# the sort function to determine the lowest cost.
def sortFunc(i):
    return i.fitness

def main():
    for i in range(POPSIZE):
        gamas = np.random.uniform(low=-0.524, high=0.524, size=OPPARAM)
        betas = np.random.uniform(low=-5, high=5, size=OPPARAM)
        INDIVIDUALS.append(Individual(0, 8, 0, 0, gamas, betas))
        EulerCalc(i)
        CostCalc(i)
        FitnessCost(i)

    INDIVIDUALS.sort(key=sortFunc, reverse=True)
    while(INDIVIDUALS[0].cost >= .1):
        INDIVIDUALS = GA(INDIVIDUALS)

    return None



if __name__ == '__main__':
    main()
