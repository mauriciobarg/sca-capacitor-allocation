# -*- coding: cp1252 -*-
import win32com.client
import pandas as pd
import numpy as np
import os
import sys
from random import *
from win32com.client import makepy


class OpenDSS():

    def __init__(self, circuit, capacitorOptions="defaultCap.csv"):

        self.circuit = circuit
        self.capacitorOptions = pd.read_csv(capacitorOptions)
        self.path = os.path.join("\\", *circuit.split("\\")[1:-1])

        try:
            sys.argv = ["makepy", "OpenDSSEngine.DSS"]
            makepy.main()
            self.dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")
            self.dssObj.Start("0")
            self.dssText = self.dssObj.Text
            print "OpenDSS foi iniciado com sucesso!"

        except:

            print "Erro ao iniciar OpenDSS!"

        try:

            self.dssText.Command = "compile '" + circuit + "'"

        except:

            print "Erro ao abrir " + circuit

        self.startCapacitors()

    def startCapacitors(self, n=3):

        for bus in xrange(self.getBusInfo(phases=n)):

            if n == 1:
                open("capacitorCommands_mono.txt", "w").close()

                self.dssText.Command = ("New Capacitor.C" + str(bus) + " bus1=" + str(self.node_list.iloc[bus]['NODE']) + " kvar=0.001 kv=34.5 phases=1")

            elif n == 3:

                open("capacitorCommands_tri.txt", "w").close()

                self.dssText.Command = ("New Capacitor.C" + str(bus) + " bus1=" + str(self.bus_list.iloc[bus]['BUS']) + " kvar=0.001 kv=34.5 phases=3")

    def placeCapacitorYN(self, capacitorVector, verbose=False):

        for i, c in enumerate(capacitorVector):

            self.dssText.Command = ("capacitor.C" + str(i) + ".kvar=" + str(self.capacitorOptions.loc[self.capacitorOptions["id"] == c, "q"].iloc[0]))

            if verbose:

                print self.dssText.Command

    def getBusInfo(self, phases=3):

        if phases == 3:

            self.bus_list = pd.read_csv(os.path.join(self.path, "bus_list.csv"),
                                        names=['BUS'],
                                        usecols=xrange(1))

            self.busN = self.bus_list.shape[0]

            return self.busN

        elif phases == 1:

            self.node_list = pd.read_csv(os.path.join(self.path, "node_list.csv"),
                                         names=['NODE'],
                                         usecols=xrange(1))

            self.nodeN = self.node_list.shape[0]

            return self.nodeN

    def getLosses(self):

        self.dssText.Command = "export Losses loss" + ".csv"

        self.losses = pd.read_csv(os.path.join(self.path, "loss.csv"),
                                  usecols=xrange(2))

        self.totalLosses = round((self.losses.iloc[:, 1:2].sum().iloc[0])/1000, 6)
        return self.totalLosses

    def getVoltages(self):

        self.dssText.Command = "export Voltages V.csv"
        self.bus_voltages = pd.read_csv(os.path.join(self.path, "V.csv")).replace(0, np.nan)

        return self.bus_voltages

    def circuitSolve(self):

        self.dssText.Command = "Solve"
