import json
import os
from pathlib import Path

from PC_00_Common.LogUtil import LogUtil
from PC_05_91GCYY.Config import FILE_JSON_ALL_CATEGORY
from PC_05_91GCYY.Executor import get_save_path_by_category_code
from PC_05_91GCYY.Vo.Category import Category


def change_host_for_m3u8(dir_m3u8, process_level):
    dir_m3u8_add_key_uri = f'{dir_m3u8}_ADD_KEY_URI'
    for index, file_m3u8 in enumerate(Path(dir_m3u8_add_key_uri).glob('*.m3u8')):
        LogUtil.set_process(process_level, index + 1)
        LogUtil.process_log.process_start(process_level, msg='为.m3u8更换域名', obj=file_m3u8, order=index + 1)

        # 读取文件内容
        content = file_m3u8.read_text()
        # 使用正则表达式替换内容
        # replaced_content = re.sub(r'eo.com.yangxingyue1.cn', f'ecn.eisjo.cn', content)
        replaced_content = content.replace(r'eo.com.yangxingyue1.cn', f'ecn.eisjo.cn')
        # 将修改后的内容写回到文件
        file_m3u8.write_text(replaced_content)

        LogUtil.process_log.process_end(process_level, msg='为.m3u8更换域名', obj=file_m3u8, order=index + 1)


class Changer:
    def __init__(self):
        self.list_category_json_all = []

        # 读取现有JSON文件中的数据
        if os.path.isfile(FILE_JSON_ALL_CATEGORY):
            with open(FILE_JSON_ALL_CATEGORY, 'r', encoding='utf-8') as json_file:
                self.list_category_json_all = json.load(json_file)

    def start(self, process_level: int = 2):
        LogUtil.set_process(process_level, 1)
        list_category = []
        LogUtil.process_log.process(process_level, f"扫描获取到分类数量: {len(self.list_category_json_all)}")
        for category_json in self.list_category_json_all:
            category = Category(category_code=category_json.get('category_code'),
                                category_name=category_json.get('category_name'), href=category_json.get('href'),
                                super_category_code=category_json.get('super_category_code'),
                                page_count=category_json.get('page_count'),
                                list_sub_category_code=category_json.get('list_sub_category_code'))
            list_category.append(category)

        LogUtil.set_process(process_level, 2)
        LogUtil.process_log.process_start(process_level, msg='批量修改域名')
        self.change_host_for_category_list(list_category, process_level + 1)
        LogUtil.process_log.process_end(process_level, msg='批量修改域名')

    def change_host_for_category_list(self, list_category, process_level):
        for index, category in enumerate(list_category):
            order = index + 1
            LogUtil.set_process(process_level, order)
            LogUtil.process_log.process_start(process_level, msg='分类批量修改域名', order=order, obj=category)
            if category.page_count:
                dir_save, dir_m3u8, dir_img = get_save_path_by_category_code(category.category_code)
                change_host_for_m3u8(dir_m3u8=dir_m3u8, process_level=process_level + 1)
            else:
                LogUtil.process_log.process(process_level, msg='分类没有影片', obj=category)
            LogUtil.process_log.process_end(process_level, msg='分类批量修改域名', order=order, obj=category)


if __name__ == '__main__':
    changer = Changer()
    changer.start()
