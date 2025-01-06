import requests
from bs4 import BeautifulSoup


def fetch_by_github_api(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        raw_data = response.json()
        results = []
        for item in raw_data["items"]:
            repo_info = {
                "link": item["html_url"],
                "description": item["description"],
                "stars": item["stargazers_count"],
            }
            results.append(repo_info)
        results = sorted(results, key=lambda x: x["stars"], reverse=True)
        return results
    else:
        print(f"Failed to get data, status code: {response.status_code}")
        return []


def get_github_collection_results(
    collection_id: str, count: int = 5, base_url="https://github.com"
) -> list[dict]:
    url = f"{base_url}/collections/{collection_id}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for article in soup.select("article"):
            repo_link = article.select_one("h1.h3 a")["href"]
            stars_anchor = article.select_one('a[data-ga-click*="stargazers"]')
            if stars_anchor:
                stars_content = "".join(filter(str.isdigit, stars_anchor.get_text()))
                stars = int(stars_content.strip()) if stars_content else 0
            else:
                stars = 0
            description = article.select_one("div.color-fg-muted").text.strip()
            results.append(
                {
                    "link": base_url + repo_link,
                    "stars": stars,
                    "description": description,
                }
            )
        results = sorted(results, key=lambda x: x["stars"], reverse=True)
        return results[:count]
    else:
        print(f"Failed to get data, status code: {response.status_code}")
        return []
