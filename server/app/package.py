"""
Project     : bugaboo
Filename    : package.py
Author      : zhancongc
Description : 支持views路由函数的库函数
"""

import json
import requests
import hashlib
import datetime
import configparser


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
    conf = configparser.ConfigParser()
    conf.read(filenames='config.ini', encoding='utf8')
    app_id = conf.get('app', 'app_id')
    app_secret = conf.get('app', 'app_secret')
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    data = {'js_code': code, 'secret': app_secret, 'grant_type': 'authorization_code',
            'appid': app_id}
    r = requests.post(url, data=data)
    print(json.loads(r.text))
    return json.loads(r.text)


def get_sha1(value):
    """
    :param value: unicode string
    :return: encrypt unicode string
    """
    conf = configparser.ConfigParser()
    conf.read(filenames='config.ini', encoding='utf8')
    application_secret = conf.get('app', 'application_secret')
    sh = hashlib.sha1()
    sh.update(value.encode())
    sh.update(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S').encode())
    sh.update(application_secret.encode())
    return sh.hexdigest()


'''
获取随机数
openssl rand -base64 8
'''
