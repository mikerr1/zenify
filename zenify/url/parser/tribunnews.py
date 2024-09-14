from zenify.url.parser import UrlParser
from zenify.utils import initiate_logger

class UrlParserTribunNews(UrlParser):

    def __init__(self):
        super().__init__()
        self.__logger = initiate_logger("UrlParserTribunNews")

        self.name = "tribunnews"
        self.main_url = "https://tribunnews.com"
        self.url_regex_list = [
            r"^(http|https):\/\/.*tribunnews.*\/\d{4}\/\d{2}\/\d{2}\/.*$",
            r"^(http|https):\/\/.*tribun.*\/\w.*\/\d*\/.*$",
        ]

    @property
    def logger(self):
        return self.__logger