import json
import requests
from app import app


def wxlogin(code):
    appid = app.config.get('APP_ID')
    with open('appsecret.txt', 'r') as f:
        app_secret = f.readline().strip()
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    data = {'js_code': code, 'secret': app_secret, 'grant_type': 'authorization_code',
            'appid': appid}
    r = requests.post(url, data=data)
    return json.loads(r.text)

'''
011D6BBL00pBY92XORAL0M7gBL0D6BBS
'{"session_key":"sdkBgQyQyFjUFpf2zjjrCQ==","openid":"oyab15UR9j5BbTtj_sKKMHNEtSSw","unionid":"oy9ft0RKmgFXI_K8NFZYSY6CjnIA"}'

'''
