# -*- coding: utf-8 -*-
from math import sin, cos, pi
from random import uniform, choice, random, randint
from operator import attrgetter
from copy import deepcopy, copy
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plot
import matplotlib.lines as mlines
import time

# import OpenDSS as dss
# DSSobj = dss.OpenDSS("C:\Users\BR0147834487\Desktop\TCC\SCA_OpenDSS\ieee_37\ieee37.dss")

from dssFunctions import Losses, Costs, Voltages, DSSobj
objFunc = [Losses, Costs]
cts = [Voltages]

# from objectiveFunctions import T1, T2, T3
# objFunc = [T1, T2, T3]
# cts = []

# from objectiveFunctions import BKF1, BKF2
# from constraints import BKC1, BKC2
# objFunc = [BKF1, BKF2]
# cts = [BKC1, BKC2]

# from objectiveFunctions import CEP1, CEP2
# from constraints import CEPC1, CEPC2
# objFunc = [CEP1, CEP2]
# cts = [CEPC1, CEPC2]

# from objectiveFunctions import F13 as objFunc
# from constraints import F13C1, F13C2
# constraints = [F13C1, F13C2]

# from objectiveFunctions import ZDT3A, ZDT3B
# objFunc = [ZDT3A, ZDT3B]
# cts = []

# from objectiveFunctions import V1, V2, V3
# objFunc = [V1, V2, V3]
# cts = []


class Agent():

    def __init__(
        self,
        objectiveFunctions,
        dimensions,
        lowerBounds,
        upperBounds,
        constraints,
        method,
        ptype
    ):

        self._upperBounds = upperBounds                                    # Limites superiores das funções
        self._lowerBounds = lowerBounds                                    # Limites inferiores das funções
        self._constraints = constraints                                    # Restrições
        self._dimensions = dimensions                                      # Número de variáves da função objetivo
        self._objectiveFunctions = objectiveFunctions                      # Funções objetivo
        self._method = method
        self._ptype = ptype                                                # Tipo do problema
        self._S = []                                                       # Vetor com agente dominados por esse agente
        self._N = 0                                                        # Número de agentes que dominam esse agente
        self._rank = 0                                                     # Em qual fronteira de Pareto o indivíduo está (iniciado em 1)
        self._crowdingDistance = 0                                         # Distância populacional
        self._penaltyFlag = False
        self._defaultPenalty = abs(10e10)
        self._initialValues()
        self._fixConstraints()
        self._updateFitness()

    def _initialValues(self):                                                  # Define os valores iniciais, levando em conta os limites e as restrições

        if (
            (len(self._upperBounds) == 1) and
            (len(self._lowerBounds) == 1)
        ):                                                                     # Caso tenha sido fornecido somente um limite, considera-se que as funções tem limites iguais

            self._upperBounds = (
                self._upperBounds * max(self._dimensions))
            self._lowerBounds = (
                self._lowerBounds * max(self._dimensions))

        elif len(self._upperBounds) != len(self._lowerBounds):                 # Gera um erro caso exista algum limite faltando

            raise ValueError('Boundary dimensions must agree!')

        self._value = [None] * max(self._dimensions)                           # Inicia o vetor que irá conter os valores de X

        if self._ptype == "Float":

            for dim in xrange(max(self._dimensions)):

                self._value[dim] = uniform(self._lowerBounds[dim],                 # Inicia os valores com um valor aleatório entre os limites
                                           self._upperBounds[dim])

        elif self._ptype == "Int":

            for dim in xrange(max(self._dimensions)):

                self._value[dim] = randint(self._lowerBounds[dim],                 # Inicia os valores com um valor aleatório entre os limites
                                           self._upperBounds[dim])

    def _fixConstraints(self, mode='penalyze'):                                                 # Ajusta os valores para que atendam as restrições

        if len(self._constraints) > 0:

            constraintsEval = [constrain(self._value)                          # Avalia as restrições para os valores do agente
                               for constrain
                               in self._constraints]

            if mode == 'bring-back':

                while constraintsEval.count(False) > 0:                            # Avalia se as todas as restrições já foram atendidas (as restrições retornam True ou False)

                    for i in xrange(len(self._value)):

                        if self._ptype == "Float":

                            self._value[i] = uniform(self._lowerBounds[i],             # Gera um novo valor até que as restrições sejam atendidas
                                                     self._upperBounds[i])

                        elif self._ptype == "Int":

                            self._value[i] = randint(self._lowerBounds[i],             # Gera um novo valor até que as restrições sejam atendidas
                                                     self._upperBounds[i])

                    constraintsEval = [constrain(self._value)
                                       for constrain
                                       in self._constraints]

            elif mode == 'penalyze':

                if constraintsEval.count(False) > 0:

                    self._penaltyFlag = True

                else:

                    self._penaltyFlag = False

    def _fixOutOfBounds(self):                                                 # Traz os valores que saem do espaço de busca de volta

        for i in xrange(len(self._value)):

            if self._value[i] > self._upperBounds[i]:

                # self._value[i] = self._upperBounds[i]                        # Traz para a fronteira do espaço

                if self._ptype == "Float":

                    self._value[i] = uniform(self._lowerBounds[i],                 # Traz para um valor aleatório dentro do espaço
                                             self._upperBounds[i])

                elif self._ptype == "Int":

                    self._value[i] = randint(self._lowerBounds[i],                 # Traz para um valor aleatório dentro do espaço
                                             self._upperBounds[i])

            elif self._value[i] < self._lowerBounds[i]:

                # self._value[i] = self._lowerBounds[i]

                if self._ptype == "Float":

                    self._value[i] = uniform(self._lowerBounds[i],                 # Traz para um valor aleatório dentro do espaço
                                             self._upperBounds[i])

                elif self._ptype == "Int":

                    self._value[i] = randint(self._lowerBounds[i],                 # Traz para um valor aleatório dentro do espaço
                                             self._upperBounds[i])

    def _updateFitness(self):                                                  # Recalcula as funções objetivo

        if len(self._objectiveFunctions) == 1:                                 # Mono-objetivo

            if self._penaltyFlag:

                if self._method == 'MAX':

                    self._fitness = (
                        self._objectiveFunctions[0](self._value)) - self._defaultPenalty

                elif self._method == 'MIN':

                    self._fitness = (
                        self._objectiveFunctions[0](self._value)) + self._defaultPenalty

                self._penaltyFlag = False

            else:

                self._fitness = (
                    self._objectiveFunctions[0](self._value))

        elif len(self._objectiveFunctions) > 1:                                # Multi-objetivo

            self._fitness = [None] * len(self._objectiveFunctions)

            if self._penaltyFlag:

                if self._method == 'MAX':

                    for i in xrange(len(self._objectiveFunctions)):

                        self._fitness[i] = (
                            self._objectiveFunctions[i](self._value)) - self._defaultPenalty

                elif self._method == 'MIN':

                    for i in xrange(len(self._objectiveFunctions)):

                        self._fitness[i] = (
                            self._objectiveFunctions[i](self._value)) + self._defaultPenalty

                self._penaltyFlag = False

            else:

                for i in xrange(len(self._objectiveFunctions)):

                    self._fitness[i] = (
                        self._objectiveFunctions[i](self._value))

    def domination(self, other, method):                                       # Comparador de dominação

        fitnessA = self.getFX()
        fitnessB = other.getFX()
        noObjectives = len(fitnessA)
        dominationState = [None] * noObjectives

        if method == "MAX":

            for i in xrange(noObjectives):

                if fitnessA[i] > fitnessB[i]:

                    dominationState[i] = 1

                elif fitnessA[i] < fitnessB[i]:

                    dominationState[i] = -1

                else:

                    dominationState[i] = 0

        elif method == "MIN":

            for i in xrange(noObjectives):

                if fitnessA[i] < fitnessB[i]:

                    dominationState[i] = 1

                elif fitnessA[i] > fitnessB[i]:

                    dominationState[i] = -1

                else:

                    dominationState[i] = 0

        if min(dominationState) < 0:

            return False

        elif sum(dominationState) == 0:

            return False

        else:

            return True

    def __lt__(self, other):                                                   # Operador de distância populacional

        if ((self._rank < other.getRank()) or
                (self._rank == other.getRank() and
                 self._crowdingDistance > other.getCD())
                ):

            return True

        else:

            return False

    def updateValues(self, R1, b, Psc, bestValue):                             # Atualiza os valores de X basedo no método SCA

        for i in xrange(len(self._value)):

            r2 = uniform(0, 2 * pi)
            r3 = b * random()
            r4 = random()

            if r4 < Psc:

                if self._ptype == "Float":

                    self._value[i] = (self._value[i] +
                                      R1 * sin(r2) * abs(r3 * bestValue[i] -
                                                         self._value[i]))

                elif self._ptype == "Int":

                    self._value[i] = int((self._value[i] +
                                          R1 * sin(r2) * abs(r3 * bestValue[i] -
                                                             self._value[i])))

            else:

                if self._ptype == "Float":

                    self._value[i] = (self._value[i] +
                                      R1 * cos(r2) * abs(r3 * bestValue[i] -
                                                         self._value[i]))

                elif self._ptype == "Int":

                    self._value[i] = int((self._value[i] +
                                          R1 * cos(r2) * abs(r3 * bestValue[i] -
                                                             self._value[i])))

        self._fixOutOfBounds()
        self._fixConstraints()
        self._updateFitness()

    def getS(self):

        return self._S

    def getN(self):

        return self._N

    def getRank(self):

        return self._rank

    def getCD(self):

        return self._crowdingDistance

    def getX(self):

        return self._value

    def getFX(self):

        return self._fitness

    def setN(self, n):

        self._N = n

    def setS(self, s):

        self._S = s

    def setRank(self, r):

        self._rank = r

    def setCD(self, cd):

        self._crowdingDistance += cd

    def addS(self, Q):

        self._S.append(Q)

    def addN(self, n=1):

        self._N += n

    def subN(self, n=1):

        self._N -= n


class Population():

    def __init__(
        self,
        size,
        objectiveFunctions,
        dimensions,
        lowerBounds,
        upperBounds,
        constraints,
        maxGeneration,
        a,
        b,
        Psc,
        method,
        ptype
    ):

        self._size = size                                                  # Tamanho da população
        self._population = [Agent(objectiveFunctions,                      # Gera a população inicial
                                  dimensions,
                                  lowerBounds,
                                  upperBounds,
                                  constraints,
                                  method,
                                  ptype)
                            for i
                            in xrange(self._size)]
        self._method = method                                              # Define se o problema é de maximização ou minimização
        self._maxGeneration = maxGeneration                                # Número máximo de gerações (iterações)
        self._best = (self._population[0]._value,                          # Inicia o melhor indivíduo como o primeiro da população
                      self._population[0]._fitness)
        self._currentGeneration = None                                     # Geração atual
        self._R1 = None                                                    # Paramêtro do método SCA
        self._a = a                                                        # Paramêtro do método SCA
        self._b = b                                                        # Paramêtro do método SCA
        self._Psc = Psc                                                    # Paramêtro do método SCA
        self._fronts = []                                                  # Frentes de Pareto (iniciado em 1)
        self._nObjectives = len(objectiveFunctions)                        # Número de objetivos
        self._population0 = None                                           # Guarda uma cópia de população

    def setBest(self):                                                         # Encontra o melhor indivíduo da população

        if self._nObjectives == 1:                                             # Mono-objetivo

            if self._method == 'MAX':

                bestFitness = (max(self._population,
                                   key=attrgetter('_fitness'))._fitness)
                bestValues = (max(self._population,
                                  key=attrgetter('_fitness'))._value[:])

                if bestFitness > self._best[1]:

                    self._best = (bestValues, bestFitness)

            elif self._method == 'MIN':

                bestFitness = (min(self._population,
                                   key=attrgetter('_fitness'))._fitness)
                bestValues = (min(self._population,
                                  key=attrgetter('_fitness'))._value[:])

                if bestFitness < self._best[1]:

                    self._best = (bestValues, bestFitness)

        elif self._nObjectives > 1:                                            # Multi-objetivo

            bestAgent = choice(self._fronts[0])                              # Escolhe um indivíduo aleatório da primeira fronteira
            # bestAgent = choice(self._population)
            bestFitness = bestAgent._fitness
            bestValues = bestAgent._value[:]
            self._best = (bestValues, bestFitness)

    def addFront(self, agent, front):                                          # Adiciona um indivíduo a uma fronteira

        try:

            self._fronts[front - 1].append(agent)

        except IndexError:

            self._fronts.append([])
            self._fronts[front - 1].append(agent)

    def ndSort(self):                                                          # Non-dominated sort

        self._fronts = []

        for agentP in self._population:

            agentP.setS([])
            agentP.setN(0)

            for agentQ in self._population:

                if agentP.domination(agentQ, self._method):

                    agentP.addS(agentQ)

                elif agentQ.domination(agentP, self._method):

                    agentP.addN()

            if agentP.getN() == 0:

                agentP.setRank(1)

                self.addFront(agentP, 1)

        i = 1
        while len(self._fronts[i - 1]) != 0:

            newFront = []

            for agentP in self._fronts[i - 1]:

                for agentQ in agentP.getS():

                    agentQ.subN()

                    if agentQ.getN() == 0:

                        agentQ.setRank(i + 1)
                        newFront.append(agentQ)
            i += 1
            self._fronts.append(newFront)

    def setCrowdingDistance(self):                                             # Calcula a distância populacional

        for front in self._fronts:

            if front:                                                      # Verifica se a frente não está vazia

                for agent in front:

                    agent.setCD(0)

                for obj in xrange(self._nObjectives):

                    front.sort(key=lambda agent: agent._fitness[obj])

                    front[0].setCD(float('Inf'))
                    front[-1].setCD(float('Inf'))

                    fMin = front[0].getFX()[obj]
                    fMax = front[-1].getFX()[obj]


# for k in xrange(1, len(front) - 1):
##
# front[k].setCD((front[k + 1].getFX()[obj] -
# front[k - 1].getFX()[obj]) /
# (fMax - fMin))

                    for k in xrange(1, len(front) - 1):

                        try:

                            front[k].setCD((front[k + 1].getFX()[obj] -
                                            front[k - 1].getFX()[obj]) /
                                           (fMax - fMin))

                        except ZeroDivisionError:

                            front[k].setCD(0)

    def savePop(self):                                                         # Guarda uma cópia da população atual

        self._population0 = deepcopy(self._population)

    def mergePop(self):                                                        # Une a população atual com a cópia guardada

        self._population += deepcopy(self._population0)

    def slicePop(self):                                                        # Retorna a população para o tamanho original

        self._population = self._population[:self._size]

    def ccoSort(self):                                                         # Ordena a população utilizando o crowded-comparison-operator (sobrecarrecado na classe Agente)

        self._population.sort()

    def updateR1(self):

        self._R1 = (self._a -
                    self._a * (self._currentGeneration / self._maxGeneration))

    def updateValues(self):                                                    # Atualiza os valores da população utilizando o método SCA

        for agent in self._population:

            agent.updateValues(self._R1, self._b, self._Psc, self._best[0])

    def nextGeneration(self):                                                  # Avança uma geração

        if self._currentGeneration is None:

            self._currentGeneration = 1

        else:

            self._currentGeneration += 1

    def getBest(self):

        return self._best

    def getCurrentGeneration(self):

        return self._currentGeneration

    def report(self, everyGeneration):                                         # Mosta informações sobre a população (mono-objetivo)

        if self._currentGeneration % everyGeneration == 0:

            print 'Current Generation: {0}'.format(self._currentGeneration)
            print 'Best Value of X: {0}'.format(self._best[0])
            print 'Best Value of Y: {0}'.format(self._best[1])
            print '=========================='

    def reportGraph(self, front=1):                                            # Gera o gráfico das funções objetivo (multi-objetivo)

        if self._nObjectives == 2:                                             # Dois objetivos

            x_axis = []
            y_axis = []

            for agent in self._fronts[front - 1]:

                x_axis.append(agent.getFX()[0])
                y_axis.append(agent.getFX()[1])

            fig = plot.figure()
            ax = fig.gca()
            ax.scatter(x_axis, y_axis, facecolors='none', edgecolors='blue')
            ax.set_xlabel('f1()')
            ax.set_ylabel('f2()')
            ax.set_title('Pareto Front')
            label = mlines.Line2D([], [],
                                  color='none',
                                  marker='o',
                                  markersize=10,
                                  label='1st Front',
                                  markerfacecolor='none',
                                  markeredgecolor='blue')
            plot.legend(handles=[label])
            ax.grid(color='grey', linestyle='-.')
            plot.show()

        elif self._nObjectives == 3:                                           # Três objetivos

            x_axis = []
            y_axis = []
            z_axis = []

            for agent in self._fronts[front - 1]:

                x_axis.append(agent.getFX()[0])
                y_axis.append(agent.getFX()[1])
                z_axis.append(agent.getFX()[2])

            fig = plot.figure()
            ax = Axes3D(fig)
            ax.scatter(x_axis,
                       y_axis,
                       z_axis,
                       facecolors='none',
                       edgecolors='blue')
            ax.set_xlabel('f1()')
            ax.set_ylabel('f2()')
            ax.set_zlabel('f3()')
            ax.set_title('Pareto Front')
            label = mlines.Line2D([], [],
                                  color='none',
                                  marker='o',
                                  markersize=10,
                                  label='1st Front',
                                  markerfacecolor='none',
                                  markeredgecolor='blue')
            plot.legend(handles=[label])
            plot.grid()
            plot.show()

    def exportFront(self, front=1):

        with open('front.txt', 'w') as f:

            for agent in self._fronts[front - 1]:

                f.write(str(agent.getX()) + " - " + str(agent.getFX()) + "\n")


def SCA(populationSize,
        objectiveFunctions,
        dimensions,
        lowerBounds,
        upperBounds,
        constraints,
        maxGenerations,
        a,
        b,
        Psc,
        method,
        ptype='Float'
        ):

    if len(objectiveFunctions) == 1:                                           # Mono-objetivo

        population = Population(populationSize,
                                objectiveFunctions,
                                dimensions,
                                lowerBounds,
                                upperBounds,
                                constraints,
                                maxGenerations,
                                a,
                                b,
                                Psc,
                                method,
                                ptype)

        population.nextGeneration()
        population.setBest()

        while population.getCurrentGeneration() < maxGenerations:

            population.updateR1()
            population.updateValues()
            population.setBest()
            population.report(10)
            population.nextGeneration()

    elif len(objectiveFunctions) > 1:

        population = Population(populationSize,
                                objectiveFunctions,
                                dimensions,
                                lowerBounds,
                                upperBounds,
                                constraints,
                                maxGenerations,
                                a,
                                b,
                                Psc,
                                method,
                                ptype)

        population.nextGeneration()

        while population.getCurrentGeneration() < maxGenerations:

            print population.getCurrentGeneration()
            population.ndSort()
            population.setCrowdingDistance()
            population.setBest()
            population.savePop()
            population.updateR1()
            population.updateValues()
            population.mergePop()
            population.ndSort()
            population.setCrowdingDistance()
            population.ccoSort()
            population.slicePop()
            population.nextGeneration()

    population.exportFront()
    # population.reportGraph()


a = time.time()
SCA(100, objFunc, [DSSobj.getBusInfo()], [0], [8], cts, 200, 5, 3, 0.5, 'MIN', 'Int')
b = time.time()
print b-a
