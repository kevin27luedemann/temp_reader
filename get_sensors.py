import sys,os,signal
from glob import glob
import numpy as np
from datetime import datetime as dt
import time
from optparse import OptionParser

keep_running        = True

def signal_handler(signum, frame):
    global keep_running
    keep_running    = False

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

def get_sensors():
    sensors     = [se +"/w1_slave" for se in glob("/sys/bus/w1/devices/28*")]
    if len(sensors) == 0:
        print("No sensors found!")
        sys.exit(1)
    return sensors

def read_sensor(se):
    with open(se,"r") as fi:
        data = fi.read()
    se_name     = LUT_bez[se.split("/")[-2]]
    tempera     = float(data.split("t")[-1][1:])*0.001
    return se_name,tempera

def init_file(praefix="", postfix=""):
    now         = dt.strftime(dt.now(),"%Y%m%d_%H%M%S")
    output      = open(praefix+"{}.dat".format(now)+postfix,"a")
    output.write("#")
    for se in sensors:
        se_name,_   = read_sensor(se)
        output.write("\t{}".format(se_name))
    output.write("\n")
    return output

def init_db_client(db):
    return db

def loop(sensors,output,db_client="",quiet=False):
    while keep_running:
        now         = dt.strftime(dt.now(),"%Y%m%d_%H%M%S")
        out         = "{}".format(now)

        for se in sensors:
            _,tempera       = read_sensor(se)
            out        += "\t{}".format(tempera)
        out            += "\n"

        output.write(out)
        output.flush()
        if not(quiet):
            print(out[:-1])
        time.sleep(2)

if __name__ == "__main__":
    signal.signal(signal.SIGINT,  signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = OptionParser()

    parser.add_option(  "-f", "--praefix", dest="praefix",default="",
                        help="File praefix and folder localtion")
    parser.add_option(  "", "--postfix", dest="postfix",default="",
                        help="Specify custom input file postfix")
    parser.add_option(  "", "--db", dest="db",default="",
                        help="Store into database")
    parser.add_option(  "-q", "--quiet", dest="quiet",
                        action="store_true",default=False,
                        help="Make the script quiet and do not print to STDOUT.")

    (options, args) = parser.parse_args()

    sensors     = get_sensors()
    output      = init_file(praefix=options.praefix,postfix=options.postfix)

    if options.db != "":
        client  = init_db_client(db)
    else:
        client  = ""

    loop(sensors,output,db_client=client,quiet=options.quiet)

    output.close()
