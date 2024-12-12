from __future__ import annotations

from pathlib import Path

import pandas as pd
import rich

from primary import pd_ext
from primary.collectors.loc_gov_bonds import scrawler


def download_bonds(source_file: str | Path, output_dir: Path | str, source_file_type: str = "csv",
                   record_result: bool = True):
    result = pd_ext.read_to_df(source_file, file_type=source_file_type)
    downloaded_url = {}
    overall_download_result = {}
    for index, row in result.iterrows():
        ad_code = row["行政区划代码"]
        pc_code = row["债券代码"]
        ## todo: 河南特殊处理
        all_docs_url, credit_report_urls = scrawler.get_debt_doc_urls(pcCode=pc_code, adCode=ad_code)
        overall_download_result[pc_code] = all_docs_url
        if downloaded_url.get(all_docs_url, None) is None:
            if len(credit_report_urls) >= 1:
                for url in credit_report_urls:
                    if url.endswith(".pdf"):
                        scrawler.download_pdf_in_pdfviewer(url, row["债券名称"], output_dir)
                    elif url.endswith(".zip"):
                        scrawler.download_zip(url, row["债券名称"], output_dir)
                downloaded_url[all_docs_url] = credit_report_urls
        else:
            continue

    df = pd.DataFrame(list(overall_download_result.items()), columns=['债券代码', 'URL'])
    if record_result:
        df.to_csv(output_dir / "result.csv", index=False, encoding='utf-8')
