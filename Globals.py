from appJar import gui
# These are all the global variables that we using in the code.
def init():
	global app
	global continue_reading
	global uid
	global uidStr
	global start_times
	global end_times
	global user_ssn

	# Title for the window, the "app" is the window.
	app = gui("RFID Reader")
	continue_reading = True
	# The user id.
	uid = 0
	# This is hte user id turned into a string.
	uidStr = ""
	# Start time for the timetable, Start of the class.
	start_times = ("08:00", "10:25", "13:00", "15:20")
	# End time for the timetable, End of the class
	end_times = ("10:15", "12:40", "15:15", "17:35")
	# This is where the social security number is kept.
	user_ssn = ""