import os
import random
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from primary.collectors.bilibili.downloader import *

current_path = os.getcwd()


def test_download_all():
    output_directory = "./output"
    danmu_output_text_folder = os.path.join(output_directory, "弹幕文本")
    video_folder = os.path.join(output_directory, "视频")  # 视频文件夹路径
    subtitle_folder = os.path.join(output_directory, "字幕")  # 字幕文件夹路径

    links = read_bv_list(current_path + "/bilibili/bvlist.txt")
    if links:
        download_videos(links, output_dir=output_directory)
        organize_files(output_directory)
        danmu_folder = os.path.join(output_directory, "弹幕")
        extract_chinese_characters(danmu_folder, danmu_output_text_folder)
        limit_danmu_count(danmu_folder, max_danmu_count=2000)
        # 拆分视频为无声视频和音频
        split_video_to_audio_and_silent_video(video_folder, output_directory)
    # 获取字幕
    for link in links:
        download_subtitles(link, subtitle_folder)


def test_time():
    print(int(time.time()))


def test_get_dict_get():
    dict_tmp = {"key": "value"}
    print(dict_tmp.get("k1", "k1"))


def status_code(id):
    time.sleep(random.choices([1, 0.5]))
    print(f'{id}')


def test_executor():
    for i in range(15):
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.submit(status_code, i)
