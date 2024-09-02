from requests import Request


class ZenRequest:
    def __init__(self,
                 method=None,
                 url=None,
                 cookies=None,
                 headers=None,
                 params=None):
        super().__init__()

        self.__request = Request(method=method,
                                 url=url,
                                 cookies=cookies,
                                 headers=headers,
                                 params=params)

        self.__prepared = self.__request.prepare()

    def get_request(self):
        return self.__request

    def get_prepared(self):
        return self.__prepared

