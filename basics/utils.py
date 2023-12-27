from urllib.parse import urlparse

# wenn man einen Link postet, wird der Domain-Name ausgegeben
def get_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain