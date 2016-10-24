#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to send packets to the radio link
#


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev



pipes = [[0xF0, 0xF0, 0xF0, 0xF0, 0xE1], [0xAB, 0xCD, 0xAB, 0xCD, 0x71]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
time.sleep(1)
radio.setRetries(15,15)
radio.setPayloadSize(25)
radio.setChannel(0x76)

radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()


radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0]) 
radio.printDetails()


while True:
	message = list("Hello!")
	# send a packet to receiver
	radio.write(message)
	print ("Sent:{}".format(message))
	# did it return with a payload?
	if radio.isAckPayloadAvailable():
		returnedPL = []
		radio.read(returnedPL, radio.getDynamicPayloadSize())
		print ("Received back:{}".format(returnedPL))
	else:
		print ("No payload received")
	time.sleep(2)
