import libtorrent as lt

def get_torrent_info_hash(torrent_path):
    info = lt.torrent_info(torrent_path)
    return info.info_hash().to_string()

# 示例使用
torrent_path = 'your_torrent_file.torrent'
info_hash = get_torrent_info_hash(torrent_path)
print(f"Torrent 文件的 info_hash 是: {info_hash}")