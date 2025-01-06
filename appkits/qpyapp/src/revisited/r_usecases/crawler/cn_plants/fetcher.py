from pprint import pprint
import os
import requests
import pandas as pd
import random
from multiprocessing import Pool
import time
from multiprocessing import Queue, Process, Pool, Manager
import multiprocessing
from multiprocessing import Process
from multiprocessing import Array

from playwright.sync_api import sync_playwright

# https://www.cvh.ac.cn/spms/list.php?&stateProvince[]=%E4%BA%91%E5%8D%97%E7%9C%81!&taxonName=Clematis%20yunnanensis&offset=30


user_agent = [
    # Opera
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",

    # Firefox
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",

    # Safari
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",

    # chrome
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",

    # 360
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",

    # 淘宝浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",

    # 猎豹浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",

    # QQ浏览器
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ",

    # sogou浏览器
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",

    # maxthon浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",

    # UC浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/17D50 UCBrowser/12.8.2.1268 Mobile AliApp(TUnionSDK/0.1.20.3)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.1.0; OPPO R11t Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.19 SP-engine/2.15.0 baiduboxapp/11.19.5.10 (Baidu; P1 8.1.0)",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 SP-engine/2.14.0 main%2F1.0 baiduboxapp/11.18.0.16 (Baidu; P2 13.3.1) NABar/0.0 ",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.10(0x17000a21) NetType/4G Language/zh_CN",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36"

]
# referer="https://www.cvh.ac.cn/spms/list.php?taxonName=Primula+annulata&family=&genus=&country=&county=&locality=&minimumElevation=&maximumElevation=&recordedBy=&recordNumber=&year=&collectionCode=&identifiedBy=&dateIdentified="
headers = {
    "Referer": "",
    "User-Agent": random.choice(user_agent),
}


# 代理
def proxie():
    # 账密模式
    # proxyUrl = "http://%(user)s:%(password)s@%(server)s" % {
    #     "user": "9BC96199",  # Authkey
    #     "password": "73BA23D0E4D5",  # Authpwd
    #     "server": "tun-vdpzuj.qg.net:13542",
    # }
    proxy_url = "103.83.97.11:8090"
    proxies = {
        "http": proxy_url,
        "https": proxy_url,
    }

    url2 = 'http://httpbin.org/get'
    r = requests.get(url=url2)
    origin = r.json()['origin']
    print('本次测试起源代理为: ' + str(origin))
    return proxies


# 1: 读取关键字
def read_keywords(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        plant_names = file.readlines()

    plant_names = [name.strip() for name in plant_names]  # 去除每行末尾的换行符和空格
    return plant_names


## 2: 获取关键字查询结果
def query_keywords(keywords):
    print(f"搜索关键词:{keywords}-------")
    url = f'https://www.cvh.ac.cn/controller/spms/list.php?&taxonName={keywords}'
    headers['Referer'] = url
    try:
        response = requests.get(url=url, headers=headers, timeout=10)
        return {keywords: response.json()}
    except Exception as e:
        print('错误')
        with open('植物名称_错误.txt', 'a', encoding='utf-8') as f:
            f.write(keywords + '\n')
            f.close()
        raise e


## 获取详细信息
def create_detail(name, collection):
    url_data = f'https://www.cvh.ac.cn/controller/spms/detail.php?id={collection['collectionID']}'
    url_png = f'https://image.cvh.ac.cn/files/l/{collection['institutionCode']}/{collection['collectionCode']}.jpg'
    print('url_data: ' + url_data)
    headers['Referer'] = url_data
    try:
        response_data = requests.get(url_data, headers=headers, timeout=10)  # 超时设置为10秒
        # print(response_data.text)
        data_json = response_data.json()['rows']
        print(data_json)
        plant_info = {
            '中文名': data_json['chineseName'],
            '拉丁名': name,
            '采集人': data_json['recordedBy'],
            '采集号': data_json['recordNumber'],
            '采集时间': data_json['verbatimEventDate'],
            '采集地': data_json['stateProvince'],
            '海拔': data_json['elevation'],
            '生境': data_json['habitat'],
            '习性': data_json['occurrenceRemarks'],
            '物候期': data_json['reproductiveCondition'],
            '图片链接': url_png,
            '本地图片链接': ''
        }
        print(plant_info)

        df = pd.DataFrame([plant_info])  # 将数据转为 DataFrame
        file_path = 'last-one.csv'  # 指定 CSV 文件路径
        file_exists = os.path.isfile(file_path)  # 检查文件是否存在
        df.to_csv(file_path, mode='a+', header=not file_exists, index=False,
                  encoding='utf-8')  # 写入数据到 CSV 文件，第一次写入时加表头，追加时不加表头
    except Exception as e:
        print(e)
        ## 'Gentiana crassuloides'


def main():
    plant_names = read_keywords("name_ignore_stats.csv")
    # alreay_used = read_keywords('already.csv')
    for plant_name in plant_names[::-1]:
        try:
            keywords_collections = query_keywords(plant_name)
            collections = keywords_collections[plant_name]["rows"]
            stateProvince = ""
            counts = 1
            for current_collection in collections:
                if current_collection['stateProvince'] != stateProvince and counts <= 3:
                    create_detail(plant_name, current_collection)
                    # time.sleep(0.3)
                    counts += 1
                    stateProvince = current_collection['stateProvince']
        except Exception as e:
            print(e)
            continue

    print('over')


def get_image():
    """
    curl 'https://img7.iplant.cn/image2/236/86F1AE4AF5F5AA36.jpg' \
  -H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Pragma: no-cache' \
  -H 'Referer: https://ppbc.iplant.cn/' \
  -H 'Sec-Fetch-Dest: image' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' --output 3.jpg

    :return:
    """
    url = 'https://img7.iplant.cn/image2/236/86F1AE4AF5F5AA36.jpg'

    headers = {
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://ppbc.iplant.cn/',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }

    # 发送GET请求并获取图片内容
    response = requests.get(url, headers=headers)

    # 将图片内容保存到文件
    if response.status_code == 200:
        with open('3.jpg', 'wb') as f:
            f.write(response.content)
        print('图片下载成功')
    else:
        print(f'下载失败，状态码: {response.status_code}')


import subprocess

# 构建curl命令
curl_command = '''curl 'https://img7.iplant.cn/image2/236/86F1AE4AF5F5AA36.jpg' \
  -H 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Pragma: no-cache' \
  -H 'Referer: https://ppbc.iplant.cn/' \
  -H 'Sec-Fetch-Dest: image' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' --output 3.jpg'''

# 方法1：使用shell=True（简单但不太安全）
try:
    subprocess.run(curl_command, shell=True, check=True)
    print("下载成功")
except subprocess.CalledProcessError as e:
    print(f"下载失败: {e}")


# 方法2：更安全的方式，将命令拆分为列表（推荐）
def download_with_curl():
    curl_args = [
        'curl',
        'https://img7.iplant.cn/image2/236/86F1AE4AF5F5AA36.jpg',
        '-H', 'Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        '-H', 'Accept-Language: zh-CN,zh;q=0.9',
        '-H', 'Cache-Control: no-cache',
        '-H', 'Connection: keep-alive',
        '-H', 'Pragma: no-cache',
        '-H', 'Referer: https://ppbc.iplant.cn/',
        '-H', 'Sec-Fetch-Dest: image',
        '-H', 'Sec-Fetch-Mode: no-cors',
        '-H', 'Sec-Fetch-Site: same-site',
        '-H',
        'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        '-H', 'sec-ch-ua: "Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        '-H', 'sec-ch-ua-mobile: ?0',
        '-H', 'sec-ch-ua-platform: "macOS"',
        '--output', '4.jpg'
    ]

    try:
        result = subprocess.run(curl_args, capture_output=True, text=True, check=True)
        print("下载成功")
        return result
    except subprocess.CalledProcessError as e:
        print(f"下载失败: {e}")
        return None


def get_create_time():
    with sync_playwright() as p:
        # 方法4: 选择不同的浏览器类型
        # 使用Chrome
        browser_chrome = p.chromium.launch(channel='chrome', headless=True)

        # 使用Firefox
        browser_firefox = p.firefox.launch(headless=False)

        # 使用Safari (仅在macOS上可用)
        browser_safari = p.webkit.launch(headless=False)

        # 分别在不同浏览器中执行操作
        for browser in [browser_chrome, browser_firefox, browser_safari]:
            page = browser.new_page()
            page.goto("")

            # 执行脚本并等待结果
            result = page.evaluate("""() => {
                    return {
                        title: document.title,
                        url: window.location.href,
                        userAgent: navigator.userAgent
                    }
                }""")

            print(f"浏览器信息: {result}")
            browser.close()


# 调用方法2

if __name__ == '__main__':
    # get_image()
    # download_with_curl()
    # main()
    plant_names = read_keywords("name_ignore_stats.csv")
    with open("遗漏.csv","r") as f:
       lines =  f.readlines()
    existings_names = [line.split(",")[1] for line in lines]
    print(existings_names)
    result = []
    for plant_name in plant_names:
        if plant_name not in existings_names:
            result.append(plant_name)
    print(result)
    with open('没有标本.csv','w') as f:
        for item in result:
            f.write(item+"\n")
