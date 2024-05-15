import os

# URL_HOST = 'https://g1hs.nestokra.com'
# HEADERS = {
#     'cookie': '_zhchat_chat_entIds=%5B%5D; _zhchat_chat_channelIds=%5B%7B%22customerId%22%3A%22661fcaeee3a0f40ae5581599%22%2C%22channelId%22%3A%22E6Z9dw%22%7D%5D; isWelcomeTipsNoShow=1; PHPSESSID=2ed5d416031097d9e089e767f587ee3d',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
# }
# HEADERS = {
#     'cookie': 'PHPSESSID=21124a1bdba1fe58c1dab5d3ef6d4269; isWelcomeTipsNoShow=1',
#     'referer': 'https://7qg6.rollsran.xyz/category/1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
# }
# URL_HOST = 'https://7qg6.rollsran.xyz'

HEADERS = {
    'cookie': 'PHPSESSID=174536a24707e8432027842581640847; isWelcomeTipsNoShow=1',
    'referer': 'https://d55o.rollsran.xyz/category/1?page=119',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
URL_HOST = 'https://d55o.rollsran.xyz'
DIR_OUTPUT = os.path.join(os.getcwd(), 'OutputData')
DIR_M3U8 = os.path.join(DIR_OUTPUT, 'M3U8')
DIR_IMG = os.path.join(DIR_OUTPUT, 'IMG')

FILE_JSON_CURRENT = os.path.join(DIR_OUTPUT, 'JSON_CURRENT.json')
FILE_EXCEL_CURRENT = os.path.join(DIR_OUTPUT, 'EXCEL_CURRENT.xlsx')
FILE_JSON_ALL = os.path.join(DIR_OUTPUT, 'JSON_ALL.json')
FILE_EXCEL_ALL = os.path.join(DIR_OUTPUT, 'EXCEL_ALL.xlsx')

def check_dir():
    if not os.path.isdir(DIR_OUTPUT):
        os.makedirs(DIR_OUTPUT)
    if not os.path.isdir(DIR_M3U8):
        os.makedirs(DIR_M3U8)
    if not os.path.isdir(DIR_IMG):
        os.makedirs(DIR_IMG)
