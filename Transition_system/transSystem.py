# import time
from  transitionInit import *

password = "arsenal"

input_name = raw_input("Input name:")
# path = pathCreation(nameCheck(input_name))
# movie = (path)

tr_sys = Transition()
path = tr_sys.pathCreation(tr_sys.nameCheck(input_name))

while not tr_sys.kbdIden():
		pass
print "Keyboard added"

while not tr_sys.passChk(password):
	pass

tr_sys.videoPlayback(path)