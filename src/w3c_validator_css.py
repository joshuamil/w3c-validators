#!/usr/bin/env python


# import libraries
import time, sys, cgi, cgitb, urllib, urllib2

# Import Element Tree
import xml.etree.ElementTree as ET


# Enable debugging
cgitb.enable(display=1, logdir="/Library/WebServer/Documents/errors/")

# Define the cgi parameters
params = cgi.FieldStorage()


# Begin HTML output
print "Content-Type: text/plain;charset=utf-8"
print  # This blank line is required


# Default parameters
vtype = 'CSS'
baseUrl = 'http://jigsaw.w3.org/css-validator/validator'
uri = 'http://www.google.com'
profile = 'css3' # css1, css2, css3, svg, svgbasic, svgtiny, mobile, atsc-tv, tv, none
warning = 'no' # no, 0, 1, 2
lang = 'en' # fr, it, ko, ja, es, zh-cn, nl, de, it, pl
output = 'soap12' # text/plain, text, soap12


# Set the profile
if "profile" in params:
	profile = params["profile"].value

# Set the warning level
if "warning" in params:
	warning = params["warning"].value
	

# Set the URL to validate
if "url" in params:
	uri = params["url"].value
	

# Set the validator URL
validator = baseUrl + '?uri=' + uri + '&warning=' + str(warning) + '&profile=' + profile + '&output=' + output

print "Begin validation of: " + uri


'''
# Define the HTTP library manager
req = urllib2.Request(validator)

response = urllib2.urlopen(req)

soapResponse = response.read()

print soapResponse

tree = ET.parse(str(soapResponse))

'''


# Temporarily work with a local file to figure out XPATH statements
tree = ET.parse('/Library/WebServer/CGI-Executables/dat/soap_example.xml')

root = tree.getroot()

errs = tree.findall('.//{http://www.w3.org/2005/07/css-validator}errorlist')

for a in errs:
	
	print a.findtext('.//{http://www.w3.org/2005/07/css-validator}uri')
	
	for b in a.findall('.//{http://www.w3.org/2005/07/css-validator}error'):
		
		eline = b.findtext('.//{http://www.w3.org/2005/07/css-validator}line')
		etype = b.findtext('.//{http://www.w3.org/2005/07/css-validator}errortype')
		ecntx = b.findtext('.//{http://www.w3.org/2005/07/css-validator}context')
		estyp = b.findtext('.//{http://www.w3.org/2005/07/css-validator}errorsubtype')
		eskip = b.findtext('.//{http://www.w3.org/2005/07/css-validator}skippedstring')
		emesg = b.findtext('.//{http://www.w3.org/2005/07/css-validator}message')
		
		print eline, etype, ecntx, estyp, eskip, emesg
		



