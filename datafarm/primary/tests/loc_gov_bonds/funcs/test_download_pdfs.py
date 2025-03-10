import csv
import os
from pathlib import Path

import pandas as pd
from qpyconf import settings

from tests.loc_gov_bonds.test_standard_process import REWORKSPACE, download_dir, source_file_path
from primary import pd_ext
from primary.collectors.loc_gov_bonds import download_bonds, scrawler

WORKING_DIR = Path(settings.workspace)


def test_download_pdf_files():
    """
    1. download
    :return:
    """
    os.makedirs(download_dir, exist_ok=True)
    download_bonds(source_file_path, download_dir)


def test_download_pdfs():
    """
    1. test download all pdfs
    :return:
    """
    result = pd_ext.read_to_df(WORKING_DIR / "rework/guangdong/bonds.xlsx", file_type="xlsx")
    downloaded_url = {}
    overall_download_result = {}
    for index, row in result.iterrows():
        ad_code = row["行政区划代码"]
        pc_code = row["债券代码"]
        all_docs_url, credit_report_urls = scrawler.get_debt_doc_urls(pcCode=pc_code, adCode=ad_code)
        overall_download_result[pc_code] = all_docs_url
        if downloaded_url.get(all_docs_url, None) is None:
            if len(credit_report_urls) >= 1:
                for url in credit_report_urls:
                    if (url.endswith(".pdf")):
                        scrawler.download_pdf_in_pdfviewer(url, row["债券名称"], WORKING_DIR / "rework/guangdong/2024")
                    elif url.endswith(".zip"):
                        scrawler.download_zip(url, row["债券名称"], WORKING_DIR / "rework/guangdong/2024")
                downloaded_url[all_docs_url] = credit_report_urls
        else:
            continue

    df = pd.DataFrame.from_dict(overall_download_result)
    df.columns = ['债券代码', 'URL']
    df.to_csv(WORKING_DIR / "rework/guangdong/downloads.csv", index=False, encoding='utf-8')


def test_download_single():
    """
    1. test download single file
    :return:
    """
    url = "https://www.governbond.org.cn/uploadFiles/44/attachFiles/202405/2a2fbbd0-5164-4d27-97f0-45fa43caf057.pdf"
    scrawler.download_pdf_in_pdfviewer(url, "demo", WORKING_DIR / "rework/guangdong/2024")


def test_get_url():
    pc_code = "2371423"
    ad_code = "23"
    all_docs_url, credit_report_urls = scrawler.get_debt_doc_urls(pcCode=pc_code, adCode=ad_code)
    print(all_docs_url, credit_report_urls)
