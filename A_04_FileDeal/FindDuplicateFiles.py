import os
import hashlib
from collections import defaultdict


def get_file_hash(file_path, hash_type='md5'):
    """
    计算文件的哈希值
    """
    if not os.path.isfile(file_path):
        return None
    hasher = hashlib.new(hash_type)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicate_files(directory):
    """
    在指定目录下查找重复文件
    """
    hashes = defaultdict(list)
    file_path_list = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            file_path_list.append(item_path)

    # print(f'扫描到{len(file_path_list)}个文件: {file_path_list}')

    # for root, dirs, files in os.walk(directory):
    #     for file in files:
    #         file_path_list.append(os.path.join(root, file))

    for file_path in file_path_list:
        hash_value = get_file_hash(file_path)
        if hash_value:
            hashes[hash_value].append(file_path)

    # print(f'文件的hashes: {hashes}')
    print(f'hash分组共{len(hashes)}组')

    duplicate_hashes = defaultdict(list)

    for hash_MD5, files in hashes.items():
        if len(files) > 1:
            duplicate_hashes[hash_MD5] = files

    # print(f'有重复文件的hash分组共{len(duplicate_hashes)}个')

    duplicates = [files for _, files in hashes.items() if len(files) > 1]
    # print(f'duplicates: {duplicates}')
    return duplicates


# 使用示例
directory = r'D:\15.Development Projects\06.pachon\pythonProject1\PC_05_91GCYY\OutputData01\M3U8'  # 替换为你的目录路径
duplicates = find_duplicate_files(directory)
# for dup_group in duplicates:
#     print(f"Duplicate files found with the same hash:")
#     for file_path in dup_group:
#         print(file_path)
#     print()
