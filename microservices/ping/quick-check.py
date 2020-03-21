import os, time, http.client, asyncio
import requests
# from termcolor import colored

sites = [
	"http://www.google.com",
	"http://www.google.com",
    "http://www.google.com",
    "http://www.google.com",
    "http://www.google.com"
]

async def my_funct(site):
    r = requests.get(site, verify=False, timeout=10)
    print(r.status_code)

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

def getListOfTasks(sites):
    listOfTasks = []
    for site in sites:
        listOfTasks.append(asyncio.create_task(my_funct(site)))

    return listOfTasks

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def main():
    listOfTasks = getListOfTasks(sites)
    print(f"ASYNC started at {time.strftime('%X')}")
    for task in listOfTasks:
        await task
    
    print(f"ASYNC finished at {time.strftime('%X')}")
	# results = await asyncio.gather(map(my_funct, sites))
	# print(results)



	

# await asyncio.sleep(1)

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

# for future in asyncio.as_completed(map(my_funct, sites)):
#     result = await future