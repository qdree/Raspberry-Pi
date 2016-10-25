from  transitionInit import *

tr_sys = Transition()

def wait(seconds):
	start_time = time.time()
	while True:
		current_time = time.time()
		if current_time - start_time == seconds:
			return

def dataReceive():
	while not radio.available(0):
		wait(1/100)

	recv_message = []
	radio.read(recv_message, radio.getDynamicPayloadSize())
	print ("Received: {}".format(recv_message))
	print ("Translating the received message...")
	string = ""
	for n in recv_message:
		# Decode into standart unicode set
		if (n >= 32 and n <= 126):
			string += chr(n)
			return string.lower()		

pipes = [[0xF0, 0xF0, 0xF0, 0xF0, 0xE4], [0xAB, 0xCD, 0xAB, 0xCD, 0x74]]
#radio.begin(0, 17)
radio.setPayloadSize(25)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.startListening()
radio.printDetails()

password = "arsenal"

# input_name = raw_input("Input name:")
ackPL = [0]
ackPL1 = [1]
ackPL2 = [2]

while not re.match('.+english.+ | .+german.+', dataReceive()): #wait for video name, to set quest language
	dataReceive()
	radio.writeAckPayload(1, ackPL, len(ackPL)) #send acknowledgement that video name recognized

video_name = name_from_rad

while True:
	received_string = dataReceive()
	if received_string == "by_pass":
		radio.writeAckPayload(1, ackPL1, len(ackPL1)) #send acknowledgement about by_pass operation
		break
	elif received_string == "open_door":
		radio.writeAckPayload(1, ackPL2, len(ackPL2)) #send acknowledgement about open_door operation
#		tr_sys = Transition()
		path = tr_sys.pathCreation(tr_sys.nameCheck(video_name)) #create address to the video
		#path = tr_sys.pathCreation("samplevideo")

		pygame.init() #initialize pygame
		screen = pygame.display.set_mode((tr_sys.width,tr_sys.height), FULLSCREEN) #create the screen
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

print "Door is opened"
tr_sys.fillScreen((0,0,0))
