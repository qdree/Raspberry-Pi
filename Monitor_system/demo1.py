from monitorInit import *

mon_video_setup = VideoSetup()
mon_comm = Communication()

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

video_name = mon_comm.dataReceive("(.*english.*) | (.*german.*)", ackPL)
path = mon_video_setup.pathCreation(mon_video_setup.nameCheck(video_name)) #create address to the video
print "video name chosen"


# RECEIVING COMMAND FROM "BRACELET"
while True:
	print "Ready to receive commands from bracelet"
	pygame.init() #initialize pygame
	screen = pygame.display.set_mode((mon_video_setup.width,mon_video_setup.height), FULLSCREEN) #create the screen
	screen.fill((0,0,0)) # fill the screen black
	print "..."
	while not mon_comm.dataReceive(".*OnHand.*", ackPL1) == "onhand": #wait for keyboard
		events = pygame.event.get() 
		# process other events
		for event in events:
			mods = pygame.key.get_mods()
			if event.type == KEYDOWN:
				if event.key == K_F10 and mods & pygame.KMOD_RSHIFT and mods & pygame.KMOD_CTRL: #program exit combination
					quit()
				
	radio.writeAckPayload(1, ackPL1, len(ackPL1)) #send acknowledgement about OnHand operation

	mon_video_setup.videoPlayback(path) #run video from path
	break

print "Ready to send message"
#TRANSMITTING COMMAND TO "BOMB"
radio.stopListening()
radio.openWritingPipe(pipes[2])
mon_video_setup.fillScreen((0,0,0))
while not mon_comm.dataTransmit("timer_start"):
	pass
