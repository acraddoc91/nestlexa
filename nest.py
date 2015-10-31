import requests
import json

#These are unique to each user and thermostat respectively. You'll want to grab your authorisation token and thermostat ID and stick them in here
authcode = ''
thermID = ''

baseurl = 'https://developer-api.nest.com/devices/thermostats/'
totURL = baseurl + thermID + '?auth=' + authcode

def getData():
	data = requests.get(totURL)
	return json.loads(data.text)

def putData(data): 
	head = {'Content-type': 'application/json'}
	r = requests.put(totURL, json=data, headers=head)
	return r.status_code
