import argparse
import os
import asyncio
import signal
import sys
import threading
from pathlib import Path

from playwright.async_api import async_playwright

URL_TEMPLATE = """
https://patents.google.com/?q=({keywords})&assignee={assignee}&before=priority:{end_date}&after=priority:{start_date}&num=100
"""

BASE_URL = "https://patents.google.com/"

from pydantic import BaseModel


class SearchParameter(BaseModel):
    """
    输入
    """
    keyword: str = None
    start_date: str = None
    end_date: str = None
    total_pages: int = None
    assignee: str = None
    inventor: str = None


class PatentSummary(BaseModel):
    """
    输出
    """
    patent_code: str = None
    title: str = None
    abstract: str = None
    patent_url: str = None
    patent_download_url: str = None


def create_url(search_parameter: SearchParameter):
    fetch_url = URL_TEMPLATE.format(
        keywords=search_parameter.keyword,
        assignee=search_parameter.assignee,
        start_date=search_parameter.start_date,
        end_date=search_parameter.end_date
    )
    ## 可以后面添加任意内容按照需要
    if len(search_parameter.keyword) < 1:
        fetch_url = fetch_url.replace("q=()", '')
    if search_parameter.inventor:
        fetch_url += f"&inventor={search_parameter.inventor}"

    return fetch_url


def append_parameters_into_url(fetch_url, param_name, search_parameter: SearchParameter):
    param_value = search_parameter.model_dump().get(param_name)
    fetch_url += f"&{param_name}={param_value}"
    return fetch_url


async def download_pdf_in_pdfviewer(url, download_file_name, pdf_dir):
    async with async_playwright() as p:
        # 使用chromium代替webkit可能有更好的兼容性
        browser = await p.chromium.launch(
            headless=True,  # 设置为False以查看浏览过程
            args=['--disable-web-security']  # 禁用web安全策略
        )

        context = await browser.new_context(
            accept_downloads=True,
            extra_http_headers={
                'Accept': 'application/pdf',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Referer': BASE_URL,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
            }
        )

        page = await context.new_page()

        try:
            # 2. 设置下载监听
            print("准备下载...")
            async with page.expect_download(timeout=30000) as download_info:
                # 3. 使用page.evaluate()来触发下载
                await page.evaluate('''() => {{
                    const link = document.createElement('a');
                    link.href = '{down_load_url}';
                    link.download = 'document.pdf';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }}'''.format(down_load_url=url))

                # 4. 等待下载开始
                download = await download_info.value
                print("下载已开始...")

                # 5. 保存文件
                download_path = os.path.join(os.getcwd(), pdf_dir / "{name}.pdf".format(name=download_file_name))
                await download.save_as(download_path)
                print(f"文件已保存到: {download_path}")

        except Exception as e:
            print(f"下载过程中出现错误: {e}")

        finally:
            # 8. 清理资源
            await context.close()
            await browser.close()


async def fetch_patents(fetch_url, total_pages=10, pdf_dir="output"):
    # first page
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        patents = []
        ## 1. 获取所有信息
        ## 2. 下载每一个文件
        ## 3. 开始下一页循环
        for index in range(0, total_pages):
            try:
                await page.goto(fetch_url + "&page=" + str(index))
                await page.wait_for_load_state('domcontentloaded')
                await page.wait_for_selector(".result")
                patent_summaries = await page.query_selector_all('.result')
                for summary in patent_summaries:
                    title_element = await summary.query_selector(".result-title")
                    title_link = await title_element.query_selector("a")
                    title = await title_link.text_content()
                    title = title.replace("\n", "").strip()

                    abstract_element = await summary.query_selector(".abstract")
                    abstract = await abstract_element.text_content()
                    abstract = abstract.replace("\n", "").strip()

                    pdf_link = await summary.query_selector(".pdfLink")
                    patent_code = await pdf_link.text_content()
                    patent_code = patent_code.replace("\n", "").strip()
                    download_url = await pdf_link.get_attribute("href")

                    patent_url = 'https://patents.google.com/patent/' + patent_code
                    patents.append(PatentSummary(title=title, abstract=abstract, patent_code=patent_code,
                                                 patent_url=patent_url, patent_download_url=download_url))
                    await download_pdf_in_pdfviewer(download_url, download_file_name=patent_code,
                                                    pdf_dir=Path(pdf_dir))
            except Exception as e:
                print(f"获取{index}失败。。。。。。")
                print(e)
        await browser.close()
    return patents


async def main(parameter: SearchParameter):
    url = create_url(parameter)
    patents = await fetch_patents(url, parameter.total_pages)

    # Create output directory if it doesn't exist
    Path("output").mkdir(exist_ok=True)

    # Write to CSV with proper headers
    import csv
    csv_file = Path("output") / "patents.csv"
    headers = ["patent_code", "title", "abstract", "patent_url", "patent_download_url"]

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for patent in patents:
            writer.writerow(patent.model_dump())

    # Print summary
    print(f"\nDownload Summary:")
    print(f"Total patents processed: {len(patents)}")
    print(f"Results saved to: {csv_file}")

    # Also print details to console
    for patent in patents:
        print(f"\nPatent: {patent.title}")
        print(f"Code: {patent.patent_code}")
        print("---")


stop_event = threading.Event()


def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Stopping downloads...')
    stop_event.set()
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    # parser = argparse.ArgumentParser(description="Download patent PDFs for a specified company and date range.")
    #
    # parser.add_argument('company', type=str, help='Name of the company to search for.')
    # parser.add_argument('start_year', type=str, help='Start year of the date range.')
    # parser.add_argument('end_year', type=str, help='End year of the date range.')
    # parser.add_argument('total_pages', type=int, help='Total Search Result Page')
    # parser.add_argument('keywords', type=str, help='Search Keywords')
    # args = parser.parse_args()
    parameter = SearchParameter(
        keyword="",
        assignee="Groq",
        start_date="2020-01-01",
        end_date="2024-12-01",
        total_pages=10
    )
    # parameter = SearchParameter(
    #     keyword=args.keyword,
    #     assignee=args.company,
    #     start_date=args.start_year,
    #     end_date=args.end_year,
    #     total_pages=args.total_pages
    # )
    asyncio.run(main(parameter))
