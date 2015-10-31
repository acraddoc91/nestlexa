import requests
import json

#This reads you're authirsation code and thermostat ID from the AuthDetails file. You'll need to change these for you
f = open('AuthDetails', 'r')
firstline = f.readline()
secondline = f.readline()
authcode = firstline[9:len(firstline)-1]
thermID = secondline[8:]
f.close()

baseurl = 'https://developer-api.nest.com/devices/thermostats/'
totURL = baseurl + thermID + '?auth=' + authcode

def getData():
	data = requests.get(totURL)
	return json.loads(data.text)

def putData(data): 
	head = {'Content-type': 'application/json'}
	r = requests.put(totURL, json=data, headers=head)
	return r.status_code
