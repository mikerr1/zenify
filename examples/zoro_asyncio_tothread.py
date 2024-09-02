import json
from requests import Session, Request
import requests
import asyncio

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
cookies = Cookies(cookies).get()
headers = Headers(headers).get()
params = Params(params).get()

# Read URLS from input file
with open("input.csv", "r") as f:
    products = [line.strip() for line in f.readlines() if line[0] == "G"]

urls = [Url(f"https://api.prod.zoro.com/catalog/v1/catalog/product?zoroNos={product_id}&shallow=false&nonLive=false")
        for
        product_id in products]


# Create session
zs = ZenSession()

requests_collection = []

for url in urls:
    zr = ZenRequest(method="GET",
                    url=url,
                    cookies=cookies,
                    headers=headers,
                    params=params).get_prepared()

    # check if prepared request was cached previously
    if not cache.exists(zr) or cache.is_expire(zr):
        requests_collection.append(zr)

    else:
        data = cache.read(zr)
        response = data["response"]
        print("Read from cache")
        # print(json.dumps(response.json(), indent=2))


async def execute_requests(requests_list=None):
    tasks = []
    for r in requests_collection:
        tasks.append(asyncio.to_thread(zs.get_session().send, r))

    return await asyncio.gather(*tasks)


if len(requests_collection) > 0:
    results = asyncio.run(execute_requests(requests_collection))

    for result in results:
        request = result.request
        response = result
        if response.status_code == 200:
            cache.save(request, response)
            logger.info(f"Response {response.status_code} received from {request.url}")
        else:
            logger.info(f"Failed to open {request.url} received response {response.status_code}")