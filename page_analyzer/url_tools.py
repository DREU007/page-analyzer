from urllib.parse import urlparse, urlunparse
from validators import domain


def make_normalized_dict(url):
    url_data = urlparse(url)
    normalized_url_db = f"{url_data.scheme}://{url_data.hostname}"
    return {
        "normalized_url": url_data.hostname,
        "db_normalized_url": normalized_url_db
    }

def validate(normalized_url):
    return domain(normalized_url)

