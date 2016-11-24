import re, os, gtk.gdk, pygame, sys, time, spidev
from pygame.locals import *
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24

GPIO.setmode(GPIO.BCM)
radio = NRF24(GPIO, spidev.SpiDev())

def wait(seconds):
	start_time = time.time()
	while True:
		current_time = time.time()
		#print (float(current_time - start_time))
		if float(current_time - start_time) >= seconds:
			break

class VideoSetup:
	def __init__(self):

		GPIO.setwarnings(False)
		GPIO.setup(27, GPIO.OUT) #Relay pin
		GPIO.output(27, GPIO.LOW) #set relay in open state
			
		
		self.WIDTH = 800
		self.HEIGHT = 600

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
		video_lang = str(vName).split('.')[0].lower()
		pattern = re.compile(r'(.*\.mp4) | (.*\.mpeg) | (.*\.avi) | (.*\.mkv) | (.*\.divx)', flags = re.I | re.X | re.U) #pattern for regex
		os.chdir('/media/')

		for dirName, curdirList, fileList in os.walk(os.getcwd()): #iterate through generator of pathes
			for file in fileList:
				full_path = os.path.join(dirName, file) #full path to file creation
				re_file = str(pattern.findall(str(full_path))).split('/') #get all files matching the pattern 
				if len(re_file) > 1:
					file_full_name = re_file[-1].translate(None, ',()[]\'\"') #chars to avoid in name
					file_name = file_full_name.split('.')[0] #pure name without format
					
					if re.match("(.*{}.*)".format(video_lang), file_name):
					#if video_name == file_name.lower(): #check chosen file with files from a list
						print ('Path to target file : {0}'.format(full_path))
						return full_path
					else:
						print ("Found : {0} located in :{1}".format(file_full_name, full_path))

	def videoPlayback(self, movie):
		
		#start_time = time.time()
		while True:
			if not self.player_active:
				omxc = os.popen("omxplayer -b %s" %movie)
				print ("\nplayer started")
				self.player_active = True
				wait(1)
				
		#	current_time = time.time()
#			if (float(current_time - start_time) >= 1 and self.player_active and os.system("pidof omxplayer.bin") == 256): #check if player opened and process finished
			if (self.player_active and os.system("pidof omxplayer.bin") == 256): #check if player opened and process finished
				#print current_time - start_time
				print ("\nplayer is inactive")
				self.player_active = False
				break
	
	def processEvents(self):
		events = pygame.event.get()
		
		# process other events
		for event in events:
			mods = pygame.key.get_mods()
			if event.type == QUIT: return
			if event.type == KEYDOWN:
				if event.key == K_F10 and mods & pygame.KMOD_RSHIFT and mods & pygame.KMOD_CTRL:
					quit()
					
	
	def fillScreen(self, color):
		pygame.init() #initialize pygame
		screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT), FULLSCREEN) #create the screen
		pygame.mouse.set_visible(False)
		screen.fill(color) # fill the screen black
		while True:
			self.processEvents()


class Communication(VideoSetup):

	def dataReceive(self, find_that):
		radio.startListening()
		pattern = re.compile(find_that, flags = re.I | re.X | re.U)
		string = ""
		ack = [1]
		while True:
			if radio.available(0):
				recv_message = []
				radio.read(recv_message, radio.getDynamicPayloadSize())
				print ("Received: {}".format(recv_message))
				print ("Translating the received message...")
				
				for n in recv_message:
					# Decode into standart unicode set
					if (n >= 32 and n <= 126):
						string += chr(n)
				print (string)
				if pattern.match(string):
					radio.writeAckPayload(1, ack, len(ack)) #send acknowledgement
					print ("Loaded payload reply of {}".format(ack))
					radio.stopListening()
					return string.lower()
				else:
					string = ''

	def dataTransmit(self, string):
		while True:
			message = list(string)
			# send a packet to receiver
			radio.write(message)
			print ("Sent:{}".format(message))
			# did it return with a payload?
			if radio.isAckPayloadAvailable():
				returnedPL = []
				radio.read(returnedPL, radio.getDynamicPayloadSize())
				print ("Received back:{}".format(returnedPL))
				return True
			else:
				print ("No payload received")

			wait(1)

	
