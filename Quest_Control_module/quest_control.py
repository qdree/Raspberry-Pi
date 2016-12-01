import sys
from ControlPanel_Init import *

conPanel_comm = C#open pipe to Bomb system ommunication()

pipes = [[0xAB, 0xCD, 0xAB, 0xCD, 0x81], [0xAB, 0xCD, 0xAB, 0xCD, 0x82], [0xAB, 0xCD, 0xAB, 0xCD, 0x83], [0xAB, 0xCD, 0xAB, 0xCD, 0x84], [0xAB, 0xCD, 0xAB, 0xCD, 0x85]]
radio.begin(0,17)
radio.setRetries(0,15)
radio.setPayloadSize(25)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[0])
radio.startListening()
radio.printDetails()

ackPL = [0]

commmand = sys.argv[1]

if commmand == english:
	for i in range(1,5):
		radio.openWritingPipe(pipes[i]) #open pipe to all devices in network 
		conPanel_comm.dataTransmit("english")
elif commmand == german:
	for i in range(1,5):
		radio.openWritingPipe(pipes[i]) #open pipe to all devices in network 
		conPanel_comm.dataTransmit("german")
elif commmand == mor_on:
	radio.openWritingPipe(pipes[2]) #open pipe to Moriarty Says system
	conPanel_comm.dataTransmit("mor_on")
elif commmand == mor_off:
	radio.openWritingPipe(pipes[2])
	conPanel_comm.dataTransmit("mor_off") #open pipe to Moriarty Says system
elif commmand == open_door:
	radio.openWritingPipe(pipes[3]) #open pipe to Transition system 
	conPanel_comm.dataTransmit("open_door") 
elif commmand == by_pass:
	radio.openWritingPipe(pipes[3]) #open pipe to Transition system 
	conPanel_comm.dataTransmit("by_pass")
elif commmand == time_on:
	radio.openWritingPipe(pipes[4]) #open pipe to Bomb system 
	conPanel_comm.dataTransmit("time_on")
elif commmand == time_stop:
	radio.openWritingPipe(pipes[4]) #open pipe to Bomb system 
	conPanel_comm.dataTransmit("time_stop")
elif commmand == bomb_on:
	radio.openWritingPipe(pipes[4]) #open pipe to Bomb system 
	conPanel_comm.dataTransmit("bomb_on")
elif commmand == bomb_off:
	radio.openWritingPipe(pipes[4]) #open pipe to Bomb system 
	conPanel_comm.dataTransmit("bomb_off")