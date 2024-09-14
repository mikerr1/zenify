from zenify.cache import ZCache
from zenify.settings import Settings

class Zenify:
    def __init__(self, settings: Settings):
        self.__cache = None
        self.__config = None
        self.__settings = settings

    def config(self):
        if not self.__config:
            self.__config = Config()
        return self.__config

    def cache(self):
        if not self.__cache:
            settings = self.settings
            print(settings)
            if not settings:
                raise
            self.__cache = ZCache(settings=settings)
        return self.__cache

    @property
    def settings(self):
        return self.__settings

    @settings.setter
    def settings(self, settings):
        self.__settings = settings

    @settings.deleter
    def settings(self):
        del self.__settings





