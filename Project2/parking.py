# Intro to AI project 2
# Nathan Borkholder
# Section 1

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp


POPSIZE = 200
OPPARAM = 10
BINARYSIZE = 7
MUTATIONPROB = .005  # .5%
INFEASCONST = 200  # K

class Individual:
    def __init__(self, x, y, headAng, v, binary, gammas, betas):
        self.x = x
        self.y = y
        self.headAng = headAng
        self.v = v
        self.gamma = gammas
        self.beta = betas
        self.binary = binary
        self.stateHistory = []
        self.fitness = 0
        self.cost = 0
        self.infeasible = False

    #does Euler calculations and checks for infeasible regions.
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

def GA(population):
    fitnessPercents = []
    fitnessTotal = 0
    #find fitness total for percentages
    for i in range(POPSIZE):
        fitnessTotal += population[i].fitness

    #calculate fitness percents and store in array
    for i in range(POPSIZE):
        fitnessPercents.append((population[i].fitness / fitnessTotal))

    #add best 2 individuals to next generation (elitism)
    population2 = [population[0], population[1]]
    halfPop = int(POPSIZE/2)

    #generate children creates 198 individuals
    for i in range(0, halfPop-1):
        #generates 2 parents based on fitness percents
        parent1, parent2 = np.random.choice(population, 2, p=fitnessPercents)
        while parent1 == parent2:
            parent1, parent2 = np.random.choice(population, 2, p=fitnessPercents)

        #cross point randomly chosen
        crossPoint, crossPoint2, crossPoint3, crossPoint4 = 0, 0, 0, 0
        upperValue = OPPARAM * BINARYSIZE * 2
        val1, val2, val3 = 0, 0, 0
        cross = []
        #make sure they are not equal
        while val1 == val2 or val1 == val3 or val2 == val3:
            val1 = int(np.random.randint(1,upperValue-2))
            val2 = int(np.random.randint(1, upperValue-2))
            val3 = int(np.random.randint(1,upperValue-2))

        cross.append(val1)
        cross.append(val2)
        cross.append(val3)
        cross.sort()
        crossPoint = cross[0]
        crossPoint2 = cross[1]
        crossPoint3 = cross[2]

        parent1Low = parent1.binary[0:crossPoint]
        parent1Mid = parent1.binary[crossPoint:crossPoint2]
        parent1Mid2 = parent1.binary[crossPoint2:crossPoint3]
        parent1High = parent1.binary[crossPoint3:]

        parent2Low = parent2.binary[0:crossPoint]
        parent2Mid = parent2.binary[crossPoint:crossPoint2]
        parent2Mid2 = parent2.binary[crossPoint2:crossPoint3]
        parent2High = parent2.binary[crossPoint3:]

        # combines the arrays to create the children
        child1 = parent1Low + parent2Mid + parent1Mid2 + parent2High
        child2 = parent2Low + parent1Mid + parent2Mid2 + parent1High

        # applys mutation on children
        child1 = Mutation(child1)
        child2 = Mutation(child2)

        # add the children to the population
        population2.append(splitBinary(child1))
        population2.append(splitBinary(child2))

    return population2



# takes in a binary stirng of 140 bits
# applies mutation with probablity of MutationProb
# returns the mutated binary string
def Mutation(binary):
    binary2 = ""
    for i in range(OPPARAM * 2 * BINARYSIZE):
        mutate = np.random.uniform(0, 1)
        if mutate <= MUTATIONPROB:
            if binary[i] == 0:
                binary2 += '1'
            else:
                binary2 += '0'
        else:
            binary2 += binary[i]
    return binary2


def EulerCalc(index, population):
    #resets individuals from previous generation
    population[index].cost = 0
    population[index].fitness = 0
    population[index].x = 0
    population[index].y = 8
    population[index].headAng = 0
    population[index].v = 0
    population[index].stateHistory = []
    population[index].infeasible = False

    gammas = []
    betas = []
    for g in range(OPPARAM):
        gammas.append(population[index].gamma[g])
        betas.append(population[index].beta[g])

    # interpolate math
    x = np.arange(10)
    betasCubic = sp.interpolate.CubicSpline(x, betas, bc_type='natural')
    gammasCubic = sp.interpolate.CubicSpline(x, gammas, bc_type='natural')
    betas_x, step = np.linspace(0, OPPARAM - 1, 100, retstep=True)
    gammas_x = np.linspace(0, OPPARAM - 1, 100)
    betas_y = betasCubic(betas_x)
    gammas_y = gammasCubic(gammas_x)

    # uses interpolated values for euler calculations
    for i in range(100):
        #checks against constraints
        if not population[index].infeasible:
            if gammas_y[i] < -.524:
                gammas_y[i] = -.524
            elif gammas_y[i] > .524:
                gammas_y[i] = .524
            elif betas_y[i] < -5:
                betas_y[i] = -5
            elif betas_y[i] > 5:
                betas_y[i] = 5
            population[index].calcNewVals(gammas_y[i], betas_y[i], step)

# takes in the complete binary for all control variables as a single string
# splits the binary into 7 bit strings and converts them to gammas and betas
# creates an individual based on the binary, gammas, betas
def splitBinary(binary):
    gammas = []
    betas = []
    count = 0
    while count < 140:
        gammas.append(ConvertFromBinaryG(binary[count:count + BINARYSIZE]))
        count += BINARYSIZE
        betas.append(ConvertFromBinaryB(binary[count:count + BINARYSIZE]))
        count += BINARYSIZE
    return Individual(0,8,0,0,binary, gammas, betas)

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

# calculates the fitness of an individual, given the population and the index in the population.
def FitnessCost(index, population):
    j = population[index].cost
    population[index].fitness = 1 / (j + 1)

#converts a decimal value into 7 bit binary given the range for gammas
def ConvertToBinaryG(value):
    lb = -0.524
    R = .524 * 2
    d = ((value - lb) * (2 ** BINARYSIZE - 1)) / R
    d = int(d)
    binary = '{0:07b}'.format(d)
    return binarytoGray(binary)

#converts binary to a decimal value, uses the range of gammas
def ConvertFromBinaryG(d):
    d = graytoBinary(d)
    d = int(d, 2)
    lb = -0.524
    R = .524 * 2

    value = (d / (2 ** BINARYSIZE - 1)) * R + lb
    return value

#converts a decimal value into 7 bit binary given the range for betas
def ConvertToBinaryB(value):
    lb = -5.0
    R = 5.0 * 2
    d = ((value - lb) * (2 ** BINARYSIZE - 1)) / R
    d = int(d)
    binary = '{0:07b}'.format(d)
    return binarytoGray(binary)

#converts binary to a decimal value, uses the range of betas
def ConvertFromBinaryB(d):
    d = graytoBinary(d)
    d = int(d, 2)
    lb = -5.0
    R = 5.0 * 2

    value = (d / (2 ** BINARYSIZE - 1)) * R + lb
    return value

#code from https://www.geeksforgeeks.org/gray-to-binary-and-binary-to-gray-conversion/
# Python3 program for Binary To Gray
# and Gray to Binary conversion

# Helper function to xor two characters
def xor_c(a, b):
    return '0' if (a == b) else '1'


# Helper function to flip the bit
def flip(c):
    return '1' if (c == '0') else '0'


# function to convert binary string
# to gray string
def binarytoGray(binary):
    gray = ""

    # MSB of gray code is same as
    # binary code
    gray += binary[0]
    # Compute remaining bits, next bit
    # is computed by doing XOR of previous
    # and current in Binary
    for i in range(1, BINARYSIZE):
        # Concatenate XOR of previous
        # bit with current bit
        gray += xor_c(binary[i - 1],
                      binary[i])
    return gray


# function to convert gray code
# string to binary string
def graytoBinary(gray):
    binary = ""

    # MSB of binary code is same
    # as gray code
    binary += gray[0]

    # Compute remaining bits
    for i in range(1, BINARYSIZE):

        # If current bit is 0,
        # concatenate previous bit
        if (gray[i] == '0'):
            binary += binary[i - 1]

        # Else, concatenate invert
        # of previous bit
        else:
            binary += flip(binary[i - 1])

    return binary

# the sort function to determine the lowest cost.
def sortFunc(i):
    return i.cost


def main():
    generation = 0
    population = []
    #generates intitial generation
    for i in range(POPSIZE):
        controls = ""
        #creates two random binary strings and appends them to the controls string
        for e in range(OPPARAM):
            binary = ""
            binary2 = ""
            for t in range(BINARYSIZE):
                temp = str(np.random.randint(0, 2))
                temp2 = str(np.random.randint(0, 2))
                binary += temp
                binary2 += temp2
            controls += binarytoGray(binary)
            controls += binarytoGray(binary2)
        #appends individuals to the population array
        population.append(splitBinary(controls))

        #Calls Euler calcualtions, cost, and fitness on each individual in the population.
        EulerCalc(i, population)
        CostCalc(i, population)
        FitnessCost(i, population)

    generation += 1
    population.sort(key=sortFunc)
    print("Generation", generation, ": J =", population[0].cost)

    #Use GA until cost is met.
    while population[0].cost >= .1 and generation < 1200:
        population = GA(population)
        generation += 1
        #loop through all individuals in new population calculating all new values
        for i in range(POPSIZE):
            EulerCalc(i, population)
            CostCalc(i, population)
            FitnessCost(i, population)
        #sort and print population
        population.sort(key=sortFunc)
        print("Generation", generation, ": J =", population[0].cost)

    print("Final state values:")
    print("x_f =", population[0].x)
    print("y_f =", population[0].y)
    print("alpha_f =", population[0].headAng)
    print("v_f =", population[0].v)

    #extract all control and state variables from the solution individual.
    states = population[0].stateHistory
    xs = []
    ys = []
    headAngs = []
    vs = []
    gs = population[0].gamma
    bs = population[0].beta
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
    plt.xlim([-15,15])
    plt.ylim([-10,20])
    plt.show()

    hundredTime = np.arange(100)

    #State variable x graph
    plt.plot(hundredTime, xs, 'b')
    plt.title('State Variable X')
    plt.xlabel('Time (s)')
    plt.ylabel('x (ft)')
    plt.show()

    #State variable y graph
    plt.plot(hundredTime, ys, 'b')
    plt.title('State Variable Y')
    plt.xlabel('Time (s)')
    plt.ylabel('y (ft)')
    plt.show()

    #State variable heading angle graph
    plt.plot(hundredTime, headAngs, 'b')
    plt.title('State Variable Heading Angle')
    plt.xlabel('Time (s)')
    plt.ylabel('Heading Angle (rad)')
    plt.show()

    #state variable v graph
    plt.plot(hundredTime, vs, 'b')
    plt.title('State Variable Velocity')
    plt.xlabel('Time (s)')
    plt.ylabel('v (ft/s)')
    plt.show()

    tensTime = np.arange(10)

    #contorl variable heading angle rate graph
    plt.plot(tensTime, gs, 'b')
    plt.title('Control Variable Heading Angle Rate')
    plt.xlabel('Time (s)')
    plt.ylabel('Heading Angle Rate (rad/s)')
    plt.show()

    #control variable velocity graph
    plt.plot(tensTime, bs, 'b')
    plt.title('Control Variable Acceleration')
    plt.xlabel('Time (s)')
    plt.ylabel('Heading Angle Rate ($ft/s^{2}$)')
    plt.show()

    #ouputs control variables to file controls.dat
    f = open("controls.dat", "w")
    for i in range(OPPARAM):
        f.writelines([str(gs[i]), "\n"])
        f.writelines([str(bs[i]), "\n"])
    f.close()
    return None

#main call
if __name__ == '__main__':
    main()
