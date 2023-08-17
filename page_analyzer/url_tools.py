from urllib.parse import urlparse
from validators import domain


def normalize(url):
    url_data = urlparse(url)
    return url_data.hostname

def validate(normalized_url):
    return domain(normalized_url)

