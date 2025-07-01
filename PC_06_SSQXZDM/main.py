import re
import time
from urllib.parse import quote, unquote

import requests
import json

from lxml import etree

from PC_00_Common.ReqUtil import ReqUtil
from PC_00_Common.XpathUtil.XpathUtil import xpath_util
from PC_06_SSQXZDM.Config import HEADERS, FILE_JSON_MAIN_PROVINCE, FILE_JSON_AREA

session = requests.Session()
session.headers = HEADERS
session.cookies.set('existmag', 'all')

req_util = ReqUtil.ReqUtil(session=session)


def get_province_list():
    """获取省级行政区列表"""
    url = "http://xzqh.mca.gov.cn/map"
    res_main = req_util.try_get_req_times(url, msg='获取主页信息')
    xpath_etree_res = etree.HTML(res_main.text)
    text_script = xpath_util.get_unique(xpath_etree_res, '//body/script/text()', msg='获取 脚本')
    provinces_json = re.search(r"var json = (.+);", text_script).group(1)
    provinces = json.loads(provinces_json)

    with open(FILE_JSON_MAIN_PROVINCE, 'w', encoding='utf-8') as f:
        json.dump(provinces, f, ensure_ascii=False, indent=4)
    print(f"主页省级数据已成功写入文件: {FILE_JSON_MAIN_PROVINCE}")

    return provinces


def get_city_list(province_dict):
    """获取市级行政区列表"""

    province_name_full = province_dict.get('area_name_full')

    encoding_sheng_ji = quote(province_name_full, encoding='gbk')

    url = f"http://xzqh.mca.gov.cn/defaultQuery?shengji={encoding_sheng_ji}&diji=-1&xianji=-1"
    response = req_util.try_get_req_times(url, msg=f'获取省份{province_name_full}的数据')

    xpath_etree_res = etree.HTML(response.text)

    xpath_tr_cities = xpath_etree_res.xpath('//table[@class="info_table"]//tr[@class="shi_nub"]')

    province_renkou = 0
    province_mianji = 0

    for index, xpath_tr_city in enumerate(xpath_tr_cities):
        city_name = xpath_util.get_unique(xpath_tr_city, '@flag', msg='获取城市名称')
        xpath_tr_infos = xpath_tr_city.xpath('td')
        renkou_str = xpath_util.get_unique(xpath_tr_infos[2], 'text()', msg='获取城市人口').strip()
        renkou = float(renkou_str) if renkou_str else 0
        mianji_str = xpath_util.get_unique(xpath_tr_infos[3], 'text()', msg='获取城市面积').strip()
        mianji = float(mianji_str) if mianji_str else 0
        area_code = xpath_util.get_unique(xpath_tr_infos[4], 'text()', msg=f'获取城市行政区划代码{city_name}').strip()
        if not area_code:
            area_code = province_dict['area_code']
        city_dict = {
            'area_lv': '2',
            'area_name': city_name,
            'area_code': area_code,
            'up_code': province_dict['area_code'],
            'children': [],
            'area_path': f"{province_dict['area_path']}>{city_name}",
            'area_name_full': city_name,
            'zhudi': xpath_util.get_unique(xpath_tr_infos[1], 'text()', msg='获取城市驻地').strip(),
            'renkou': renkou,
            'mianji': mianji,
            'quhao': xpath_util.get_unique(xpath_tr_infos[5], 'text()', msg='获取城市区号').strip(),
            'youbian': xpath_util.get_unique(xpath_tr_infos[6], 'text()', msg='获取城市邮编').strip()
        }

        province_renkou += renkou
        province_mianji += mianji

        province_dict['children'].append(city_dict)
        get_district_list(city_dict, xpath_etree_res)

    province_dict['renkou'] = province_renkou
    province_dict['mianji'] = province_mianji


def get_district_list(city_dict, xpath_etree_res):
    """获取区县级行政区列表"""
    xpath_tr_areas = xpath_etree_res.xpath(f'//table[@class="info_table"]//tr[@parent="{city_dict["area_name"]}"]')
    for index, xpath_tr_area in enumerate(xpath_tr_areas):
        area_name = xpath_util.get_unique(xpath_tr_area[0], 'text()', msg='获取区县名称').strip()
        renkou_str = xpath_util.get_unique(xpath_tr_area[2], 'text()', msg=f'获取区县人口{area_name}').strip()
        renkou = float(renkou_str) if renkou_str else 0
        mianji_str = xpath_util.get_unique(xpath_tr_area[3], 'text()', msg=f'获取区县面积{area_name}').strip()
        mianji = float(mianji_str) if mianji_str else 0
        area_code = xpath_util.get_unique(xpath_tr_area[4], 'text()', msg=f'获取区县行政区划代码{area_name}').strip()
        if not area_code:
            area_code = city_dict['area_code']
        area_dict = {
            'area_lv': '3',
            'area_name': area_name,
            'area_code': area_code,
            'up_code': city_dict['area_code'],
            'children': [],
            'area_path': f"{city_dict['area_path']}>{area_name}",
            'area_name_full': area_name,
            'zhudi': xpath_util.get_unique(xpath_tr_area[1], 'text()', msg=f'获取区县驻地{area_name}').strip(),
            'renkou': renkou,
            'mianji': mianji,
            'quhao': xpath_util.get_unique(xpath_tr_area[5], 'text()', msg=f'获取区县区号{area_name}').strip(),
            'youbian': xpath_util.get_unique(xpath_tr_area[6], 'text()', msg=f'获取区县邮编{area_name}').strip()
        }
        city_dict['children'].append(area_dict)


def main():
    data = []
    provinces = get_province_list()

    for index, province in enumerate(provinces):
        province_name_full = province.get('shengji')
        province_name = province_name_full.split("（", 1)[0]
        province_dict = {
            'area_lv': '1',
            'area_name': province_name,
            'area_code': province.get('quHuaDaiMa'),
            'up_code': '0',
            'children': [],
            'area_path': province_name,
            'area_name_full': province_name_full,
            'zhudi': '',
            'renkou': '',
            'mianji': '',
            'quhao': '',
            'youbian': ''
        }
        data.append(province_dict)
        get_city_list(province_dict)
        time.sleep(2)

    # 保存为JSON文件
    with open(FILE_JSON_AREA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"省市区三级级数据已成功写入文件: {FILE_JSON_AREA}")


if __name__ == '__main__':
    main()
