from urllib.parse import urlparse

class UrlError(BaseException):
    def __init__(self, message):
        super().__init__()
        self.args = (message, )

class Url:
    total_urls = 0
    max_urls = 9999

    def __init__(self,
                 url: str | None = None,
                 parse: bool = True):
        # Url.total_urls += 1
        #
        # assert Url.total_urls <= Url.max_urls, "Max URLs limit reached. Cant create another URL"

        self.__url = url
        self.__parsed = urlparse(url) if parse else None

    def __str__(self):
        return str(self.__url)

    def as_string(self):
        return str(self.__url)

    @staticmethod
    def is_valid(url):

        # check if url is Url object
        obj = Url(url) if not isinstance(url, Url) else url

        # print(type(obj))

        if "://" not in obj.__url: return False
        if obj.scheme not in ["http", "https"]: return False
        if obj.netloc == "" or len(obj.netloc) < 1: return False
        if "." not in obj.netloc: return False
        return True

    @property
    def scheme(self):
        return self.__parsed[0]

    @property
    def netloc(self):
        return self.__parsed[1]

    @property
    def path(self):
        return self.__parsed[2]

    @property
    def params(self):
        return self.__parsed[3]

    @property
    def query(self):
        return self.__parsed[4]

    @property
    def fragment(self):
        return self.__parsed[5]





if __name__ == "__main__":

    test_urls = [
        ["//asdf", False],
        ["http//asdfff", False],
        ["https://a/sdf/", False],
        ["@", False],
        ["#", False],
        [Url("httpaaa"), False],
        ["http://test.com", True]
    ]

    print("Test #: Test Data".ljust(40), "Expected result")

    for i in range(len(test_urls)):

        # print(test_urls[i])

        url = test_urls[i][0]
        expected_result = test_urls[i][1]

        print(f"Test {i}: {url}".ljust(40), str(expected_result).rjust(5),
              end=" ")

        try:
            assert Url.is_valid(url) == expected_result, f"Assertion {i} failed"
            print("Passed")
        except UrlError as e:
            print("Not Passed", e)
        except AssertionError as e:
            print("Not passed assertion error", e)


