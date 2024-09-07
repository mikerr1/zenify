from bs4 import BeautifulSoup

def clean(html=None):
    soup = BeautifulSoup(html, 'lxml')
    # Remove script tags
    for script in soup.find_all('script'):
        script.decompose()
    # Remove style tags
    for style in soup.find_all('style'):
        style.decompose()
    for image in soup.find_all('img'):
        image.decompose()
    # Remove other unwanted elements
    # ...
    return str(soup)


class Html:
    def __init__(self, html):
        self.__original_html = html

    def __str__(self):
        return str(self.__original_html)