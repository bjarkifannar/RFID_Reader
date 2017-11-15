#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import json
import os
import io
import codecs

continue_reading = True
uid = 0
uidStr = ""

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
	global continue_reading
	print "Ctrl+C captured, ending read."
	continue_reading = False
	GPIO.cleanup()
	
def get_user():
	global uid
	global uidStr
	
	print uidStr
	
	try:
		userFile = open("Data/Users.json", "r")
		userData = json.load(userFile)
		
		data = userData[uidStr]
		
		print data["name"]
		print data["email"]
		print data["ssn"]
	except Exception, ex:
		print "\nUser not found"
	
	print "\n"

def add_user():
	global uid
	global uidStr
	
	n_ssn = raw_input("Enter your ssn (Kennitala): ")
	n_name = raw_input("Enter your name: ")
	n_email = raw_input("Enter your email: ")
	
	userFile = open("Data/Users.json", "r")
	jsonData = json.dumps(userFile.read(), ensure_ascii=False)
	userDataInitial = json.loads(jsonData)
	
	userDataInitial = userDataInitial.encode("utf-8")
	userDataStr = userDataInitial[:-1].replace(' u\'', ' "').replace('{u\'', '{"').replace('\'', '"').replace('"{', '{').replace('}"', '}') + ', "%s": {"ssn": "%s", "name": "%s", "email": "%s"}}' % (uidStr, n_ssn, n_name, n_email)
	
	userFile = open("Data/Users.json", "w")
	userFile.write(userDataStr)

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

def start_loop(action):
	os.system('clear')
	
	# This loop keeps checking for chips. If one is near it will get the UID and authenticate
	while continue_reading:
		global uid
		global uidStr
		
		# Scan for cards    
		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

		# If a card is found
		if status == MIFAREReader.MI_OK:
			print "ID detected"
		
		# Get the UID of the card
		(status, uid) = MIFAREReader.MFRC522_Anticoll()

		# If we have the UID, continue
		if status == MIFAREReader.MI_OK:
			uidStr = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
		
			if action == 0:
				get_user()
			elif action == 1:
				add_user()
			
			# Select the scanned tag
			MIFAREReader.MFRC522_SelectTag(uid)
			
			time.sleep(1)
