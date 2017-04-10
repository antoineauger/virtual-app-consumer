import logging
import sys

logging.basicConfig(level=logging.WARNING)


# Helper function and check of the arguments supplied
def usage():
    """ Print short help """
    print("#################################################################")
    print("#                                                               #")
    print("# iQAS: an integration platform for QoO Assessment as a Service #")
    print("# Module: Virtual App Consumer                                  #")
    print("# (C) 2017 Antoine Auger                                        #")
    print("#                                                               #")
    print("#################################################################\n")

if len(sys.argv) != 1:
    usage()
    print('ERROR: Wrong number of parameters')
    exit()
