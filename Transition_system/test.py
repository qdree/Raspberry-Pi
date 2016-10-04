from videoAccess import *
from kbd_identification import *

kbd_found = False
correct_pwd = False
password = "arsenal"

#video setup before program workflow
input_name = raw_input("Input name:")
pathCreation(nameCheck(input_name))

#keyboard identification
while not kbdIden():
		pass
print 'Keyboard added'

#password check
input_password = raw_input("ENTER PASSWORD:")
while not input_password == password:
	input_password = raw_input("ENTER PASSWORD:")