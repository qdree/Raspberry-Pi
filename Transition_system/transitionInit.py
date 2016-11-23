import pyudev 
import evdev 
import functools
import re
import os
#import gtk.gdk
from pygame.locals import *
import pygame, sys, eztext
import RPi.GPIO as GPIO
import time
from lib_nrf24 import NRF24
import spidev

#radio = NRF24(GPIO, spidev.SpiDev())
GPIO.setmode(GPIO.BCM)
radio = NRF24(GPIO, spidev.SpiDev())
HEIGHT = 800
WIDTH = 600

def wait(seconds):
	start_time = time.time()
	while True:
		current_time = time.time()
		#print (float(current_time - start_time))
		if float(current_time - start_time) >= seconds:
			break

class Transition:
	def __init__(self):
		
		GPIO.setup(18, GPIO.OUT) #LED pin
		GPIO.output(18, GPIO.LOW) #turn off LED
		GPIO.setwarnings(False)
				
		self.context = pyudev.Context()
		self.monitor = pyudev.Monitor.from_netlink(self.context)
		self.monitor.filter_by(subsystem = 'input')

		#self.width = gtk.gdk.screen_width() #get screen width
		#self.height = gtk.gdk.screen_height() #get screen height

		self.player_active = False #player activity flag

	def nameCheck(self, fName):
		
		try: #if logfile present
			with open('logfile.txt', 'r+') as logfile:
				for line in logfile: #iterate though logfile
					if line == fName or len(fName) < 1:
						return line
					else:
						logfile.seek(0)
						logfile.truncate() #cleanup
						logfile.write(fName)
						logfile.flush()
						return fName

		except IOError: #if no logfile
			with open('logfile.txt', 'w') as logfile: #create file
				logfile.write(fName)
				logfile.flush() 
			return fName

		print fName
		
	def pathCreation(self, vName):
		video_name = str(vName).split('.')[0].lower()
		pattern = re.compile(r'(.*\.mp4) | (.*\.mpeg) | (.*\.avi) | (.*\.mkv)', flags = re.I | re.X | re.U) #pattern for regex
		os.chdir('/media/')

		for dirName, curdirList, fileList in os.walk(os.getcwd()): #iterate through generator of pathes
			for file in fileList:
				full_path = os.path.join(dirName, file) #full path to file creation
				re_file = str(pattern.findall(str(full_path))).split('/') #get all files matching the pattern 
				if len(re_file) > 1:
					file_full_name = re_file[-1].translate(None, ',()[]\'\"') #chars to avoid in name
					file_name = file_full_name.split('.')[0] #pure name without format
					
					if video_name == file_name.lower(): #check chosen file with files from a list
						print ('Path to target file : {0}'.format(full_path))
						return full_path
					else:
						print ("Found : {0} located in :{1}".format(file_full_name, full_path))

	def videoPlayback(self, movie):
		
		start_time = time.time()
		while True:
			if not self.player_active:
				omxc = os.popen("omxplayer -b %s" %movie)
				print ("\nplayer started")
				self.player_active = True
				
			current_time = time.time()
			if (float(current_time - start_time) >= 1.5 and self.player_active and os.system("pidof omxplayer.bin") == 256): #check if player opened and process finished
				print current_time - start_time
				print ("\nplayer is inactive")
				self.player_active = False
				break

	def kbdIden(self):
		
		target_device_data = [] #list to store recieved data about device
		for device in iter(functools.partial(self.monitor.poll, 0), None):
				#print ('{0.action} on {0.device_path}'.format(device))

				target_device_data.append(device.device_path) #data collection
				try:
					if device.action == "add":
						for dev in target_device_data:
							splitted = dev.split('/')
							target = splitted[-1]
							if re.match('event[0-9+]',target): #check of event.. param.
								added_dev = str(evdev.InputDevice('/dev/input/{0}'.format(target))).split('/') #data collection about target device
								#print (added_dev)
								#re_addded_dev  = re.findall('.*name ".* Keyboard".*', added_dev[3])
								if re.match('.*name ".* Keyboard".*', added_dev[3]): #check if target device is keyboard
									print ('Added device is {}'.format(added_dev[3]))
									return True
				except Exception as e:
					print (e)

	def passChk(self, password):
	   
		pygame.init() #initialize pygame
		#screen = pygame.display.set_mode((self.width,self.height), FULLSCREEN) #create the screen
		screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN) #create the screen
		pygame.mouse.set_visible(False)

		screen.fill((255,255,255)) # fill the screen black

		text = eztext.Input(maxlength=20, color=(255,255,255), prompt='PASSWORD:', font = pygame.font.Font(None, 62))
		clock = pygame.time.Clock() #create the pygame clock

		while True:
			clock.tick(15) # make sure the program is running at 15 fps
			text.set_pos(WIDTH/2.0, HEIGHT/2.0)

			# events for text
			events = pygame.event.get()

			# process other events
			for event in events:
				mods = pygame.key.get_mods()
				if event.type == QUIT: return
				if event.type == KEYDOWN:
					if event.key == K_F10 and mods & pygame.KMOD_RSHIFT and mods & pygame.KMOD_CTRL:
						quit()

			screen.fill((0,0,0)) #clear the screen
			text.update(events) #update text

			# check password input
			if text.chk_value(password):
				print "correct"
				return True
			else:
				print "something wrong"

			text.draw(screen) #blit text on screen
			pygame.display.flip() #refresh display
			
	def fillScreen(self, color):
		pygame.init() #initialize pygame
		screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN) #create the screen
		pygame.mouse.set_visible(False)
		screen.fill(color) # fill the screen black
		while True:
			events = pygame.event.get()
			
			# process other events
			for event in events:
				mods = pygame.key.get_mods()
				if event.type == QUIT: return
				if event.type == KEYDOWN:
					if event.key == K_F10 and mods & pygame.KMOD_RSHIFT and mods & pygame.KMOD_CTRL:
						quit()
