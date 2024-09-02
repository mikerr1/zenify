class Params:
    def __init__(self, params):
        self.__params = params

    def __str__(self):
        return str(self.__params)

    def get(self):
        return self.__params