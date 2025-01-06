
from qpycases import proxy_checker

def test_read_local_proxies():
    proxy_urls = proxy_checker.read_local_proxies()
    print(proxy_urls)
    assert len(proxy_urls)>1