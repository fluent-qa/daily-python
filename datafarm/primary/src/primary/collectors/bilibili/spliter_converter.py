import os
import subprocess


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


if __name__ == '__main__':
    output_directory = "./output"
    video_folder = os.path.join(output_directory, "视频")  # 视频文件夹路径
    split_video_to_audio_and_silent_video(video_folder, output_directory)
