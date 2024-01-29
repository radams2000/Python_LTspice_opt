
import matplotlib.pyplot as plt
import numpy as np
def myPlot_1x(title,type,logFlag,X,Y1,Y1label,fwrite,fname): # Y1 is target, Y2 is optimized

    fig, axs = plt.subplots()
    if type == 'fresp':
        if logFlag:
            axs.semilogx(X, 20 * np.log10(Y1), label=Y1label)
        else:
            axs.plot(X, 20 * np.log10(Y1), label=Y1label)
        axs.legend()
        plt.ylabel('dB')
        plt.xlabel('freq')
    if type == 'transient':
        axs.plot(X, Y1, label=Y1label)
        axs.legend()
        plt.ylabel('Volts')
        plt.xlabel('time')
    if type == 'phase':
        if logFlag:
            axs.semilogx(X, Y1, label=Y1label)
        else:
            axs.plot(X, Y1, label=Y1label)
        axs.legend()
        plt.ylabel('Radians')
        plt.xlabel('freq')
    plt.title(title)
    fig.canvas.draw_idle()
    fig.canvas.flush_events()
    if fwrite:
        # plt.savefig(fname, dpi=600, bbox_inches='tight')
        plt.savefig(fname, dpi=600)



def myPlot_2x(title,type,logFlag,X,Y1,Y2,Y1label,Y2label,fwrite,fname): # Y1 is target, Y2 is optimized

    fig, axs = plt.subplots()
    if type == 'fresp':
        if logFlag:
            axs.semilogx(X, 20 * np.log10(Y1), label=Y1label)
            axs.semilogx(X, 20 * np.log10(Y2), label=Y2label)
        else:
            axs.plot(X, 20 * np.log10(Y1), label=Y1label)
            axs.plot(X, 20 * np.log10(Y2), label=Y2label)
        axs.legend()
        plt.ylabel('dB')
        plt.xlabel('freq')
    if type == 'phase':
        if logFlag:
            axs.semilogx(X, Y1, label=Y1label)
            axs.semilogx(X, Y2, label=Y2label)
        else:
            axs.plot(X, Y1, label=Y1label)
            axs.plot(X, Y2, label=Y2label)
        axs.legend()
        plt.ylabel('Radians')
        plt.xlabel('freq')

    if type == 'transient':
        axs.plot(X, Y1, label=Y1label)
        axs.plot(X, Y2, label=Y2label)
        axs.legend()
        plt.ylabel('Volts')
        plt.xlabel('time')

    plt.title(title)
    fig.canvas.draw_idle()
    fig.canvas.flush_events()
    if fwrite:
        # plt.savefig(fname, dpi=600, bbox_inches='tight')
        plt.savefig(fname, dpi=600)



def myPlot_3x(title,type,logFlag,X,Y1,Y2,Y3,Y1label,Y2label,Y3label,fwrite,fname): # Y1 is target, Y2 is optimized

    fig, axs = plt.subplots()
    if type == 'fresp':
        if logFlag:
            axs.semilogx(X, 20 * np.log10(Y1), label=Y1label)
            axs.semilogx(X, 20 * np.log10(Y2), label=Y2label)
            axs.semilogx(X, 20 * np.log10(Y3), label=Y3label)
        else:
            axs.plot(X, 20 * np.log10(Y1), label=Y1label)
            axs.plot(X, 20 * np.log10(Y2), label=Y2label)
            axs.plot(X, 20 * np.log10(Y3), label=Y3label)
        axs.legend()
        plt.ylabel('dB')
        plt.xlabel('freq')

    if type == 'phase':
        if logFlag:
            axs.semilogx(X, Y1, label=Y1label)
            axs.semilogx(X, Y2, label=Y2label)
            axs.semilogx(X, Y3, label=Y3label)
        else:
            axs.plot(X, Y1, label=Y1label)
            axs.plot(X, Y2, label=Y2label)
            axs.plot(X, Y3, label=Y3label)
        axs.legend()
        plt.ylabel('Radians')
        plt.xlabel('freq')

    if type == 'transient':
        axs.plot(X, Y1, label=Y1label)
        axs.plot(X, Y2, label=Y2label)
        axs.plot(X, Y3, label=Y3label)
        axs.legend()
        plt.ylabel('Volts')
        plt.xlabel('time')

    plt.title(title)
    fig.canvas.draw_idle()
    fig.canvas.flush_events()
    if fwrite:
        # plt.savefig(fname, dpi=600, bbox_inches='tight')
        plt.savefig(fname, dpi=600)



def myPlot_2x_errweights(title1,title2,type,logFlag,X,Y1,Y2,errWeights,Y1label,Y2label,fwrite,fname): # Y1 is target, Y2 is optimized

    fig, axs = plt.subplots(2)
    if type == 'fresp':
        if logFlag:
            axs[0].semilogx(X, 20 * np.log10(Y1),label=Y1label)
            axs[0].semilogx(X,20 * np.log10(Y2),label=Y2label)
        else:
            axs[0].plot(X, 20 * np.log10(Y1), label=Y1label)
            axs[0].plot(X, 20 * np.log10(Y2), label=Y2label)
        axs[0].legend()
        axs[0].set_ylabel('dB')
        axs[0].set_xlabel('freq')
        if logFlag:
            axs[1].semilogx(X,errWeights,label='error weights')
        else:
            axs[1].plot(X, errWeights, label='error weights')
        axs[1].legend()
        axs[0].set_title(title1)
        axs[1].set_title(title2)
        plt.subplots_adjust(left=0.2,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.5)

    if type == 'transient':
        axs[0].plot(X, Y1, label=Y1label)
        axs[0].plot(X, Y2, label=Y2label)
        axs[0].legend()
        axs[0].set_ylabel('Volts')
        axs[0].set_xlabel('time')
        axs[1].plot(X, errWeights, label='error weights')
        axs[1].legend()
        axs[0].set_title(title1)
        axs[1].set_title(title2)
        plt.subplots_adjust(left=0.2,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.5)

    if type == 'phase':
        if logFlag:
            axs[0].semilogx(X, Y1, label=Y1label)
            axs[0].semilogx(X, Y2, label=Y2label)
        else:
            axs[0].plot(X, Y1, label=Y1label)
            axs[0].plot(X, Y2, label=Y2label)
        axs[0].legend()
        axs[0].set_ylabel('Radians')
        axs[0].set_xlabel('freq')
        if logFlag:
            axs[1].semilogx(X, errWeights, label='error weights')
        else:
            axs[1].plot(X, errWeights, label='error weights')
        axs[1].legend()
        axs[0].set_title(title1)
        axs[1].set_title(title2)
        plt.subplots_adjust(left=0.2,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.5)

    fig.canvas.draw_idle()
    fig.canvas.flush_events()
    if fwrite:
        # plt.savefig(fname, dpi=600, bbox_inches='tight')
        plt.savefig(fname, dpi=600)

def myPlot_1x_errweights(title1,title2,type,logFlag,X,Y1,errWeights,Y1label,fwrite,fname): # Y1 is target, Y2 is optimized

    fig, axs = plt.subplots(2)
    if type == 'fresp':
        if logflag:
            axs[0].semilogx(X, 20 * np.log10(Y1),label=Y1label)
        else:
            axs[0].plot(X, 20 * np.log10(Y1), label=Y1label)
        axs[0].legend()
        axs[0].set_ylabel('dB')
        axs[0].set_xlabel('freq')
        if logFlag:
            axs[1].semilogx(X,errWeights,label='error weights')
        else:
            axs[1].plot(X, errWeights, label='error weights')
        axs[1].legend()
        axs[0].set_title(title1)
        axs[1].set_title(title2)
        plt.subplots_adjust(left=0.2,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.5)

    if type == 'phase':
        if logflag:
            axs[0].semilogx(X, Y1,label=Y1label)
        else:
            axs[0].plot(X, Y1, label=Y1label)
        axs[0].legend()
        axs[0].set_ylabel('Radians')
        axs[0].set_xlabel('freq')
        axs[1].semilogx(X,errWeights,label='error weights')
        axs[1].legend()
        axs[0].set_title(title1)
        axs[1].set_title(title2)
        plt.subplots_adjust(left=0.2,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.5)

    if type == 'transient':
        axs[0].plot(X, Y1, label=Y1label)
        axs[0].legend()
        axs[0].set_ylabel('Volts')
        axs[0].set_xlabel('time')
        axs[1].plot(X, errWeights, label='error weights')
        axs[1].legend()
        axs[0].set_title(title1)
        axs[1].set_title(title2)
        plt.subplots_adjust(left=0.2,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.5)

    fig.canvas.draw_idle()
    fig.canvas.flush_events()
    if fwrite:
        plt.savefig(fname, dpi=600)