#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import json

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
	global continue_reading
	print "Ctrl+C captured, ending read."
	continue_reading = False
	GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
	
	# Scan for cards    
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

	# If a card is found
	if status == MIFAREReader.MI_OK:
		print "Card detected"
	
	# Get the UID of the card
	(status,uid) = MIFAREReader.MFRC522_Anticoll()

	# If we have the UID, continue
	if status == MIFAREReader.MI_OK:
		uidStr = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
		
		print uidStr
		
		try:
			userFile = open("Data/Users.json", "r")
			userData = json.load(userFile)
			data = userData[uidStr]
			print data["name"]
			print data["email"]
			print data["ssn"]
		except Exception, ex:
			print ex, "User not found"
		
		# Select the scanned tag
		MIFAREReader.MFRC522_SelectTag(uid)
		
		time.sleep(1)
