import os, time, http.client, asyncio
import requests
# from termcolor import colored

sites = [
	"http://www.google.com",
	"http://www.facebook.com",	
]

def my_funct(site):
	r = requests.get(site, verify=False, timeout=10)
	return r.status_code

# for site in sites:
# 	print(my_funct(site))

# while 1:
# 	for site in SITES:
# 		conn = http.client.HTTPConnection(site, timeout=10)
# 		conn.request("HEAD", "/")
# 		response = conn.getresponse()
		
# 		if response.status != 200:
# 			print("\a")
# 			response.status = colored(response.status, 'red')
					
# 		print("{0:30} {1:10} {2:10}".format(site, response.status, response.reason))
# 		conn.close()
	
# 	time.sleep(2)
# 	os.system("clear")

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def main():
	results = await asyncio.gather(map(sites))
	print(results)
	

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

# for future in asyncio.as_completed(map(my_funct, sites)):
#     result = await future