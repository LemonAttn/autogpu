import hashlib
from io import BytesIO
from PIL import Image

import requests
import matplotlib.pyplot as plt
from fake_useragent import UserAgent


def login(phone = None,
          password = None
          ):
    headers = {
        'User-Agent': UserAgent().random
    }
    if phone is not None and password is not None:
        # 1、获取ticket
        login_url = 'https://www.autodl.com/api/v1/new_login'
        sha1 = hashlib.sha1()
        sha1.update(str(password).encode('utf-8'))
        data = {
            'phone': str(phone),
            'password': sha1.hexdigest(),
            'phone_area': '+86'
        }
        response = requests.post(url = login_url, headers = headers, json = data).json()
        ticket = response['data']['ticket']
        # 2、获取token
        passport_url = 'https://www.autodl.com/api/v1/passport'
        response = requests.post(url = passport_url, headers = headers, json = {'ticket': ticket}).json()
        token = response['data']['token']
        with open('./config.py', 'w', encoding = 'utf-8') as f:
            f.write(f'Authorization = "{token}"')
    else:
        # 1、获取二维码和uuid
        login_url = 'https://www.autodl.com/api/v1/wx/login'
        response = requests.get(url = login_url, headers = headers).json()
        qrcode_url = response['data']['qrcode_url']
        uuid = response['data']['uuid']
        # 2、获取ticket
        response = requests.get(url = qrcode_url, headers = headers).content
        img = Image.open(BytesIO(response))
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        query_url = 'https://www.autodl.com/api/v1/wx/polling/query'
        response = requests.post(url = query_url, headers = headers, json = {'uuid': uuid}).json()
        ticket = response['data']['ticket']
        # 3、获取token
        passport_url = 'https://www.autodl.com/api/v1/passport'
        response = requests.post(url = passport_url, headers = headers, json = {'ticket': ticket}).json()
        token = response['data']['token']
        with open('./config.py', 'w', encoding = 'utf-8') as f:
            f.write(f'Authorization = "{token}"')