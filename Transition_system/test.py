from videoAccess import *
from kbd_identification import *
import RPi.GPIO as GPIO
import os
import time 

player_active = False
password = "arsenal"

#pins setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT) #LED pin
GPIO.output(18, GPIO.LOW) #turn off LED

#video setup before program workflow 
#test version. finaly name should be recieved from radio transmitter, not from input form
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
#Test version, final one should have animated "PASSWORD" text with some animation of text input. 
#Possibly will be created using PyGame
input_password = raw_input("ENTER PASSWORD:")
while not input_password == password:
	input_password = raw_input("ENTER PASSWORD:")
print ("Correct password!")

#if possible following operation will be replaced with another one, which suspends screen but not disables it
# os.system('vcgencmd display_power 1') #screen monitor switcher //ON
# time.sleep(1.5)

#video playback
while True:
	if not player_active:
		omxc = os.popen("omxplayer -b %s" %movie)
		print ("\nplayer started")
		player_active = True
		time.sleep(1)
	if (player_active and os.system("pidof omxplayer.bin") == 256): #check if player opened and process finished
		print ("\nplayer is inactive")
		player_active = False
		break

#test output. final should unlock electrical magnet	
print ("Door is opened!")
#os.system("killall omxplayer.bin")

print ("\nEnd of program!")
