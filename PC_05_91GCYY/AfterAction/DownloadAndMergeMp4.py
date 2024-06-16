import concurrent
import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from A_08_m3u8.M3u8ToMp4 import M3u8ToMp4
from PC_00_Common.LogUtil.LogUtil import async_log, com_log

DIR_OUTPUT = os.path.join(os.getcwd(), '../OutputData_main_A')


for cache_name in os.listdir(DIR_OUTPUT):
    path_item = os.path.join(DIR_OUTPUT, cache_name)
    if os.path.isdir(path_item) and re.match(r'[\d]+', cache_name):
        dir_m3u8 = os.path.join(path_item, 'M3U8_ca49e0_ADD_KEY_URI')
        m3u8_files_without_mp4 = []
        m3u8_files_with_mp4 = []
        m3u8_files = []
        mp4_files = []
        list_mp4_name = []
        if os.path.isdir(dir_m3u8):
            dir_path = Path(dir_m3u8)
            # 获取指定目录下所有的 .m3u8 文件
            m3u8_files = [m3u8_file for m3u8_file in dir_path.glob('*.m3u8')]
            # 获取指定目录下所有的 .mp4 文件
            mp4_files = dir_path.glob('*.mp4')
            list_mp4_name = [mp4_file.stem for mp4_file in mp4_files]

            for m3u8_file in m3u8_files:
                if m3u8_file.stem in list_mp4_name:
                    m3u8_files_with_mp4.append(m3u8_file)
                else:
                    m3u8_files_without_mp4.append(m3u8_file)
        print(cache_name, len(m3u8_files), len(list_mp4_name), len(m3u8_files_with_mp4), len(m3u8_files_without_mp4))
        if len(m3u8_files_without_mp4)>0:
            m3u8_to_mp4 = M3u8ToMp4()

            # 使用ThreadPoolExecutor来并行处理M3u8文件
            with ThreadPoolExecutor(max_workers=10) as executor:  # 可根据实际情况调整max_workers的数量
                futures = {executor.submit(m3u8_to_mp4.download_and_merge_by_m3u8_file, m3u8_file, async_log) for m3u8_file in
                           m3u8_files_without_mp4}
                # 收集所有完成的Future对象的结果（可选，根据需要处理结果或异常）
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        com_log.info(f'Task completed with result: {result}')
                    except Exception as exc:
                        com_log.error(f'Task generated an exception: {exc}')

