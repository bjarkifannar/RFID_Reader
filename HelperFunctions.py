# Imports
import Globals

import time
import json

# Returns the current time
def time_get():
	return time.strftime("%w %H:%M", time.gmtime()) # Time format: <Day of the week> <Hours>:<Minutes>

# Fixes a JSON string and returns it
def fix_json(j):
	j = str(j) # Make sure it's a string
	return j.replace(' u\'', ' "').replace('{u\'', '{"').replace('\'', '"').replace('"{', '{').replace('}"', '}')

# Resets labels in the app
def reset_labels():
	Globals.app.clearLabel('msg')

# Marks attendance for the user
def attendance():
	try:
		# Open data files
		timetableFile = open("Data/Timetable.json", "r")
		AttFile = open("Data/Attendance.json", "r")

		# Load the JSON
		ttData = json.load(timetableFile)
		attData = json.load(AttFile)

		# Get the time
		cur_time = time_get()
		cur_day = cur_time.split(' ')[0]
		time_h_m = cur_time.split(' ')[1]

		# Class info
		day_class = ""
		class_name = ""
		class_group = ""
		in_week = ""
		
		if time_h_m >= Globals.start_times[0] and time_h_m <= Globals.end_times[0]: # 1st class of the day
			day_class = "0"
		elif time_h_m >= Globals.start_times[1] and time_h_m <= Globals.end_times[1]: # 2nd class of the day
			day_class = "1"
		elif time_h_m >= Globals.start_times[2] and time_h_m <= Globals.end_times[2]: # 3rd class of the day
			day_class = "2"
		elif time_h_m >= Globals.start_times[3] and time_h_m <= Globals.end_times[3]: # 4th class of the day
			day_class = "3"
		
		class_name = ttData[cur_day][day_class]["class"] # Get the class name
		
		# If the class name is not empty
		if not class_name == "":
			class_group = ttData[cur_day][day_class]["group"] # Get the class group
			in_week = ttData[cur_day][day_class]["in_week"] # Is it the first or second time in the week for this class?
			
			class_n_g = class_name + '-' + class_group # The class name and group
			
			attData[class_n_g][in_week][Globals.user_ssn.encode("utf-8")] = "m" # Make the attendance be "m" for the user in this class
			
			# Open the attendance file and write the new data in it
			AttFile = open("Data/Attendance.json", "w")
			AttFile.write(fix_json(attData))
	except Exception, ex: # If someting went wrong
		# Print the error
		print "ERROR!"
		print ex

# Draws the timetable
def draw_timetable():
	try:
		# Open the timetable file and get the JSON
		timetableFile = open("Data/Timetable.json", "r")
		data = json.load(timetableFile)
		
		# Start a label frame, set the background to white and make it stick to all sides
		Globals.app.startLabelFrame("Timetable", 0, 0, 1, 3)
		Globals.app.setLabelFrameBg("Timetable", "white")
		Globals.app.setSticky("news")
		
		# A for loop for the days in the week
		for i in range(1, 6):
			data2 = data[str(i)] # Data for each day

			# If there is at least one class that day
			if not data2 == "{}":
				for d2 in data2: # For each class in the day
					dat = data2[d2] # Get the data
					starts = int(dat["starts"][:-3]) # Get the start hour
					string = dat["starts"] + " - " + dat["ends"] + "\n" # The start and end time string
					noClass = True # Is there a class at this time?
					
					if dat["class"] == "": # If there is no class
						string = "Enginn tími" # Add a message to the row/column
					else: # If there is a class
						noClass = False # There is a class
						string = dat["class"] + "-" + dat["group"] + "\n" + dat["teacher"] # Add the class info to the row/column
					
					r = 0 # What row to put the data in
					
					if starts == 8: # If the start hour is 8
						r = 0 # Row 0
					elif starts == 10: # If the start hour is 10
						r = 1 # Row 1
					elif starts == 13: # If the start hour is 13
						r = 2 # Row 2
					elif starts == 15: # If the start hour is 15
						r = 3 # Row 3
					
					# Titles for label frame and label
					lfTitle = "lf_" + str(i) + "_" + str(r)
					lTitle = "l_" + str(i) + "_" + str(r)
					
					# Start a label frame and change the title
					Globals.app.startLabelFrame(lfTitle, r, i)
					Globals.app.setLabelFrameTitle(lfTitle, dat["starts"] + " - " + dat["ends"])
					
					if noClass: # If there is no class
						Globals.app.setLabelFrameBg(lfTitle, "green") # Set the background to green
					else: # If there is a class
						Globals.app.setLabelFrameBg(lfTitle, "yellow") # Set the background to yellow
					
					# Add the message to the label frame and close it
					Globals.app.addLabel(lTitle, string, r, i)
					Globals.app.stopLabelFrame()
		
		# Close the timetable label frame
		Globals.app.stopLabelFrame()
	except Exception, ex: # If something went wrong
		# Print the error
		print "ERROR!"
		print ex