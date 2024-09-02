import json
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
cookies = Cookies(cookies).get()
headers = Headers(headers).get()
params = Params(params).get()


# Read URLS from input file
with open("input.csv", "r") as f:
    products = [line.strip() for line in f.readlines() if line[0] == "G"]

urls = [Url(f"https://api.prod.zoro.com/catalog/v1/catalog/product?zoroNos={product_id}&shallow=false&nonLive=false")
        for
        product_id in products[:5]]

# [print(url) for url in urls]

# Create session
zs = ZenSession()

for url in urls:
    zr = ZenRequest(method="GET",
                   url=url,
                   cookies=cookies,
                   headers=headers,
                   params=params).get_prepared()


    # check if prepared request was cached previously
    if not cache.exists(zr) or cache.is_expire(zr):
        response = zs.get_session().send(zr)
        assert response.status_code == 200, "Error: Failed to request url"
        cache.save(request=zr, response=response)
        logger.info(f"Response {response.status_code} received from {zr.url}")
    else:
        data = cache.read(zr)
        response = data["response"]
        # print(type(data["response"]), dir(data["response"]))
        # print(response.json())

        print(json.dumps(response.json(), indent=2))


