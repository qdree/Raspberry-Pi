#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to receive packets from the radio link
#

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev



pipes = [[0xF0, 0xF0, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE2], [0xAB, 0xCD, 0xAB, 0xCD, 0x71], [0xAB, 0xCD, 0xAB, 0xCD, 0x72]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setRetries(0,15)

radio.setPayloadSize(25)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

#radio.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[2])
radio.openReadingPipe(2, pipes[3])

radio.printDetails()
#radio.startListening()

while True:
	radio.startListening()
	ackPL1 = [1]
	ackPL2 = [2]
	while not radio.available(0):
		time.sleep(1/100)

	recv_message = []
	radio.read(recv_message, radio.getDynamicPayloadSize())
	print ("Received: {}".format(recv_message))
	print ("Translating the received message...")
	string = ""
	for n in recv_message:
		# Decode into standart unicode set
		if (n >= 32 and n <= 126):
			string += chr(n)
	print (string)
	radio.openWritingPipe(pipes[0])
	radio.writeAckPayload(1, ackPL1, len(ackPL1))
	radio.stopListening()
#	radio.startListening()
	radio.openWritingPipe(pipes[1])
	radio.writeAckPayload(2, ackPL2, len(ackPL2))
	print ("Loaded payload reply of {0}, to first dev and {1} to second".format(ackPL1, ackPL2))
