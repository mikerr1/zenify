import re

class UrlParser():
    def __init__(self):
        self.__logger = None
        self.name = None
        self.main_url = None
        self.url_regex_list = []

    def find_matching_regex(self, url: str):
        patterns = self.url_regex_list
        for pattern in patterns:
            if re.match(pattern, url):
                self.logger.debug(f"MATCHED {url} {pattern}")
                return pattern
        self.logger.debug(f"NOT MATCHED {url}")
        return None

    @property
    def logger(self):
        return self.__logger





