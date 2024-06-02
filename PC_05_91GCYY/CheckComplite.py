import json
import os
import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import pandas
import requests
from lxml import etree

from A_04_FileDeal.FileNameValidate import validate, correct_name
from A_07_Utils.ExcelUtils import format_excel_text
from PC_00_Common.LogUtil import LogUtil
from PC_00_Common.ReqUtil import SavePicUtil
from PC_00_Common.XpathUtil.XpathUtil import xpath_util

from PC_05_91GCYY.Config import URL_HOST, DIR_M3U8, DIR_IMG, FILE_JSON_CURRENT, FILE_JSON_ALL, FILE_EXCEL_CURRENT, \
    FILE_EXCEL_ALL, DIR_OUTPUT, HEADERS, FILE_JSON_ALL_CATEGORY, DIR_CATEGORY, FILE_JSON_CURRENT_CATEGORY, \
    FILE_EXCEL_CURRENT_CATEGORY, FILE_EXCEL_ALL_CATEGORY

# 创建session对象
from PC_00_Common.ReqUtil import ReqUtil
from PC_05_91GCYY.Vo.Category import Category
from PC_05_91GCYY.Vo.CheckResult import CheckResult

session = requests.Session()
session.headers = HEADERS
session.cookies.set('existmag', 'all')
session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=50))

save_pic_util = SavePicUtil.SavePicUtil(session=session)
req_util = ReqUtil.ReqUtil(session=session)


class Checker:
    def __init__(self):
        self.list_category_json_all = []
        self.list_json_all = []
        self.list_check_result: [CheckResult] = []
        # 将影片按分类进行分类
        self.group_dict_video = defaultdict(list)
        # 汇总不同分类下的serno集合
        self.group_dict_serno = defaultdict(set)
        # 读取现有JSON文件中的数据
        if os.path.isfile(FILE_JSON_ALL):
            with open(FILE_JSON_ALL, 'r', encoding='utf-8') as json_file:
                self.list_json_all = json.load(json_file)

        # 读取现有JSON文件中的数据
        if os.path.isfile(FILE_JSON_ALL_CATEGORY):
            with open(FILE_JSON_ALL_CATEGORY, 'r', encoding='utf-8') as json_file:
                self.list_category_json_all = json.load(json_file)

    def start(self, process_level: int = 2):
        LogUtil.set_process(process_level, 1)
        list_category = []
        LogUtil.process_log.process(process_level, f"扫描获取到分类数量: {len(self.list_category_json_all)}")
        LogUtil.process_log.process(process_level, f"扫描获取到影片数量: {len(self.list_json_all)}")
        for category_json in self.list_category_json_all:
            category = Category(category_code=category_json.get('category_code'),
                                category_name=category_json.get('category_name'), href=category_json.get('href'),
                                super_category_code=category_json.get('super_category_code'),
                                page_count=category_json.get('page_count'),
                                list_sub_category_code=category_json.get('list_sub_category_code'))
            list_category.append(category)
        # 将影片进行分类
        for video_json in self.list_json_all:
            self.group_dict_video[video_json.get('category')].append(video_json)
        LogUtil.process_log.process(process_level, f"影片已分类: 数量={len(self.group_dict_video)}")

        LogUtil.set_process(process_level, 2)
        LogUtil.process_log.process_start(process_level, msg='第一次检查分类列表')
        list_check_result = self.check_category_list(list_category, process_level + 1)
        list_check_result_duplicate = [check_result for check_result in list_check_result if check_result.is_check and not check_result.is_no_duplicate]
        LogUtil.process_log.process_end(process_level, msg=f'第一次检查, 因为重复而缺失的检查结果有 {len(list_check_result_duplicate)} 个: {list_check_result_duplicate}')
        LogUtil.process_log.process_end(process_level, msg='第一次检查分类列表')

        LogUtil.set_process(process_level, 3)
        if len(list_check_result_duplicate) > 0:
            LogUtil.process_log.process_start(process_level, msg='有需要补全的数据')
            LogUtil.process_log.process_start(process_level, msg='补全数据')
            self.complete_data(list_check_result_duplicate, process_level + 1)
            LogUtil.process_log.process_end(process_level, msg='补全数据')
            # LogUtil.set_process(process_level, 4)
            # LogUtil.process_log.process_start(process_level, msg='第2次检查分类列表')
            # list_check_result = self.check_category_list(list_category, process_level + 1)
            # list_check_result_duplicate = [check_result for check_result in list_check_result if
            #                                check_result.is_check and not check_result.is_no_duplicate]
            # LogUtil.process_log.process_end(process_level,
            #                                 msg=f'第2次检查, 因为重复而缺失的检查结果有 {len(list_check_result_duplicate)} 个: {list_check_result_duplicate}')
            # LogUtil.process_log.process_end(process_level, msg='第2次检查分类列表')
        else:
            LogUtil.process_log.process_start(process_level, msg='没有需要补全的数据')

        # 检查不同分类之间是否有重复
        LogUtil.set_process(process_level, 4)
        count_fk = 0
        set_merge = set()
        for category_code, set_video_category_serno in self.group_dict_serno.items():
            count_fk += len(set_video_category_serno)
            set_merge.update(set_video_category_serno)
        LogUtil.process_log.process(process_level, msg=f'不同分类之间重复数量: {count_fk - len(set_merge)}')

    def complete_data(self, list_check_result, process_level):
        from PC_05_91GCYY import executor
        for index, check_result in enumerate(list_check_result):
            order = index + 1
            LogUtil.set_process(process_level, order)
            LogUtil.process_log.process_start(process_level, msg='补全分类', order=order, obj=check_result)
            if check_result.is_check:
                if not check_result.is_no_duplicate:
                    list_serno_maybe_lost = []
                    set_serno = self.group_dict_serno[check_result.category.category_code]
                    set_serno_int = [int(serno) for serno in set_serno]
                    max_serno = max(set_serno_int)
                    min_serno = min(set_serno_int)
                    for serno in range(min_serno - check_result.count_diff, max_serno + 1 + check_result.count_diff):
                        if serno not in set_serno_int:
                            list_serno_maybe_lost.append(serno)
                    if len(list_serno_maybe_lost) > 0:
                        LogUtil.process_log.process(process_level,
                                                    msg=f'分类 {check_result.category} 缺失 {check_result.count_diff} 个, '
                                                        f'可能得缺失列表: {list_serno_maybe_lost}')
                        list_task = executor.get_video_by_list_serno(list_serno_maybe_lost,
                                                                     category_code=check_result.category.category_code,
                                                                     process_level=process_level)

                        LogUtil.process_log.process(process_level,
                                                    msg=f'分类 {check_result.category} 缺失 {check_result.count_diff} 个, '
                                                        f'补全 {len(list_task)} 个, 补全列表: {list_task}')
                else:
                    LogUtil.process_log.process(process_level, msg='分类没有重复, 无需补全', obj=check_result)
            else:
                LogUtil.process_log.process(process_level, msg='分类没有数据, 无需补全', obj=check_result)
            LogUtil.process_log.process_end(process_level, msg='补全分类', order=order, obj=check_result)

    def check_category_list(self, list_category, process_level):
        list_check_result: [CheckResult] = []
        for index, category in enumerate(list_category):
            order = index + 1
            LogUtil.set_process(process_level, order)
            LogUtil.process_log.process_start(process_level, msg='检查分类', order=order, obj=category)
            check_result: CheckResult = self.check_category(category, process_level + 1)
            if check_result.is_check:
                if check_result.is_no_duplicate:
                    if check_result.is_file_complete:
                        LogUtil.process_log.process(process_level, msg=f'分类检查结果: 完全正常', obj=check_result)
                    else:
                        LogUtil.process_log.process(process_level, msg=f'分类检查结果: 资源不全', obj=check_result,
                                                    level=LogUtil.Level.ERROR)
                else:
                    LogUtil.process_log.process(process_level, msg=f'分类检查结果: 有重复不全', obj=check_result,
                                                level=LogUtil.Level.ERROR)
            elif category.list_sub_category_code:
                LogUtil.process_log.process(process_level, f"影片没有页数且有子分类", obj=category)
            else:
                LogUtil.process_log.process(process_level, f"影片没有页数且没有子分类", obj=category, level=LogUtil.Level.ERROR)
            list_check_result.append(check_result)
            LogUtil.process_log.process_end(process_level, msg='检查分类', order=order, obj=category)
        return list_check_result

    def check_category(self, category, process_level) -> CheckResult:
        if category.page_count:
            dir_img = os.path.join(DIR_OUTPUT, category.category_code, 'IMG')
            dir_m3u8 = os.path.join(DIR_OUTPUT, category.category_code, 'M3U8')
            list_video_category = self.group_dict_video[category.category_code]  # 分类下的影片列表
            list_serno = [video.get('serno') for video in list_video_category]  # 编号列表
            set_video_category_serno = set(list_serno)  # 标号集合
            self.group_dict_serno[category.category_code] = set_video_category_serno
            count_video = len(list_video_category)
            count_serno = len(set_video_category_serno)
            count_img = len(os.listdir(dir_img))
            count_m3u8 = len(os.listdir(dir_m3u8))
            check_result = CheckResult(category=category, is_check=True, count_video=count_video,
                                       count_serno=count_serno,
                                       count_m3u8=count_m3u8, count_img=count_img)
            return check_result
        else:
            return CheckResult(category=category, is_check=False)


if __name__ == '__main__':
    checker = Checker()
    checker.start()
