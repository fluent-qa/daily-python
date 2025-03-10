import csv
import time
from typing import List

import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from pydantic import BaseModel

from primary import pd_ext


def test_save_cookie():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.tgb.cn/blog/2368012")
        page.pause()
        storage = context.storage_state(path="auth_cookies.json")
        print("Cookie已保存到 auth_cookies.json")
        browser.close()


class PostModel(BaseModel):
    title: str
    link: str


BASE_URL = "https://www.tgb.cn"


def test_load_cookie_run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="auth_cookies.json")
        page = context.new_page()
        structured_post: List[PostModel] = []

        for index in range(1):

            request_url = f"https://www.tgb.cn/user/blog/moreTopic?pageNum=2&pageNo={index}&sortFlag=T&userID=2138102"
            # page.goto("https://www.tgb.cn/blog/2368012")
            page.goto(request_url)
            ## https://www.tgb.cn/user/blog/moreTopic?pageNum=2&pageNo=2&sortFlag=T&userID=2368012
            # print("Cookie已保存到 auth_cookies.json")
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            posts = soup.select(".suh")
            for post in posts:
                structured_post.append(
                    PostModel(
                        title=post.text.replace("\t", "").replace("\n", ""),
                        link=BASE_URL + "/" + post.select("a")[0].get_attribute_list("href")[0]
                    )
                )
            pd_ext.models_to_file(structured_post, f"2138102-{index}.csv")
        pd_ext.models_to_file(structured_post, "2138102.csv")
        browser.close()


def test_get_comments():
    all_text = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="auth_cookies.json")
        page = context.new_page()
        # read urls
        urls = pd.read_csv("2368012.csv")['link']
        index = 118
        for url in urls:
            url = url.replace("https://www.tgb.cna", "https://www.tgb.cn/a")
            page.goto(url)
            print(f"start go to {url}")
            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            article_full = soup.select("#first")[0].text
            all_text.append("----正文---------\n")
            all_text.append(article_full.replace("\t", "").replace("\n", ""))
            all_text.append("----评论--------\n")
            page_location = ""
            while page_location != page.url:
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                comment_items = soup.select(".comment-data-text")
                for comment_item in comment_items:
                    all_text.append(comment_item.text.replace("\t", "").replace("\n", ""))
                page_location = page.url
                try:
                    page.get_by_text("下一页").first.click()
                except Exception as e:
                    print(e)
                time.sleep(0.5)
            with open(f"2368012-c-{index}.txt", "a") as f:
                f.writelines(all_text)
            index = index + 1

        browser.close()
    with open("2368012-comments.txt", "w", encoding="utf-8") as f:
        f.writelines(all_text)
