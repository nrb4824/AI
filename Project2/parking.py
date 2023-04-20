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

def GA(population, fitness):
    return None

def EulerCalc(index):
    x = np.arange(10)
    #cs = sp.interpolate.CubicSpline(x, INDIVIDUALS[index].betas, bc_type=((1, -.524), (2, .524)))
    cs = sp.interpolate.CubicSpline(x, INDIVIDUALS[index].betas, bc_type='natural')
    #cs = sp.interpolate.splrep(INDIVIDUALS[index].gamas, s=0)
    #array = sp.interpolate.splev(x, cs)
    for i in range(100):
        print(cs(i/10))
    # timestep = .1
    # for i in range(OPPARAM):
    #     gamma = INDIVIDUALS[index].gamas[i]
    #     beta = INDIVIDUALS[index].betas[i]
    #     for t in range(10):
    #         INDIVIDUALS[index].calcNewVals(gamma, beta, timestep)

#calculates the cost function for a given individual
#Final state is [0 0 0 0] so there is no need to subtract in the square root
def CostCalc(index):
    if INDIVIDUALS[index].infeasible:
       j = INFEASCONST
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

def main():
    for i in range(POPSIZE):
        gamas = np.random.uniform(low=-0.524, high=0.524, size=OPPARAM)
        betas = np.random.uniform(low=-5, high=5, size=OPPARAM)
        INDIVIDUALS.append(Individual(0, 8, 0, 0, gamas, betas))
        print("help")
        EulerCalc(i)
        CostCalc(i)



    return None



if __name__ == '__main__':
    main()
