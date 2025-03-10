import json

import requests

from .constans import *


def make_bilibili_get_request(url, headers=None, cookies=None, params=None):
    """
    Makes a request to the Bilibili API with the specified headers and cookies.

    Args:
        url (str): The URL to request.
        headers (dict, optional): The request headers. Defaults to None.
        cookies (dict, optional): The cookies to include in the request. Defaults to None.

    Returns:
        dict: The JSON response, or None if an error occurs.
    """
    try:
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def make_bili_get_call(url, params=None):
    response = make_bilibili_get_request(url, headers=DEFAULT_HEADERS, cookies=DEFAULT_COOKIES, params=params)
    return response
