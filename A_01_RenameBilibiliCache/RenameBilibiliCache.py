import os


def start(path):
    # 确保给定的路径存在
    if not os.path.exists(path):
        print(f"路径 {path} 不存在")
        return

        # 确保给定的路径是一个目录
    if not os.path.isdir(path):
        print(f"{path} 不是一个目录")
        return

        # 列出指定目录下的所有文件和文件夹
    items = os.listdir(path)

    cache_list = []

    # 遍历这些文件和文件夹
    for item in items:
        if is_cache(item):
            cache_list.append(item)


def is_cache(item):
    item_path = os.path.join(cache_path, item)
    sub_list = os.listdir(item_path)
    if not os.path.isdir(item_path):
        print(f"子文件：{item} 不符合要求")
        return False
    if len(sub_list) != 1:
        print(f"子文件夹：{item} 不符合要求")
        return False
    if not os.path.isdir(os.path.join(item_path, sub_list[0])):
        print(f"子文件夹：{item} 不符合要求")
        return False
    if not os.path.isfile(os.path.join(item_path, sub_list[0], 'entry.json')):
        print(f"子文件夹：{item} 不符合要求")
        return False
    print(f"子文件夹：{item} 是符合要求的缓存目录")
    return True


cache_path = input('请输入缓存文件夹: ')

start(cache_path)
