import os, time, http.client
from termcolor import colored

SITES = [
	"www.google.com",
	"www.facebook.com",	
]

while 1:
	for site in SITES:
		conn = http.client.HTTPConnection(site, timeout=10)
		conn.request("HEAD", "/")
		response = conn.getresponse()
		
		if response.status != 200:
			print("\a")
			response.status = colored(response.status, 'red')
					
		print("{0:30} {1:10} {2:10}".format(site, response.status, response.reason))
		conn.close()
	
	time.sleep(2)
	os.system("clear")
