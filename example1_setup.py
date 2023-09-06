import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.signal import cheby1, freqs



def setTarget(pass_cell, freqx, match_mode):
    # User-defined target response. The user-defined response must be calculated
    # at the same frequencies used in the LTSpice sim
    # freqx = freqs returned by initial LTSpice simulation
    # match_mode = 1, 2, or 3 (ampl only, phase only, or both)

    # Default values for the targets and frequency-dependent weighting functions
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

    if match_mode == 1:  # Match ampl only, set targets and error weighting function
       
        target_phase = np.ones(len(freqx))  # Not used
        target = Hampl  # This is what is returned by function
        err_weights_ampl = np.ones(len(freqx))
        err_weights_phase = np.ones(len(freqx))  # Not used
        err_weights = err_weights_ampl  # err_weights is returned by function

    elif match_mode == 2:  # Match phase only, set targets and weighting function
        target_ampl = np.ones(len(freqx))  # Not used
        target_phase = Hphase  # Used
        target = target_phase  # Returned by function
        err_weights_ampl = np.ones(len(freqx))  # Not used
        err_weights_phase = np.ones(len(freqx))
        err_weights = err_weights_phase  # err_weights is returned by function

    elif match_mode == 3:  # Match both ampl and phase, set targets and weighting function
        target_ampl = Hampl
        target_phase = Hphase
        target = np.concatenate((target_ampl, target_phase))  # Concatenate ampl and phase
        err_weights_ampl = np.ones(len(freqx))
        err_weights_phase = np.ones(len(freqx))
        err_weights = np.concatenate((err_weights_ampl, err_weights_phase))  # Concatenate err_weights
        ret_cell = [target, err_weights]  # Return concatenated target and err_weights

    # *** plot the target ****
    if match_mode == 1: # ampl only
        plt.figure()
        plt.semilogx(freqx, 20 * np.log10(target_ampl))
        plt.title('chebychev target ampl dB')
        plt.show(block=False)

    elif match_mode == 2: # phase only
        plt.figure()
        plt.semilogx(freqx, target_phase)
        plt.title('chebychev target phase')
        plt.show(block=False)

    elif match_mode == 3:  # Match both ampl and phase
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.semilogx(freqx, 20 * np.log10(target_ampl))
        plt.title('chebychev target ampl dB')
        
        plt.subplot(2, 1, 2)
        plt.semilogx(freqx, target_phase)
        plt.title('chebychev target phase radians')
        
        plt.tight_layout()
        plt.show(block=False)

    return target, err_weights


def simControl():
    # user-supplied file paths
    spicePath = r'C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe'  # This is the path to your LT Spice installation
    filePath = r'C:\\Users\\radam\\Documents\\LTspiceXVII\\'  # This is the path to the working LTSPICE folder (schems, netlists, simulation output files)
  
    fileName = 'example1'  # name of the LTSpice schematic you want to optimize (without the .asc)

    # Cell arrays filled out by the user
 
    simControlOPtInstNames = ['R2', 'R4', 'C1', 'C2', 'C3'] # component inst names that are allowed to be changed
    simControlMinVals = [100, 100, 1e-12, 1e-12, 1e-12] # Min values of the above components
    simControlMaxVals = [1e5, 2.5e3, 1e-6, 1e-6, 1e-6] # max values of the above components
    simControlInstTol = ['E96', 'E96', 'E24', 'E24', 'E24'] # tolerance of the above components
    LTSPice_output_node = 'V(vout)' # LTspice output simulation variable
   
    # Set the match mode.
    # 1 = amplitude only
    # 2 = phase only
    # 3 = amplitude and phase both

    matchMode = 1 # ampl only
    
    simControl = [fileName, spicePath, filePath, simControlOPtInstNames,
                  simControlMinVals, simControlMaxVals, simControlInstTol,
                  LTSPice_output_node, matchMode]
    
    return simControl