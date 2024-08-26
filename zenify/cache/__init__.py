import os.path
import pickle
import time
from zenify.utils import hash_url
import os.path
import pickle
import time

from zenify.utils import hash_url


class Cache:

    _lifetime: int | None = None

    _folder_name: str | None = "cache"

    _directory: str | None = None

    _data = {}

    def __init__(self, cache_lifetime):
        self._lifetime = cache_lifetime

    def set_dir(self, directory: str):
        if not os.path.exists(directory) or not os.path.isdir(directory):
            os.mkdir(directory)
        self._directory = directory

    def exists(self, request):
        url = request.__dict__["url"]
        filename = ".".join([hash_url(url), "pkl"])

        if os.path.exists(os.path.join(self._directory, filename)):
            return True

    def is_expire(self, request):
        url = request.__dict__["url"]
        filename = ".".join([hash_url(url), "pkl"])

        data = self._read_cache(request)
        # print(data)

        now = int(time.time())

        # print("now", now)
        # print("timestamp", data["timestamp"])
        # print(now - data["timestamp"])

        if now - data["timestamp"] > self._lifetime:
            return True
        return False

    def _read_cache(self, request):

        url = request.__dict__["url"]
        filename = ".".join([hash_url(url), "pkl"])

        with open(os.path.join(self._directory, filename), "rb") as f:
            data = pickle.load(f)

        return(data)



    def cache_request_and_response(self, request, response):
        url = request.__dict__["url"]
        data = {
            "timestamp": int(time.time()),
            "url": url,
            "request": request,
            "response": response
        }

        filename = ".".join([hash_url(url), "pkl"])

        with open(os.path.join(self._directory, filename), "wb") as f:
            pickle.dump(data, f)

