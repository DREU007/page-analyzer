from urllib.parse import urlparse
from validators import domain
from bs4 import BeautifulSoup


def make_normalized_dict(url):
    url_data = urlparse(url)
    normalized_url_db = f"{url_data.scheme}://{url_data.hostname}"
    return {
        "normalized_url": url_data.hostname,
        "db_normalized_url": normalized_url_db
    }


def validate(normalized_url):
    return domain(normalized_url)

def normalize_255(func):
   def wrapper(*args, **kwargs):
       result = func(*args, **kwargs)
       if result is None:
           return
       stripped_result = str(result).strip()
       if len(stripped_result) > 255:
           return stripped_item[:252] + "..."
       return stripped_result
   return wrapper


class ParseHtml:
    def __init__(self, html):
        self.html_soup = BeautifulSoup(html, 'html.parser')

    @normalize_255
    def get_title(self):
        if self.html_soup.title:
            return self.html_soup.title.string

    @normalize_255
    def get_h1(self):
        if self.html_soup.h1:
            return self.html_soup.h1.string

    @normalize_255
    def get_meta_content_attr(self):
        for meta in self.html_soup.find_all('meta'):
            if meta.get('name') == 'description':
                return meta.get('content')
