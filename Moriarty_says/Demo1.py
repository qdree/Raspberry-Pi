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


mon_video_setup = VideoSetup()
mon_comm = Communication()

def distanceMeasurement(dist_limit):
	while not distance >= dist_limit:

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
ackPL = [0]
ackPL1 = [1]

video_lang = morS_comm.dataReceive("(.*english.*) | (.*german.*)", ackPL)
name_start = morS_video_setup.pathCreation(morS_video_setup.nameCheck(video_lang+"start")) #create address to the video for game start
name_end = morS_video_setup.pathCreation(morS_video_setup.nameCheck(video_lang+"end")) #create address to the video for game start

name_lose = morS_video_setup.pathCreation(morS_video_setup.nameCheck(video_lang+"lose")) #create address to the video for lose
name_win = morS_video_setup.pathCreation(morS_video_setup.nameCheck(video_lang+"win")) #create address to the video for win
print "all video files were chosen"

while True:
	print "Ready to receive commands from bomb"

	if morS_comm.dataReceive(".*mor_off.*", ackPL1) == "mor_off":
		break
	elif morS_comm.dataReceive(".*mor_on.*", ackPL1) == "mor_on":
		pygame.init() #initialize pygame
		screen = pygame.display.set_mode((morS_video_setup.width,morS_video_setup.height), FULLSCREEN) #create the screen
		screen.fill((0,0,0)) # fill the screen black
		print "..."
		while not distanceMeasurement(1000): #wait til people come close enough to table
			morS_video_setup.processEvents()

		morS_video_setup.videoPlayback(name_start) #run video before game start
		
		GPIO.output(arduino_1, True)
		GPIO.output(arduino_2, True)

		if (GPIO.input(inArduino_1) == 0 and GPIO.input(inArduino_2) == 0):
			morS_video_setup.videoPlayback(name_end) #run video after game	

	if morS_comm.dataReceive(".*win.*", ackPL1) == "win":
		morS_video_setup.videoPlayback(name_win) #run video if bomb was disarmed
		break

	if morS_comm.dataReceive(".*lose.*", ackPL1) == "lose":
		morS_video_setup.videoPlayback(name_win) #run video if bomd exploded
		break


morS_video_setup.fillScreen((0,0,0))

		

