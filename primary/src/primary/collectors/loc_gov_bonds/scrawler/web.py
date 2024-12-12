import os
import zipfile
from time import sleep
from pathlib import Path

import requests
from playwright.sync_api import sync_playwright


def get_debt_doc_urls(pcCode, adCode):
    detail_url = "https://www.celma.org.cn/zqgkxq/index.jhtml?pcCode={pcCode}&adCode={adCode}".format(
        pcCode=pcCode, adCode=adCode
    )

    # url = "https://www.celma.org.cn/zqgkxq/index.jhtml?pcCode=2471119&adCode=23"
    from DrissionPage import Chromium

    try:

        tab = Chromium().latest_tab
        tab.get(detail_url)
        notice_ele = tab.ele("#asd")
        elements = notice_ele.eles("xpath://a", timeout=5)
        all_doc_url, downloaded_url = "", []
        for element in elements:
            print(element.text)
            if find_download_url(element):
                all_doc_url = element.attr("href")
                element.click()
                ele_fj = tab.ele("@class=content-fj")
                elements_fj = ele_fj.eles("xpath://a")
                for item in elements_fj:
                    # print(item.text)
                    # if "信用评级" in item.text or "评级报告" in item.text or "债券评级报告" in item.text:
                    #     downloaded_url.append(item.attr("href"))
                    if "信息披露文件" in item.text or "信息披露" in item.text or "信息披露" in item.text:
                        downloaded_url.append(item.attr("href"))
                    # if "募投项目情况汇总" in item.text or "债券募投项目情况" in item.text:
                    #     downloaded_url.append(item.attr("href"))
                if len(downloaded_url) > 0:
                    break
        return all_doc_url, downloaded_url
    except Exception as e:
        return "", ""
    # tab.close()


def find_download_url(element):
    keyword_list = ["发行公开", "发行信息公开", "发行前公告", "信息披露", "债券发行文件",
                    "债券发行", "发行文件", "信用评级报告", "信息披露文件"]
    exclude_list = "结果"
    for keyword in keyword_list:
        if keyword in element.text or keyword in element.attr("title"):
            if exclude_list in element.text or exclude_list in element.attr("title"):
                return False
            return True
    return False


def extract_zip_with_encoding(zip_path, extract_path, remove_zip=True):
    """
    Extract a ZIP file with proper encoding handling for Chinese characters.
    
    Args:
        zip_path (Path): Path to the ZIP file
        extract_path (Path): Directory to extract files to
        remove_zip (bool): Whether to remove the ZIP file after extraction
    """
    try:
        extract_path.mkdir(exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_info in zip_ref.filelist:
                # Try different encodings for Chinese characters
                filename = None
                for encoding in ['gbk', 'utf-8', 'cp437']:
                    try:
                        filename = file_info.filename.encode('cp437').decode(encoding)
                        break
                    except:
                        continue

                if filename is None:
                    filename = file_info.filename  # Fallback to original filename

                # Extract with the original filename first
                zip_ref.extract(file_info, extract_path)

                # Rename the extracted file to use correct Chinese characters
                old_path = extract_path / file_info.filename
                new_path = extract_path / filename
                if old_path != new_path and old_path.exists():
                    if new_path.exists():
                        new_path.unlink()  # Remove existing file if it exists
                    old_path.rename(new_path)

            print(f"Extracted ZIP contents to {extract_path}")

        if remove_zip and zip_path.exists():
            zip_path.unlink()
            print(f"Removed ZIP file: {zip_path}")

    except Exception as e:
        print(f"Error extracting ZIP {zip_path}: {str(e)}")
        raise


def download_zip(url, bond_name, save_dir):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.governbond.org.cn/',
            'Accept': '*/*'
        }

        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        zip_filename = f"{bond_name}.zip"
        download_path = save_dir / zip_filename

        # Save the file in chunks
        with open(download_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"Successfully downloaded ZIP for {bond_name}")

        # # Extract the ZIP file to a subdirectory named after the bond
        # extract_path = save_dir / bond_name
        # extract_zip_with_encoding(download_path, extract_path)

    except Exception as e:
        print(f"Error handling ZIP for {bond_name}: {str(e)}")


def download_pdf_in_pdfviewer(url, download_file_name, pdf_dir):
    with sync_playwright() as p:
        # 使用chromium代替webkit可能有更好的兼容性
        browser = p.chromium.launch(
            headless=True,  # 设置为False以查看浏览过程
            args=['--disable-web-security']  # 禁用web安全策略
        )

        context = browser.new_context(
            accept_downloads=True,
            extra_http_headers={
                'Accept': 'application/pdf',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Referer': 'https://www.governbond.org.cn/',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
            }
        )

        page = context.new_page()

        try:
            # 1. 先访问主站
            # print("访问主站...")
            # page.goto('https://www.governbond.org.cn/', wait_until='networkidle')
            # page.wait_for_timeout(2000)  # 等待2秒

            # 2. 设置下载监听
            print("准备下载...")
            with page.expect_download(timeout=30000) as download_info:
                # 3. 使用page.evaluate()来触发下载
                page.evaluate('''() => {{
                    const link = document.createElement('a');
                    link.href = '{down_load_url}';
                    link.download = 'document.pdf';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }}'''.format(down_load_url=url))

                # 4. 等待下载开始
                download = download_info.value
                print("下载已开始...")

                # 5. 保存文件
                download_path = os.path.join(os.getcwd(), pdf_dir / "{name}.pdf".format(name=download_file_name))
                download.save_as(download_path)
                print(f"文件已保存到: {download_path}")

        except Exception as e:
            print(f"下载过程中出现错误: {e}")

        finally:
            # 8. 清理资源
            context.close()
            browser.close()
