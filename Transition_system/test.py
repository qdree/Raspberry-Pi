from videoAccess import *
from kbd_identification import *

kbd_found = False
password = "arsenal"

#video setup before program workflow
input_name = raw_input("Input name:")
try:
	pathCreation(nameCheck(input_name))
except Exception as e:
	print e

#keyboard identification
while not kbd_found:
	while not kbdIden():
		if kbdIden():
			print 'Keyboard added'
			kbd_found = True

input_password = raw_input("PASSWORD: ")

if input_password.lower() == password:
	print "Correct!!!!"