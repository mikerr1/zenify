import time

from requests import Request, Session

from zenify.utils import initiate_logger
from zenify import Zenify
from zenify.cache import Cache


class Scraper(Zenify):

    name: str | None = None
    domain: str | None = None
    _session: Session | None = None

    _cookies = None
    _headers = None
    _params = None
    _max_attempt = 5
    _attempts = []
    _urls = []
    _prepared_requests = []
    _scrape_status = []

    _cache: Cache | None = None

    _logger = None

    def __init__(self, name: str = "Default"):
        super().__init__()
        self._logger = initiate_logger("zenify")
        self.name = name
        self._logger.info(f"Scraper {self.name} created")

    def set_cache(self, cache: Cache | None = None):
        if cache is not None:
            self._cache = cache

    def _set_cookies(self, cookies):
        self._cookies = cookies

    def _set_headers(self, headers):
        self._headers = headers

    def _set_params(self, params):
        self._params = params

    def set_parameters(self, cookies, headers, params):
        self._set_cookies(cookies = cookies)
        self._set_headers(headers = headers)
        self._set_params(params = params)

    def _create_session(self):
        self._session = Session()
        return self._session

    def get_session(self):
        return self._session

    def prepare_requests(self,
                        method,
                        enable_cookies = True,
                        enable_headers = True,
                        enable_params = True):

        cookies = self._cookies if enable_cookies == True else None
        headers = self._headers if enable_headers == True else None
        params = self._params if enable_params == True else None

        for url in self._urls:

            prepped = Request(
                method = method,
                url = url,
                cookies = cookies,
                headers = headers,
                params = params
            ).prepare()

            self._prepared_requests.append(prepped)
            self._logger.info(f"Request {prepped} for url {url} is added")
            self._logger.debug(f"{prepped.__dict__}")

            self._scrape_status.append([0 for i in range(self._max_attempt)])
            self._logger.info(f"Status placehoder for url {url} is added")


    def run(self,
               timeout=5,
               slow_down=2,
               ):

        s = self._create_session() if not self._session else self._session

        while True:

            self._logger.info("Restarting loop...")

            for request in self._prepared_requests:

                try:
                    # check if cache exists for this url
                    if self._cache.exists(request) and not self._cache.is_expire(request):
                        self._logger.info(f"Cache found .... skipping to next url")
                        time.sleep(0.5)
                        continue
                    else:
                        self._logger.info(f"An expire cache found, refreshing the cache")

                    response = s.send(request, timeout=timeout)

                    self._logger.info(f"Scrapping {request}")
                    if response.status_code == 200:
                        self._logger.info(f"Scrape {request} status is success")

                        self._cache.cache_request_and_response(request, response)

                except ConnectionError as e:
                    self._logger.info(e)

                time.sleep(slow_down)

            time.sleep(slow_down)


    def save_to_csv(self, filename):
        pass

    def save_to_json(self, filename):
        pass

    def save_to_html(self, filename):
        pass



    def feed_url(self, url):
        if url not in self._urls:
            self._urls.append(url)

            self._logger.info(f"{url} added")
        else:
            self._logger.info(f"{url} found.. possibly already fed previously")



