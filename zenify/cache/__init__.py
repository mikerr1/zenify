import os.path
import pickle
import time

from requests import Request, Session, PreparedRequest

from zenify.utils import hash_url
from zenify.collection.item import CollectionItem


class ZCache:

    def __init__(self, cache_lifetime: int | None = 3600):
        self.__lifetime = cache_lifetime
        self.__folder_name: str | None = "cache"
        self.__directory: str | None = None
        self.__data = {}

    def set_dir(self, directory: str):
        if not os.path.exists(directory) or not os.path.isdir(directory):
            os.mkdir(directory)
        self.__directory = directory

    @property
    def directory(self):
        return self.__directory

    def exists(self, request: PreparedRequest) -> bool:
        url = request.__dict__["url"]
        filename = ".".join([hash_url(url), "pkl"])

        if os.path.exists(os.path.join(self.get_dir(), filename)):
            return True
        return False

    def is_expire(self, request: PreparedRequest) -> bool:
        data = self.read(request)
        now = int(time.time())

        if now - data["timestamp"] > self.__lifetime:
            return True
        return False

    def read(self, request: PreparedRequest):
        url = request.__dict__["url"]
        filename = ".".join([hash_url(url), "pkl"])

        with open(os.path.join(self.get_dir(), filename), "rb") as f:
            data = pickle.load(f)
        return data

    @staticmethod
    def save_item(item: CollectionItem):
        url = str(item.url)
        filename = ".".join([hash_url(url), "pkl"])
        directory = item.cache_dir

        # print(directory, filename)
        # print(len(item.response.content))

        with open(os.path.join(directory, filename), "wb") as f:

            pickle.dump(item, f)


    def save(self, request, response):
        url = request.__dict__["url"]
        data = {
            "timestamp": int(time.time()),
            "url": url,
            "request": request,
            "response": response
        }

        filename = ".".join([hash_url(url), "pkl"])

        with open(os.path.join(self.get_dir(), filename), "wb") as f:
            pickle.dump(data, f)

    def get_dir(self):
        return self.__directory if self.__directory is not None else ""
