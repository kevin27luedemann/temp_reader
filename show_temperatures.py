import numpy as np
import sys,os
import matplotlib.pyplot as plt
from datetime import datetime as dt

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please hand over a file containing the temperatures!")
        sys.exit()
    if len(sys.argv) > 2:
        name        = np.copy(sys.argv[1:])
    else:
        name        = [sys.argv[1]]
    with open(name[0],"r") as fi:
        line    = fi.readline()
    line        = line.split("\t")
    line[-1]    = line[-1][:-1]
    data        = np.genfromtxt(name[0])
    if len(sys.argv) > 2:
        for na in name[1:]:
            data= np.append(data,np.genfromtxt(na),axis=0)

    time        = [dt.strptime("{:d}".format(int(ti)),"%Y%m%d%H%M%S") for ti in data[:,0]]
    time        = np.array(time)

    fig,ax      = plt.subplots()
    for i in range(len(line)-1):
        ax.plot(time,data[:,i+1],label=line[i+1])
    ax.grid(True)
    ax.set_xlabel("Temperature/°C")
    ax.legend(loc="best")
    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()
