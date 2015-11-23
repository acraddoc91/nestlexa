import json
import sys
sys.path += [os.path.dirname(__file__)]
import easyCurl

#This reads you're authirsation code and thermostat ID from the AuthDetails file. You'll need to change these for you
authcode = ''
thermID = ''

#baseurl = 'https://developer-api.nest.com/devices/thermostats/'
#Looks like the URL changed
baseurl = 'https://firebase-apiserver02-tah01-iad01.dapi.production.nest.com:9553/devices/thermostats/'
totURL = baseurl + thermID + '?auth=' + authcode

def getTotURL():
	return totURL

def getData():
	data = easyCurl.getJson(totURL)
	return data.text

def putData(data): 
	r = easyCurl.putJson(totURL, data)
	return r
