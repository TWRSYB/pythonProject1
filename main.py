# 导入 requests
import requests
import json

url = 'https://www.chinamoney.com.cn/ags/ms/cm-u-bk-currency/LprChrtCSV?startDate=2019-01-01'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

response = requests.post(url=url, headers=headers)
res_text = response.text
res_json = json.loads(res_text)
print(res_json)
print(res_json['data'])