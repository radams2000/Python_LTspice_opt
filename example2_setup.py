import numpy as np

from myPlots import myPlot_1x_errweights




# set the LTspice paths and the schematic instances that are allowed to be adjusted

def simControl():
    # ******************************** USER INPUT SECTION *****************

    # user-supplied file paths
    spicePath = r'C:\\Program Files\\LTC\\LTspiceXVII\\XVIIx64.exe'  # This is the path to your LT Spice installation
    filePath = r'C:\\Users\\radam\\Documents\\LTspiceXVII\\'  # This is the path to the working LTSPICE folder (schems, netlists, simulation output files)
    fileName = 'example2'  # name of the LTSpice schematic you want to optimize (without the .asc)

    # Lists to define which components will be adjusted
    #
    simControlOPtInstNames = ['R2VAL', 'C1', 'C3VAL', 'C4', 'R1', 'CRATIO']  # inst names that will be adjusted
    simControlMinVals = [1e3, 300e-12, 50e-12, 200e-12, 300, 1.0]  # min values of the instances above
    simControlMaxVals = [4e3, 10e-9,  2e-9, 3e-9, 1e3, 3.0]  # max values of the instances above
    simControlInstTol = ['E96', 'E24', 'E24', 'E24', 'E96', 'E96']  # tolerances of the instances above, 1% R, 5% C and L
    LTSPice_output_node = 'V(vout)'  # LTspice output variable where freq response is taken from


    # Set the match mode.
    # 1 = amplitude only
    # 2 = phase only
    # 3 = amplitude and phase both
    matchMode = 1

    #  max # of iterations in he particle-swarm global optimization phase (enter 0 to skip)
    maxIter_ps = 20
    #  max # of iterations in the least-squares optimization phase (enter 0 to skip lsq)
    maxIter_lsq = 100



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

def setTarget(freqx, matchMode): # note, matchMode 1 only since it's a passband/stopband style of optimization
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
    # err_weights[rng] = 1 + 8 * (rng - f1ai) / deltai
    err_weights[rng] = 3
    #  export a json file
    # headers = ["frequency", "Amplitude", "ErrorWeight"]
    # exportJson = np.column_stack((freqx,target,err_weights)).tolist()
    # exportJson.insert(0, headers)
    # json_file_path = 'target.json'
    # with open(json_file_path, 'w') as json_file:
    #     json.dump(exportJson, json_file, indent=2)

    #  plot
    myPlot_1x_errweights('chebychev target ampl','errWeights','fresp',freqx,target,err_weights,'target ampl',1,'target_ampl+errWeights.pdf')

    return target, err_weights


