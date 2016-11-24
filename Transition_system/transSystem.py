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
	
video_name = dataReceive("(.*english.*) | (.*german.*)", ackPL)
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

def main_cycle():
	while True:
		pygame.init() #initialize pygame
		screen = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN) #create the screen
		pygame.mouse.set_visible(False)
		screen.fill((0,0,0)) # fill the screen black
		print "MESSAGES"	
		mode_message = dataReceive(".*", ackPL1)

		while True:
			tr_sys.processEvents()
			print "\nWhat mode ?"

			if mode_message == "open_door":
				print "!!!", mode_message, "!!!"
				
				print "\nKeyboard???"
				while not tr_sys.kbdIden(): #wait for keyboard
					if dataReceive(".*", ackPL1) == "by_pass":
						print "EXIT WHILE KEYBOARD AWAITING"
						return
					else: 
						pass
					tr_sys.processEvents()
					
				print "Keyboard added"
				GPIO.output(18, GPIO.HIGH) #turn on LED

				tr_sys.passChk(password)

				tr_sys.videoPlayback(path) #run video from path

				return
					
			elif mode_message == "by_pass":
				return
				print "RECEIVED MESSAGE TO EXIT"
		print "BLACK SCREEEEEEEEN"


main_cycle()
print "Door is opened"
GPIO.output(27, GPIO.HIGH) #short the relay

tr_sys.fillScreen((0,0,0))
