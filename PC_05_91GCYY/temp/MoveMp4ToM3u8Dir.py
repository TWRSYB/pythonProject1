import os
import re
import shutil

DIR_OUTPUT = os.path.join(os.getcwd(), '../OutputData_main')

list_cache_dir = []
for item in os.listdir(DIR_OUTPUT):
    path_item = os.path.join(DIR_OUTPUT, item)
    if os.path.isdir(path_item) and re.match(r'[\d]+', item):
        list_cache_dir.append(path_item)

dir_mp4 = os.path.join(DIR_OUTPUT, 'Mp4_112_127')
list_mp4_path = []
for item in os.listdir(dir_mp4):
    list_mp4_path.append(os.path.join(dir_mp4, item))

for dir_cache in list_cache_dir:
    dir_m3u8 = os.path.join(dir_cache, 'M3U8_ca49e0_ADD_KEY_URI')
    if os.path.isdir(dir_m3u8):
        list_file_name = [os.path.splitext(item)[0] for item in os.listdir(dir_m3u8)]
        for path_mp4 in list_mp4_path:
            if os.path.splitext(os.path.basename(path_mp4))[0] in list_file_name:
                # 使用shutil.move移动文件
                shutil.move(path_mp4, dir_m3u8)
                list_mp4_path.remove(path_mp4)
