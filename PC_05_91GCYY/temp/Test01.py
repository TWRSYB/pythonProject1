import requests
import certifi

print(certifi.where())

get = requests.get(url='https://lp3-cdn-tos.bytecdntd.com/awimg/uuv/3870.jpg')
print(get)
