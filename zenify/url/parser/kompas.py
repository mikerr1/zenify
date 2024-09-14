from zenify.url.parser import UrlParser
from zenify.utils import initiate_logger

class UrlParserKompas(UrlParser):
    def __init__(self):
        super().__init__()
        self.__logger = initiate_logger("UrlParserKompas")

        self.name = "Kompas"
        self.main_url = "https://kompas.com"
        self.url_regex_list = [
            r"^(http|https):\/\/.*\/read\/\d{4}\/\d{2}\/\d{2}\/\d+\/.*$"
        ]

    @property
    def logger(self):
        return self.__logger