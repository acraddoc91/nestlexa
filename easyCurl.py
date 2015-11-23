import pycurl
from StringIO import StringIO
import json

class response:
	def __init__(self, cont, statcode):
		self.text = cont
		self.status_code = statcode

def getJson(url):
	c = pycurl.Curl()
	b = StringIO()
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	c.setopt(c.FOLLOWLOCATION, True)
	c.perform()
	statcode = c.getinfo(c.RESPONSE_CODE)
	c.close()
	r = response(b.getvalue(), statcode)
	return r
	
def putJson(url, data):
	c = pycurl.Curl()
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.HTTPHEADER, ['Content-type: application/json'])
	c.setopt(pycurl.CUSTOMREQUEST, 'PUT')
	c.setopt(pycurl.POSTFIELDS, json.dumps(data))
	c.setopt(c.FOLLOWLOCATION, True)
	c.perform()
	statcode = c.getinfo(c.RESPONSE_CODE)
	c.close()
	return statcode