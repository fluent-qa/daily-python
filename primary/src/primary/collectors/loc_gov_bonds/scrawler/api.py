from time import sleep

import requests

local_gov_debt_url = """
https://www.governbond.org.cn:4443/api/loadBondData.action?timeStamp=1731404338868&dataType=ZQFXLISTBYAD&adList=&adCode=87&zqlx=&year=&fxfs=&qxr=&fxqx=&zqCode=&zqName=
"""

index_str = 'page={page_no}&pageSize=20'

import requests
from time import sleep
from typing import Dict, Any


def fetch_bond_data(
        page: int = 1,
        page_size: int = 10,
        year: str = "",
        ad_code: str = "87"
) -> Dict[str, Any]:
    """
    Fetch bond data from the API

    Args:
        page: Page number
        page_size: Number of items per page
        year: Year filter
        ad_code: Area code
    """
    url = "https://www.governbond.org.cn:4443/api/loadBondData.action"

    # Query parameters
    params = {
        "timeStamp": "1731404338868",  # You might want to generate this dynamically
        "dataType": "ZQFXLISTBYAD",
        "adList": "",
        "adCode": ad_code,
        "zqlx": "",
        "year": year,
        "fxfs": "",
        "qxr": "",
        "fxqx": "",
        "zqCode": "",
        "zqName": "",
        "page": page,
        "pageSize": page_size
    }

    # Headers
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.celma.org.cn",
        "Pragma": "no-cache",
        "Referer": "https://www.celma.org.cn/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"'
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}


def fetch_all_bond_data(
        start_page: int = 1,
        max_pages: int = 20,
        page_size: int = 50,
        delay: int = 2
) -> list:
    """
    Fetch all bond data with pagination

    Args:
        start_page: Starting page number
        max_pages: Maximum number of pages to fetch
        page_size: Number of items per page
        delay: Delay between requests in seconds
    """
    all_data = []

    for page in range(start_page, start_page + max_pages):
        print(f"Fetching page {page}...")

        response_data = fetch_bond_data(
            page=page,
            page_size=page_size
        )

        if not response_data:
            print(f"No data returned for page {page}")
            break
        print(response_data)
        all_data.append(response_data)

        # Add delay between requests
        if page < start_page + max_pages - 1:  # Don't sleep after last request
            sleep(delay)

    return all_data


# Example usage
if __name__ == "__main__":
    # Fetch single page
    # data = fetch_bond_data(page=1, page_size=10)
    # print("Single page data:", data)

    # Fetch multiple pages
    all_data = fetch_all_bond_data(
        start_page=1,
        max_pages=1500,
        page_size=10,
        delay=2
    )
    print(f"Fetched {len(all_data)} pages of data")

    # Save to file
    import json

    with open('bond_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
