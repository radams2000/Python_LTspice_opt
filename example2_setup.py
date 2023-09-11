import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.signal import cheby1, freqs

# set the target frequency response and error weights

def setTarget(freqx, match_mode):
    target = np.ones(len(freqx))
    err_weights = np.ones(len(freqx))
    f1i = np.where(freqx > 210e3)[0][0]  # edge of passband
    f1ai = np.where(freqx > 150e3)[0][0]  # start of region where passband weight should be increased
    f2i = np.where(freqx > 290e3)[0][0]  # start of stopband
    target[:f1i] = 1.0 # note, in pyhon, this index range is from 0 to f1i-1
    target[f1i:f2i] = 5e-7  # don't-care band, weights in this region are set to 0
    target[f2i:] = 5e-7  # not 0, just for plotting reasons (log10 will blow up ...)
    err_weights[:f1i] = 1  # passband error weights
    err_weights[f2i:] = 10  # stopband error weights
    err_weights[f1i:f2i] = 0  # don't-care band error weights
    deltai = f1i - f1ai
    rng = np.arange(f1ai, f1i)
    err_weights[rng] = 1 + 4 * (rng - f1ai) / deltai
    #tmp = len(freqx)
    #rng = np.arange(f2i,tmp)
    #deltai = tmp-f2i
    #err_weights[rng]=20- 10*(rng-rng[0]) / deltai

    # plot the target response and error weighting function
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.semilogx(freqx, target)
    plt.title('target response')
    plt.ylim([min(target)-0.5, max(target)+0.5])

    plt.subplot(2, 1, 2)
    plt.semilogx(freqx, err_weights)
    plt.ylim([min(err_weights)-0.5, max(err_weights)+0.5])
    plt.title('errWeights')

    plt.tight_layout()
    #plt.show(block=False)

        
    return target, err_weights


# set the LTspice paths and the schematic instances that are allowed to be adjusted

def simControl():
    # user-supplied file paths
    spicePath = r'C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe'  # This is the path to your LT Spice installation
    filePath = r'C:\\Users\\radam\\Documents\\LTspiceXVII\\'  # This is the path to the working LTSPICE folder (schems, netlists, simulation output files)
    fileName = 'example2'  # name of the LTSpice schematic you want to optimize (without the .asc)

    
    # Lists to define which components will be adjusted
    
    simControlOPtInstNames = ['R3', 'R2', 'R4', 'C1', 'C2', 'C3', 'L1', 'C4'] # inst names that will be adjusted
    simControlMinVals = [1000, 100, 1000, 1e-12, 1e-12, 30e-12, 1e-5, 1e-12] # min values of the instances above
    simControlMaxVals = [10e3, 1e5, 2.5e3, 1e-6, 1e-6, 1e-6, 1e-3, 1e-5] # max values of the instances above
    simControlInstTol = ['E96', 'E96', 'E96', 'E24', 'E24', 'E24', 'E12', 'E24'] # tolerances of the instances above
    LTSPice_output_node = 'V(vout)' # LTspice output variable where freq response is taken from

    
    # Set the match mode.
    # 1 = amplitude only
    # 2 = phase only
    # 3 = amplitude and phase both

    matchMode = 1
    
    simControl = [fileName, spicePath, filePath, simControlOPtInstNames,
                  simControlMinVals, simControlMaxVals, simControlInstTol,
                  LTSPice_output_node, matchMode]
    
    return simControl
