from appJar import gui

def init():
	global app
	global continue_reading
	global uid
	global uidStr
	global start_times
	global end_times
	global user_ssn

	app = gui("RFID Reader")
	continue_reading = True
	uid = 0
	uidStr = ""
	start_times = ("08:00", "10:25", "13:00", "15:20")
	end_times = ("10:15", "12:40", "15:15", "17:35")
	user_ssn = ""