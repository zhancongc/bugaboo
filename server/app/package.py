import json
import requests
import hashlib
import datetime
from app import app
from config import configs


def wxlogin(code):
    """
    :param code: code generate by weixin mini program, just like: 011D6BBL00pBY92XORAL0M7gBL0D6BBS
    :return: dict object contains session_key, openid, unionid, just like:
    {
        "session_key":"sdkBgQyQyFjUFpf2zjjrCQ==",
        "openid":"oyab15UR9j5BbTtj_sKKMHNEtSSw",
        "unionid":"oy9ft0RKmgFXI_K8NFZYSY6CjnIA"
    }
    """
    appid = app.config.get('APP_ID')
    with open('appsecret.txt', 'r') as f:
        app_secret = f.readline().strip()
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    data = {'js_code': code, 'secret': app_secret, 'grant_type': 'authorization_code',
            'appid': appid}
    r = requests.post(url, data=data)
    return json.loads(r.text)


def get_sha1(value):
    """
    :param value: unicode string
    :return: encrypt unicode string
    """
    sh = hashlib.sha1()
    sh.update(value.encode())
    sh.update(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
    sh.update(configs['development'].APPLICATION_SECRET)
    return sh.hexdigest()



'''
获取随机数
openssl rand -base64 8
'''
