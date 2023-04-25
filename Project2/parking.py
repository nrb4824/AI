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
        # elif self.y > 25:
        #     self.infeasible = True

        state = [self.x, self.y, self.headAng, self.v]
        self.stateHistory.append(state)


POPSIZE = 500
GENS = 0
OPPARAM = 10
BINARYSIZE = 7
MUTATIONPROB = .005  # .5%
INFEASCONST = 200  # K

def GA(population):
    fitnessPercents = []
    fitnessTotal = 0
    #find fitness total for percentages
    for i in range(POPSIZE):
        fitnessTotal += population[i].fitness

    #calculate fitness percents and store in array
    for i in range(POPSIZE):
        fitnessPercents.append((population[i].fitness / fitnessTotal))

    #add best 4 individuals to next generation (elitism)
    population2 = [population[0], population[1], population[2], population[3]]
    halfPop = int(POPSIZE/2)

    #generate children creates 196 individuals
    for i in range(0, halfPop-2):
        #generates 2 parents based on fitness percents
        parent1, parent2 = np.random.choice(population, 2, p=fitnessPercents)
        #cross point randomly chosen
        crossPoint = 0
        crossPoint2 = 0
        while crossPoint == crossPoint2:
            val1 = int(np.random.randint(1,8))
            val2 = int(np.random.randint(1, 8))
            if val1 > val2:
                crossPoint2 = val1
                crossPoint = val2

            else:
                crossPoint2 = val2
                crossPoint = val1

        #creates seperate arrays for the crosspoints for each parent
        parent1LowG = parent1.gamas[0:crossPoint]
        parent1MidG = parent1.gamas[crossPoint:crossPoint2]
        parent1HighG = parent1.gamas[crossPoint2:]

        parent1LowB = parent1.betas[0:crossPoint]
        parent1MidB = parent1.betas[crossPoint:crossPoint2]
        parent1HighB = parent1.betas[crossPoint2:]

        parent2LowG = parent2.gamas[0:crossPoint]
        parent2MidG = parent2.gamas[crossPoint:crossPoint2]
        parent2HighG = parent2.gamas[crossPoint2:]

        parent2LowB = parent2.betas[0:crossPoint]
        parent2MidB = parent2.betas[crossPoint: crossPoint2]
        parent2HighB = parent2.betas[crossPoint2:]

        #combines the arrays to create the children
        child1G = np.concatenate((parent1LowG, parent2MidG, parent1HighG))
        child1B = np.concatenate((parent1LowB, parent2MidB, parent1HighB))
        child2G = np.concatenate((parent2LowG, parent1MidG, parent2HighG))
        child2B = np.concatenate((parent2LowB, parent1MidB, parent2HighB))

        #applys mutation on children
        child1G = Mutation(child1G, True)
        child1B = Mutation(child1B, False)
        child2G = Mutation(child2G, True)
        child2B = Mutation(child2B, False)

        #add the children to the population
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
        #loops through each bit and if mutated flips the bit
        b2 = ""
        for j in b:
            mutate = np.random.choice([1, 2], 1, p=[1-MUTATIONPROB, MUTATIONPROB])
            if mutate == 2:
                if j == 0:
                    b2 += '1'
                else:
                    b2 += '0'
            #otherwise add the bit back into the string
            else:
                b2 += j
        #checks to make sure mutation isn't out of bounds
        if type:
            d = ConvertFromBinaryG(b2)
            if d > .524:
                d = .524
            elif d < -.524:
                d = -.524
        else:
            d = ConvertFromBinaryB(b2)
            if d > 5:
                d = 5
            elif d < -5:
                d = -5
        newList.append(d)
    return newList


def EulerCalc(index, population):
    #resets individuals from previous generation
    if population[index].cost == 0:
        # interpolate math
        x = np.arange(10)
        gammas = population[index].gamas
        betas = population[index].betas
        betasCubic = sp.interpolate.CubicSpline(x, betas, bc_type='natural')
        gammasCubic = sp.interpolate.CubicSpline(x, gammas, bc_type='natural')
        betas_x, step = np.linspace(0, OPPARAM-1, 100, retstep=True)
        gammas_x = np.linspace(0, OPPARAM-1, 100)
        betas_y = betasCubic(betas_x)
        gammas_y = gammasCubic(gammas_x)

        # uses interpolated values for euler calculations
        for i in range(100):
            #checks against constraints
            if gammas_y[i] < -.524:
                gammas_y[i] = -.524
            elif gammas_y[i] > .524:
                gammas_y[i] = .524
            elif betas_y[i] < -5:
                betas_y[i] = -5
            elif betas_y[i] > 5:
                betas_y[i] = 5
            population[index].calcNewVals(gammas_y[i], betas_y[i], step)


# calculates the cost function for a given individual
# Final state is [0 0 0 0] so there is no need to subtract in the square root
def CostCalc(index, population):
    if population[index].cost == 0:
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
    if population[index].fitness == 0:
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
    return i.cost


def main():
    generation = 0
    population = []
    #generates intitial generation
    for i in range(POPSIZE):
        gamas = np.random.uniform(low=-0.524, high=0.524, size=OPPARAM)
        betas = np.random.uniform(low=-5, high=5, size=OPPARAM)
        population.append(Individual(0, 8, 0, 0, gamas, betas))
        EulerCalc(i, population)
        CostCalc(i, population)
        FitnessCost(i, population)
    generation += 1
    population.sort(key=sortFunc)
    print("Generation ", generation, " : J = ", population[0].cost, population[5].cost)

    #Use GA until cost is met.
    while (population[0].cost >= .1):
        population = GA(population)
        generation += 1
        for i in range(POPSIZE):
            EulerCalc(i, population)
            CostCalc(i, population)
            FitnessCost(i, population)
        population.sort(key=sortFunc)
        print("Generation ", generation, " : J = ", "1-5: ", population[0].cost, population[1].cost,population[2].cost,population[3].cost,population[4].cost, population[5].cost, " 20th:", population[20].cost)

    states = population[0].stateHistory
    xs = []
    ys = []
    headAngs = []
    vs = []
    for i in states:
        xs.append(i[0])
        ys.append(i[1])
        headAngs.append(i[2])
        vs.append(i[3])

    #solution trajectory graph
    obstaclesx = [-15, -4, -4, 4, 4, 15]
    obstaclesy = [3, 3, -1, -1, 3, 3]
    plt.plot(obstaclesx, obstaclesy, 'g')
    plt.plot(xs, ys, 'b')
    plt.title('Solution Trajectory')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

    hundredTime = np.arange(100)

    plt.plot(hundredTime, xs, 'b')
    plt.title('State Variable X')
    plt.xlabel('Time (s)')
    plt.ylabel('x (ft)')
    plt.show()

    plt.plot(hundredTime, ys, 'b')
    plt.title('State Variable Y')
    plt.xlabel('Time (s)')
    plt.ylabel('y (ft)')
    plt.show()

    plt.plot(hundredTime, headAngs, 'b')
    plt.title('State Variable Heading Angle')
    plt.xlabel('Time (s)')
    plt.ylabel('Heading Angle (rad)')
    plt.show()

    plt.plot(hundredTime, vs, 'b')
    plt.title('State Variable Velocity')
    plt.xlabel('Time (s)')
    plt.ylabel('v (ft/s)')
    plt.show()



    return None


if __name__ == '__main__':
    main()
