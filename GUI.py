#!/usr/bin/env python
# -*- coding: utf8 -*-

import Globals
import HelperFunctions
import UserFunctions

import RPi.GPIO as GPIO
import MFRC522
import signal
import json
import time
import os
import io
import codecs
from appJar import gui

Globals.init()

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
	#global continue_reading
	print "Ctrl+C captured, ending read."
	Globals.continue_reading = False
	GPIO.cleanup()
	Globals.app.stop()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

def start_loop(action):
	# This loop keeps checking for chips. If one is near it will get the UID and authenticate
	while Globals.continue_reading:
		HelperFunctions.reset_labels()
		
		# Scan for cards    
		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

		# Get the UID of the card
		(status, Globals.uid) = MIFAREReader.MFRC522_Anticoll()

		# If we have the UID, continue
		if status == MIFAREReader.MI_OK:
			Globals.uidStr = str(Globals.uid[0])+","+str(Globals.uid[1])+","+str(Globals.uid[2])+","+str(Globals.uid[3])
		
			if action == 0:
				UserFunctions.get_user()
			elif action == 1:
				UserFunctions.add_user()
			
			# Select the scanned tag
			MIFAREReader.MFRC522_SelectTag(Globals.uid)
			
			time.sleep(5)

def init_app():
	HelperFunctions.draw_timetable()
	
	Globals.app.startLabelFrame("Message", 3, 0)
	
	Globals.app.setSticky("news")
	
	Globals.app.addEmptyLabel('msg')
	Globals.app.setLabelWidths('msg', 700)
	
	Globals.app.stopLabelFrame()
	
	start_loop(0)

Globals.app.setGeometry("800x600")
Globals.app.setStretch("both")
Globals.app.thread(init_app)
Globals.app.go()
