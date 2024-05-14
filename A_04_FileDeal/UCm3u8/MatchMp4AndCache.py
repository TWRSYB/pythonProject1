import os

from A_05_ADB.ADB import get_item_list_from_android_dir, create_directory_on_device, copy_file_on_device, \
    move_file_on_device

dir_mp4 = input(f'请输入mp4文件所在目录:')

listdir_mp4 = os.listdir(dir_mp4)

mp4_list = []

for item in listdir_mp4:
    if os.path.isfile(os.path.join(dir_mp4, item)) and item.endswith(f'.mp4'):
        mp4_list.append(item)

print(f'扫描到 {len(mp4_list)} 个mp4文件: {mp4_list}')


dir_cache = input(f'请输入cache所在目录:')

listdir_cache = get_item_list_from_android_dir(dir_cache)

cache_list = []

for item in listdir_cache:
    if item[1]:
        cache_list.append(item[0])

print(f'扫描到 {len(cache_list)} 个缓存文件夹: {cache_list}')

matched_cache_list = []
for mp4 in mp4_list:
    for cache in cache_list:
        if f'{mp4.removesuffix(".mp4")}.m3u8_contents' == cache:
            matched_cache_list.append(cache)

print(f'匹配到 {len(matched_cache_list)} 个缓存: {matched_cache_list}')


if len(matched_cache_list) > 0:
    dir_target = input(f'输入要剪切的目标目录:')
    create_result = create_directory_on_device(dir_target)
    print(create_result[1])
    for matched_cache in matched_cache_list:
        move_file_on_device(f'{dir_cache}/{matched_cache}', dir_target)
