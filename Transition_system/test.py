from videoAccess import *
from kbd_identification import *
import RPi.GPIO as GPIO
import os
import time 

GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()
GPIO.setup(18, GPIO.OUT) #LED pin
GPIO.output(18, GPIO.LOW) #turn off LED

kbd_found = False
correct_pwd = False
active = False 
player_active = False
password = "arsenal"

#video setup before program workflow
input_name = raw_input("Input name:")
path = pathCreation(nameCheck(input_name))

movie = (path)
# os.system('vcgencmd display_power 0') #screen monitor switcher //OFF

#keyboard identification
while not kbdIden():
		pass
print "Keyboard added"

GPIO.output(18, GPIO.HIGH) #turn off LED

#password check
input_password = raw_input("ENTER PASSWORD:")
while not input_password == password:
	input_password = raw_input("ENTER PASSWORD:")
print ("Correct password!")

#	if not active:
		# os.system('vcgencmd display_power 1') #screen monitor switcher //ON
		# time.sleep(1.5)
#active = True
if not player_active:
	omxc = os.popen("omxplayer -b %s" %movie)
	print ("\nplayer started")
	player_active = True
	#time.sleep(2)
elif (player_active and os.system("pidof omxplayer.bin") == 256):
	print ("\nplayer is inactive")
	player_active = False
#	active = False

print ("Door is opened!")

#os.system("killall omxplayer.bin")

print ("\nEnd of program!")
