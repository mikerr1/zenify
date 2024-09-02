import os.path
import pickle
import time
from zenify.utils import hash_url
import os.path
import pickle
import time

from zenify.utils import hash_url


class Cache:

    def __init__(self, cache_lifetime: int | None = 3600):
        self.__lifetime = cache_lifetime
        self.__folder_name: str | None = "cache"
        self.__directory: str | None = None
        self.__data = {}

    def set_dir(self, directory: str):
        if not os.path.exists(directory) or not os.path.isdir(directory):
            os.mkdir(directory)
        self.__directory = directory

    def exists(self, request):
        url = request.__dict__["url"]
        filename = ".".join([hash_url(url), "pkl"])

        if os.path.exists(os.path.join(self.__directory, filename)):
            return True

    def is_expire(self, request):
        url = request.__dict__["url"]
        filename = ".".join([hash_url(url), "pkl"])

        data = self._read_cache(request)

        now = int(time.time())

        if now - data["timestamp"] > self.__lifetime:
            return True
        return False

    def _read_cache(self, request):

        url = request.__dict__["url"]
        filename = ".".join([hash_url(url), "pkl"])

        with open(os.path.join(self.__directory, filename), "rb") as f:
            data = pickle.load(f)

        return data

    def cache_request_and_response(self, request, response):
        url = request.__dict__["url"]
        data = {
            "timestamp": int(time.time()),
            "url": url,
            "request": request,
            "response": response
        }

        filename = ".".join([hash_url(url), "pkl"])

        with open(os.path.join(self.__directory, filename), "wb") as f:
            pickle.dump(data, f)
