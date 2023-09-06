import numpy as np
import matplotlib.pyplot as plt
import time

from scipy.signal import cheby1, freqs

def simControl():
    # user-supplied file paths
    spicePath = r'C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe'  # This is the path to your LT Spice installation
    filePath = r'C:\\Users\\radam\\Documents\\LTspiceXVII\\'  # This is the path to the working LTSPICE folder (schems, netlists, simulation output files)
    
    fileName = 'example3'

    # simControlOPtInstNames = ['R1', 'C1', 'L1', 'R7']
    # simControlMinVals = [10, 100e-12, 1e-6, 10]
    # simControlMaxVals = [1e6, 1e-7, 0.1, 1e6]
    # simControlInstTol = ['E96', 'E96', 'E96', 'E96']

    simControlOPtInstNames = ['R1', 'C1', 'R7']
    simControlMinVals = [10, 100e-12,  10]
    simControlMaxVals = [1e6, 1e-7, 1e6]
    simControlInstTol = ['E96', 'E24', 'E96'] # 1% R, 5% C

    LTSPice_output_node = 'V(vout)'
    matchMode = 1
    
    simControl = [fileName, spicePath, filePath, simControlOPtInstNames,
                  simControlMinVals, simControlMaxVals, simControlInstTol,
                  LTSPice_output_node, matchMode]
    
    return simControl




def setTarget(pass_cell, freqx, match_mode):
    # User-defined target response. The user-defined response must be calculated
    # at the same frequencies used in the LTSpice sim
    # freqx = freqs returned by initial LTSpice simulation
    # match_mode = 1, 2, or 3 (ampl only, phase only, or both)

    # Default values for the frequency-dependent weighting functions
    print('found ',len(freqx),' freqs in simulation')
    err_weights_ampl = np.ones(len(freqx))
    err_weights_phase = np.ones(len(freqx))
    target_ampl = np.ones(len(freqx))
    target_phase = np.ones(len(freqx))
    if match_mode == 3: # match ampl + phase; return error is concatenation, so need 2X length
        target = np.ones(2*len(freqx))
        err_weights = np.ones(2*len(freqx))
    else:
        target = np.ones(len(freqx))
        err_weights = np.ones(len(freqx))

    
    

    

 
    X = np.linspace(0, 80000, 21)  # every 4KHz from datasheet plot
    VdB = [0, 0.5, 1, 1.5, 2, 3, 4.8, 7, 11, 17, 22, 13, 8, 5, 6, 4.5, 3, 2.5, 3, 3, 4.5]  # from datasheet plot, freq resp in dB
    mic_dB = np.interp(freqx, X, VdB)
    #mic_dB = mic_dB+26 # set 26 dB gain target at DC

    plt.figure()
    plt.semilogx(freqx, mic_dB)
    plt.title('Mic dB response')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain (dB)')
    plt.grid(True)
    plt.show(block=False)

    mic_lin = 10**(mic_dB / 20)

    plt.figure()
    plt.semilogx(freqx, mic_lin)
    plt.title('Mic linear response')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid(True)
    plt.show(block=False)

    target = 30.0 / mic_lin

    err_weights = np.sqrt(mic_lin)  # greatest weights where the target is smallest


    plt.figure()
    plt.semilogx(freqx, target)
    plt.title('Inverse mic response, linear')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.grid(True)
    plt.show(block=False)


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
    plt.show(block=False)
    plt.pause(0.1)



    # Continue with other examples or user-defined cases

    return target, err_weights
