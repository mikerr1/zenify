from urllib.parse import urlparse, urlunparse
from zenify.url import Url

class TribunNewsUrlParser():
    name = "tribunnews"
    main_url = "https://tribunnews.com"

    @property
    def article_url_regex(self):
        return r"^.*/\d{4}/\d{2}/\d{2}/.*$"

    @staticmethod
    def parse(url: str | Url, as_string=False):
        if type(url) is str:
            url = Url(url)
        main_url = Url(TribunNewsUrlParser.main_url)

        to_parse = [main_url.scheme,
                    main_url.netloc,
                    url.path,
                    main_url.params,
                    main_url.query,
                    main_url.fragment
                    ]
        parsed_back = urlunparse(to_parse)
        # print("parsed_back", type(parsed_back), parsed_back)
        if as_string:
            return str(parsed_back)
        else:
            return parsed_back


class KompasUrlParser():
    name = "kompas"
    main_url = "https://kompas.com"