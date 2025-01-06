import requests

request_ip_url = "https://proxylist.geonode.com/api/proxy-list?protocols=https%2Chttp&limit=500&page=1&sort_by=lastChecked&sort_type=desc"

ip_proxy_context = {'ip': '', 'index': '1', 'port': '', 'url': ''}


def get_ip_pools():
    response = requests.get(request_ip_url)
    ip_json = response.json()
    return ip_json['data']


ip_pools = get_ip_pools()


def proxy_request(random_index):
    ip_proxy_context = {
        'ip': ip_pools[random_index]['ip'],
        'used_ip': ip_pools,
        'index': 1,
        'port': ip_pools[random_index]['port'],
        'url': ":".join([ip_pools[random_index]['ip'], ip_pools[random_index]['port']])
    }
    return {
        "http": ip_proxy_context['url'],
        "https": ip_proxy_context['url'],
    }


if __name__ == '__main__':
    result = proxy_request(1)
    print(result)
