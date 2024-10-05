import json
import os
from datetime import datetime

from PC_01_PIC.hitxhot.hitxhot_套图下载 import download_gallery

if __name__ == '__main__':
    path_output = './OutputData'

    # 原始JSON文件名
    original_json_file = f'{path_output}/任务列表.json'

    # 临时JSON文件名
    temp_json_file = f'{path_output}/任务列表_处理中.json'

    # 读取原始JSON文件
    with open(original_json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # print(data)
    # print(type(data))

    # 准备一个空列表用于写入临时文件
    temp_data = []

    # 处理数据并写入临时文件
    for item in data:
        if isinstance(item, dict):
            if item.get("status") == 1:
                temp_data.append(item)
            else:
                gallery = download_gallery(item)
                temp_data.append(gallery)
        elif isinstance(item, str):
            gallery = download_gallery({'key': item})
            temp_data.append(gallery)

        # 将处理后的item写入到临时文件
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            json.dump(temp_data, f, ensure_ascii=False, indent=4)
    # 在所有元素都处理完毕后，可以将临时文件重命名为原始文件名（如果需要）
    backup_json_file = f'{original_json_file}{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    print(backup_json_file)
    os.rename(original_json_file, backup_json_file)  # 先删除原始文件（注意：这可能会丢失数据，请谨慎操作）
    os.rename(temp_json_file, original_json_file)  # 重命名临时文件为原始文件名