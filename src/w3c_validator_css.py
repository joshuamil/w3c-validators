#!/usr/bin/env python

# Import libraries
import time, sys, cgi, cgitb, urllib, urllib2, re

# Import Element Tree
import xml.etree.ElementTree as ET


# Enable debugging
cgitb.enable(display=1, logdir="/Library/WebServer/Documents/errors/")

# Define the cgi parameters
params = cgi.FieldStorage()

# Create a RegEx pattern to strip spaces
pat = re.compile(r'\s+')


# Default parameters
vtype = 'CSS'
baseUrl = 'http://jigsaw.w3.org/css-validator/validator'
uri = 'http://www.google.com'

# Possible values for validation API params
possibleModes = ['live','test']
mode = possibleModes[0]

possibleProfiles = ['css1','css2','css3','svg','svgbasic','svgtiny','mobile','atsc-tv','tv','none']
profile = possibleProfiles[2]

possibleWarnings = ['no','0','1','2']
warning = possibleWarnings[0]

possibleLangs = ['en','fr','it','ko','ja','es','zh-cn','nl','de','it','pl']
lang = possibleLangs[0]

possibleOutputs = ['soap12','text']
output = possibleOutputs[0]


# Set the mode
if "mode" in params and params["mode"].value in possibleModes:
	mode = params["mode"].value

# Set the profile
if "profile" in params and params["profile"].value in possibleProfiles:
	profile = params["profile"].value

# Set the warning level
if "warning" in params and params["warning"].value in possibleWarnings:
	warning = params["warning"].value
	
# Set the language
if "lang" in params and params["lang"].value in possibleLangs:
	lang = params["lang"].value
	
# Set the output type
if "output" in params and params["output"].value in possibleOutputs:
	output = params["output"].value

# Set the URL to validate
if "url" in params:
	uri = params["url"].value
	
	
# Set the validator URL
validator = baseUrl + '?uri=' + uri + '&warning=' + str(warning) + '&profile=' + profile + '&output=' + output


# Determine which mode we're running in
if mode == "live":

	# Define the HTTP library manager
	req = urllib2.Request(validator)
	
	# Call the W3C CSS Validation API
	response = urllib2.urlopen(req)
	
	# Read the response
	soapResponse = response.read()
	
	# Parse the SOAP response into an element tree
	tree = ET.fromstring(str(soapResponse))

elif mode == "test":
	
	# Temporarily work with a local file to figure out XPATH statements
	tree = ET.parse('/Library/WebServer/CGI-Executables/dat/soap_example.xml')



# Find the number of errors
errCount = tree.findtext('.//{http://www.w3.org/2005/07/css-validator}errorcount')

# Find the errorlist instances
errList = tree.findall('.//{http://www.w3.org/2005/07/css-validator}errorlist')


# Begin output
print "Content-Type: text/json;charset=utf-8"
print  # This blank line is required


# Begin outputting the errors
print '[{"errorCount":"'+str(errCount)+'","errors":['

# Handle the response
if len(errList) > 0 and int(errCount) > 0:

	# Iterate over the errorlist nodes if there are errors and the errorlist is not empty
	for idx, a in enumerate(errList):
		
		# Get the error nodes from the current errorlist node
		err = a.findall('.//{http://www.w3.org/2005/07/css-validator}error')
		
		#Iterate over the error nodes and capture the error details
		for idx, val in enumerate(err, start=1):
			
			# Get the Line Number
			try:
				eline = pat.sub(' ',val.findtext('.//{http://www.w3.org/2005/07/css-validator}line')).strip()
			except:
				eline = ""
				
			# Get the Error Type
			try:
				etype = pat.sub(' ',val.findtext('.//{http://www.w3.org/2005/07/css-validator}errortype')).strip()
			except:
				etype = ""
			
			# Get the Error Context
			try:
				ecntx = pat.sub(' ',val.findtext('.//{http://www.w3.org/2005/07/css-validator}context')).strip()
			except:
				ecntx = ""
				
			# Get the Error Sub-Type
			try:
				estyp = pat.sub(' ',val.findtext('.//{http://www.w3.org/2005/07/css-validator}errorsubtype')).strip()
			except:
				estyp = ""
			
			# Get the Skipped-String
			try:
				eskip = pat.sub(' ',val.findtext('.//{http://www.w3.org/2005/07/css-validator}skippedstring')).strip()
			except:
				eskip = ""
				
			# Get the Error Message
			try:
				emesg = pat.sub(' ',val.findtext('.//{http://www.w3.org/2005/07/css-validator}message')).strip()
			except:
				emesg = ""
			
			
			# Output each error into the JSON string
			print '{'
			print ' "file":"' + a.findtext('.//{http://www.w3.org/2005/07/css-validator}uri') + '"'
			print ',"line":"' + eline + '"'
			print ',"errortype":"' + etype + '"'
			print ',"context":"' + ecntx + '"'
			print ',"errorsubtype":"' + estyp + '"'
			print ',"skippedstring":"' + eskip + '"'
			print ',"message":"' + emesg + '"'
			print '}'
			if idx != len(err):
				print ","
				
else:
	# If there are no errors, return an empty JSON object
	print '{}'
	


# Begin outputting the warnings
if warning != 'no':
	
	# Find the number of errors
	warnCount = tree.findtext('.//{http://www.w3.org/2005/07/css-validator}warningcount')
	
	# Find the warninglist instances
	warnList = tree.findall('.//{http://www.w3.org/2005/07/css-validator}warninglist')
	
	print ']},{["warningCount":"'+str(warnCount)+'","warnings":['
	
	# Handle the response
	if len(warnList) > 0 and int(warnCount) > 0:
		print '{}'
	else:
		print '{}'


# Output the closing JSON string
print "]}]"


