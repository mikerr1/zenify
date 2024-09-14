import time

from requests import Request, Session

from zenify.utils import initiate_logger
from zenify import Zenify
from zenify.cache import ZCache


class Scraper(Zenify):

    def __init__(self, name: str = "Default"):
        super().__init__()
        self.name = name

        self.__name: str | None = None
        self.__domain: str | None = None
        self.__session: Session | None = None

        self.__cookies = None
        self.__headers = None
        self.__params = None
        self.__max_attempt = 5
        self.__attempts = []
        self.__urls = []
        self.__prepared_requests = []
        self.__scrape_status = []

        self.__cache: ZCache | None = None
        self.__logger = initiate_logger("zenify")
        self.__logger.info(f"Scraper {self.name} created")

    def set_cache(self, cache: ZCache | None = None):
        if cache is not None:
            self.__cache = cache

    def __set_cookies(self, cookies):
        self.__cookies = cookies

    def __set_headers(self, headers):
        self.__headers = headers

    def __set_params(self, params):
        self.__params = params

    def set_parameters(self, cookies, headers, params):
        self.__set_cookies(cookies=cookies)
        self.__set_headers(headers=headers)
        self.__set_params(params=params)

    def __create_session(self):
        self.__session = Session()
        return self.__session

    def get_session(self):
        return self.__session

    def get_prepared_requests(self):
        return self.__prepared_requests

    def prepare_requests(self,
                         method,
                         enable_cookies=True,
                         enable_headers=True,
                         enable_params=True):

        cookies = self.__cookies if enable_cookies is True else None
        headers = self.__headers if enable_headers is True else None
        params = self.__params if enable_params is True else None

        for url in self.__urls:
            prepped = Request(
                method=method,
                url=url,
                cookies=cookies,
                headers=headers,
                params=params
            ).prepare()

            self.__prepared_requests.append(prepped)
            self.__logger.info(f"Request {prepped} for url {url} is added")
            self.__logger.debug(f"{prepped.__dict__}")

            self.__scrape_status.append([0 for i in range(self.__max_attempt)])
            self.__logger.info(f"Status placeholder for url {url} is added")

    def run(self,
            timeout=5,
            slow_down=2,
            ):

        s = self.__create_session() if not self.__session else self.__session

        self.__logger.info("Restarting loop...")

        for request in self.__prepared_requests:

            try:
                # check if cache exists for this url
                if self.__cache.exists(request) and not self.__cache.is_expire(request):
                    self.__logger.info(f"Cache found .... skipping to next url")
                    time.sleep(0.25)
                    continue
                else:
                    self.__logger.info(f"An expire cache found, refreshing the cache")

                response = s.send(request, timeout=timeout)

                self.__logger.info(f"Scrapping {request}")
                if response.status_code == 200:
                    self.__logger.info(f"Scrape {request} status is success")

                    self.__cache.save_request_response(request, response)

            except ConnectionError as e:
                self.__logger.info(e)

            time.sleep(slow_down)

        time.sleep(slow_down)

    def __save_to_csv(self, filename):
        pass

    def __save_to_json(self, filename):
        pass

    def __save_to_html(self, filename):
        pass

    def __save(self, filename, file_type):
        pass

    def add_url(self, url):
        if url not in self.__urls:
            self.__urls.append(url)

            self.__logger.info(f"{url} added")
        else:
            self.__logger.info(f"{url} found.. possibly already fed previously")
