import glob
import os
import re
import shutil
from pathlib import Path

DIR_OUTPUT = os.path.join(os.getcwd(), '../OutputData_main_jxs')

list_cache_dir = []
for item in os.listdir(DIR_OUTPUT):
    path_item = os.path.join(DIR_OUTPUT, item)
    if os.path.isdir(path_item) and re.match(r'[\d]+', item):
        list_cache_dir.append(path_item)



for dir_cache in list_cache_dir:
    dir_m3u8 = os.path.join(dir_cache, 'M3U8_ca49e0_ADD_KEY_URI')
    m3u8_files_without_mp4 = []
    m3u8_files_with_mp4 = []
    m3u8_files = []
    mp4_files = []
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
    print(dir_cache, len(m3u8_files), len(list_mp4_name), len(m3u8_files_with_mp4), len(m3u8_files_without_mp4))