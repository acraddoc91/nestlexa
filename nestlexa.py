#!/usr/bin/env python

import sys
import json
import os.path
sys.path += [os.path.dirname(__file__)]
import nest

#take any speech to be sent to alexa and convert it to json form it wants
def constructResponse(speech = None, end_session = True):
	reply = {"version" : "1.0"}
	response = {}
	if speech:
		response['outputSpeech'] = {'type':'PlainText', 'text':speech}
	response['shouldEndSession'] = end_session
	reply['response'] = response
	return json.dumps(reply)
	
def doIntent(intentJson):
	if intentJson['name']=='GetTemp':
		data = nest.getData()
		speech = 'The current temperature is ' + str(data['ambient_temperature_f']) + ' degrees farenheit'
		return constructResponse(speech)
	if intentJson['name']=='SetTemp':
		temp = int(intentJson['slots']['temp']['value'])
		if temp > 78:
			speech = 'That\'s pretty hot, if you really want it above 78 set it manually'
		elif temp < 64:
			speech = 'That\'s pretty cold, if you really want it below 64 set it manually'
		else:
			payload = {'target_temperature_f':temp}
			r = nest.putData(payload)
			if r == 200:
				speech = 'The target temperature has been set to ' + str(temp) + ' degrees farenheit'
			else:
				speech = 'Something appears to have gone wrong, try again'
		return constructResponse(speech)
	if intentJson['name']=='BumpTemp':
		data = nest.getData()
		currTemp = int(data['ambient_temperature_f'])
		newTemp = currTemp + int(intentJson['slots']['bump']['value']
		payload = {'target_temperature_f':newTemp}
		r = nest.putData(payload)
		if r == 200:
				speech = 'The target temperature has been set to ' + str(temp) + ' degrees farenheit'
			else:
				speech = 'Something appears to have gone wrong, try again'
		return constructResponse(speech)
	if intentJson['name']=='DropTemp':
		data = nest.getData()
		currTemp = int(data['ambient_temperature_f'])
		newTemp = currTemp - int(intentJson['slots']['drop']['value']
		payload = {'target_temperature_f':newTemp}
		r = nest.putData(payload)
		if r == 200:
				speech = 'The target temperature has been set to ' + str(temp) + ' degrees farenheit'
			else:
				speech = 'Something appears to have gone wrong, try again'
		return constructResponse(speech)
						

#parses what alexa has sent and figures out what to send back
def doAlexa(environ, start_response):
	#first figure out if alexa has actually sent us anything
	try:
		length = int(environ.get('CONTENT_LENGTH', '0'))
	except ValueError:
		length = 0
	
	if length > 0:
		#read what alexa has sent and load it into json form so we can manipulate it
		body = environ['wsgi.input'].read(length)
		alexaMsg = json.loads(body)
		alexaRequest = alexaMsg['request']
		if alexaRequest['type'] == 'LaunchRequest':
			response = constructResponse("Please ask your nest to do something")
			return response
		elif alexaRequest['type'] == 'IntentRequest':
			response = doIntent(alexaRequest['intent'])
			return response
		else:
			response = constructResponse("Something messed up, sorry")
			return response
	else:
		return constructResponse("Something really messed up")
			
			
#main program
def nestlexa(environ, start_response):
	#start running the alexa subroutine
	output = doAlexa(environ, start_response)
	#some extra crap that needs to be here
	status = '200 OK'
    	start_response('200 OK', [('Content-Type', 'application/json'), ('Content-Length', str(len(output)))])
    	#finally return the json to alexa
	return output
	
application = nestlexa
