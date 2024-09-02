import asyncio
import aiohttp


# print(headers, cookies, params)

url = "http://httpbin.org/json"


async def fetch(client, url):
    async with client.get(url) as response:
        # print(response)
        return response


async def main():
    async with aiohttp.ClientSession() as client:
        result = await fetch(client, url)
        print(result.__dict__)
        print(result.status)

asyncio.run(main())