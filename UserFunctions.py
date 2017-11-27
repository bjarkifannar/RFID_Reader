import Globals
import io
import codecs

def get_user():
	#global uid
	#global uidStr
	#global app
	#global user_ssn
	
	print uidStr
	
	message = ''
	
	try:
		userFile = open("Data/Users.json", "r")
		userData = json.load(userFile)
		
		data = userData[uidStr]
		
		user_ssn = data["ssn"]
		message = message + data['name'] + '\n' + data['email'] + '\n' + data['ssn']
		
		attendance()
	except Exception, ex:
		message = 'User not found'
	
	app.setLabel('msg', message)

def add_user():
	#global uid
	#global uidStr
	
	n_ssn = raw_input("Enter your ssn (Kennitala): ")
	n_name = raw_input("Enter your name: ")
	n_email = raw_input("Enter your email: ")
	
	userFile = open("Data/Users.json", "r")
	jsonData = json.dumps(userFile.read(), ensure_ascii=False)
	userDataInitial = json.loads(jsonData)
	
	userDataInitial = userDataInitial.encode("utf-8")
	userDataStr = HelperFunctions.fix_json(userDataInitial.rstrip()[:-1]) + ', "%s": {"ssn": "%s", "name": "%s", "email": "%s"}}' % (uidStr, n_ssn, n_name, n_email)
	
	userFile = open("Data/Users.json", "w")
	userFile.write(userDataStr)