import concurrent
import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from A_08_m3u8.M3u8ToMp4 import M3u8ToMp4
from PC_00_Common.LogUtil import LogUtil
from PC_00_Common.LogUtil.LogUtil import async_log, com_log


class DownloadAndMergeMp4:
    def __init__(self, dir_output_data):
        self.dir_output_data = dir_output_data

    def download_and_merge_mp4(self, process_level: int = 2):
        list_cache = []
        for item in os.listdir(self.dir_output_data):
            if os.path.isdir(os.path.join(self.dir_output_data, item)) and re.match(r'\d+', item):
                list_cache.append(item)
        for index, cache_name in enumerate(list_cache):
            order = index + 1
            if LogUtil.set_process(process_level, order):
                LogUtil.process_log.process_skip(process_level, msg='扫描缓存', order=order, obj=cache_name)
                continue
            LogUtil.process_log.process_start(process_level, msg='扫描缓存', order=order, obj=cache_name)
            self.analyse_cache_and_download(cache_name, process_level + 1)
            LogUtil.process_log.process_end(process_level, msg='扫描缓存', order=order, obj=cache_name)

    def analyse_cache_and_download(self, cache_name, process_level):
        dir_m3u8 = os.path.join(self.dir_output_data, cache_name, 'M3U8_ca49e0_ADD_KEY_URI')
        LogUtil.set_process(process_level, order=1)
        if os.path.isdir(dir_m3u8):
            LogUtil.process_log.process(process_level, '缓存有m3u8文件夹', obj=cache_name)
            m3u8_files_without_mp4 = []
            m3u8_files_with_mp4 = []
            Path_m3u8 = Path(dir_m3u8)
            # 获取指定目录下所有的 .m3u8 文件
            m3u8_files = [m3u8_file for m3u8_file in Path_m3u8.glob('*.m3u8')]
            # 获取指定目录下所有的 .mp4 文件
            list_mp4_name = [mp4_file.stem for mp4_file in Path_m3u8.glob('*.mp4')]

            for m3u8_file in m3u8_files:
                if m3u8_file.stem in list_mp4_name:
                    m3u8_files_with_mp4.append(m3u8_file)
                else:
                    m3u8_files_without_mp4.append(m3u8_file)
            LogUtil.process_log.process(process_level,
                                        f'缓存{cache_name}扫描结果: m3u8数量={len(m3u8_files)}, mp4数量={len(list_mp4_name)}'
                                        f', 有mp4的m3u8数量={len(m3u8_files_with_mp4)}, 没有mp4的m3u8数量={len(m3u8_files_without_mp4)}')
            if len(m3u8_files_without_mp4) > 0:
                # 使用ThreadPoolExecutor来并行处理M3u8文件
                set_future = set()
                with ThreadPoolExecutor(max_workers=3) as executor:  # 可根据实际情况调整max_workers的数量
                    for i, m3u8_file in enumerate(m3u8_files_without_mp4):
                        m3u8_to_mp4 = M3u8ToMp4(path_m3u8_file=m3u8_file,
                                                dir_cache=os.path.join(os.getcwd(), 'OutputData', cache_name),
                                                log=async_log)
                        future = executor.submit(m3u8_to_mp4.download_and_merge_by_m3u8_file)
                        set_future.add(future)
                # 收集所有完成的Future对象的结果（可选，根据需要处理结果或异常）
                for future in concurrent.futures.as_completed(set_future):
                    LogUtil.process_log.process(process_level + 1, f'得到 下载并合并 结果 {future.result()}')
                    try:
                        result = future.result()
                        if result[0]:
                            com_log.info(f'下载并合并完成, 执行结果: {result}')
                        else:
                            com_log.error(f'下载并合并 失败: {future.result()}')
                    except Exception as exc:
                        com_log.error(f'下载并合并遇到异常, 异常: {exc}')
        else:
            LogUtil.process_log.process(process_level, '缓存没有m3u8文件夹', obj=cache_name)


if __name__ == '__main__':
    mp_ = DownloadAndMergeMp4(os.path.join(os.getcwd(), '../OutputData_main_A'))
    mp_.download_and_merge_mp4(2)
