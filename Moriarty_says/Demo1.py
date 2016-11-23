from morSaysInit import *

TRIG = 23 
ECHO = 24
inArduino_1 = 14
inArduino_2 = 15
outArduino_1 = 22
outArduino_2 = 27

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(inArduino_1, GPIO.IN)
GPIO.setup(inArduino_2, GPIO.IN)
GPIO.setup(outArduino_1, GPIO.OUT)
GPIO.setup(outArduino_2, GPIO.OUT)


morS_video_setup = VideoSetup()
morS_comm = Communication()

def distanceMeasurement():
	#produce impulse 
	GPIO.output(TRIG, True)
	wait(0.00001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO) == 0:
		pulse_start = time.time()
	while GPIO.input(ECHO) == 1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance, 2)
	print ("Distance: {}cm".format(distance))
	return distance


pipes = [[0xAB, 0xCD, 0xAB, 0xCD, 0x71], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE2]]
radio.begin(0,17)
radio.setRetries(0,15)
radio.setPayloadSize(25)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])
radio.startListening()
radio.printDetails()

#input_name = raw_input("Input name:")

video_lang = morS_comm.dataReceive("(.*english.*) | (.*german.*)")

name_start = ''
name_end = ''

name_lose = ''
name_win = ''

def nameSet(language):
	name_start = morS_video_setup.pathCreation(morS_video_setup.nameCheck(language + "start")) #create address to the video for game start
	name_end = morS_video_setup.pathCreation(morS_video_setup.nameCheck(language + "end")) #create address to the video for game start

	name_lose = morS_video_setup.pathCreation(morS_video_setup.nameCheck(language + "lose")) #create address to the video for lose
	name_win = morS_video_setup.pathCreation(morS_video_setup.nameCheck(language + "win")) #create address to the video for win


while True:
	if (name_start == None or name_end == None or name_win == None or name_lose == None):
		nameSet(video_lang)	
	elif (len(name_start) <= 1 or len(name_end) <= 1 or len(name_win) <= 1 or len(name_lose) <= 1):
		nameSet(video_lang)
	else:
		break

print "all video files were chosen"

while True:
	game_mode_message = morS_comm.dataReceive("(.*mor_on.*) | (.*mor_off.*)") #message from Quest Control Panel

	if game_mode_message == "mor_on":
		print "..."
		pygame.init() #initialize pygame
		screen = pygame.display.set_mode((morS_video_setup.WIDTH,morS_video_setup.HEIGHT), FULLSCREEN) #create the screen
		pygame.mouse.set_visible(False)
		screen.fill((0,0,0)) # fill the screen black

		while distanceMeasurement() >= float(5): #wait til people come close enough to table
			print "Measuring...."
			events = pygame.event.get()
			
			#process other events
			for event in events:
				mods = pygame.key.get_mods()
				if event.type == QUIT: quit()
				if event.type == KEYDOWN:
					if event.key == K_F10 and mods & pygame.KMOD_RSHIFT and mods & pygame.KMOD_CTRL:
						quit() 
 
		print "\nLET'S GAME BEGINS!!!!"

		morS_video_setup.videoPlayback(name_start) #run video before game start
				
		GPIO.output(outArduino_1, True)
		GPIO.output(outArduino_2, True)

		print "\nYOU WON THE GAME!!!!"
		if (GPIO.input(inArduino_1) == 0 and GPIO.input(inArduino_2) == 0):
			morS_video_setup.videoPlayback(name_end) #run video after game	
		print "\nReady to receive commands from bomb"
	
		bomb_state_massage = morS_comm.dataReceive("(.*win.*) | (.*lose.*) ") #message from Bomb

		if bomb_state_massage == "win":
			morS_video_setup.videoPlayback(name_win) #run video if bomb was disarmed
			print "\nBOMB DISARMED!!!! CONGRATULATIONS"
			break
		elif bomb_state_massage == "lose":
			morS_video_setup.videoPlayback(name_win) #run video if bomd exploded
			print "\nBOMB EXPLODED!!!!"
			break

	elif game_mode_message == "mor_off":
		break

print "FINISH"
morS_video_setup.fillScreen((0,0,0))
