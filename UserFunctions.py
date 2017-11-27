#!/usr/bin/env python
# -*- coding: utf8 -*-

# Imports
import Globals
import HelperFunctions

import io
import codecs
import json

# Gets the user and returns the info
def get_user():
	print Globals.uidStr # Prints the User ID string to the terminal (Good for debugging)
	
	message = '' # Create an empty message
	
	try:
		# Open the user file and get the JSON data
		userFile = open("Data/Users.json", "r")
		userData = json.load(userFile)
		
		data = userData[Globals.uidStr] # Get the data for this user
		
		Globals.user_ssn = data["ssn"] # The user's SSN (Kennitala)
		message = message + data['name'] + '\n' + data['email'] + '\n' + data['ssn'] # Add the user info to the message
		
		HelperFunctions.attendance() # Mark the attendance for the user
	except Exception, ex: # If something went wrong
		# Let the user know that he/she is not found
		message = 'User not found'
		print ex # Print an error message if it's there
	
	Globals.app.setLabel('msg', message) # Show the message

# Adds a user
def add_user():
	# Gets the user's details
	n_ssn = raw_input("Enter your ssn (Kennitala): ")
	n_name = raw_input("Enter your name: ")
	n_email = raw_input("Enter your email: ")
	
	# Open the user file and get the info
	userFile = open("Data/Users.json", "r")
	jsonData = json.dumps(userFile.read(), ensure_ascii=False) # Make sure it's using UTF-8
	userDataInitial = json.loads(jsonData)
	
	# Encode the JSON data to a UTF-8 string and fix it
	userDataInitial = userDataInitial.encode("utf-8")
	userDataStr = HelperFunctions.fix_json(userDataInitial.rstrip()[:-1]) + ', "%s": {"ssn": "%s", "name": "%s", "email": "%s"}}' % (Globals.uidStr, n_ssn, n_name, n_email)
	
	# Open the user file and write the data
	userFile = open("Data/Users.json", "w")
	userFile.write(userDataStr)
