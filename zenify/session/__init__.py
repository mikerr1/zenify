import requests
from requests import Session


class ZenSession():
    num_of_instance = 0

    def __init__(self):
        ZenSession.num_of_instance += 1
        assert ZenSession.num_of_instance <= 1, "Error: creating more than 1 session is not allowed"

        self.__session = Session()

    def get_session(self):
        return self.__session



if __name__ == "__main__":
    try:
        s1 = ZenSession()

        print(isinstance(s1, Session))

        s2 = ZenSession()
    except Exception as e:
        print(e)
