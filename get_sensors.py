import sys,os
from glob import glob
import numpy as np
from datetime import datetime as dt
import time

LUT = { "28-01212fc82672":"0",
        "28-0321316c7509":"1",
        "28-03213176d537":"1 Ring",
        "28-012131ef6bc0":"2 Ring",
        "28-01212fd0a894":"3 Ring"}

LUT_bez = { "28-01212fc82672":"der erste",
            "28-0321316c7509":"der zweite",
            "28-03213176d537":"1 Ring",
            "28-012131ef6bc0":"2 Ring",
            "28-01212fd0a894":"3 Ring"}

if __name__ == "__main__":
    sensors     = [se +"/w1_slave" for se in glob("/sys/bus/w1/devices/28*")]
    if len(sensors) == 0:
        print("No sensors found!")
        sys.exit(1)
    now         = dt.strftime(dt.now(),"%Y%m%d_%H%M%S")
    output      = open("{}.dat".format(now),"a")
    output.write("#")
    for se in sensors:
        se_name     = LUT_bez[se.split("/")[-2]]
        output.write("\t{}".format(se_name))
    output.write("\n")
    while True:
        now         = dt.strftime(dt.now(),"%Y%m%d_%H%M%S")
        out         = "{}".format(now)
        for se in sensors:
            with open(se,"r") as fi:
                data = fi.read()
            se_name     = LUT_bez[se.split("/")[-2]]
            tempera     = float(data.split("t")[-1][1:])*0.001
            out        += "\t{}".format(tempera)
        out            += "\n"

        output.write(out)
        output.flush()
        print(out[:-1])
        time.sleep(2)


    output.close()
