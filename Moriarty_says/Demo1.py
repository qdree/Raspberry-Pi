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

while True:
	if (name_start == None or len(name_start) <= 1):
		name_start = morS_video_setup.pathCreation(video_lang + "start") #create address to the video for game start
	else:
		if (name_end == None or len(name_end) <= 1):
			name_end = morS_video_setup.pathCreation(str(video_lang) + "end") #create address to the video for game start
		else:
			if (name_win == None or len(name_win) <= 1):
				name_win = morS_video_setup.pathCreation(str(video_lang) + "win") #create address to the video for game start
			else:
				if (name_lose == None or len(name_lose) <= 1):
					name_lose = morS_video_setup.pathCreation(str(video_lang) + "lose") #create address to the video for game start
				else:
					break

print "all video files were chosen"

def main_cycle():
	while True:
		pygame.init() #initialize pygame
		screen = pygame.display.set_mode((morS_video_setup.WIDTH,morS_video_setup.HEIGHT), FULLSCREEN) #create the screen
		pygame.mouse.set_visible(False)
		screen.fill((0,0,0)) # fill the screen black
		
		game_mode_message = morS_comm.dataReceive(".*") #message from Quest Control Panel
		while True:
			morS_video_setup.processEvents()
			if game_mode_message == "mor_on":
				print "..."

				while distanceMeasurement() >= float(5): #wait til people come close enough to table
					if morS_comm.dataReceive(".*") == "mor_off":
						return
					else:
						print "Measuring...."
						pass
					morS_video_setup.processEvents()
		 
				print "\nLET'S GAME BEGINS!!!!"

				morS_video_setup.videoPlayback(name_start) #run video before game start
						
				GPIO.output(outArduino_1, True)
				GPIO.output(outArduino_2, True)

				print "WAITING FOR PLAYERS SUCCESS"
				while not (GPIO.input(inArduino_1) == 1 and GPIO.input(inArduino_2) == 1):
					if morS_comm.dataReceive(".*") == "mor_off":
						return
					else: 
						pass
					morS_video_setup.processEvents()
			
				morS_video_setup.videoPlayback(name_end) #run video after game	
				print "\nYOU WON THE GAME!!!!"
				GPIO.output(27, GPIO.HIGH) #short relay in open state


				print "\nReady to receive commands from bomb"
			
				bomb_state_massage = morS_comm.dataReceive("(.*win.*) | (.*lose.*) ") #message from Bomb

				if bomb_state_massage == "win":
					morS_video_setup.videoPlayback(name_win) #run video if bomb was disarmed
					print "\nBOMB DISARMED!!!! CONGRATULATIONS"
					return
				elif bomb_state_massage == "lose":
					morS_video_setup.videoPlayback(name_win) #run video if bomd exploded
					print "\nBOMB EXPLODED!!!!"
					return

			elif game_mode_message == "mor_off":
				return

main_cycle()

print "FINISH"
morS_video_setup.fillScreen((0,0,0))
