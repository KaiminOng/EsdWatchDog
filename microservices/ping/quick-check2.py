import aiohttp
import asyncio
import time

# List of urls
urls = [
	"http://www.2342332.com",
	"http://www.svsfv.com",
	"http://www.google.com",
	"http://www.google.com",
	"http://www.google.com",
	"http://www.google.com",
]

async def main():
    results = []
    '''ClientSession is the heart and the main entry point for all client API operations.
    The session contains a cookie storage and connection pool, 
    thus cookies and connections are shared between HTTP requests sent by the same session.
    '''
    async with aiohttp.ClientSession() as session:
        for url in urls:
            # Able to connect to url
            try:
                async with session.get(url) as resp:
                    # If status code shows 200
                    if resp.status == 200:
                        results.append(True)
            # Unable to connect to url
            except aiohttp.ClientError:
                results.append(False)
        print(results)


if __name__ == "__main__":
    s = time.perf_counter()
    # Not sure what is the diff with using loop or not
    asyncio.run(main())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")