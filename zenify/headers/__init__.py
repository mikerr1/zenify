class Headers:
    def __init__(self, headers):
        self.__headers = headers

    def get(self):
        return self.__headers

    def __str__(self):
        return str(self.__headers)