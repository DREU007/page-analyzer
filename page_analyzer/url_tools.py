from urllib.parse import urlparse
from validators import url as validate_url 
from bs4 import BeautifulSoup


def normalize(url):
    url_data = urlparse(url)
    return f"{url_data.scheme}://{url_data.hostname}"


def validate(normalized_url):
    return validate_url(normalized_url)


def _normalize_255(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            return
        stripped_result = str(result).strip()
        if len(stripped_result) > 255:
            return stripped_result[:252] + "..."
        return stripped_result
    return wrapper


class ParseHtml:
    def __init__(self, html):
        self.html_soup = BeautifulSoup(html, 'html.parser')

    @_normalize_255
    def get_title(self):
        if self.html_soup.title:
            return self.html_soup.title.string

    @_normalize_255
    def get_h1(self):
        if self.html_soup.h1:
            return self.html_soup.h1.string

    @_normalize_255
    def get_meta_content_attr(self):
        for meta in self.html_soup.find_all('meta'):
            if meta.get('name') == 'description':
                return meta.get('content')
