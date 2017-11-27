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
		#global uid
		#global uidStr

		reset_labels()
		
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
	draw_timetable()
	
	Globals.app.startLabelFrame("Message", 3, 0)
	
	Globals.app.setSticky("news")
	
	Globals.app.addEmptyLabel('msg')
	Globals.app.setLabelWidths('msg', 700)
	
	Globals.app.stopLabelFrame()
	
	start_loop(0)

def reset_labels():
	Globals.app.clearLabel('msg')

def draw_timetable():
	try:
		timetableFile = open("Data/Timetable.json", "r")
		data = json.load(timetableFile)
		
		#print data["1"]["0"]["class"]
		Globals.app.startLabelFrame("Timetable", 0, 0, 1, 3)
		Globals.app.setLabelFrameBg("Timetable", "white")
		Globals.app.setSticky("news")
		
		for i in range(1, 6):
			data2 = data[str(i)]
			if not data2 == "{}":
				for d2 in data2:
					dat = data2[d2]
					starts = int(dat["starts"][:-3])
					string = dat["starts"] + " - " + dat["ends"] + "\n"
					noClass = True
					
					if dat["class"] == "":
						string = "Enginn tími"
					else:
						noClass = False
						string = dat["class"] + "-" + dat["group"] + "\n" + dat["teacher"]
					
					r = 0
					
					if starts == 8:
						r = 0
					elif starts == 10:
						r = 1
					elif starts == 13:
						r = 2
					elif starts == 15:
						r = 3
					
					lfTitle = "lf_" + str(i) + "_" + str(r)
					lTitle = "l_" + str(i) + "_" + str(r)
					
					Globals.app.startLabelFrame(lfTitle, r, i)
					Globals.app.setLabelFrameTitle(lfTitle, dat["starts"] + " - " + dat["ends"])
					
					if noClass:
						Globals.app.setLabelFrameBg(lfTitle, "green")
					else:
						Globals.app.setLabelFrameBg(lfTitle, "yellow")
					
					Globals.app.addLabel(lTitle, string, r, i)
					Globals.app.stopLabelFrame()
		
		Globals.app.stopLabelFrame()
	except Exception, ex:
		print "ERROR!"
		print ex

def attendance():
	try:
		#global start_times
		#global end_times
		#global user_ssn
		
		timetableFile = open("Data/Timetable.json", "r")
		AttFile = open("Data/Attendance.json", "r")
		ttData = json.load(timetableFile)
		attData = json.load(AttFile)
		cur_time = HelperFunctions.time_get()
		cur_day = cur_time.split(' ')[0]
		time_h_m = cur_time.split(' ')[1]
		day_class = ""
		class_name = ""
		class_group = ""
		in_week = ""
		
		if time_h_m >= Globals.start_times[0] and time_h_m <= Globals.end_times[0]:
			day_class = "0"
		elif time_h_m >= Globals.start_times[1] and time_h_m <= Globals.end_times[1]:
			day_class = "1"
		elif time_h_m >= Globals.start_times[2] and time_h_m <= Globals.end_times[2]:
			day_class = "2"
		elif time_h_m >= Globals.start_times[3] and time_h_m <= Globals.end_times[3]:
			day_class = "3"
		
		class_name = ttData[cur_day][day_class]["class"]
		class_group = ttData[cur_day][day_class]["group"]
		in_week = ttData[cur_day][day_class]["in_week"]
		
		class_n_g = class_name + '-' + class_group
		
		attData[class_n_g][in_week][Globals.user_ssn.encode("utf-8")] = "m"
		
		AttFile = open("Data/Attendance.json", "w")
		AttFile.write(HelperFunctions.fix_json(attData))
	except Exception, ex:
		print "ERROR!"
		print ex

Globals.app.setGeometry("800x600")
Globals.app.setStretch("both")
Globals.app.thread(init_app)
Globals.app.go()
