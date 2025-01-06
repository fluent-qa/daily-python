import os

import requests

from .models import GoogleSearchMode


def search_google(
    keyword: str,
    mode: GoogleSearchMode = GoogleSearchMode.ARTICLES,
    max_results: int = 10,
):
    global websites_to_search
    global terms_to_search
    api_key = os.environ["GOOGLE_CLOUD_API_KEY"]
    cse_id = os.environ["CUSTOM_SEARCH_ENGINE_ID"]

    # Create a combined query with the "site:" search operator
    base_query = f"{keyword}"
    base_query += " " + terms_to_search[mode]
    site_specific_queries = " OR ".join(
        [f"site:{site}" for site in websites_to_search[mode]]
    )
    query = f"{base_query} {site_specific_queries}"

    # Endpoint for Google Custom Search
    url = "https://www.googleapis.com/customsearch/v1"

    all_items = []
    pages = -(-max_results // 10)  # This is a ceiling division trick

    for page in range(pages):
        start_index = page * 10 + 1

        # Parameters for the search query
        params = {
            "key": api_key,
            "cx": cse_id,
            "q": query,
            "num": 10
            if (max_results - len(all_items)) > 10
            else (max_results - len(all_items)),
            # fetch remaining if less than 10
            "start": start_index,
        }

        # Make the API request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            results = response.json()

            # Extract the desired data
            for item in results.get("items", []):
                page_map = item.get("pagemap", {})
                og_description = page_map.get("metatags", [{}])[0].get(
                    "og:description", ""
                )
                all_items.append(
                    {
                        "title": item["title"],
                        "link": item["link"],
                        "description": item["snippet"] + " " + og_description,
                    }
                )
        else:
            print(f"Error {response.status_code}: {response.text}")
            break

        if len(all_items) >= max_results:
            break

    return all_items


def search_google_for_articles(keyword: str, max_results: int = 10):
    return search_google(keyword, GoogleSearchMode.ARTICLES, max_results)


def search_google_for_courses(keyword: str, max_results: int = 10):
    return search_google(keyword, GoogleSearchMode.COURSES, max_results)


def search_google_for_books(keyword: str, max_results: int = 10):
    return search_google(keyword, GoogleSearchMode.BOOKS, max_results)


def search_google_for_research(keyword: str, max_results: int = 10):
    return search_google(keyword, GoogleSearchMode.RESEARCH, max_results)


def search_google_for_podcasts(keyword: str, max_results: int = 10):
    return search_google(keyword, GoogleSearchMode.PODCASTS, max_results)


def search_google_for_videos(keyword: str, max_results: int = 10):
    return search_google(keyword, GoogleSearchMode.VIDEOS, max_results)


def search_google_for_tools_software(keyword: str, max_results: int = 10):
    return search_google(keyword, GoogleSearchMode.TOOLS_SOFTWARE, max_results)


def search_google_for_conferences_or_events(keyword: str, max_results: int = 10):
    return search_google(keyword, GoogleSearchMode.CONFERENCES_EVENTS, max_results)


def search_google_for_slides_or_presentations(keyword: str, max_results: int = 10):
    return search_google(keyword, GoogleSearchMode.SLIDES_PRESENTATIONS, max_results)


if __name__ == "__main__":
    search_query = "Auto-GPT"
    articles = search_google(search_query)
    # Print the results
    for article in articles:
        print(article["title"])
        print(article["link"])
        print(article["description"])
        print("-" * 80)
