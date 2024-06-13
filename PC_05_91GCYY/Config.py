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

# HEADERS = {
#     'cookie': 'PHPSESSID=174536a24707e8432027842581640847; isWelcomeTipsNoShow=1',
#     'referer': 'https://d55o.rollsran.xyz/category/1?page=119',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
# }
# URL_HOST = 'https://d55o.rollsran.xyz'
# HEADERS = {
#     'cookie': '_zhchat_chat_entIds=%5B%5D; _zhchat_chat_channelIds=%5B%7B%22customerId%22%3A%22661fcaeee3a0f40ae5581599%22%2C%22channelId%22%3A%22E6Z9dw%22%7D%5D; PHPSESSID=0cee5fd378d4ec39be25b9156f44dc98; isWelcomeTipsNoShow=1',
#     'referer': 'https://g1hs.nestokra.com/vid/4158.html',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
# }
# URL_HOST = 'https://g1hs.nestokra.com'

# HEADERS = {
#     'cookie': '_zhchat_chat_entIds=%5B%5D; _zhchat_chat_channelIds=%5B%7B%22customerId%22%3A%22661fcaeee3a0f40ae5581599%22%2C%22channelId%22%3A%22E6Z9dw%22%7D%5D; PHPSESSID=71285703d1d828367a90af7a12caeeec; isWelcomeTipsNoShow=1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
# }
# URL_HOST = 'https://g1hs.nestokra.com'
# HEADERS = {
#     'cookie': 'PHPSESSID=943253905816fb8f3cefa8808d77feb2; isWelcomeTipsNoShow=1',
#     'referer': 'https://nqkh.judoegg.com/',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
# }
# URL_HOST = 'https://nqkh.judoegg.com/'
HEADERS = {
    'cookie': '_zhchat_chat_entIds=%5B%5D; _zhchat_chat_channelIds=%5B%7B%22customerId%22%3A%22661fcaeee3a0f40ae5581599%22%2C%22channelId%22%3A%22E6Z9dw%22%7D%5D; isWelcomeTipsNoShow=1; PHPSESSID=be737e29b41e8d594bb542c43ad46788',
    'referer': 'https://g1hs.nestokra.com/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
URL_HOST = 'https://g1hs.nestokra.com/'
DIR_OUTPUT = os.path.join(os.getcwd(), 'OutputData')
DIR_M3U8 = os.path.join(DIR_OUTPUT, 'M3U8')
DIR_M3U8_ADD_KEYURI = os.path.join(DIR_OUTPUT, 'M3U8_ADD_KEYURI')
DIR_IMG = os.path.join(DIR_OUTPUT, 'IMG')
DIR_CATEGORY = os.path.join(DIR_OUTPUT, 'CATEGORY')
DIR_LOG = os.path.join(DIR_OUTPUT, 'LOG')

FILE_JSON_CURRENT = os.path.join(DIR_OUTPUT, 'JSON_CURRENT.json')
FILE_EXCEL_CURRENT = os.path.join(DIR_OUTPUT, 'EXCEL_CURRENT.xlsx')
FILE_JSON_ALL = os.path.join(DIR_OUTPUT, 'JSON_ALL.json')
FILE_EXCEL_ALL = os.path.join(DIR_OUTPUT, 'EXCEL_ALL.xlsx')

FILE_JSON_CURRENT_CATEGORY = os.path.join(DIR_CATEGORY, 'JSON_CURRENT.json')
FILE_EXCEL_CURRENT_CATEGORY = os.path.join(DIR_CATEGORY, 'EXCEL_CURRENT.xlsx')
FILE_JSON_ALL_CATEGORY = os.path.join(DIR_CATEGORY, 'JSON_ALL.json')
FILE_EXCEL_ALL_CATEGORY = os.path.join(DIR_CATEGORY, 'EXCEL_ALL.xlsx')

# 确保文件夹存在
os.makedirs(DIR_OUTPUT, exist_ok=True)
os.makedirs(DIR_M3U8, exist_ok=True)
os.makedirs(DIR_M3U8_ADD_KEYURI, exist_ok=True)
os.makedirs(DIR_IMG, exist_ok=True)
os.makedirs(DIR_LOG, exist_ok=True)
os.makedirs(DIR_CATEGORY, exist_ok=True)
