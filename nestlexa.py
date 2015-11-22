#!/usr/bin/env python

import sys
import json
import os.path
sys.path += [os.path.dirname(__file__)]
import nest

#take any speech to be sent to alexa and convert it to json form it wants
def constructResponse(speech = None, card = None, end_session = True):
	reply = {"version" : "1.0"}
	response = {}
	if speech:
		response['outputSpeech'] = {'type':'PlainText', 'text':speech}
	if card:
		response['card'] = {'type':'Simple', 'title':'Nestlexa', 'content':card}
	response['shouldEndSession'] = end_session
	reply['response'] = response
	return json.dumps(reply)
	
def setAbsTemp(temp):
	if temp > 78:
		speech = 'That\'s pretty hot, if you really want it above 78 set it manually'
		card = None
	elif temp < 64:
		speech = 'That\'s pretty cold, if you really want it below 64 set it manually'
		card = None
	else:
		payload = {'target_temperature_f':temp}
		r = nest.putData(payload)
		if r == 200:
			speech = 'The target temperature has been set to ' + str(temp) + ' degrees farenheit'
			card = 'The target temperature has been set to ' + str(temp) + ' degrees farenheit'
		else:
			speech = 'Something appears to have gone wrong, try again'
			card = None
	return {'speech':speech, 'card':card}
	
def doIntent(intentJson):
	if intentJson['name']=='GetTemp':
		data = nest.getData()
		speech = 'The current temperature in the apartment is ' + str(data['ambient_temperature_f']) + ' degrees farenheit'
		card = 'The current temperature in the apartment is ' + str(data['ambient_temperature_f']) + ' degrees farenheit'
		return constructResponse(speech, card)
	if intentJson['name']=='SetTemp':
		try:
			temp = int(intentJson['slots']['temp']['value'])
			response = setAbsTemp(temp)
			return constructResponse(response['speech'],response['card'])
		except:
			return constructResponse('Sorry I didn\'t quite hear what you said, could you repeat that?')
	if intentJson['name']=='BumpTemp':
		data = nest.getData()
		currTemp = int(data['target_temperature_f'])
		try:
			newTemp = currTemp + int(intentJson['slots']['bump']['value'])
			response = setAbsTemp(newTemp)
			return constructResponse(response['speech'],response['card'])
		except:
			return constructResponse('Sorry I didn\'t quite hear what you said, could you repeat that?')
	if intentJson['name']=='DropTemp':
		data = nest.getData()
		currTemp = int(data['target_temperature_f'])
		try:
			newTemp = currTemp - int(intentJson['slots']['drop']['value'])
			response = setAbsTemp(newTemp)
			return constructResponse(response['speech'],response['card'])
		except:
			return constructResponse('Sorry I didn\'t quite hear what you said, could you repeat that?')
	if intentJson['name']=='GetSetTemp':
		data = nest.getData()
		speech = 'The current set temperature is ' + str(data['target_temperature_f']) + ' degrees farenheit'
		card = 'The current set temperature is ' + str(data['target_temperature_f']) + ' degrees farenheit'
		return constructResponse(speech, card)
	else:
		speech = 'I\'m not sure I can do that, ask me something else'
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
