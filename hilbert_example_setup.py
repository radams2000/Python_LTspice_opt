import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.signal import cheby1, freqs


def simControl():

    # ******************************** USER INPUT SECTION *****************
    # user-supplied file paths
    spicePath = r'C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe'  # This is the path to your LT Spice installation
    filePath = r'C:\\Users\\radam\\Documents\\LTspiceXVII\\'  # This is the path to the working LTSPICE folder (schems, netlists, simulation output files)

    fileName = 'hilbert'  # name of the LTSpice schematic you want to optimize (without the .asc)

    # Lists to be filled out by the user

    simControlOPtInstNames = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6','C1a', 'C2a', 'C3a', 'C4a', 'C5a', 'C6a']  # component inst names that are allowed to be changed
    simControlMinVals = [1e-6, 0.14e-6, 21e-9, 3e-9, 4.4e-10, 63e-12, 3.8e-7, 54e-9, 8e-9, 1.2e-9, 165e-12, 24e-12]  # Min values of the above components
    simControlMaxVals = [25e-6, 3.6e-6, 525e-9, 75e-9, 11e-9, 1.9e-9, 9.5e-6, 1.35e-6, 1.95e-7, 2.8e-8, 4.1e-9, 600e-12]  # max values of the above components
    simControlInstTol = ['E96', 'E96', 'E96', 'E96','E96', 'E96', 'E96', 'E96','E96', 'E96', 'E96', 'E96']  # tolerance of the above components
    LTSPice_output_node = 'V(vout)'  # LTspice output simulation variable

    # Set the match mode.
    # 1 = amplitude only
    # 2 = phase only
    # 3 = amplitude and phase both
    matchMode = 1  # ampl only
    #  max # of iterations in he particle-swarm global optimization phase (enter 0 to skip)
    maxIter_ps = 2
    #  max # of iterations in the least-squares optimization phase (enter 0 to skip lsq)
    maxIter_lsq = 100


    # *******************************************************************************************

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

def setTarget(freqx, match_mode):
    # User-defined target response. The user-defined response must be calculated
    # at the same frequencies used in the LTSpice sim
    # freqx = freqs returned by initial LTSpice simulation
    # match_mode = 1

    # Default values for the targets and frequency-dependent weighting functions
    print('found ',len(freqx),' freqs in simulation')
    flo = np.where(freqx > 15)[0][0]  # edge of passband
    fhi = np.where(freqx > 25e3)[0][0]  # start of region where passband weight should be increased
    target = 1.414*np.ones(len(freqx))
    err_weights = np.ones(len(freqx))

    err_weights[:flo] = 0  # below 20 hz, dont care error weights
    err_weights[fhi:] = 0  # above 20 khz, dont care


    return target, err_weights


