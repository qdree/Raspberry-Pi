import os
import glob
import sys
# curDir = sys.argv[1]
curDir = os.getcwd()
for dirName, fileList in os.walk(curDir):
    #print('Found directory: %s' % dirName)
    for fname in fileList:
        fullName = os.path.join(dirName, fname)
        print fullName
    #     try:
    #        if fname.split(".")[-1] == "bin" and len(fname) > 15:
    #           os.rename(fullName, os.path.join(dirName, fname[:-15]+".bin"))
    #           print fullName +": ok"
    #     except OSError, e:
    #        print e + " for" + fullName