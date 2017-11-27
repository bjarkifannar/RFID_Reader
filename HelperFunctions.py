import time

def time_get():
	return time.strftime("%w %H:%M", time.gmtime())

def fix_json(j):
	j = str(j)
	return j.replace(' u\'', ' "').replace('{u\'', '{"').replace('\'', '"').replace('"{', '{').replace('}"', '}')