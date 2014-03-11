#!/usr/bin/env python

# import HTML validator
from py_w3c.validators.html.validator import HTMLValidator
import time, sys


# Set the URL to validate
if len(sys.argv) < 1:
	url = 'http://www.google.com'
else:
	url = sys.argv[1]
	
	
# Indicate if the reults should be dumped to the console
if len(sys.argv) < 3:
	dump = 0
else:
	dump = sys.argv[2]
	
# Validation Type
vtype = 'HTML'
	
	
# Specify a file path for storing results
pt = '../target/'
	
# Create a filename to store the results in
fn = 'Results_' + vtype + '_' + time.strftime('%m%d%y_%H%M%S') + '.txt'


# Create validator object
vld = HTMLValidator()

# Validate URL
vld.validate(url)

# Capture validator errors
e = vld.errors

# Capture validator warnings
w = vld.warnings

# Create a line separator
sep = ''.join(['=']*80)

# Output the results
res = ''
res = ''.join([res,sep])
res = '\n'.join([res,'W3C VALIDATOR RESULTS'])
res = '\n'.join([res,sep])
res = '\n'.join([res,'URL: ' + url])
res = '\n'.join([res,'Date/Time: ' + time.strftime('%c')])
res = '\n'.join([res,sep])
res = '\n'.join([res,'Total Errors: ' + str(len(e))])
res = '\n'.join([res,sep])
res = '\n'.join([res,'Error Summary: '])
res = '\n'.join([res,sep])

# Itereate over each error item
for item in e:
		res = '\n'.join([res,'Line: ' + item['line'] + ' - ' + item['message']])


# Output the results to a new file
text_file = open(pt+fn, "w")
text_file.write(str(res))
text_file.close()

# Respond to the user
print 'Results written to new file:', fn


# Print the results if asked
if int(dump) == 1:
	print str(res)


