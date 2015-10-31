import requests
import json

#This is the authorisation code for your nest account generated when you set up through REST
authcode = ''
baseurl = 'https://developer-api.nest.com/devices/thermostats/'
#This is the ID for your particular thermostat you want to interface with. You'll probably want to change this.
thermID = ''
totURL = baseurl + thermID + '?auth=' + authcode

def getData():
	data = requests.get(totURL)
	return json.loads(data.text)

def putData(data): 
	head = {'Content-type': 'application/json'}
	r = requests.put(totURL, json=data, headers=head)
	return r.status_code
