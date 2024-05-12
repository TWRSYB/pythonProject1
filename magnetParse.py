import time

import libtorrent as lt

def get_torrent_file_list(magnet_hash):
    # 创建一个会话对象
    ses = lt.session()

    # 从磁力链接获取元数据
    params = {
        'save_path': '.',  # 下载保存路径，这里仅用于获取元数据，可随意指定
        'storage_mode': lt.storage_mode_t(2),  # 使用只读模式，因为我们不打算下载文件
    }
    handle = lt.add_magnet_uri(ses, magnet_hash, params)

    # 等待元数据下载完成
    while (not handle.has_metadata()):
        time.sleep(1)

    # 解析元数据
    torrent_info = handle.get_torrent_info()
    files = torrent_info.files()

    # 提取文件列表
    file_list = [(f.path, f.size) for f in files]

    return file_list

# 使用已知的磁力链接哈希值
magnet_hash = "这里是您的磁力链接哈希值"

file_list = get_torrent_file_list(magnet_hash)
for file_path, file_size in file_list:
    print(f"{file_path} - {file_size} bytes")