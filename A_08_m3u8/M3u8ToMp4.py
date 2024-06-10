import re
import sys

from Crypto.Cipher import AES
import os
import requests


class M3u8ToMp4:
    def __init__(self, session):
        self.session = session

    # def download_and_merge_by_m3u8_url(self, url_m3u8):
    #     m3u8_content = session.get(url_m3u8).text

    def download_and_merge_by_m3u8_file(self, path_m3u8_file):
        # 获取文件的目录和文件名
        dir_m3u8, m3u8_file_name = os.path.split(path_m3u8_file)
        # 去除文件名的扩展名
        m3u8_file_base_name, _ = os.path.splitext(m3u8_file_name)
        # 构造新文件夹的路径
        path_m3u8_cache = os.path.join(dir_m3u8, m3u8_file_base_name)
        os.makedirs(path_m3u8_cache, exist_ok=True)

        with open(path_m3u8_file, 'r') as f:
            m3u8_content = f.read()

        """从M3U8文件中提取密钥URL"""
        match_key_url = re.search(r'URI="([^"]+)"', m3u8_content)
        print(match_key_url)
        url_key = match_key_url.group(1) if match_key_url else None
        path_key = None
        if url_key:
            path_key = os.path.join(path_m3u8_cache, f'{m3u8_file_base_name}.key')
            res_get_key = self.session.get(url_key)
            if res_get_key.status_code == 200:
                with open(path_key, 'wb') as f:
                    f.write(res_get_key.content)

        list_ts_url = re.findall(r'(http[s]?://[^\s"]+\.ts)', m3u8_content)
        print(list_ts_url)
        list_decrypted_ts_path = []
        for idx, url_ts in enumerate(list_ts_url):
            # 直接保存为解密后的文件，不保留未解密的版本
            ts_output_path = os.path.join(path_m3u8_cache, f'decrypted_ts_{idx}.ts')
            list_decrypted_ts_path.append(ts_output_path)
            self.__download_and_decrypt_ts(url_ts, path_key, ts_output_path)
        path_mp4 = os.path.join(path_m3u8_cache, f'{m3u8_file_base_name}.mp4')
        self.__merge_decrypted_ts_to_mp4(list_decrypted_ts_path, path_mp4)

    def __download_and_decrypt_ts(self, url_ts, path_key, output_path, iv=None):
        """直接在内存中下载并使用给定的密钥解密TS数据，然后保存为文件"""
        with open(path_key, 'rb') as file_key:
            key = file_key.read()
        response = self.session.get(url_ts, stream=True)
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

    def __merge_decrypted_ts_to_mp4(self, list_ts_file_path, output_filename):
        """使用ffmpeg将解密后的TS文件合并为MP4"""
        cmd = f"ffmpeg -i \"concat:{'|'.join(list_ts_file_path)}\" -c copy \"{output_filename}\""
        os.system(cmd)


if __name__ == "__main__":
    path_app = os.path.split(os.path.abspath(sys.argv[0]))[0]
    path_m3u8_file = os.path.join(path_app, 'OutputData', '4158 (1).m3u8')

    HEADERS = {
        'cookie': 'PHPSESSID=943253905816fb8f3cefa8808d77feb2; isWelcomeTipsNoShow=1',
        'referer': 'https://nqkh.judoegg.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    session = requests.Session()
    session.headers = HEADERS
    session.cookies.set('existmag', 'all')
    session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=50))

    m3u8_to_mp4 = M3u8ToMp4(session)
    m3u8_to_mp4.download_and_merge_by_m3u8_file(path_m3u8_file)
