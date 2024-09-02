class Url:
    total_urls = 0
    max_urls = 9999

    def __init__(self, url: str | None = None):
        Url.total_urls += 1

        assert Url.total_urls <= Url.max_urls, "Max URLs limit reached. Cant create another URL"

        self.__url = url

    def __str__(self):
        return self.__url


if __name__ == "__main__":
    urls = [Url(f"https://asdf.asdf.com/{i}") for i in range(5)]

    print(Url.__dict__)

    for url in urls:
        print(url)
