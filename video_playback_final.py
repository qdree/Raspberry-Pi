import RPi.GPIO as GPIO
import os
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT) #LED pin

movie = ("/home/pi/Videos/movie.mp4")
GPIO.output(18, GPIO.HIGH) #turn LED on 


start_button_state = True
previous_button_state = True

os.system('vcgencmd display_power 0')
active  = False
player_active  = False
print "\nStart"

while True:
	start_button_state = GPIO.input(17)
	
	# Check EXIT button
	if GPIO.input(24) == False:
		os.system('vcgencmd display_power 1')
		break        
	# Check  Start button
	if start_button_state != previous_button_state:
		if start_button_state == False: 
			sleep(0.2)
			start_button_control_check = GPIO.input(17)
			if  start_button_control_check == False:
				if not active:
					os.system('vcgencmd display_power 1')
					sleep(1.5)
					active = True
					omxc = os.popen('omxplayer -b %s' %movie)
					print "\nplayer started"	
					player_active = True	
					sleep(1)
				start_button_state = start_button_control_check
		previous_button_state = start_button_state
			
	# Check if player  ended
	if (player_active and os.system('pidof omxplayer.bin') == 256):
		print "\nplayer is inactive"
		player_active = False
		active = False
		GPIO.output(18, GPIO.LOW) # turn LED off
		os.system('vcgencmd display_power 0')
		
# finish and clean up
os.system('killall omxplayer.bin')
GPIO.cleanup()
print '\n', "Bye"
	
	


