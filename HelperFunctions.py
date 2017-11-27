import Globals

import time
import json

def time_get():
	return time.strftime("%w %H:%M", time.gmtime())

def fix_json(j):
	j = str(j)
	return j.replace(' u\'', ' "').replace('{u\'', '{"').replace('\'', '"').replace('"{', '{').replace('}"', '}')

def attendance():
	try:
		timetableFile = open("Data/Timetable.json", "r")
		AttFile = open("Data/Attendance.json", "r")
		ttData = json.load(timetableFile)
		attData = json.load(AttFile)
		cur_time = time_get()
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
		
		if not class_name == "":
			class_group = ttData[cur_day][day_class]["group"]
			in_week = ttData[cur_day][day_class]["in_week"]
			
			class_n_g = class_name + '-' + class_group
			
			attData[class_n_g][in_week][Globals.user_ssn.encode("utf-8")] = "m"
			
			AttFile = open("Data/Attendance.json", "w")
			AttFile.write(fix_json(attData))
	except Exception, ex:
		print "ERROR!"
		print ex
