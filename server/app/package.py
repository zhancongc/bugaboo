import json
import requests
from app import app


def wxlogin(code):
    appid = app.config.get('APP_ID')
    with open('appsecret', 'r') as f:
        app_secret = f.readline().strip()
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    data = {'js_code': code, 'secret': app_secret, 'grant_type': 'authorization_code',
            'appid': appid}
    r = requests.post(url, data=data)
    return json.loads(r.text)
