import numpy as np
import matplotlib.pyplot as plt
from myPlots import myPlot_1x_errweights



# set the LTspice paths and the schematic instances that are allowed to be adjusted

def simControl():
    # ******************************** USER INPUT SECTION *****************

    # user-supplied file paths
    spicePath = r'C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe'  # This is the path to your LT Spice installation
    filePath = r'C:\\Users\\radam\\Documents\\LTspiceXVII\\'  # This is the path to the working LTSPICE folder (schems, netlists, simulation output files)
    fileName = 'example2_diff'  # name of the LTSpice schematic you want to optimize (without the .asc)

    # Lists to define which components will be adjusted
    #
    simControlOPtInstNames = ['C4VAL','R1VAL','R2VAL','R3VAL','C2VAL','C1','C3']  # inst names that will be adjusted
    simControlMinVals = [300e-12, 100, 300, 300, 200e-12, 200e-12, 50e-12]  # min values of the instances above
    simControlMaxVals = [3e-9,   300, 5e3,   5e3, 5e-9, 5e-9, 1e-9]  # max values of the instances above
    simControlInstTol = ['E96', 'E96', 'E96', 'E96', 'E96', 'E96', 'E96']  # tolerances of the instances above
    LTSPice_output_node = 'V(vout)'  # LTspice output variable where freq response is taken from


    # Set the match mode.
    # 1 = amplitude only
    # 2 = phase only
    # 3 = amplitude and phase both

    matchMode = 1

    maxIter_ps = 20 #  max # of iterations in he particle-swarm global optimization phase (enter 0 to skip)
    maxIter_lsq = 70    #  max # of iterations in the least-squares optimization phase (enter 0 to skip lsq)



    # switch to control whether initial schematic values are used in the initial differential evolution population
    # if set to 0, all the initial values are populated with random vectors that span the [min max] range for each component
    useInitialGuess_de = 0

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


    return simControlDict


# set the target frequency response and error weights

def setTarget(freqx, match_mode):
    target = np.ones(len(freqx))
    err_weights = np.ones(len(freqx))
    f1i = np.where(freqx > 150e3)[0][0]  # edge of passband
    f1ai = np.where(freqx > 110e3)[0][0]  # start of region where passband weight should be increased
    f2i = np.where(freqx > 234e3)[0][0]  # start of stopband
    target[:f1i] = 1.0 # note, in pyhon, this index range is from 0 to f1i-1
    target[f1i:f2i] = 5e-7  # don't-care band, weights in this region are set to 0
    target[f2i:] = 5e-7  # not 0, just for plotting reasons (log10 will blow up ...)
    err_weights[:f1i] = 1  # passband error weights
    err_weights[f2i:] = 10  # stopband error weights
    err_weights[f1i:f2i] = 0  # don't-care band error weights
    deltai = f1i - f1ai
    rng = np.arange(f1ai, f1i)
    err_weights[rng] = 1 + 4 * (rng - f1ai) / deltai


    # plot the target response and error weighting function

    myPlot_1x_errweights('chebychev target ampl','errWeights','fresp',freqx,target,err_weights,'target ampl',1,'target_ampl+errWeights_ampl.pdf')

    return target, err_weights


