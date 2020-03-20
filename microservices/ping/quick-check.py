import os, time, http.client, asyncio
from termcolor import colored

SITES = [
	"www.google.com",
	"www.facebook.com",	
]

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
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
