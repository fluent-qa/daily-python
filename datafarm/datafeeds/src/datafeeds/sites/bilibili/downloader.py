"""
获取bilibili视频信息,步骤：
1. 读取获取视频信息的url的清单
"""
from __future__ import annotations

import json
import os
import time

from dataclasses import dataclass
from datetime import datetime
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import xml.etree.ElementTree as ET
from typing import Dict

import requests

## constants,常量，配置，如果失败需要修改cookies
DEFAULT_HEADERS = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'origin': 'https://www.bilibili.com',
    'priority': 'u=1, i',
    'referer': 'https://www.bilibili.com/video/BV1Qb421Y7SV/?vd_source=c668c05f4b5039b3290cec826cf03f14',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
}

DEFAULT_COOKIES = {
    'buvid3': '0C25C8A6-EA71-F822-F8E0-D989C2DE341079944infoc',
    # 'b_nut': '1740392079',
    # '_uuid': '9CDA82F10-3A85-696B-12EF-F7B110DFAF731080098infoc',
    # 'enable_web_push': 'DISABLE',
    # 'enable_feed_channel': 'DISABLE',
    # 'buvid4': '7B80DD12-10E3-9840-42AC-D6AF2434DC8A80488-025022410-CvOVun1%2BX15dfH4%2ByQODmg%3D%3D',
    # 'rpdid': '|(J~lkk|kkk|0J\'u~R|Jmku)l',
    # 'header_theme_version': 'CLOSE',
    # 'hit-dyn-v2': '1',
    # 'fingerprint': '26b9a5c72e7e719ce17094db143e7b87',
    # 'buvid_fp_plain': 'undefined',
    # 'buvid_fp': 'c1c5a9ace7d054c6d980668a8287e8ec',
    # 'b_lsid': '982F4621_195418713FC',
    # 'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDA4MjAzMzQsImlhdCI6MTc0MDU2MTA3NCwicGx0IjotMX0.kSm556YWR09NRAVgoilHdFMr19tpUlNe7IkIiyhCA3c',
    # 'bili_ticket_expires': '1740820274',
    # 'bp_t_offset_608721975': '1038191353193824256',
    'SESSDATA': 'ca456f57%2C1756113344%2C6b3cf*22CjDoIx2OyeG8Wt8dbXVwBEAYdEe5EEUviWR90Z6QtwR9ag0uEFL-uTOTZl8vhIbUaXQSVklwb1pyTXRQaERLY3NVSlVJR2hBTGR6TGpVUVJSY3NYTXJISnV5U3ZmQkkzQlRvU3liWTBVY1hqWWczcXQ2SXN3aVdUbDV1bmpzV01vdWs5MG53d3Z3IIEC',
    'bili_jct': '38028b3b1efc816095eba45955763581',
    # 'DedeUserID': '3546803955829068',
    # 'DedeUserID__ckMd5': '9ceb6008f1060048',
    # 'sid': '6stk7ud6',
    # 'home_feed_column': '4',
    # 'browser_resolution': '150-895',
    # 'CURRENT_FNVAL': '4048'
}

view_url = 'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
wbi_url = 'https://api.bilibili.com/x/player/wbi/v2'


# 1. 读取BV地址列表
def read_bv_list(file_path: str) -> []:
    """从指定文件中读取BV地址列表"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            bv_list = [line.strip() for line in file if line.strip()]
        return bv_list
    except FileNotFoundError:
        print(f"文件未找到：{file_path}")
        return []
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return []


# 2.从网址中提取BV号
def extract_bvid(url: str) -> str | None:
    """从完整的视频网址中提取BV号"""
    if "BV" in url:
        return url.split("/video/")[-1].split('/')[0]
    else:
        print(f"无法从网址中提取BV号：{url}")
        return None


def make_bilibili_get_request(url, headers=None, cookies=None, params=None):
    """
    Makes a request to the Bilibili API with the specified headers and cookies.

    Args:
        url (str): The URL to request.
        headers (dict, optional): The request headers. Defaults to None.
        cookies (dict, optional): The cookies to include in the request. Defaults to None.

    Returns:
        dict: The JSON response, or None if an error occurs.
    """
    try:
        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e},please cookie settings")
        return None


def make_bili_get_call(url, params=None):
    response = make_bilibili_get_request(url, headers=DEFAULT_HEADERS, cookies=DEFAULT_COOKIES, params=params)
    return response


## 3. 获取aid-cid
def get_aid_cid(bvid: str):
    """
    first step: get aid/cid
    :param bvid:
    :return:
    """
    response_data = make_bilibili_get_request(view_url.format(bvid=bvid), headers=DEFAULT_HEADERS,
                                              cookies=DEFAULT_COOKIES)
    # Print the response
    if response_data:
        print(response_data)
        try:
            return response_data['data']['aid'], response_data['data']['cid']
        except Exception as e:
            print(f'{bvid} is not found')
            return 0, 0
    else:
        print("Request failed.")
        return 0, 0


# 4. 下载单个视频
def download_video(bv_url, output_dir):
    """下载单个视频"""
    print(f"正在下载：{bv_url}")
    download_command = ['you-get', '-o', output_dir, bv_url]
    try:
        result = subprocess.run(download_command, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"下载成功：{bv_url}")
            print(result.stdout)
        else:
            print(f"下载失败：{bv_url}")
            print(result.stderr)
    except Exception as e:
        print(f"下载过程中发生错误：{bv_url}")
        print(f"错误信息：{e}")


# 5. 使用多线程批量下载视频
def download_videos(bv_list, worker_num=5, output_dir='./'):
    """使用多线程批量下载视频"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with ThreadPoolExecutor(max_workers=worker_num) as executor:
        for bv_url in bv_list:
            executor.submit(download_video, bv_url, output_dir)


@dataclass
class BVMetaData:
    bv_id: str
    aid: str
    cid: str
    title: str
    pub_date: str
    bv_url: str
    video_status: bool = False
    subtitle_status: bool = False

    def file_name(self):
        # clean_title = re.sub(r'[【】\[\]（）\(\)\/\\]', '', self.title)
        clean_title = self.title
        if self.pub_date:
            return "-".join([self.pub_date, self.bv_id, clean_title]).replace(" ", "")
        else:
            return "-".join([self.bv_id, clean_title]).replace(" ", "")


def download_and_rename_video(bv_meta: BVMetaData, output_dir):
    """下载单个视频"""
    bv_url = bv_meta.bv_url
    print(f"正在下载：{bv_url}")
    file_name = bv_meta.file_name()
    # download_command = ['you-get', '-o', output_dir, "-O", file_name, bv_url]
    download_command = ['you-get', '-o', output_dir, bv_url]
    try:
        result = subprocess.run(download_command, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"下载成功：{bv_url}")
            print(result.stdout)
            bv_meta.video_status = True
        else:
            print(f"下载失败：{bv_url}")
            print(result.stderr)
            bv_meta.video_status = False
    except Exception as e:
        print(f"下载过程中发生错误：{bv_url}")
        print(f"错误信息：{e}")
        bv_meta.video_status = False
    return bv_meta


def get_bv_meta(bv_url: str):
    bv_id = extract_bvid(bv_url)
    response_data = make_bilibili_get_request(view_url.format(bvid=bv_id), headers=DEFAULT_HEADERS,
                                              cookies=DEFAULT_COOKIES)

    try:
        return BVMetaData(
            bv_id=bv_id,
            aid=response_data['data']['aid'],
            cid=response_data['data']['cid'],
            title=response_data['data']['title'],
            pub_date=datetime.fromtimestamp(response_data['data']['pubdate']).strftime("%Y-%m-%d"),
            bv_url=bv_url
        )
    except Exception as e:
        print(f"获取{bv_id} 相关信息失败,检查Cookie是否过期", e)


# 6.组织文件
def organize_files(output_dir, bv_meta_mapping: Dict):
    """根据文件特征移动文件"""
    video_folder = os.path.join(output_dir, "视频")
    danmu_folder = os.path.join(output_dir, "弹幕")
    subtitle_folder = os.path.join(output_dir, "字幕")  # 新增字幕文件夹

    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    if not os.path.exists(danmu_folder):
        os.makedirs(danmu_folder)
    if not os.path.exists(subtitle_folder):
        os.makedirs(subtitle_folder)

    for file_name in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file_name)
        if os.path.isfile(file_path):
            if file_name.endswith(".mp4"):
                title_name = file_name.replace(".mp4", "")
                bv_meta = bv_meta_mapping.get(title_name.replace(" ", ""), None)
                if bv_meta:
                    shutil.move(file_path, os.path.join(video_folder, bv_meta.file_name() + ".mp4"))
                print(f"移动文件：{file_name} -> 【视频】文件夹")
            elif file_name.endswith(".cmt.xml"):
                title_name = file_name.replace(".cmt.xml", "")
                bv_meta = bv_meta_mapping.get(title_name.replace(" ", ""), None)
                if bv_meta:
                    shutil.move(file_path, os.path.join(danmu_folder, bv_meta.file_name() + ".cmt.xml"))
                print(f"移动文件：{file_name} -> 【弹幕】文件夹")


# 提取弹幕文件中的中文汉字
def extract_chinese_characters(danmu_folder, output_text_folder):
    """提取弹幕文件中的中文汉字"""
    if not os.path.exists(output_text_folder):
        os.makedirs(output_text_folder)

    for file_name in os.listdir(danmu_folder):
        if file_name.endswith(".cmt.xml"):
            file_path = os.path.join(danmu_folder, file_name)
            chinese_text = extract_chinese_from_xml(file_path)
            output_file_path = os.path.join(output_text_folder, f"{os.path.splitext(file_name)[0]}.txt")
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write("\n".join(chinese_text))
            print(f"提取中文内容并保存到：{output_file_path}")


# 从弹幕文件中提取中文字符
def extract_chinese_from_xml(file_path):
    """从弹幕文件中提取中文字符"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        chinese_characters = []
        for element in root.findall(".//d"):  # 假设弹幕内容在<d>标签中
            text = element.text
            if text:
                chinese_text = re.findall(r'[\u4e00-\u9fff]+', text)  # 使用正则表达式提取中文字符
                chinese_characters.extend(chinese_text)
        return chinese_characters
    except Exception as e:
        print(f"解析文件时发生错误：{file_path}")
        print(f"错误信息：{e}")
        return []


# 限制弹幕文件中的弹幕数量
def limit_danmu_count(danmu_folder, max_danmu_count=2000):
    """限制弹幕文件中的弹幕数量"""
    for file_name in os.listdir(danmu_folder):
        if file_name.endswith(".cmt.xml"):
            file_path = os.path.join(danmu_folder, file_name)
            limit_danmu_in_file(file_path, max_danmu_count)


# 限制单个弹幕文件中的弹幕数量
def limit_danmu_in_file(file_path, max_danmu_count):
    """限制单个弹幕文件中的弹幕数量"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        danmu_elements = root.findall(".//d")  # 假设弹幕内容在<d>标签中
        if len(danmu_elements) > max_danmu_count:
            for element in danmu_elements[max_danmu_count:]:
                root.remove(element)
            tree.write(file_path, encoding='utf-8', xml_declaration=True)
            print(f"限制弹幕数量：{file_path} -> 保留 {max_danmu_count} 条弹幕")
    except Exception as e:
        print(f"处理文件时发生错误：{file_path}")
        print(f"错误信息：{e}")


# 将视频文件拆分为无声视频和音频
def split_video_to_audio_and_silent_video(video_folder, output_folder):
    """
    将视频文件拆分为无声视频和音频文件
    :param video_folder: 包含视频文件的文件夹路径
    :param output_folder: 输出文件夹路径
    """
    silent_video_folder = os.path.join(output_folder, "无声视频")
    audio_folder = os.path.join(output_folder, "音频")

    # 创建输出文件夹
    if not os.path.exists(silent_video_folder):
        os.makedirs(silent_video_folder)
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    # 遍历视频文件夹中的所有视频文件
    for video_file in os.listdir(video_folder):
        if video_file.endswith(".mp4"):
            video_path = os.path.join(video_folder, video_file)
            base_name = os.path.splitext(video_file)[0]

            # 输出文件路径
            silent_video_output = os.path.join(silent_video_folder, f"{base_name}_无声.mp4")
            audio_output = os.path.join(audio_folder, f"{base_name}.mp3")

            # 使用ffmpeg提取无声视频
            silent_video_command = [
                "ffmpeg", "-i", video_path, "-c:v", "copy", "-an", silent_video_output
            ]
            subprocess.run(silent_video_command, capture_output=True)

            # 使用ffmpeg提取音频
            audio_command = [
                "ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_output
            ]
            subprocess.run(audio_command, capture_output=True)

            print(f"处理完成：{video_file} -> 无声视频：{silent_video_output}，音频：{audio_output}")


def get_subtitles(aid: str, cid: str):
    """
    获取subtitle
    :return:
    """
    params = {
        # 'aid': '1803768206',
        # 'cid': '1523511798',
        'aid': aid,
        'cid': cid
    }
    response_data = make_bilibili_get_request(wbi_url, headers=DEFAULT_HEADERS, cookies=DEFAULT_COOKIES, params=params)
    if response_data:
        print(response_data)
        try:
            return response_data['data']['subtitle']['subtitles'][0]['subtitle_url']
        except Exception as e:
            return None

    else:
        print("Request failed.")
        return None


def download_subtitles(bv_meta: BVMetaData, subtitle_folder: str):
    subtitle_path = get_subtitles(aid=bv_meta.aid, cid=bv_meta.cid)  #
    if subtitle_path:
        res = make_bili_get_call(url="https:" + subtitle_path)
        print(res)
        subtitles = res['body']
        convert_to_srt(subtitles, os.path.join(subtitle_folder, bv_meta.file_name() + '.srt'))
        bv_meta.subtitle_status = True
    else:
        print(f"{bv_meta.bv_id} has no subtitles")
        bv_meta.subtitle_status = False
    return bv_meta


## 转化为字幕文件
def convert_to_srt(json_data, output_file="output.srt"):
    """Converts JSON data to SRT format and saves it to a file."""
    srt_content = ""
    for i, entry in enumerate(json_data):
        # start_time = format_time(entry['from'])
        # end_time = format_time(entry['to'])
        content = entry['content']
        # srt_content += f"{i + 1}\n{start_time} --> {end_time}\n{content}\n\n"
        srt_content += f"{content}\n"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(srt_content)


def format_time(seconds):
    """Converts seconds to SRT time format (HH:MM:SS,MS)."""
    milliseconds = int(seconds * 1000)
    hours = milliseconds // (3600 * 1000)
    milliseconds %= (3600 * 1000)
    minutes = milliseconds // (60 * 1000)
    milliseconds %= (60 * 1000)
    seconds = milliseconds // 1000
    milliseconds %= 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


import csv


# Add this function to write metadata to CSV
def write_metadata_to_csv(bv_metas, file_path: str):
    """
    Write BV metadata to a CSV file
    :param bv_metas: List of BVMetaData objects
    :param file_path: file path
    """
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['bv_id', 'title', 'video_download_status', 'subtitle_download_status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for meta in bv_metas:
            writer.writerow({
                'bv_id': meta.bv_id,
                'title': meta.title,
                'video_download_status': meta.video_status,
                'subtitle_download_status': meta.subtitle_status
            })
    print(f"Metadata written to {file_path}")


def downloads_all_videos(bv_metas, output_directory: str):
    with ThreadPoolExecutor(max_workers=5) as executor:
        for bv_meta in bv_metas:
            executor.submit(download_and_rename_video, bv_meta, output_directory)


if __name__ == '__main__':
    current_path = os.getcwd()
    ## 修改bvlist位置
    bvlist_path = current_path + "/bvlist.txt"
    ## 修改保存位置
    output_directory = "./output"
    danmu_output_text_folder = os.path.join(output_directory, "弹幕文本")
    danmu_folder = os.path.join(output_directory, "弹幕")
    video_folder = os.path.join(output_directory, "视频")  # 视频文件夹路径
    subtitle_folder = os.path.join(output_directory, "字幕")

    bv_urls = read_bv_list(bvlist_path)
    print(bv_urls)
    bv_metas = []
    bv_metas_mapping = {}
    # download_videos(bv_list=bv_urls, output_dir=output_directory)

    # Get all metadata first
    for bv_url in bv_urls:
        bv_meta = get_bv_meta(bv_url)
        if bv_meta:
            bv_metas.append(bv_meta)
            bv_metas_mapping[bv_meta.title.replace(" ", "")] = bv_meta
    downloads_all_videos(bv_metas, output_directory)

    organize_files(output_directory, bv_meta_mapping=bv_metas_mapping)
    extract_chinese_characters(danmu_folder, danmu_output_text_folder)
    limit_danmu_count(danmu_folder, max_danmu_count=2000)

    for bv_meta in bv_metas:
        download_subtitles(bv_meta, subtitle_folder)
    split_video_to_audio_and_silent_video(video_folder, output_directory)

    write_metadata_to_csv(bv_metas, output_directory + f"/{int(time.time())}_download_result.csv")
