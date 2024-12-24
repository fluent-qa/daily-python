import requests
import argparse
import os
from bs4 import BeautifulSoup
from datetime import datetime
import re
import threading
import signal
import sys
import category

stop_event = threading.Event()


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def download_pdf(pdf_url, pdf_path):
    headers = {}
    if os.path.exists(pdf_path):
        headers['Range'] = f"bytes={os.path.getsize(pdf_path)}-"
    response = requests.get(pdf_url, headers=headers, stream=True)
    with open(pdf_path, 'ab') as pdf_file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                pdf_file.write(chunk)
            if stop_event.is_set():
                print(f"Download stopped: {pdf_path}")
                return
    print(f"Downloaded: {pdf_path}")


def fetch_patents(company="nvidia", start_year="2022", end_year="2024"):
    if int(start_year) >= int(end_year):
        print("Error: start_year should be less than or equal to end_year.")
        return

    base_url = "https://patents.google.com/"
    search_url = f"{base_url}?assignee={company}&before=priority:{end_year}1231&after=priority:{start_year}0101&num=100&sort=new&clustered=true"

    print(search_url)
    response = requests.get(search_url)
    if response.status_code != 200:
        print(f"Failed to fetch patents for {company} from {start_year} to {end_year}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    patent_links = soup.find_all('a', class_='pdfLink style-scope search-result-item')
    output_dir = f"patents/{company}_{start_year}_{end_year}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    threads = []
    for link in patent_links:
        try:
            pdf_url = link['href']
            patent_number = link.find('span', class_='style-scope search-result-item').text.strip()
            sanitized_patent_number = sanitize_filename(patent_number)
            pdf_path = os.path.join(output_dir, f"{sanitized_patent_number}.pdf")

            # 检查文件是否存在且大小不为0
            if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
                print(f"File already exists and is not empty: {pdf_path}")
                continue

            thread = threading.Thread(target=download_pdf, args=(pdf_url, pdf_path))
            threads.append(thread)
            thread.start()
        except Exception as e:
            print(f"Failed to download patent: {e}")

    for thread in threads:
        thread.join()


def signal_handler(sig, frame):
    print('You pressed Ctrl+C! Stopping downloads...')
    stop_event.set()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    parser = argparse.ArgumentParser(description="Download patent PDFs for a specified company and date range.")
    parser.add_argument('company', type=str, help='Name of the company to search for.')
    parser.add_argument('start_year', type=int, help='Start year of the date range.')
    parser.add_argument('end_year', type=int, help='End year of the date range.')
    args = parser.parse_args()

    fetch_patents(args.company, args.start_year, args.end_year)
    category.category(pdf_folder=f"patents/{args.company}_{args.start_year}_{args.end_year}",
                      output_folder=f"patents/cat_{args.company}_{args.start_year}_{args.end_year}")
