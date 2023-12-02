import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.signal import cheby1, freqs
from myPlots import myPlot_1x_errweights


def simControl():

    # ******************************** USER INPUT SECTION *****************
    # user-supplied file paths
    spicePath = r'C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe'  # This is the path to your LT Spice installation
    filePath = r'C:\\Users\\radam\\Documents\\LTspiceXVII\\'  # This is the path to the working LTSPICE folder (schems, netlists, simulation output files)

    fileName = 'example1'  # name of the LTSpice schematic you want to optimize (without the .asc)

    # Lists to be filled out by the user

    simControlOPtInstNames = ['R2', 'R4', 'C1', 'C2', 'C3']  # component inst names that are allowed to be changed
    simControlMinVals = [400, 1.0e3, 50e-9, 20e-9, 300e-12]  # Min values of the above components
    simControlMaxVals = [4000, 10e3, 400e-9, 160e-9, 2e-9]  # max values of the above components
    simControlInstTol = ['E12', 'E12', 'E12', 'E12', 'E12']  # tolerance of the above components
    LTSPice_output_node = 'V(vout)'  # LTspice output simulation variable

    # Set the match mode.
    # 1 = amplitude only
    # 2 = phase only
    # 3 = amplitude and phase both
    matchMode = 1  # ampl only
    #  max # of spice sims in the initial differential evolution phase (enter 0 to skip differential evolution)
    maxSpiceSims_de = 300
    #  max # of spice sims in the least-squares optimization phase (enter 0 to skip lsq)
    maxIter_lsq = 60
    maxIter_ps = 2
    # switch to control whether initial schematic values are used in the initial differential evolution population
    # if set to 0, all the initial values are populated with random vectors that span the [min max] range for each component
    useInitialGuess_de = 1
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
    simControlDict['maxSpiceSims_deD'] = maxSpiceSims_de
    simControlDict['maxIter_psD'] = maxIter_ps

    return simControlDict

def setTarget(freqx, matchMode):
    # User-defined target response. The user-defined response must be calculated
    # at the same frequencies used in the LTSpice sim
    # freqx = freqs returned by initial LTSpice simulation
    # matchMode = 1, 2, or 3 (ampl only, phase only, or both)

    # Default values for the targets and frequency-dependent weighting functions
    print('found ',len(freqx),' freqs in simulation')
    err_weights_ampl = np.ones(len(freqx))
    err_weights_phase = np.ones(len(freqx))
    target_ampl = np.ones(len(freqx))
    target_phase = np.ones(len(freqx))
    if matchMode == 3: # match ampl + phase; return error is concatenation, so need 2X length
        target = np.ones(2*len(freqx))
        err_weights = np.ones(2*len(freqx))
    else:
        target = np.ones(len(freqx))
        err_weights = np.ones(len(freqx))

    # Example 1: match a single op-amp design to a 3rd-order lowpass.

    # Design a 5-th-order chebyshev filter in s-domain
    Wp = 1  # We will scale the actual cutoff later
    b1,a1 = cheby1(3, 1, Wp,'low', analog=True,output='ba')  # 3rd-order 1dB chebyshev lowpass, w=1 rad/sec
    b1 = -b1 # spice circuit is inverting
    #a1 = np.poly(p)  # Coefficients of 1/(p(1)*s^2 + p(2)*s + p(3))
    #b1 = -1.0  # Use neg sign because it's an inverting filter
    fcutoff = 20e3  # Cutoff frequency in Hz
    w,H = freqs(b1, a1, freqx / fcutoff) # the complex transfer function with normaized w0=1
    Hampl = np.abs(H) # magnitude only
    Hampl = Hampl / Hampl[0]  # DC gain = 1
    Hphase = np.unwrap(np.angle(H)) # the phase in radians, in case we want to match phase

    if matchMode == 1:  # Match ampl only, set targets and error weighting function
       
        target_phase = np.ones(len(freqx))  # Not used
        target = Hampl  # This is what is returned by function
        err_weights_ampl = np.ones(len(freqx))
        err_weights_phase = np.ones(len(freqx))  # Not used
        err_weights = err_weights_ampl  # err_weights is returned by function

    elif matchMode == 2:  # Match phase only, set targets and weighting function
        target_ampl = np.ones(len(freqx))  # Not used
        target_phase = Hphase  # Used
        target = target_phase  # Returned by function
        err_weights_ampl = np.ones(len(freqx))  # Not used
        err_weights_phase = np.ones(len(freqx))
        err_weights = err_weights_phase  # err_weights is returned by function

    elif matchMode == 3:  # Match both ampl and phase, set targets and weighting function
        target_ampl = Hampl
        target_phase = Hphase
        target = np.concatenate((target_ampl, target_phase))  # Concatenate ampl and phase
        err_weights_ampl = np.ones(len(freqx))
        err_weights_phase = np.ones(len(freqx))
        err_weights = np.concatenate((err_weights_ampl, err_weights_phase))  # Concatenate err_weights
        ret_cell = [target, err_weights]  # Return concatenated target and err_weights

    # *** plot the target ****

    if matchMode == 1 or matchMode == 3: # ampl only or ampl/phase, plot ampl
        myPlot_1x_errweights('chebychev target ampl','err weights','fresp',freqx,target,err_weights,'target ampl',1,'target_ampl+errWeights.pdf')
    if matchMode == 2 or matchMode == 3: # phase only or mixed, plot phase
        myPlot_1x_errweights('chebychev target phase','err weights','phase',freqx,target_phase,err_weights,'target phase',1,'target_phase+errWeights.pdf')

    return target, err_weights


