import requests
import os
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor
import shutil
import xml.etree.ElementTree as ET
import re


# 读取BV地址列表
def read_bv_list(file_path):
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


# 从网址中提取BV号
def extract_bvid(url):
    """从完整的视频网址中提取BV号"""
    if "BV" in url:
        return url.split("BV")[-1].split('/')[0]
    else:
        print(f"无法从网址中提取BV号：{url}")
        return None


# 获取视频的CID
def get_cid(bvid, cookies):
    """通过B站API获取视频的CID"""
    url = "https://api.bilibili.com/x/player/pagelist"
    params = {"bvid": bvid}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com"
    }
    try:
        response = requests.get(url, params=params, headers=headers, cookies=cookies)
        if response.status_code == 200:
            data = response.json()
            if data["code"] == 0 and data["data"]:
                return data["data"][0]["cid"]
            else:
                print(f"获取CID失败，返回数据：{data}")
        else:
            print(f"获取CID失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"获取CID时发生异常：{e}")
    time.sleep(1)  # 增加延时
    return None


# 获取字幕信息并保存
def download_subtitle(bvid, cid, subtitle_folder, cookies):
    """从B站API获取字幕并保存到指定文件夹"""
    url = "https://api.bilibili.com/x/player/v2"
    params = {"bvid": bvid, "cid": cid}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com"
    }
    try:
        response = requests.get(url, params=params, headers=headers, cookies=cookies)
        if response.status_code == 200:
            data = response.json()
            if data["code"] == 0 and data["data"] and data["data"]["subtitle"]["subtitles"]:
                subtitle_info = data["data"]["subtitle"]["subtitles"][0]
                subtitle_url = subtitle_info["subtitle_url"]
                # 修复字幕URL格式
                if subtitle_url and subtitle_url.startswith("//"):
                    subtitle_url = "https:" + subtitle_url
                if not subtitle_url:
                    print(f"该视频没有字幕：{bvid}")
                    return
                subtitle_response = requests.get(subtitle_url, headers=headers, cookies=cookies)
                if subtitle_response.status_code == 200:
                    subtitle_data = subtitle_response.json()
                    subtitle_text = "\n".join(
                        [f"{item['from']} --> {item['to']}\n{item['content']}" for item in subtitle_data["body"]])
                    subtitle_file_name = f"{bvid}.srt"
                    subtitle_file_path = os.path.join(subtitle_folder, subtitle_file_name)
                    with open(subtitle_file_path, "w", encoding="utf-8") as subtitle_file:
                        subtitle_file.write(subtitle_text)
                    print(f"字幕下载成功：{subtitle_file_path}")
                    return
            print(f"该视频没有字幕：{bvid}")
        else:
            print(f"获取字幕失败：{bvid}，状态码：{response.status_code}")
    except Exception as e:
        print(f"获取字幕时发生异常：{e}")


# 下载单个视频
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


# 使用多线程批量下载视频
def download_videos(bv_list, output_dir='./'):
    """使用多线程批量下载视频"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with ThreadPoolExecutor(max_workers=5) as executor:
        for bv_url in bv_list:
            executor.submit(download_video, bv_url, output_dir)


# 组织文件
def organize_files(output_dir):
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
                shutil.move(file_path, os.path.join(video_folder, file_name))
                print(f"移动文件：{file_name} -> 【视频】文件夹")
            elif file_name.endswith(".cmt.xml"):
                shutil.move(file_path, os.path.join(danmu_folder, file_name))
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


# 主程序
if __name__ == "__main__":
    SESSDATA = "d78e4cb6%2C1755522587%2Cca858%2A21CjCM2a73JEGf4wpzpdVyBvvNgfzajQRejeqGr1RKQFstqWKtZBjnKFAKggUgH64b1XkSVmM3b2ZTc2UwbGdyekJ3dlJ3cEFLUlBpRDZoVUFVNkY0MElkZm5xWnpmbEZ3dU5nWXlkZnJ2YUpfMVhwbDBOZFBrVEhoYXhtVEpENzY5RmVKTHRGd3JnIIEC"
    bili_jct = "e67d47c2a71839d890496d64358da983"
    buvid3 = "2513C173-2AF3-3AD4-DD56-79E79149FCE542129infoc"

    bv_list_file = r"C:\Users\KKK\Desktop\KJ\B站产品筹备\004技术抓取\000 B站\000H下载视频\000综合UP\079暮易House\BV.txt"
    output_directory = r"D:\八爪鱼下载\B站视频\000综合UP\079暮易House\全部视频"
    danmu_output_text_folder = os.path.join(output_directory, "弹幕文本")
    video_folder = os.path.join(output_directory, "视频")  # 视频文件夹路径
    subtitle_folder = os.path.join(output_directory, "字幕")  # 字幕文件夹路径

    # 读取BV地址列表并提取BV号
    bv_list = read_bv_list(bv_list_file)
    bvid_list = [extract_bvid(url) for url in bv_list if extract_bvid(url)]

    # 准备Cookie参数
    cookies = {
        "SESSDATA": SESSDATA,
        "bili_jct": bili_jct,
        "buvid3": buvid3
    }

    if bvid_list:
        download_videos(bv_list, output_dir=output_directory)
        organize_files(output_directory)
        danmu_folder = os.path.join(output_directory, "弹幕")
        extract_chinese_characters(danmu_folder, danmu_output_text_folder)
        limit_danmu_count(danmu_folder, max_danmu_count=2000)

        # 拆分视频为无声视频和音频
        split_video_to_audio_and_silent_video(video_folder, output_directory)

        # 下载字幕
        for bvid in bvid_list:
            cid = get_cid(bvid, cookies)
            if cid:
                download_subtitle(bvid, cid, subtitle_folder, cookies)
    else:
        print("BV地址列表为空，无法进行下载")
