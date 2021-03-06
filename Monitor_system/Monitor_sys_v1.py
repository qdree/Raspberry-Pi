from monitorInit import *

mon_video_setup = VideoSetup()
mon_comm = Communication()

pipes = [[0xAB, 0xCD, 0xAB, 0xCD, 0x82], [0xAB, 0xCD, 0xAB, 0xCD, 0x86], [0xAB, 0xCD, 0xAB, 0xCD, 0x85]]
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

path = ''

while True:
	if path == None:
		path = mon_video_setup.pathCreation(video_name) #create address to the video
	elif len(path) <= 1:
		path = mon_video_setup.pathCreation(video_name) #create address to the video
	else:
		break

print path, type(path)

print "video name chosen"


# RECEIVING COMMAND FROM "BRACELET"
while True:
	print "Ready to receive commands from bracelet"
	pygame.init() #initialize pygame
	screen = pygame.display.set_mode((mon_video_setup.WIDTH ,mon_video_setup.HEIGHT), FULLSCREEN) #create the screen
	pygame.mouse.set_visible(False)
	screen.fill((0,0,0)) # fill the screen black
	
	print "..."
	
	while not mon_comm.dataReceive(".*OnHand.*", ackPL1) == "onhand": #wait correct message
		mon_video_setup.processEvents()
				
	radio.writeAckPayload(1, ackPL1, len(ackPL1)) #send acknowledgement about OnHand operation

	mon_video_setup.videoPlayback(path) #run video from path
	
	print "Ready to send message"
	
	#TRANSMITTING COMMAND TO "BOMB"
	radio.stopListening()
	radio.openWritingPipe(pipes[2])

	while not mon_comm.dataTransmit("timer_start"):
		mon_video_setup.processEvents()
	break

mon_video_setup.fillScreen((0,0,0))
