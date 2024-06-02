import json
import os
import re
import shutil
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
from PC_05_91GCYY import Config
from PC_05_91GCYY.CheckComplite import Checker
from PC_05_91GCYY.Config import URL_HOST, DIR_M3U8, DIR_IMG, FILE_JSON_CURRENT, FILE_JSON_ALL, FILE_EXCEL_CURRENT, \
    FILE_EXCEL_ALL, DIR_OUTPUT, HEADERS, FILE_JSON_ALL_CATEGORY, DIR_CATEGORY, FILE_JSON_CURRENT_CATEGORY, \
    FILE_EXCEL_CURRENT_CATEGORY, FILE_EXCEL_ALL_CATEGORY

# 创建session对象
from PC_00_Common.ReqUtil import ReqUtil
from PC_05_91GCYY.Vo.Category import Category
from PC_05_91GCYY.Vo.Task import Task

session = requests.Session()
session.headers = HEADERS
session.cookies.set('existmag', 'all')
session.mount('https://', requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=50))

save_pic_util = SavePicUtil.SavePicUtil(session=session)
req_util = ReqUtil.ReqUtil(session=session)


def get_task_img(task: Task, dir_img):
    save_pic_util.save_pic(task.img_src, dir_img, task.get_name())


def get_task_m3u8(task: Task, dir_m3u8):
    res_get_m3u8 = req_util.try_get_req_times(f'{URL_HOST}{task.m3u8_url}', msg=f'获取.m3u8文件')
    if res_get_m3u8.status_code != 200:
        return
    with open(os.path.join(dir_m3u8, f'{task.get_name()}.m3u8'), 'wb') as m3u8_file:
        m3u8_file.write(res_get_m3u8.content)
    dir_m3u8_ca49e0 = f'{dir_m3u8}_ca49e0'
    os.makedirs(dir_m3u8_ca49e0, exist_ok=True)
    if task.m3u8_url.endswith('4be0'):
        res_get_m3u8_ca49e0 = req_util.try_get_req_times(f'{URL_HOST}{task.m3u8_url.replace("ca4be0", "ca49e0")}',
                                                         msg=f'获取完整.m3u8文件')
        if res_get_m3u8_ca49e0.status_code != 200:
            return
        with open(os.path.join(dir_m3u8_ca49e0, f'{task.get_name().replace("ca4be0", "ca49e0")}.m3u8'),
                  'wb') as m3u8_file:
            m3u8_file.write(res_get_m3u8_ca49e0.content)


def save_data(list_vo, list_json_all: list,
              dir_output, path_file_json_current, path_file_json_all, path_file_excel_current, path_file_excel_all,
              process_level=4):
    # 保存 Json 文件 ↓↓↓
    # 输出本次 Json 文件 ↓↓↓
    with open(path_file_json_current, 'w', encoding='utf-8') as f:
        json.dump([task.__dict__ for task in list_vo], f, ensure_ascii=False, indent=4)
    LogUtil.process_log.process(process_level, f'输出本次Json成功', obj=path_file_json_current)
    # 输出本次 Json 文件 ↑↑↑

    # 将本次数据合并到现有 Json 中 ↓↓↓
    # existing_serialized = set()  # 创建一个空集合，用于存放已存在数据的序列化字符串
    # for item in list_json_all:  # 将现有数据的每个字典序列化为字符串，并加入到集合中
    #     serialized_item = json.dumps(item, sort_keys=True)
    #     existing_serialized.add(serialized_item)
    # unique_new_json_list = []
    # for item in [task.__dict__ for task in list_vo]:  # 遍历新数据，仅保留不在已存在数据中的字典
    #     serialized_item = json.dumps(item, sort_keys=True)
    #     if serialized_item not in existing_serialized:
    #         unique_new_json_list.append(item)
    # list_json_all.extend(unique_new_json_list)  # 将新数据追加到现有数据中
    for vo in list_vo:
        if not vo.in_dict_list(list_json_all):
            list_json_all.append(vo.__dict__)
    with open(path_file_json_all, "w", encoding='utf-8') as f:  # 将合并后的数据写回JSON文件
        json.dump(list_json_all, f, ensure_ascii=False, indent=4)  # indent 参数可选，用于美化输出（增加缩进）
    LogUtil.process_log.process(process_level, f'输出所有Json成功', obj=path_file_json_all)
    # 将本次数据合并到现有 Json 中 ↑↑↑
    # 保存 Json 文件 ↑↑↑

    # 保存 Excel 文件 ↓↓↓
    # 输出本次 Excel 文件 ↓↓↓
    df = pandas.DataFrame(([task.__dict__ for task in list_vo])).astype(
        str)  # 将列表转换为 DataFrame , 格式为 str , 避免 Excel 以数字和科学计数法显示
    df.to_excel(path_file_excel_current, index=False)  # 将DataFrame保存到Excel文件, index=False表示不保存行索引到Excel文件
    format_excel_text(path_file_excel_current)
    LogUtil.process_log.process(process_level, f'输出本次Excel成功', obj=path_file_excel_current)
    # 输出本次 Excel 文件 ↑↑↑

    # 输出所有 Excel 文件 ↓↓↓
    df = pandas.DataFrame(list_json_all).astype(str)
    df.to_excel(path_file_excel_all, index=False)  # 将DataFrame保存到Excel文件, index=False表示不保存行索引到Excel文件
    format_excel_text(path_file_excel_all)
    LogUtil.process_log.process(process_level, f'输出所有Excel成功', obj=path_file_excel_all)
    # 输出所有 Excel 文件 ↑↑↑
    # 保存 Excel 文件 ↑↑↑

    # 备份数据 ↓↓↓
    backup_folder_name = os.path.join(dir_output, f'Backup_{datetime.now().strftime("%Y-%m-%d_%H%M%S")}')
    os.makedirs(backup_folder_name)
    shutil.copy2(path_file_json_current, backup_folder_name)
    shutil.copy2(path_file_json_all, backup_folder_name)
    shutil.copy2(path_file_excel_current, backup_folder_name)
    shutil.copy2(path_file_excel_all, backup_folder_name)
    LogUtil.process_log.process(process_level, f'备份数据成功', obj=backup_folder_name)
    # 备份数据 ↑↑↑


def get_save_path_by_category_code(category_code):
    dir_save = os.path.join(DIR_OUTPUT, category_code)
    dir_m3u8 = os.path.join(dir_save, 'M3U8')
    dir_img = os.path.join(dir_save, 'IMG')
    os.makedirs(dir_save, exist_ok=True)
    os.makedirs(dir_m3u8, exist_ok=True)
    os.makedirs(dir_img, exist_ok=True)
    return dir_save, dir_m3u8, dir_img


def get_task_resource(task_list, dir_m3u8, dir_img):
    for task in task_list:
        get_task_m3u8(task, dir_m3u8)
        get_task_img(task, dir_img)


def add_key_uri_for_m3u8(dir_m3u8, process_level: int):
    for index, file_m3u8 in enumerate(Path(dir_m3u8).glob('*.m3u8')):
        LogUtil.set_process(process_level, index + 1)
        LogUtil.process_log.process_start(process_level, msg='为.m3u8添加key_uri', order=index + 1)
        with file_m3u8.open('r') as file:
            content = file.read()
        # 使用正则表达式替换文本
        replaced_content = re.sub(r'#EXT-X-KEY:METHOD=AES-128,URI=".+"',
                                  f'#EXT-X-KEY:METHOD=AES-128,URI="{URL_HOST}/sec"', content)
        # 另存为新文件
        dir_m3u8_add_key_uri = f'{dir_m3u8}_ADD_KEY_URI'
        os.makedirs(dir_m3u8_add_key_uri, exist_ok=True)
        with open(os.path.join(dir_m3u8_add_key_uri, file_m3u8.name), 'w', encoding='utf-8') as new_file:
            new_file.write(replaced_content)
        LogUtil.process_log.process_end(process_level, msg='为.m3u8添加key_uri', order=index + 1)


class Executor:
    def __init__(self):
        self.list_category: [Category] = []
        self.list_category_json_all = []
        self.list_task: [Task] = []
        self.list_json_all = []
        # 读取现有JSON文件中的数据
        if os.path.isfile(FILE_JSON_ALL):
            with open(FILE_JSON_ALL, 'r', encoding='utf-8') as json_file:
                self.list_json_all = json.load(json_file)

        # 读取现有JSON文件中的数据
        if os.path.isfile(FILE_JSON_ALL_CATEGORY):
            with open(FILE_JSON_ALL_CATEGORY, 'r', encoding='utf-8') as json_file:
                self.list_category_json_all = json.load(json_file)

    def start(self):
        process_level = 1

        # 获取分类
        if LogUtil.set_process(process_level, 1):
            LogUtil.process_log.process_skip(process_level, '获取分类')
        else:
            LogUtil.process_log.process_start(process_level, '获取分类')
            self.get_category()
            LogUtil.process_log.process_end(process_level, '获取分类')
        # 获取影片
        if LogUtil.set_process(process_level, 2):
            LogUtil.process_log.process_skip(process_level, '获取影片')
        else:
            LogUtil.process_log.process_start(process_level, '获取影片')
            self.get_task()
            LogUtil.process_log.process_end(process_level, '获取影片')
        # 检查缺失情况
        if LogUtil.set_process(process_level, 3):
            LogUtil.process_log.process_skip(process_level, '检查缺失情况')
        else:
            LogUtil.process_log.process_start(process_level, '检查缺失情况')
            checker = Checker()
            checker.start(process_level=process_level + 1)
            LogUtil.process_log.process_end(process_level, '检查缺失情况')

    def get_category(self, process_level=2):
        res_home_page = req_util.try_get_req_times(url=f'{URL_HOST}')
        if not res_home_page:
            return
        etree_res_home_page = etree.HTML(res_home_page.text)  # 初始化生成一个XPath解析对象
        list_category_home = etree_res_home_page.xpath('//div/ul/li/a[contains(@href,"/category")]')
        for index, category_home in enumerate(list_category_home):
            if LogUtil.set_process(process_level, index + 1):
                LogUtil.process_log.process_skip(process_level, msg='获取首页分类', order=index + 1)
                continue
            LogUtil.process_log.process_start(process_level, msg='获取首页分类', order=index + 1)
            href = xpath_util.get_unique(category_home, './@href')
            category_code = href.replace('/category/', '')
            category_name = xpath_util.get_unique(category_home, './text()')
            category = Category(category_code, category_name, href)
            self.list_category.append(category)
            self.get_sub_category(category)
            LogUtil.process_log.process_end(process_level, msg='获取首页分类', order=index + 1, obj=category)
        save_data(list_vo=self.list_category, list_json_all=self.list_category_json_all, dir_output=DIR_CATEGORY,
                  path_file_json_current=FILE_JSON_CURRENT_CATEGORY, path_file_json_all=FILE_JSON_ALL_CATEGORY,
                  path_file_excel_current=FILE_EXCEL_CURRENT_CATEGORY, path_file_excel_all=FILE_EXCEL_ALL_CATEGORY,
                  process_level=process_level + 1)

    def get_sub_category(self, category):
        res_category = req_util.try_get_req_times(url=f'{URL_HOST}/category/{category.category_code}')
        if not res_category:
            return
        etree_res_category = etree.HTML(res_category.text)  # 初始化生成一个XPath解析对象
        page_count = 0
        list_sub_category_item = etree_res_category.xpath(
            '//div[contains(@class,"home-tab")]/div[contains(@class,"mb15")]')
        if len(list_sub_category_item) > 0:
            category.list_sub_category_code = []
            for index, sub_category_item in enumerate(list_sub_category_item):
                LogUtil.set_process(3, index + 1)
                LogUtil.process_log.process_start(3, f'获取子分类', order=index + 1, obj=category)
                href = xpath_util.get_unique(sub_category_item, './a/@href')
                category_code = href.replace('/category/', '')
                category_name = xpath_util.get_unique(sub_category_item, './div/text()')
                sub_category = Category(category_code, category_name, href, super_category_code=category.category_code,
                                        page_count=page_count)
                category.list_sub_category_code.append(category_code)
                self.list_category.append(sub_category)
                self.get_sub_category(sub_category)
                LogUtil.process_log.process_end(3, f'获取子分类', order=index + 1, obj=sub_category)
        else:
            list_page_bar_item = etree_res_category.xpath('//div[contains(@class,"pagebar")]/li/*/text()')
            page_count = 1
            if len(list_page_bar_item) > 0:
                page_count = max(
                    [int(page_bar_item) for page_bar_item in list_page_bar_item if re.match(r'\d+', page_bar_item)])
            category.page_count = page_count
            category.list_sub_category_code = None

    def get_task(self):
        if len(self.list_category) > 0:
            for index, category in enumerate(self.list_category):
                if LogUtil.set_process(2, index + 1):
                    LogUtil.process_log.process_skip(2, f"获取本次分类数据", order=index + 1, obj=category)
                    continue
                LogUtil.process_log.process_start(2, f"获取本次分类数据", order=index + 1, obj=category)
                self.read_category(category.category_code, category.page_count)
                LogUtil.process_log.process_end(2, f"获取本次分类数据", order=index + 1, obj=category)
        else:
            for index, category in enumerate(self.list_category_json_all):
                if LogUtil.set_process(2, index + 1):
                    LogUtil.process_log.process_skip(2, f"获取所有分类数据", order=index + 1, obj=category)
                    continue
                LogUtil.process_log.process_start(2, f"获取所有分类数据", order=index + 1, obj=category)
                list_task_category = self.read_category(category['category_code'], category['page_count'])
                LogUtil.process_log.process_end(2, f"获取所有分类数据", order=index + 1, obj=list_task_category)

    def read_category(self, category_code, page_count: int, category: Category = None, process_level: int = 3):
        list_task_category = []
        if category:
            category_code = category.category_code
            page_count = category.page_count
        if page_count > 0:
            dir_save, dir_m3u8, dir_img = get_save_path_by_category_code(category_code)
            for i in range(0, page_count):
                page = i + 1
                if LogUtil.set_process(process_level, page):
                    LogUtil.process_log.process_skip(process_level, f"读取页", order=page)
                    continue
                LogUtil.process_log.process_start(process_level, f"读取页", order=page)
                list_page_task = self.read_page(category_code, page, process_level + 1)
                list_task_category.extend(list_page_task)
                LogUtil.process_log.process_end(process_level, f"读取页", order=page, obj=list_page_task)
            add_key_uri_for_m3u8(dir_m3u8=dir_m3u8, process_level=process_level + 1)
        return list_task_category

    def read_page(self, category_code, page, process_level: int = 4):
        dir_save, dir_m3u8, dir_img = get_save_path_by_category_code(category_code)
        list_page_task = []
        res_page = req_util.try_get_req_times(url=f'{URL_HOST}/category/{category_code}', params={'page': page})
        if res_page.status_code != 200:
            return
        res_page_etree = etree.HTML(res_page.text)  # 初始化生成一个XPath解析对象

        mb15_list = res_page_etree.xpath('//li[@class="mb15"]')

        if len(mb15_list) < 1:
            return
        for index, mb15 in enumerate(mb15_list):
            order = index + 1
            if LogUtil.set_process(process_level, order):
                LogUtil.process_log.process_skip(process_level, f"获取影片详情", order, obj=category_code)
                continue
            LogUtil.process_log.process_start(4, f"获取影片详情", order, obj=category_code)
            href = xpath_util.get_unique(mb15, xpath='./a/@href', msg='获取 href')
            serno = re.search(r"/vid/(.+).html", href).group(1)
            title = xpath_util.get_unique(mb15, xpath='./a/@title', msg='获取 title')
            data_ratio = xpath_util.get_unique(mb15, xpath='./a/@data-ratio', msg='获取 data_ratio')
            img_src = xpath_util.get_unique(mb15, xpath='./a/img/@data-src', msg='获取 img_src')
            vip_type = xpath_util.get_unique(mb15, xpath='./a/*[@class="vip"]/text()', msg='获取 vip_type')
            play_times = xpath_util.get_unique(mb15, xpath='./a/*[@class="ico-right"]/text()', msg='获取 play_times')

            res_video_page = req_util.try_get_req_times(f'{URL_HOST}{href}')
            if res_video_page.status_code != 200:
                return
            res_video_page_etree = etree.HTML(res_video_page.text)
            script = xpath_util.get_unique(res_video_page_etree, xpath='//body/script/text()', msg='获取 script')
            m3u8_url = re.search(r"const m3u8_url = '(.+)';", script).group(1)

            task = Task(serno, href, title, category_code, data_ratio, img_src, vip_type, play_times, m3u8_url,
                        f'{page}_{order}')
            LogUtil.process_log.process_end(process_level, f"获取影片详情", order, obj=category_code)
            list_page_task.append(task)
        self.list_task += list_page_task
        self.save_task(list_page_task, dir_save, dir_img, dir_m3u8)
        return list_page_task

    def save_task(self, list_task, dir_save, dir_img, dir_m3u8):
        save_data(list_task, list_json_all=self.list_json_all,
                  dir_output=dir_save,
                  path_file_json_current=FILE_JSON_CURRENT, path_file_json_all=FILE_JSON_ALL,
                  path_file_excel_current=FILE_EXCEL_CURRENT, path_file_excel_all=FILE_EXCEL_ALL)
        get_task_resource(list_task, dir_m3u8, dir_img)

    # 通过serno获取影片
    def get_video_by_list_serno(self, list_serno, category_code, page_order: str = '未获取: 通过serno获取影片',
                                process_level: int = 4):
        dir_save, dir_m3u8, dir_img = get_save_path_by_category_code(category_code)
        list_task = []
        for serno in list_serno:
            href = f"/vid/{serno}.html"
            res_video_page = req_util.try_get_req_times(f'{URL_HOST}{href}')
            if not res_video_page:
                LogUtil.process_log.process(process_level, msg='打开影片页面失败', obj=serno, level=LogUtil.Level.ERROR)
                continue
            res_video_page_etree = etree.HTML(res_video_page.text)
            title = xpath_util.get_unique(res_video_page_etree, xpath='//div/h1[contains(@class, "mb10")]/text()',
                                          msg='获取 title')
            data_ratio = '未获取: 通过serno获取影片'
            script = xpath_util.get_unique(res_video_page_etree, xpath='//body/script/text()', msg='获取 script')
            m3u8_url = re.search(r"const m3u8_url = '(.+)';", script).group(1)
            img_src = re.search(r"const pic_thumbnail = '(.+)';", script).group(1)
            vip_type = '未获取: 通过serno获取影片'
            play_times = '未获取: 通过serno获取影片'
            task = Task(serno=f'{serno}', href=href, title=title, category=category_code, data_ratio=data_ratio,
                        img_src=img_src,
                        vip_type=vip_type, play_times=play_times, m3u8_url=m3u8_url,
                        page_order=page_order)
            list_task.append(task)
        print(list_task)
        self.save_task(list_task, dir_save, dir_img, dir_m3u8)
        return list_task

