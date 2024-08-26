from settings import *
from headers import cookies, headers, params

from zenify.utils import initiate_logger
from zenify.cache import Cache
from zenify.scraper import Scraper

logger = initiate_logger("scraper")

# Generate URLS for test
with open("input.csv", "r") as f:
    products = [line.strip() for line in f.readlines() if line[0] == "G"]

urls = [f"https://api.prod.zoro.com/catalog/v1/catalog/product?zoroNos={product_id}&shallow=false&nonLive=false" for
        product_id in products]

# Initialize zenify scraper
scraper = Scraper(name=domain_name)

# Setting scraper parameters
scraper.set_parameters(cookies=cookies, headers=headers, params=params)

# Registers the urls in scraper
[scraper.feed_url(url) for url in urls]

# Prepare requests
scraper.prepare_requests(method="GET")

# Initialize cache mechanism
cache = Cache(cache_lifetime)
cache.set_dir(os.path.join(os.getcwd(), cache_directory_name))

# Register cache to scraper
scraper.set_cache(cache)

# Start scraping
scraper.run()
