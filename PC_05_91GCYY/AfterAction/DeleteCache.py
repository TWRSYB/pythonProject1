import os
import re
import shutil

DIR_OUTPUT = os.path.join(os.getcwd(), '../OutputData_main_A')

list_cache_dir = []
for item in os.listdir(DIR_OUTPUT):
    path_item = os.path.join(DIR_OUTPUT, item)
    if os.path.isdir(path_item) and re.match(r'[\d]+', item):
        list_cache_dir.append(path_item)

for dir_cache in list_cache_dir:
    for item in os.listdir(dir_cache):
        if item.startswith('Backup_'):
            shutil.rmtree(os.path.join(dir_cache, item))
        if item == 'M3U8' or item == 'M3U8_ca49e0':
            shutil.rmtree(os.path.join(dir_cache, item))
