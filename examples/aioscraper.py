import json
import asyncio
import aiohttp

from requests import Session, Request

from settings import *
from headers import cookies, headers, params

from zenify.utils import initiate_logger
from zenify.cache import Cache
from zenify.scraper import Scraper
from zenify.url import Url
from zenify.cookies import Cookies
from zenify.headers import Headers
from zenify.params import Params
from zenify.session import ZenSession
from zenify.request import ZenRequest

# Initiate logger
logger = initiate_logger("scraper")

# Prepare cache
cache = Cache(cache_lifetime)
cache.set_dir(os.path.join(os.getcwd(), cache_directory_name))

# Prepare headers, cookies, and params
zcookies = Cookies(cookies).get()
# print(zcookies)
# exit()
zheaders = Headers(headers).get()
zparams = Params(params).get()

# Read URLS from input file
with open("input.csv", "r") as f:
    products = [line.strip() for line in f.readlines() if line[0] == "G"]

urls = [Url(f"https://api.prod.zoro.com/catalog/v1/catalog/product?zoroNos={product_id}&shallow=false&nonLive=false")
        for
        product_id in products[:5]]

urls.append(Url("'http://httpbin.org/get'"))

for url in urls:
    print(url)

async def fetch(client: aiohttp.ClientSession,
                url: str | None = None,
                params = None):
    # print(client)
    async with client.get(url, params=params) as response:
        # await print(url)
        # assert response.status == "200"

        return response


async def main():
    results = []
    async with aiohttp.ClientSession(cookies=zcookies, headers=zheaders) as client:
        # [print(k, v) for k, v in client.__dict__.items()]
        # # for k, v in client.__dict__.items():
        # #     if k == "_cookie_jar":
        # #         print(k, v.__dict__)
        # exit()
        for url in urls:
            # [print(k, v) for k, v in client.__dict__.items()]
            result = await fetch(client, str(url), params=zparams)

            print(result)


asyncio.run(main())
