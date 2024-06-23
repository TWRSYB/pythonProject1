import os
import re
from pathlib import Path

DIR_OUTPUT = os.path.join(os.getcwd(), '../OutputData_main_A')

list_m3u8_contain_ = []

for cache_name in os.listdir(DIR_OUTPUT):
    path_item = os.path.join(DIR_OUTPUT, cache_name)
    if os.path.isdir(path_item) and re.match(r'\d+', cache_name):
        # print(cache_name)
        dir_m3u8 = os.path.join(path_item, 'M3U8_ca49e0_ADD_KEY_URI')
        if os.path.isdir(dir_m3u8):
            dir_path = Path(dir_m3u8)
            # 获取指定目录下所有的 .m3u8 文件
            list_m3u8_name = [m3u8_file.stem for m3u8_file in dir_path.glob('*.m3u8')]
            for m3u8_name in list_m3u8_name:
                # print(m3u8_name)
                if "'" in m3u8_name:
                    print(m3u8_name)
