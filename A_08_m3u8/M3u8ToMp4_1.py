import os
import subprocess
import requests
from m3u8 import M3U8


# def download_m3u8_and_key(key_url, output_folder):
#     key_response = requests.get(key_url)
#     with open(os.path.join(output_folder, 'key.bin'), 'wb') as f:
#         f.write(key_response.content)


def download_ts_segments(m3u8_path, output_folder):
    # 直接读取本地的.m3u8文件内容
    with open(m3u8_path, 'r') as f:
        m3u8_content = f.read()

        # 解析m3u8内容
    m3u8_obj = M3U8(m3u8_content)

    # 确保输出目录存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历所有的.ts片段并下载
    for segment in m3u8_obj.segments:
        # 构建完整的.ts文件URL（如果.m3u8文件中有绝对URL）
        # 或者直接使用相对路径（如果.m3u8文件中的是相对路径）
        ts_url = segment.uri  # 这里假设.m3u8中的URL是相对于某个基准URL的，或者已经是本地文件路径
        # 如果是相对于某个基准URL的，你可能需要拼接它：base_url + segment.uri

        # 将URL（或路径）转换为本地文件名
        filename = os.path.join(output_folder, ts_url.split('/')[-1])

        # 下载.ts文件
        with requests.get(ts_url, stream=True) as r:  # 注意：这里假设ts_url是一个有效的URL或文件路径
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)


def decrypt_and_merge_with_ffmpeg(ts_folder, key_path, iv=None, output_mp4='output.mp4'):
    """使用ffmpeg解密并合并.ts文件为MP4"""
    ts_files = [os.path.join(ts_folder, f) for f in os.listdir(ts_folder) if f.endswith('.ts')]
    ts_files.sort()

    # 注意：以下命令行示例假设ffmpeg能够直接使用秘钥和IV（如果提供）
    # 实际上，ffmpeg直接处理AES-128加密的.ts文件可能需要特定的指令和配置
    cmd = [
        'ffmpeg',
        '-allowed_extensions', 'ALL',
        '-i', 'playlist.m3u8',  # 假定在同一个目录下
        '-method', 'AES-128',
        '-decryption_key', key_path,
    ]
    if iv:
        cmd.extend(['-decryption_iv', iv])
    cmd.extend([
        '-c', 'copy',
        output_mp4
    ])

    subprocess.run(cmd, check=True)  # 执行ffmpeg命令


def main():
    m3u8_path = r'D:\15.Development Projects\06.pachon\pythonProject1\PC_05_91GCYY\OutputData\M3U8\3038_-_6月资源106_-_大会员_-_46df68048a67b9fd7bdcaa472eca9ecc523f2d4eca4be0.m3u8'
    output_folder = r'D:\15.Development Projects\06.pachon\pythonProject1\PC_05_91GCYY\OutputData\temp'
    output_mp4 = 'output.mp4'
    key_url = f'https://g1hs.nestokra.com/sec'  # 如果秘钥不是直接在.m3u8中，则需要单独的URL

    os.makedirs(output_folder, exist_ok=True)
    # download_m3u8_and_key(key_url, output_folder)
    download_ts_segments(m3u8_path, output_folder)

    # 假设秘钥文件名和位置已知
    key_path = os.path.join(output_folder, 'key.bin')
    decrypt_and_merge_with_ffmpeg(output_folder, key_path, output_mp4)


if __name__ == '__main__':
    main()
