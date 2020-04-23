import OpenDSS as dss
import pandas as pd
import numpy as np

# DSSobj = dss.OpenDSS("\dss\ieee_13\ieee13.dss", "referenceCap.csv") # Gerado!
# DSSobj = dss.OpenDSS("\dss\ieee_34\ieee34.dss", "referenceCap.csv") # Gerado!
# DSSobj = dss.OpenDSS("\dss\ieee_37\ieee37.dss", "referenceCap.csv") # Gerado!
DSSobj = dss.OpenDSS("\dss\ieee_123\ieee123.dss", "referenceCap.csv")  # Gerado!


def Losses(capacitorVector, engine=DSSobj):

    engine.placeCapacitorYN(capacitorVector, verbose=False)
    engine.circuitSolve()

    return engine.getLosses()


def Costs(capacitorVector, engine=DSSobj):

    engine.totalCosts = 0

    for c in capacitorVector:

        engine.totalCosts = engine.totalCosts + float(engine.capacitorOptions.loc[engine.capacitorOptions["id"] == c, "c"].iloc[0])

    return engine.totalCosts


def Voltages(capacitorVector, mode="mean", min_pu=0.93, max_pu=1.05, engine=DSSobj):

    engine.placeCapacitorYN(capacitorVector, verbose=False)
    engine.circuitSolve()
    voltages = engine.getVoltages()

    if mode == "mean":
        for v1, v2, v3 in zip(voltages.loc[:, ' pu1'], voltages.loc[:, ' pu2'], voltages.loc[:, ' pu3']):

            media = np.nanmean([v1, v2, v3])
            if media < min_pu or media > max_pu:
                return False

        return True

    elif mode == "min-max":

        for v1, v2, v3 in zip(voltages.loc[:, ' pu1'], voltages.loc[:, ' pu2'], voltages.loc[:, ' pu3']):

            low = min([v1, v2, v3])
            high = max([v1, v2, v3])

            if low >= min_pu and high <= max_pu:
                return False

        return True
