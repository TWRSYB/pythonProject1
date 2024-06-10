import re
import sys
from subprocess import Popen, PIPE

from Crypto.Cipher import AES
import os
import requests

path_app = os.path.split(os.path.abspath(sys.argv[0]))[0]
print(path_app)

HEADERS = {
    'cookie': 'PHPSESSID=943253905816fb8f3cefa8808d77feb2; isWelcomeTipsNoShow=1',
    'referer': 'https://nqkh.judoegg.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
session = requests.Session()
session.headers = HEADERS
session.cookies.set('existmag', 'all')
session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=50))


# def download_and_decrypt_ts(url, key, output_path, iv=None):
#     """直接在内存中下载并解密TS数据，然后保存为解密后的文件"""
#     response = session.get(url, stream=True)
#     if response.status_code == 200:
#         # 读取加密的数据
#         encrypted_data = response.raw.read()
#
#         # 初始化AES解密器
#         cipher = AES.new(key, AES.MODE_CBC, iv) if iv else AES.new(key, AES.MODE_ECB)
#
#         # 解密数据
#         decrypted_data = cipher.decrypt(encrypted_data)
#
#         # 注意：解密后可能需要去除PKCS7填充或其他填充，这里省略了该步骤
#
#         # 直接保存解密后的数据到文件
#         with open(output_path, 'wb') as f:
#             f.write(decrypted_data)
#     else:
#         print(f"Failed to download {url}")


def download_and_decrypt_ts(url_ts, path_key, output_path, iv=None):
    """直接在内存中下载并使用给定的密钥解密TS数据，然后保存为文件"""
    with open(path_key, 'rb') as file_key:
        key = file_key.read()
    response = session.get(url_ts, stream=True)
    if response.status_code == 200:
        # 读取加密的数据
        encrypted_data = response.raw.read()
        # 初始化AES解密器
        cipher = AES.new(key, AES.MODE_CBC)
        # 解密数据
        decrypted_data = cipher.decrypt(encrypted_data)

        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
    else:
        print(f"Failed to download {url_ts}")


def merge_decrypted_ts_to_mp4(ts_files, output_filename):
    print(output_filename)
    """使用ffmpeg将解密后的TS文件合并为MP4"""
    cmd = f"ffmpeg -i \"concat:{'|'.join(ts_files)}\" -c copy \"{output_filename}\""
    print(cmd)
    os.system(cmd)


# def main(m3u8_url, decryption_key, decryption_iv=None):
#     """主函数：下载并直接解密TS片段"""
#     m3u8_content = session.get(m3u8_url).text
#     ts_urls = re.findall(r'(http[s]?://[^\s"]+\.ts)', m3u8_content)
#
#     temp_dir = 'decrypted_ts_files'
#     os.makedirs(temp_dir, exist_ok=True)
#
#     decrypted_files = []
#     for idx, url in enumerate(ts_urls):
#         # 直接保存为解密后的文件，不保留未解密的版本
#         ts_output_path = os.path.join(temp_dir, f'decrypted_ts_{idx}.ts')
#         download_and_decrypt_ts(url, decryption_key, ts_output_path, decryption_iv)
#         decrypted_files.append(ts_output_path)
#
#     # 这里省略了合并解密后的TS文件为MP4的步骤，实际应用中可以使用ffmpeg等工具完成
#     print("Decrypted TS files are saved directly.")


def get_by_m3u8_file(path_m3u8_file):
    # 获取文件的目录和文件名
    dir_path, m3u8_file_name = os.path.split(path_m3u8_file)
    # 去除文件名的扩展名
    m3u8_file_base_name, _ = os.path.splitext(m3u8_file_name)
    # 构造新文件夹的路径
    path_m3u8_folder = os.path.join(dir_path, m3u8_file_base_name)
    os.makedirs(path_m3u8_folder, exist_ok=True)

    with open(path_m3u8_file, 'r') as f:
        m3u8_content = f.read()

    """从M3U8文件中提取密钥URL"""
    match_key_url = re.search(r'URI="([^"]+)"', m3u8_content)
    print(match_key_url)
    url_key = match_key_url.group(1) if match_key_url else None
    path_key = None
    if url_key:
        path_key = os.path.join(path_m3u8_folder, f'{m3u8_file_base_name}.key')
        res_get_key = session.get(url_key)
        if res_get_key.status_code == 200:
            with open(path_key, 'wb') as f:
                f.write(res_get_key.content)

    list_ts_url = re.findall(r'(http[s]?://[^\s"]+\.ts)', m3u8_content)
    print(list_ts_url)
    list_decrypted_ts_path = []
    for idx, url_ts in enumerate(list_ts_url):
        # 直接保存为解密后的文件，不保留未解密的版本
        ts_output_path = os.path.join(path_m3u8_folder, f'decrypted_ts_{idx}.ts')
        list_decrypted_ts_path.append(ts_output_path)
        # download_and_decrypt_ts(url_ts, path_key, ts_output_path)
    path_mp4 = os.path.join(path_m3u8_folder, f'{m3u8_file_base_name}.mp4')
    merge_decrypted_ts_to_mp4(list_decrypted_ts_path, path_mp4)


if __name__ == "__main__":
    # m3u8_url = 'YOUR_M3U8_URL_HERE'
    # decryption_key = b'YOUR_DECRYPTION_KEY_IN_BYTES'  # 密钥必须是字节类型
    # decryption_iv = b'YOUR_DECRYPTION_IV_IN_BYTES' if needed else None  # 可选的初始化向量
    # main(m3u8_url, decryption_key, decryption_iv)
    path_m3u8_file = r'D:\15.Development Projects\06.pachon\pythonProject1\PC_05_91GCYY\temp\test\4158 (1).m3u8'
    get_by_m3u8_file(path_m3u8_file)
