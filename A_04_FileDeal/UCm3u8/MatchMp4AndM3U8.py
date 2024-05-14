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


dir_m3u8 = input(f'请输入m3u8所在目录:')

listdir_m3u8 = get_item_list_from_android_dir(dir_m3u8)

print(listdir_m3u8, len(listdir_m3u8))

m3u8_list = []

for item in listdir_m3u8:
    if not item[1] and item[0].endswith('.m3u8'):
        m3u8_list.append(item[0])

print(f'扫描到 {len(m3u8_list)} 个m3u8文件: {m3u8_list}')

matched_m3u8_list = []
for mp4 in mp4_list:
    for m3u8 in m3u8_list:
        if mp4.removesuffix('.mp4') == m3u8.removesuffix('.m3u8'):
            matched_m3u8_list.append(m3u8)

print(f'匹配到 {len(matched_m3u8_list)} 个m3u8文件: {matched_m3u8_list}')


if len(matched_m3u8_list) > 0:
    dir_target = input(f'输入要剪切的目标目录:')
    create_result = create_directory_on_device(dir_target)
    print(create_result[1])
    for matched_m3u8 in matched_m3u8_list:
        move_file_on_device(f'{dir_m3u8}/{matched_m3u8}', dir_target)
