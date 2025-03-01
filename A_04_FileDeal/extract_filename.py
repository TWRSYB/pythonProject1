import os

def extract_filename(path: str) -> str:
    """提取路径中的文件名（兼容跨平台和末尾斜杠）"""
    normalized_path = os.path.normpath(path)
    filename = os.path.basename(normalized_path)
    return filename if filename else None  # 处理空结果

# # 示例
# path1 = "D:/docs/example.txt"
# path2 = "https://example.com/path/file.torrent?param=123"
# path3 = "/var/log/app/"
#
# print(extract_filename(path1))  # 输出: example.txt
# print(extract_filename(path2))  # 输出: file.torrent
# print(extract_filename(path3))  # 输出: app