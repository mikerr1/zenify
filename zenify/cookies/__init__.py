from requests import Request


class Cookies:
    def __init__(self, cookies):
        self.__cookies = cookies

    def __str__(self):
        return str(self.__cookies)

    def get(self):
        return self.__cookies
