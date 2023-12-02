import numpy as np
import matplotlib.pyplot as plt
from myPlots import myPlot_1x,myPlot_2x,myPlot_3x,myPlot_2x_errweights,myPlot_1x_errweights




# set the LTspice paths and the schematic instances that are allowed to be adjusted

def simControl():
    # ******************************** USER INPUT SECTION *****************

    # user-supplied file paths
    spicePath = r'C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe'  # This is the path to your LT Spice installation
    filePath = r'C:\\Users\\radam\\Documents\\LTspiceXVII\\'  # This is the path to the working LTSPICE folder (schems, netlists, simulation output files)
    fileName = 'testTran'  # name of the LTSpice schematic you want to optimize (without the .asc)

    # Lists to define which components will be adjusted
    #
    simControlOPtInstNames = ['R1', 'R2', 'R3']  # inst names that will be adjusted
    simControlMinVals = [100, 100, 100]  # min values of the instances above
    simControlMaxVals = [20e3, 20e3, 20e3]  # max values of the instances above
    simControlInstTol = ['E96', 'E96', 'E96']  # tolerances of the instances above
    LTSPice_output_node = 'V(vout)'  # LTspice output variable where freq response is taken from


    # Set the matchMode.
    # 1 = amplitude only
    # 2 = phase only
    # 3 = amplitude and phase both
    # 4 = transient sim, match waveform

    matchMode = 4  #  time domain match

    #  max # of iterations in he particle-swarm global optimization phase (enter 0 to skip)
    maxIter_ps = 20
    #  max # of iterations in the least-squares optimization phase (enter 0 to skip lsq)
    maxIter_lsq = 200

    numTimePoints = 2048
    #  the target transient sim response will be resampled with this number of points between the start and end times
    #  make sure there are enough points to capture all the details you care about

    # switch to control whether initial schematic values are used in the initial differential evolution population
    # if set to 0, all the initial values are populated with random vectors that span the [min max] range for each component


    # ******************************************************************

    # return a dict
    simControlDict = {}
    simControlDict['fileNameD'] = fileName
    simControlDict['spicePathD'] = spicePath
    simControlDict['filePathD'] = filePath
    simControlDict['simControlOPtInstNamesD'] = simControlOPtInstNames
    simControlDict['simControlMinValsD'] = simControlMinVals
    simControlDict['simControlMaxValsD'] = simControlMaxVals
    simControlDict['simControlInstTolD'] = simControlInstTol
    simControlDict['LTSPice_output_nodeD'] = LTSPice_output_node
    simControlDict['matchModeD'] = matchMode
    simControlDict['maxIter_lsqD'] =  maxIter_lsq
    simControlDict['maxIter_psD'] = maxIter_ps
    simControlDict['numTimePointsD'] = numTimePoints

    return simControlDict


# set the target frequency response and error weights

def setTarget(timex):
    T = 0.001 #  exponential time constant
    temp1 = 1.0 - np.exp(-timex/T)
    T2 = 0.00031 #  exponential time constant
    temp2 = np.exp(-timex/T2)
    T3 = 0.0002578 #  exponential time constant
    temp3 = np.exp(-timex/T3)
    temp4 = np.convolve(temp1,temp2,'full')
    temp5 = np.convolve(temp4,temp3,'full')
    target = temp5[0:len(timex)]/max(temp5)
    err_weights = np.ones(len(timex))

    # plot the target response and error weighting function

    myPlot_1x_errweights('target', 'error weights', 'transient', timex, target,
                         err_weights, 'init sim', 1, 'target+errWeights.pdf')

        
    return target, err_weights


