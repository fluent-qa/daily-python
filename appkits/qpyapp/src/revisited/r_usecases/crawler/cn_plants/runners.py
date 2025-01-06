from time import sleep

from datafarm.cn_plants.website_runner import run


def split_file():
    with open('url.txt', "r") as f:
        lines = f.readlines()

    with open('10000.csv', 'w') as t:
        t.writelines(lines[10000:20000])

    with open('20000.csv', 'w+') as t:
        t.writelines(lines[20000:30000])

    with open('30000.csv', 'w+') as t:
        t.writelines(lines[30000:40000])

    with open('40000.csv', 'w+') as t:
        t.writelines(lines[40000:])


import requests


def fetch_species_info(tu_url: str) -> dict:
    """
    获取物种信息

    Parameters:
        pid: 物种ID
    """
    if len(tu_url.replace(" ", "")) == 0:
        return tu_url, ""
    else:
        pid = tu_url.replace("https://ppbc.iplant.cn/tu/", "")
    try:
        # 构建URL
        url = f'https://ppbc.iplant.cn/ashx/getotherinfo.ashx'

        # 查询参数
        params = {
            't': 'spgetapp',
            'pid': pid,
            # 'l': '0.2416375447999073'
        }

        # 请求头
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'ASP.NET_SessionId=dzafpvybio11okwprndv0ulz; _pk_id.5.772d=9c2a65c648d82be8.1729840203.; ValidateCode=3459; _pk_ses.5.772d=1',
            'Pragma': 'no-cache',
            'Referer': url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
        }

        # 发送请求
        response = requests.get(
            url,
            params=params,
            headers=headers
        )

        # 检查响应状态
        response.raise_for_status()

        # 返回JSON数据
        return tu_url, response.json()[-1]["app_time"]

    except Exception as e:
        print(f"请求出错: {e}")
        return url_spec, ''


# 使用示例
if __name__ == "__main__":
    # 获取物种信息
    # species_info = fetch_species_info("https://ppbc.iplant.cn/tu/13105652")
    with open('url.txt', "r") as f:
        lines = f.readlines()
    for line in lines:
        url_spec, app_time = fetch_species_info(line.strip())
        # sleep(1)
        print(",".join([url_spec, app_time]))
        with open("url_create_time.csv", 'a') as f:
            f.write(",".join([url_spec, app_time]) + "\n")

# split_file()

# run('30000.csv','30000-result.csv')
# run('20000.csv','20000-result.csv')
