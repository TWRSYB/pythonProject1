import concurrent
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from Crypto.Cipher import AES
import os
import requests

from PC_00_Common.LogUtil.LogUtil import com_log
from PC_00_Common.ReqUtil import ReqUtil


class M3u8ToMp4:
    def __init__(self, session=None):
        if not session:
            session = requests.Session()
            session.headers = {
                'cookie': 'PHPSESSID=943253905816fb8f3cefa8808d77feb2; isWelcomeTipsNoShow=1',
                'referer': 'https://nqkh.judoegg.com/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            }
            session.cookies.set('existmag', 'all')
            session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=100))
        self.req_util = ReqUtil.ReqUtil(session=session)
        self.dir_cache = os.path.join(os.getcwd(), 'OutputData', f'cache_{datetime.now().strftime("%Y%m%d_%H%M%S")}')

    # def download_and_merge_by_m3u8_url(self, url_m3u8):
    #     m3u8_content = session.get(url_m3u8).text

    def download_and_merge_by_m3u8_file(self, path_m3u8_file, log=com_log):
        # 获取 m3u8 的目录和文件名
        dir_m3u8, m3u8_file_name = os.path.split(path_m3u8_file)
        # 获取 m3u8 文件名
        m3u8_file_base_name, _ = os.path.splitext(m3u8_file_name)
        # 构造缓存文件夹
        path_m3u8_cache = os.path.join(self.dir_cache, m3u8_file_base_name)
        if os.path.exists(path_m3u8_cache):
            path_m3u8_cache = f'{path_m3u8_cache}_EXIST_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        os.makedirs(path_m3u8_cache)
        with open(path_m3u8_file, 'r') as f:
            m3u8_content = f.read()

        # 获取 key ↓↓↓
        key = None
        match_key_url = re.search(r'URI="([^"]+)"', m3u8_content)
        url_key = match_key_url.group(1) if match_key_url else None
        if url_key:
            log.info(f'获取key start: {url_key}')
            path_key = os.path.join(path_m3u8_cache, f'{m3u8_file_base_name}.key')
            res_get_key = self.req_util.try_get_req_times(url_key, msg=f'获取key')
            if not res_get_key:
                log.error(f'获取key 失败: {path_m3u8_file}')
                return
            with open(path_key, 'wb') as f:
                f.write(res_get_key.content)
            with open(path_key, 'rb') as file_key:
                key = file_key.read()
            log.info(f'获取key end: {key}')
        # 获取 key ↑↑↑

        # 下载 ts 文件并使用线程池并发处理 ↓↓↓
        log.info(f'下载 ts start: {path_m3u8_file}')
        list_decrypted_ts_path = []
        list_ts_url = re.findall(r'(http[s]?://[^\s"]+\.ts)', m3u8_content)
        with ThreadPoolExecutor(max_workers=20) as executor:  # 你可以根据实际情况调整线程数量
            futures = []
            for idx, url_ts in enumerate(list_ts_url):
                ts_output_path = os.path.join(path_m3u8_cache, f'decrypted_ts_{str(idx).zfill(6)}.ts')
                list_decrypted_ts_path.append(ts_output_path)
                futures.append(executor.submit(self.__download_and_decrypt_ts, url_ts, key, ts_output_path))

            # 等待所有下载和解密任务完成
            for future in concurrent.futures.as_completed(futures):
                print(future.result(), future.__dict__)
                if not future.result():
                    log.error(f'下载 ts 失败: {path_m3u8_file}')
                    return

        # print(list_ts_url)
        # list_decrypted_ts_path = []
        # for idx, url_ts in enumerate(list_ts_url):
        #     ts_output_path = os.path.join(path_m3u8_cache, f'decrypted_ts_{str(idx).zfill(6)}.ts')
        #     list_decrypted_ts_path.append(ts_output_path)
        #     result_download_ts = self.__download_and_decrypt_ts(url_ts, key, ts_output_path)
        #     if not result_download_ts:
        #         return
        log.info(f'下载 ts end: {path_m3u8_file}')
        # 下载 ts 文件并使用线程池并发处理 ↑↑↑

        # 合并为 mp4 ↓↓↓
        log.info(f'合并为 mp4 start: {path_m3u8_file}')
        txt_list_ts = os.path.join(path_m3u8_cache, 'list_ts.txt')
        with open(txt_list_ts, 'w', encoding='utf-8') as f:
            for ts_file in list_decrypted_ts_path:
                f.write(f"file '{ts_file}'\n")
        path_mp4 = os.path.join(dir_m3u8, f'{m3u8_file_base_name}.mp4')
        if os.path.exists(path_mp4):
            path_mp4 = os.path.join(dir_m3u8,
                                    f'{m3u8_file_base_name}_EXIST_{datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4')
        self.__merge_decrypted_ts_to_mp4(txt_list_ts, path_mp4, log=log)
        log.info(f'合并为 mp4 end: {path_m3u8_file}')
        return True
        # 合并为 mp4 ↑↑↑

    def __download_and_decrypt_ts(self, url_ts, key, output_path, iv=None) -> bool:
        """
        下载并解密 ts 文件
        :param url_ts: url
        :param key: key密钥
        :param output_path: 输出路径
        :param iv: 偏移量
        :return: ts下载结果
        """
        res_get_ts = self.req_util.try_get_req_times(url_ts, stream=True, msg=f'下载 ts文件')
        if not res_get_ts:
            return False
        # 读取加密的数据
        encrypted_data = res_get_ts.raw.read()
        # 初始化AES解密器
        cipher = AES.new(key, AES.MODE_CBC)
        # 解密数据
        decrypted_data = cipher.decrypt(encrypted_data)
        # 写入到输出目录
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        return True

    # def __merge_decrypted_ts_to_mp4(self, list_ts_file_path, output_filename):
    #     """使用ffmpeg将解密后的TS文件合并为MP4"""
    #     cmd = f"ffmpeg -y -i \"concat:{'|'.join(list_ts_file_path)}\" -c copy \"{output_filename}\""
    #     os.system(cmd)

    # def __merge_decrypted_ts_to_mp4(self, txt_list_ts, output_filename):
    #     """使用ffmpeg将解密后的TS文件合并为MP4，使用-f concat安全文件列表选项"""
    #     cmd = f'ffmpeg -y -f concat -safe 0 -i "{txt_list_ts}" -c copy "{output_filename}"'
    #     os.system(cmd)

    def __merge_decrypted_ts_to_mp4(self, txt_list_ts, output_filename, log=com_log):
        """使用ffmpeg将解密后的TS文件合并为MP4，通过subprocess模块提高安全性及控制能力"""
        cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', txt_list_ts, '-c', 'copy', output_filename]
        try:
            subprocess.run(cmd, check=True)  # check=True会让调用抛出异常如果命令执行失败
            log.info(f'合并为 mp4 成功: {output_filename}')
        except subprocess.CalledProcessError as e:
            log.error(f'合并为 mp4 异常: {output_filename}, 异常: {e}')


def main1():
    path_app = os.path.split(os.path.abspath(sys.argv[0]))[0]
    m3u8_files = [
        os.path.join(path_app, 'OutputData',
                     '3038_-_6月资源106_-_大会员_-_46df68048a67b9fd7bdcaa472eca9ecc523f2d4eca49e0.m3u8'),
        os.path.join(path_app, 'OutputData',
                     '3042_-_6月资源109_-_大会员_-_46df68048a67b9fd7bdca6472eca9ecc523f2d4eca49e0.m3u8'),
        os.path.join(path_app, 'OutputData', '4158  (1).m3u8'),
    ]

    m3u8_to_mp4 = M3u8ToMp4()

    # 使用ThreadPoolExecutor来并行处理M3u8文件
    with ThreadPoolExecutor(max_workers=10) as executor:  # 可根据实际情况调整max_workers的数量
        futures = {executor.submit(m3u8_to_mp4.download_and_merge_by_m3u8_file, m3u8_file) for m3u8_file in m3u8_files}

        # 收集所有完成的Future对象的结果（可选，根据需要处理结果或异常）
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(f"Task completed with result: {result}")
            except Exception as exc:
                print(f"Task generated an exception: {exc}")


def main2():
    path_app = os.path.split(os.path.abspath(sys.argv[0]))[0]
    m3u8_files = [
        os.path.join(path_app, 'OutputData',
                     '3038_-_6月资源106_-_大会员_-_46df68048a67b9fd7bdcaa472eca9ecc523f2d4eca49e0.m3u8'),
        os.path.join(path_app, 'OutputData',
                     '3042_-_6月资源109_-_大会员_-_46df68048a67b9fd7bdca6472eca9ecc523f2d4eca49e0.m3u8'),
        os.path.join(path_app, 'OutputData', '4158  (1).m3u8'),
    ]
    m3u8_to_mp4 = M3u8ToMp4()
    for m3u8_file in m3u8_files:
        m3u8_to_mp4.download_and_merge_by_m3u8_file(m3u8_file)


if __name__ == "__main__":
    start_time = time.time()  # 程序开始前记录时间
    main1()
    end_time = time.time()  # 程序结束后记录时间
    print(f"程序执行时间: {end_time - start_time}秒")
