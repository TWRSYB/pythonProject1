import os

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'http://xzqh.mca.gov.cn/',
}
URL_HOST = 'http://xzqh.mca.gov.cn/'
DIR_OUTPUT = os.path.join(os.getcwd(), 'OutputData')


FILE_JSON_MAIN_PROVINCE = os.path.join(DIR_OUTPUT, 'JSON_MAIN_PROVINCE.json')
FILE_JSON_PROVINCE = os.path.join(DIR_OUTPUT, 'JSON_PROVINCE.xlsx')
FILE_JSON_CITY = os.path.join(DIR_OUTPUT, 'JSON_CITY.json')
FILE_JSON_AREA = os.path.join(DIR_OUTPUT, 'JSON_AREA.json')

# 确保文件夹存在
os.makedirs(DIR_OUTPUT, exist_ok=True)
