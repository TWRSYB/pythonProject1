import os

from A_05_ADB.ADB import get_item_list_from_android_dir, create_directory_on_device, copy_file_on_device, \
    move_file_on_device

dir_m3u8 = input(f'请输入m3u8文件所在目录:')

listdir_m3u8 = os.listdir(dir_m3u8)

m3u8_list = []

for item in listdir_m3u8:
    if os.path.isfile(os.path.join(dir_m3u8, item)) and item.endswith(f'.m3u8'):
        m3u8_list.append(item)

print(f'扫描到 {len(m3u8_list)} 个m3u8文件: {m3u8_list}')


dir_cache = input(f'请输入cache所在目录:')

listdir_cache = get_item_list_from_android_dir(dir_cache)

cache_list = []

for item in listdir_cache:
    if item[1]:
        cache_list.append(item[0])

print(f'扫描到 {len(cache_list)} 个缓存文件夹: {cache_list}')

matched_cache_list = []
for m3u8 in m3u8_list:
    for cache in cache_list:
        if f'{m3u8}_contents' == cache:
            matched_cache_list.append(cache)

print(f'匹配到 {len(matched_cache_list)} 个缓存: {matched_cache_list}')


if len(matched_cache_list) > 0:
    dir_target = input(f'输入要剪切的目标目录:')
    create_result = create_directory_on_device(dir_target)
    print(create_result[1])
    for matched_cache in matched_cache_list:
        move_file_on_device(f'{dir_cache}/{matched_cache}', dir_target)
