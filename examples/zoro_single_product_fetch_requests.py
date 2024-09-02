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

url = "https://api.prod.zoro.com/catalog/v1/catalog/product?zoroNos=G802282236&shallow=false&nonLive=false"
zs = ZenSession()
zr = ZenRequest(method="GET",
                url=url,
                cookies=cookies,
                headers=headers,
                params=params).get_prepared()

r = zs.get_session().send(zr)
print(r.status_code)
