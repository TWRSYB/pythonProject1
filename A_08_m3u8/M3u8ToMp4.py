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
    def __init__(self, path_m3u8_file: str, dir_cache: str = '', session=None, log=com_log):
        """
        创建 M3u8ToMp4 对象
        :param path_m3u8_file: m3u8文件目录
        :param dir_cache: 缓存目录
        :param session: session
        """
        self.path_m3u8_file = path_m3u8_file
        self.dir_cache = dir_cache or os.path.join(os.getcwd(), 'OutputData',
                                                   f'cache_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        # 获取 m3u8 的目录和文件名
        self.dir_m3u8, self.m3u8_file_name = os.path.split(path_m3u8_file)
        # 获取 m3u8 文件名
        self.m3u8_file_base_name, _ = os.path.splitext(self.m3u8_file_name)
        # 构造缓存文件夹
        self.path_m3u8_cache = os.path.join(self.dir_cache, self.m3u8_file_base_name)
        if "'" in self.path_m3u8_cache:
            print(type(self.path_m3u8_cache))
            self.path_m3u8_cache = self.path_m3u8_cache.replace("'", '_SPC13_')
            print(self.path_m3u8_cache)
        os.makedirs(self.path_m3u8_cache, exist_ok=True)
        self.txt_list_ts = os.path.join(self.path_m3u8_cache, 'list_ts.txt')
        self.key = None
        self.list_decrypted_ts_path = []
        # if os.path.exists(self.path_m3u8_cache):
        #     self.path_m3u8_cache = f'{self.path_m3u8_cache}_EXIST_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
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
        self.log = log

    # def download_and_merge_by_m3u8_url(self, url_m3u8):
    #     m3u8_content = session.get(url_m3u8).text

    def download_and_merge_by_m3u8_file(self) -> (bool, str):

        with open(self.path_m3u8_file, 'r') as f:
            m3u8_content = f.read()

        # 获取 key ↓↓↓
        match_key_url = re.search(r'URI="([^"]+)"', m3u8_content)
        url_key = match_key_url.group(1) if match_key_url else None
        if url_key:
            self.log.info(f'获取key start: {url_key}')
            path_key = os.path.join(self.path_m3u8_cache, f'{self.m3u8_file_base_name}.key')
            res_get_key = self.req_util.try_get_req_times(url_key, msg=f'获取key')
            if not res_get_key:
                self.log.error(f'获取key 失败: {self.path_m3u8_file}')
                return False, f'获取key 失败: {self.path_m3u8_file}'
            with open(path_key, 'wb') as f:
                f.write(res_get_key.content)
            with open(path_key, 'rb') as file_key:
                self.key = file_key.read()
            self.log.info(f'获取key end: {self.key}')
        # 获取 key ↑↑↑

        # 下载 ts 文件并使用线程池并发处理 ↓↓↓
        self.log.info(f'下载 ts start: {self.m3u8_file_base_name}')

        list_ts_url = re.findall(r'(https?://[^\s"]+\.ts)', m3u8_content)
        with ThreadPoolExecutor(max_workers=20) as executor:  # 你可以根据实际情况调整线程数量
            set_future = set()
            for idx, url_ts in enumerate(list_ts_url):
                ts_output_path = os.path.join(self.path_m3u8_cache, f'decrypted_ts_{str(idx).zfill(6)}.ts')
                self.list_decrypted_ts_path.append(ts_output_path)
                try:
                    self.log.info(f'添加 ts 下载任务 第 {idx + 1} 个 for {self.m3u8_file_base_name}')
                    set_future.add(
                        executor.submit(self.__download_and_decrypt_ts, url_ts, self.key, ts_output_path, executor,
                                        None))
                except RuntimeError as e:
                    self.log.error(f'添加 ts 下载任务 第 {idx + 1} 个出现异常: {e} for {self.m3u8_file_base_name}')

            # 等待所有下载和解密任务完成
            for future in concurrent.futures.as_completed(set_future):
                self.log.info(f'得到 ts 下载任务结果 {future.result()} for {self.m3u8_file_base_name}')
                if not future.result()[0]:
                    self.log.error(f'下载 ts 失败: {future.result()}')
                    return False, f'下载 ts 失败: {self.m3u8_file_base_name}'
        with open(self.txt_list_ts, 'w', encoding='utf-8') as f:
            for ts_file in self.list_decrypted_ts_path:
                f.write(f"file '{ts_file}'\n")
        self.log.info(f'下载 ts end: {self.m3u8_file_base_name}')
        # 下载 ts 文件并使用线程池并发处理 ↑↑↑

        # 合并为 mp4 ↓↓↓
        self.log.info(f'合并为 mp4 start: {self.m3u8_file_base_name}')
        return self.merge_mp4()

        # 合并为 mp4 ↑↑↑

    def merge_mp4(self) -> (bool, str):

        # print(self.path_m3u8_cache)

        path_mp4 = os.path.join(self.dir_m3u8, f'{self.m3u8_file_base_name}.mp4')
        if os.path.exists(path_mp4):
            path_mp4 = os.path.join(self.dir_m3u8,
                                    f'{self.m3u8_file_base_name}_EXIST_{datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4')
        # 使用ffmpeg将解密后的TS文件合并为MP4，通过subprocess模块提高安全性及控制能力
        # cmd = f'ffmpeg -y -f concat -safe 0 -i "{self.txt_list_ts}" -c copy "{path_mp4}"'
        # print(cmd)
        # os.system(cmd)
        # with open(self.txt_list_ts, 'r', encoding='utf-8') as f:
        #     lines = f.readlines()
        #
        # lines = [line.strip() for line in lines]
        # print(lines)
        # cmd = f"ffmpeg -y -i \"concat:{'|'.join(lines)}\" -c copy \"{path_mp4}\""
        # print(cmd)
        # os.system(cmd)
        cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', self.txt_list_ts, '-c', 'copy', path_mp4]
        print(cmd)
        try:
            subprocess.run(cmd, check=True)  # check=True会让调用抛出异常如果命令执行失败
            self.log.info(f'合并为 mp4 成功: {path_mp4}')
            result = True, f'合并为 mp4 完成: {self.m3u8_file_base_name}'
        except subprocess.CalledProcessError as e:
            self.log.error(f'合并为 mp4 异常: {path_mp4}, 异常: {e}')
            result = False, f'合并为 mp4 异常: {path_mp4}, 异常: {e}'
        return result

    def __download_and_decrypt_ts(self, url_ts, key, output_path, executor: ThreadPoolExecutor, iv=None) -> (bool, str):
        """
        下载并解密 ts 文件
        :param url_ts: url
        :param key: key密钥
        :param output_path: 输出路径
        :param iv: 偏移量
        :return: ts下载结果
        """
        res_get_ts = self.req_util.try_get_req_times(url_ts, stream=True, msg=f'下载 ts文件: {output_path}')
        if not res_get_ts:
            self.log.error(f'有下载 ts 失败, 关闭线程池, url: {url_ts}, output_path: {output_path}')
            executor.shutdown(wait=False, cancel_futures=True)
            return False, output_path
        # 读取加密的数据
        print(res_get_ts.status_code, res_get_ts)
        encrypted_data = res_get_ts.raw.read()
        # 初始化AES解密器
        cipher = AES.new(key, AES.MODE_CBC)
        # 解密数据
        decrypted_data = cipher.decrypt(encrypted_data)
        # 写入到输出目录
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
            self.log.info(f'下载 ts 成功并写入了文件, output_path: {output_path}')
        return True, output_path


def main1(m3u8_files):
    set_future = set()
    # 使用ThreadPoolExecutor来并行处理M3u8文件
    with ThreadPoolExecutor(max_workers=10) as executor:  # 可根据实际情况调整max_workers的数量
        for m3u8_file in m3u8_files:
            # m3u8_to_mp4 = M3u8ToMp4(path_m3u8_file=m3u8_file, dir_cache=os.path.join(os.getcwd(), 'OutputData',
            #                                                                          f'test'))
            # future = executor.submit(m3u8_to_mp4.download_and_merge_by_m3u8_file)
            m3u8_to_mp4 = M3u8ToMp4(path_m3u8_file=m3u8_file, dir_cache=os.path.join(os.getcwd(), 'OutputData',
                                                   f'test'))
            future = executor.submit(m3u8_to_mp4.merge_mp4())
            set_future.add(future)

        # 收集所有完成的Future对象的结果（可选，根据需要处理结果或异常）
        for future in concurrent.futures.as_completed(set_future):
            print(future)
            try:
                result = future.result()
                print(f"Task completed with result: {result}")
            except Exception as exc:
                print(f"Task generated an exception: {exc}")


def main2(m3u8_files):
    for m3u8_file in m3u8_files:
        m3u8_to_mp4 = M3u8ToMp4(m3u8_file, dir_cache='')
        m3u8_to_mp4.download_and_merge_by_m3u8_file()


if __name__ == "__main__":
    start_time = time.time()  # 程序开始前记录时间
    path_app = os.path.split(os.path.abspath(sys.argv[0]))[0]
    m3u8_files = [
        # os.path.join(path_app, 'OutputData',
        #              '3038_-_6月资源106_-_大会员_-_46df68048a67b9fd7bdcaa472eca9ecc523f2d4eca49e0.m3u8'),
        # os.path.join(path_app, 'OutputData',
        #              '3042_-_6月资源109_-_大会员_-_46df68048a67b9fd7bdca6472eca9ecc523f2d4eca49e0.m3u8'),
        os.path.join(path_app, 'OutputData',
                     "18366_-_[中文字幕]SSIS-392 Let's Do Menes 三上悠亚 zh1_-_大会员_-_46df68048a67b9fe79dfa8472eca9ecc523f2d4eca49e0.m3u8"),
        # os.path.join(path_app, 'OutputData',
        #              "18366_-_SSIS_-_大会员_-_46df68048a67b9fe79dfa8472eca9ecc523f2d4eca49e0.m3u8"),
        # os.path.join(path_app, 'OutputData',
        #              "18366_-_SSIS-392 Do Menes 三上悠亚 zh1_-_大会员_-_46df68048a67b9fe79dfa8472eca9ecc523f2d4eca49e0.m3u8"),
        # os.path.join(path_app, 'OutputData',
        #              "18366_-_[中文字幕]SSIS-392 Do Menes 三上悠亚 zh1_-_大会员_-_46df68048a67b9fe79dfa8472eca9ecc523f2d4eca49e0.m3u8"),
        # os.path.join(path_app, 'OutputData', '4158  (1).m3u8'),
    ]
    main1(m3u8_files)
    end_time = time.time()  # 程序结束后记录时间
    print(f"程序执行时间: {end_time - start_time}秒")
