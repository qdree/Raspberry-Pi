from  transitionInit import *

wait(1)

tr_sys = Transition()

pipes = [[0xAB, 0xCD, 0xAB, 0xCD, 0x71], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]
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

password = "arsenal"

#input_name = raw_input("Input name:")
ackPL = [0]
ackPL1 = [1]
ackPL2 = [2]


def dataReceive(find_that, ack):
	pattern = re.compile(find_that, flags = re.I | re.X | re.U)
	string = ""
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
				radio.writeAckPayload(1, ack, len(ack)) #send acknowledgementnht
				print ("Loaded payload reply of {}".format(ack))
				return string
			else:
				string = ''
	
video_name = tr_sys.nameCheck(dataReceive("(.*english.*) | (.*german.*)", ackPL))
path = ''

while True:
	if path == None:
		path = tr_sys.pathCreation(video_name) #create address to the video
	elif len(path) <= 1:
		path = tr_sys.pathCreation(video_name) #create address to the video
	else:
		break

print path, type(path)

print "video name chosen"

while True:
	mode_message = dataReceive("(.*by_pass.*) | .*open_door.*", ackPL1)

	if mode_message == "by_pass":
		break
	elif mode_message == "open_door":
		radio.writeAckPayload(1, ackPL2, len(ackPL2)) #send acknowledgement about open_door operation
		pygame.init() #initialize pygame
		#screen = pygame.display.set_mode((tr_sys.width,tr_sys.height), FULLSCREEN) #create the screen
		screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN) #create the screen
		pygame.mouse.set_visible(False)
		screen.fill((0,0,0)) # fill the screen black
		while not tr_sys.kbdIden(): #wait for keyboard
			events = pygame.event.get() 
			# process other events
			for event in events:
				mods = pygame.key.get_mods()
				if event.type == KEYDOWN:
					if event.key == K_F10 and mods & pygame.KMOD_RSHIFT and mods & pygame.KMOD_CTRL: #program exit combination
						quit()
					
		print "Keyboard added"

		while not tr_sys.passChk(password): #wait for correct password
			pass

		tr_sys.videoPlayback(path) #run video from path
		break
	else:
		print "Unknown command"
		tr_sys.fillScreen((0,0,0))

print "Door is opened"
tr_sys.fillScreen((0,0,0))
