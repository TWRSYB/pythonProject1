import json
import os
import re
import shutil
from datetime import datetime

import pandas
import requests
from lxml import etree

from A_07_Utils.ExcelUtils import format_excel_text
from PC_00_Common.LogUtil.LogUtil import process_log
from PC_00_Common.ReqUtil.ReqUtil import ReqUtil
from PC_00_Common.ReqUtil.SavePicUtil import SavePicUtil
from PC_00_Common.XpathUtil.XpathUtil import xpath_util
from PC_05_91GCYY.Config import HEADERS, URL_HOST, FILE_JSON_ALL_CATEGORY, FILE_JSON_CURRENT_CATEGORY, \
    FILE_EXCEL_CURRENT_CATEGORY, DIR_OUTPUT, FILE_EXCEL_ALL_CATEGORY

session = requests.Session()
session.headers = HEADERS
session.cookies.set('existmag', 'all')
session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=50))

save_pic_util = SavePicUtil(session=session)
req_util = ReqUtil(session=session)


class Category:

    def __init__(self, category_code: str, category_name: str, href: str, super_category_code: str = '',
                 page_count: int = 0, list_sub_category_code: list = None) -> None:
        super().__init__()
        self.category_code = category_code
        self.category_name = category_name
        self.href = href
        self.super_category_code = super_category_code
        self.page_count = page_count
        self.list_sub_category_code = list_sub_category_code

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    def get_name(self):
        return f'{self.category_code}_-_{self.category_name}_-_{self.super_category_code}'


class Executor:
    def __init__(self):
        self.list_category: [Category] = []
        self.list_all_json = []

    def start(self):

        # 读取现有JSON文件中的数据
        if os.path.isfile(FILE_JSON_ALL_CATEGORY):
            with open(FILE_JSON_ALL_CATEGORY, 'r', encoding='utf-8') as json_file:
                self.list_all_json = json.load(json_file)

        res_home_page = req_util.try_get_req_times(url=f'{URL_HOST}')
        if not res_home_page.status_code:
            return
        etree_res_home_page = etree.HTML(res_home_page.text)  # 初始化生成一个XPath解析对象
        list_category_home = etree_res_home_page.xpath('//div/ul/li/a[contains(@href,"/category")]')
        for category_home in list_category_home:
            href = xpath_util.get_unique(category_home, './@href')
            category_code = href.replace('/category/', '')
            category_name = xpath_util.get_unique(category_home, './text()')
            category = Category(category_code, category_name, href)
            self.list_category.append(category)
            self.get_sub_category(category)
        self.save_data()

    def get_sub_category(self, category):
        res_category = req_util.try_get_req_times(url=f'{URL_HOST}/category/{category.category_code}')
        if not res_category.status_code:
            return
        etree_res_category = etree.HTML(res_category.text)  # 初始化生成一个XPath解析对象
        page_count = 0
        list_sub_category_item = etree_res_category.xpath(
            '//div[contains(@class,"home-tab")]/div[contains(@class,"mb15")]')
        if len(list_sub_category_item) > 0:
            category.list_sub_category_code = []
            for sub_category_item in list_sub_category_item:
                href = xpath_util.get_unique(sub_category_item, './a/@href')
                category_code = href.replace('/category/', '')
                category_name = xpath_util.get_unique(sub_category_item, './div/text()')
                sub_category = Category(category_code, category_name, href, super_category_code=category.category_code,
                                        page_count=page_count)
                category.list_sub_category_code.append(category_code)
                self.list_category.append(sub_category)
                self.get_sub_category(sub_category)
        else:
            list_page_bar_item = etree_res_category.xpath('//div[contains(@class,"pagebar")]/li/*/text()')
            page_count = 1
            if len(list_page_bar_item) > 0:
                page_count = max(
                    [int(page_bar_item) for page_bar_item in list_page_bar_item if re.match(r'\d+', page_bar_item)])
            category.page_count = page_count
            category.list_sub_category_code = None

    # 保存到 Excel 和 Json 中
    def save_data(self, list_category=None):
        list_category = list_category or self.list_category
        # 保存 Json 文件 ↓↓↓
        # 输出本次 Json 文件 ↓↓↓
        with open(FILE_JSON_CURRENT_CATEGORY, 'w', encoding='utf-8') as f:
            json.dump([category.__dict__ for category in list_category], f, ensure_ascii=False, indent=4)
        process_log.process3(f'输出本次Json成功: {FILE_JSON_CURRENT_CATEGORY}')
        # 输出本次 Json 文件 ↑↑↑

        # 将本次数据合并到现有 Json 中 ↓↓↓
        existing_serialized = set()  # 创建一个空集合，用于存放已存在数据的序列化字符串

        for item in self.list_all_json:  # 将现有数据的每个字典序列化为字符串，并加入到集合中
            serialized_item = json.dumps(item, sort_keys=True)
            existing_serialized.add(serialized_item)

        unique_new_json_list = []
        for item in [category.__dict__ for category in list_category]:  # 遍历新数据，仅保留不在已存在数据中的字典
            serialized_item = json.dumps(item, sort_keys=True)
            if serialized_item not in existing_serialized:
                unique_new_json_list.append(item)

        self.list_all_json = self.list_all_json + unique_new_json_list  # 将新数据追加到现有数据中
        with open(FILE_JSON_ALL_CATEGORY, "w", encoding='utf-8') as json_file:
            json.dump(self.list_all_json, json_file, indent=4)  # 将合并后的数据写回JSON文件, indent 参数可选，用于美化输出（增加缩进）
        process_log.process3(f'输出所有Json成功: {FILE_JSON_ALL_CATEGORY}')
        # 将本次数据合并到现有 Json 中 ↑↑↑
        # 保存 Json 文件 ↑↑↑

        # 保存 Excel 文件 ↓↓↓
        # 输出本次 Excel 文件 ↓↓↓
        df = pandas.DataFrame(([category.__dict__ for category in list_category])).astype(
            str)  # 将列表转换为 DataFrame , 格式为 str , 避免 Excel 以数字和科学计数法显示
        df.to_excel(FILE_EXCEL_CURRENT_CATEGORY, index=False)  # 将DataFrame保存到Excel文件, index=False表示不保存行索引到Excel文件
        format_excel_text(FILE_EXCEL_CURRENT_CATEGORY)
        process_log.process3(f'输出本次Excel成功: {FILE_EXCEL_CURRENT_CATEGORY}')
        # 输出本次 Excel 文件 ↑↑↑

        # 输出所有 Excel 文件 ↓↓↓
        df = pandas.DataFrame(self.list_all_json).astype(str)  # 将列表转换为 DataFrame , 格式为 str , 避免 Excel 以数字和科学计数法显示
        df.to_excel(FILE_EXCEL_ALL_CATEGORY, index=False)  # 将DataFrame保存到Excel文件, index=False表示不保存行索引到Excel文件
        format_excel_text(FILE_EXCEL_ALL_CATEGORY)
        process_log.process3(f'输出所有Excel成功: {FILE_EXCEL_ALL_CATEGORY}')
        # 输出所有 Excel 文件 ↑↑↑
        # 保存 Excel 文件 ↑↑↑

        # 备份数据 ↓↓↓
        backup_folder_name = os.path.join(DIR_OUTPUT, 'CATEGORY',
                                          f'Backup_{datetime.now().strftime("%Y-%m-%d_%H%M%S")}')
        os.makedirs(backup_folder_name)
        shutil.copy2(FILE_JSON_CURRENT_CATEGORY, backup_folder_name)
        shutil.copy2(FILE_JSON_ALL_CATEGORY, backup_folder_name)
        shutil.copy2(FILE_EXCEL_CURRENT_CATEGORY, backup_folder_name)
        shutil.copy2(FILE_EXCEL_ALL_CATEGORY, backup_folder_name)
        # 备份数据 ↑↑↑


if __name__ == '__main__':
    Executor().start()
