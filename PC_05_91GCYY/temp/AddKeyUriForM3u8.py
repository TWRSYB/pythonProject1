import os

dir_m3u8 = r'D:\15.Development Projects\06.pachon\pythonProject1\PC_05_91GCYY\OutputData\M3U8'
dir_m3u8_add_key_uri = r'D:\15.Development Projects\06.pachon\pythonProject1\PC_05_91GCYY\OutputData\M3U8_ADD_KEYURI'

import re


def replace_text_in_file(input_file_path, output_file_path):
    """
    使用正则表达式替换文件中的文本并保存为新文件。

    :param input_file_path: 原始文件的路径
    :param output_file_path: 新文件的保存路径
    :param pattern: 正则表达式模式，用于匹配需要替换的文本
    :param replacement: 替换后的文本
    """
    # 读取原文件内容
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    print(content)
    # 使用正则表达式替换文本
    replaced_content = re.sub(r'#EXT-X-KEY:METHOD=AES-128,URI=".+"',
                              '#EXT-X-KEY:METHOD=AES-128,URI="https://g1hs.nestokra.com/sec"', content)

    print(replaced_content)

    # 另存为新文件
    with open(output_file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(replaced_content)


listdir = os.listdir(dir_m3u8)
for item in listdir:
    path_item = os.path.join(dir_m3u8, item)
    if os.path.isfile(path_item) and item.endswith('.m3u8'):
        replace_text_in_file(path_item, os.path.join(dir_m3u8_add_key_uri, item))
        # with open(path_item, 'r', encoding='utf-8') as file:
        #     content = file.read()
        # print(content)
        # # 使用正则表达式替换文本
        # replaced_content = re.sub(r'#EXT-X-KEY:METHOD=AES-128,URI=".+"', '#EXT-X-KEY:METHOD=AES-128,URI="https://g1hs.nestokra.com/sec"', content)
        #
        # print(replaced_content)