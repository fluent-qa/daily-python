from playwright.sync_api import sync_playwright


def run_with_specific_browser_type(url):
    with sync_playwright() as p:
        # 方法4: 选择不同的浏览器类型
        # 使用Chrome
        browser_chrome = p.chromium.launch(channel='chrome', headless=True, timeout=3000)
        if not url.startswith("http"):
            return url, ""
        # 使用Firefox
        browser_firefox = p.firefox.launch(headless=False)

        # 使用Safari (仅在macOS上可用)
        browser_safari = p.webkit.launch(headless=False)
        page = browser_chrome.new_page()
        try:
            # 分别在不同浏览器中执行操作
            page.goto(url, timeout=10000)
            # 执行脚本并等待结果
            result = page.locator("xpath=//*[@id=\"form1\"]/div[6]/div[2]/div[1]/div[3]").text_content(timeout=2000)
            print(",".join([url, result]))
            return url, result
        except Exception as e:
            print(e)
            return url, ""

def run(url_path,result_file):
    with open(url_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        url = line.replace("\n", "")
        all_create_time = run_with_specific_browser_type(url)
        with open(result_file, 'a') as f:
            f.write(",".join(all_create_time) + "\n")

# 使用示例
if __name__ == "__main__":
    # 选择一个方法运行
    # run_in_existing_browser()
    # run_with_specific_browser_path()
    # run_with_user_data_dir()
    # run_with_specific_browser_type()
    # run_with_specific_browser_path()
    with open('url.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        url = line.replace("\n", "")
        all_create_time = run_with_specific_browser_type(url)
        with open('create_time.csv', 'a') as f:
            f.write(",".join(all_create_time) + "\n")
