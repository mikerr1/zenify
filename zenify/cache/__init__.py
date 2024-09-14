import os.path
import pickle
import time
import os
from datetime import datetime as dt
from requests import Request, Session, PreparedRequest

import zenify
from zenify.request import ZenRequest
# from zenify import Zenify
from zenify.settings import Settings
from zenify.utils import hash_url
from zenify.collection.item import CollectionItem


class ZCache:
    __settings_vars = [
        "ZCACHE_DIR",
        "ZCACHE_LIFETIME"
    ]

    def __init__(self, *args, **kwargs):
        self.__lifetime: int | None = None
        self.__folder_name: str | None = None
        self.__directory: str | None = None
        self.__data = {}

        if "settings" in kwargs.keys():
            settings = kwargs["settings"]

            for item in vars(settings):
                if item not in self.__settings_vars:
                    continue
                if item == "ZCACHE_DIR":
                    self.directory = vars(settings)["ZCACHE_DIR"]
                elif item == "ZCACHE_LIFETIME":
                    self.lifetime = vars(settings)["ZCACHE_LIFETIME"]

    @property
    def lifetime(self):
        return self.__lifetime

    @lifetime.setter
    def lifetime(self, value: int):
        self.__lifetime = value

    @property
    def directory(self):
        return self.__directory

    @directory.setter
    def directory(self, directory: str):
        if not os.path.exists(directory) or not os.path.isdir(directory):
            os.mkdir(directory)
        self.__directory = directory

    @property
    def data(self) -> dict:
        return self.__data

    @data.setter
    def data(self, data_):
        self.__data = data_

    @data.deleter
    def data(self):
        del self.__data

    def exists(self, name: str) -> bool:
        """
        Construct url from name and check if file exists
        :param request: str
        :return: bool
        """
        fullpath = self.__get_fullpath(name)
        # print(fullpath)

        if os.path.exists(fullpath):
            return True
        return False

    def is_expired(self, name):
        """
        Validate if cache file is created over the cache lifetime settings
        :param name: string
        :return: bool
        """
        fullpath = self.__get_fullpath(name)

        creation_date = os.path.getmtime(fullpath)
        expiry_date = creation_date + self.__lifetime
        now = time.time()

        if now > expiry_date:
            return True
        return False

    def __get_fullpath(self, name):
        filename = ".".join([name, "pkl"])
        directory = self.directory
        fullpath = os.path.join(directory, filename)
        return fullpath

    def delete(self, name: str):
        fullpath = self.__get_fullpath(name)
        os.remove(fullpath)

    def save(self,
             name: str,
             obj: None = None,
             append_dir: str | None = None) -> None:
        """
        save("string", obj) -> cache obj and named it as "string"
        save("string", obj" append_dir="cache") -> same as no above but saved in the directory
        :param name: string
        :param obj: obj any object
        :param append_dir: string
        :return: None
        """
        if not obj:
            raise Exception("Save method requires an object")

        if append_dir is not None:
            _dir = os.path.join(self.__directory, append_dir)
        else:
            _dir = self.directory

        if not os.path.exists(_dir):
            os.mkdir(_dir)

        if name == "request_response":
            self.save_request_response(obj[0], obj[1])
        else:
            filename = ".".join([name, "pkl"])
            cache_full_path = os.path.join(_dir, filename)

            with open(cache_full_path, "wb") as f:
                pickle.dump(obj, f)

    def load(self, name: str | PreparedRequest):
        """
        Inspect the name var, if string then load will find a while with the same name
        else if accepts requests.PreparedRequest object
        :param name: string | type(PreparedRequest)
        :return: Any
        """
        if not self.__directory:
            raise Exception(
                f"Error: Cache directory not found when trying to load {name}")

        if isinstance(name, str):
            filename = ".".join([name, "pkl"])
        elif isinstance(name, PreparedRequest):
            url = name.__dict__["url"]
            filename = ".".join([hash_url(url), "pkl"])
        else:
            raise Exception(
                f"Error: unable to determine the cache for specified {name}")

        cache_full_path = os.path.join(self.__directory, filename)

        if not os.path.exists(cache_full_path):
            return None
            # raise Exception(f"Error: Cache file not found when cache trying to load {cache_full_path}")

        with open(cache_full_path, "rb") as f:
            self.__data[name] = pickle.load(f)
            return self.__data[name]

    @staticmethod
    def save_item(item: CollectionItem):
        url = str(item.url)
        filename = ".".join([hash_url(url), "pkl"])
        directory = item.cache_dir

        # print(directory, filename)
        # print(len(item.response.content))

        with open(os.path.join(directory, filename), "wb") as f:
            pickle.dump(item, f)

    def save_request_response(self, request, response):
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

    def load_file(self,
                  file: str) -> dict:
        """
        Open file in 'rb', call pickle load function, and return as dict
        :param file: string
        :return: dict
        """
        if not self.__directory:
            raise Exception(f"Cache directory not found")
        cache_file = os.path.join(self.get_dir(), file)
        if not os.path.exists(cache_file):
            raise Exception(f"{file} File does not exists")

        with open(cache_file, "rb") as f:
            self.__data = pickle.load(f)

    def load_settings(self, settings: Settings):
        # print(vars(settings)["ZCACHE_DIR"])
        for item in vars(settings):
            # print(item, type(self.__settings_vars))
            if item in self.__settings_vars:
                if item == "ZCACHE_DIR":
                    # print("ZCACHE_DIR=", vars(settings)["ZCACHE_DIR"])
                    self.directory = vars(settings)["ZCACHE_DIR"]
                elif item == "ZCACHE_LIFETIME":
                    self.lifetime = vars(settings)["ZCACHE_LIFETIME"]

    def is_expire(self, request: PreparedRequest) -> bool:
        data = self.load_request_response(request)
        now = int(time.time())

        if now - data["timestamp"] > self.__lifetime:
            return True
        return False

    def load_request_response(self, request: PreparedRequest):
        url = request.__dict__["url"]
        filename = ".".join([hash_url(url), "pkl"])
        cache_fullpath = os.path.join(self.__directory, filename)

        if not os.path.exists(cache_fullpath):
            raise Exception(
                f"Error: Cache file not found when cache trying to load {cache_fullpath}")

        with open(cache_fullpath, "rb") as f:
            data = pickle.load(f)
        return data

    def empty_dir(self) -> None:
        """
        Delete all files in directory
        :return: None
        """
        dir_ = self.directory
        for file in os.listdir(dir_):
            os.remove(os.path.join(dir_, file))



class QuickCache:
    def __init__(self, file: str | None, obj: object | None = None):
        self.__dir = None
        self.__file = None
        self.__cache_file = None

        self.__set_cache_file(file)

    def __set_cache_file(self, cache_file) -> None:
        self.__cache_file = cache_file

    def save(self, obj) -> None:
        with open(self.__cache_file, "wb") as f:
            pickle.dump(obj, f)

    @staticmethod
    def load(file: str) -> object:
        with open(file, "rb") as f:
            obj = pickle.load(f)
            print(obj)
            return obj


def quick_cache(file: str,
                obj: object | None = None
                ) -> QuickCache:
    """
    Check if file exists, this function will pickle load it
    and return an object
    :param file: str
    :param obj: obj
    :return:
    """

    if os.path.exists(file):
        f = open(file, "rb")
        # print()
        obj = pickle.load(f)
        print("obj", obj)
        f.close()
        return obj
    else:
        if obj is not None:
            f = open(file, "wb")
            pickle.dump(obj, f)
            f.close()
