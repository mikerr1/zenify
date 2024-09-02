import asyncio
import aiohttp
from headers import headers, cookies, params

my_url = "https://api.prod.zoro.com/catalog/v1/catalog/product?zoroNos=G802282236&shallow=false&nonLive=false"


async def main():
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as client:
        result = await fetch(client, my_url, params=params)
        print(result)


async def fetch(client, url, params):
    async with client.get(url, params=params) as response:
        # print(response)
        return response


asyncio.run(main())
