import configparser
import requests
import json
import datetime
import random
from flask import request, jsonify, url_for, flash, redirect
from config import configs
from .models import User, UserInfo, God
from functools import wraps


def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    app_secret = conf.get('app', 'app_secret')
    res = requests.get(url.format(configs['development'].APP_ID, app_secret))
    access_token = json.loads(res.text).get('access_token')
    print(access_token)
    return access_token if access_token else None


def logging(msg):
    with open('response_log.txt', 'a') as fp:
        fp.write(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + msg + '\n')
    print(msg)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in configs['development'].PICTURE_ALLOWED_EXTENSIONS


def get_user_info(session_id):
    """
    :function: 通过session_id 获取用户信息
    :param session_id:
    :return:
    """
    user = User.query.filter_by(session_id).first()
    user_info = UserInfo.query.filter_by(user.user_id).first()
    return user_info


def raffle_award():
    if random.randint(1, 100) < 60:
        return 0
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    award_string = conf.get('raffle', 'daily_award')
    if award_string == '0000000000000':
        return 0
    award_array = list(award_string)
    temp = list()
    for index in range(len(award_string)):
        if award_string[index] == '1':
            temp.append(index)
    if temp:
        award_choice = random.choice(temp)
        del temp[temp.index(award_choice)]
        award_array[award_choice] = '0'
        award_string = ''.join(award_array)
    else:
        award_string = '0000000000000'
        award_choice = -1
    conf.set('raffle', 'daily_award', award_string)
    with open('config.ini', 'w') as fp:
        conf.write(fp)
    award_id = award_choice + 1
    return award_id


def login_required1(func):
    """
    :function: 判断session_id是否有效
    :param func: 路由处理函数
    :return: 如果session_id验证通过，那么返回user对象
    """
    @wraps(func)
    def authenticate(*args, **kwargs):
        res = dict()
        session_id = request.headers.get('Session-Id')
        if session_id is None:
            res.update({
                'state': 0,
                'msg': 'none session_id'
            })
            return jsonify(res)
        user = User.query.filter_by(session_id=session_id).first()
        if user is None:
            res.update({
                'state': 0,
                'msg': 'cannot found session_id'
            })
            return jsonify(res)
        # current = datetime.datetime.now()
        # expire = user.session_id_expire_time
        # if current > expire:
        #    res.update({
        #        'state': 0,
        #        'msg': 'session_id expired'
        #    })
        return func(user, *args, **kwargs)
    return authenticate


def login_required2(func):
    """
    :function: 判断后台是否登录
    :param func: 路由处理函数
    :return: 原样返回
    """
    @wraps(func)
    def whether_login(*args, **kwargs):
        access_token = request.headers.get('Access-Token')
        if access_token is None:
            flash(message="请登陆", category="error")
            return redirect(url_for('god_login'))
        god = God.query.filter_by(access_token=access_token).first()
        if god is None:
            flash(message="不存在的用户", category="error")
            return redirect(url_for('god_login'))
        current = datetime.datetime.utcnow()
        expire = god.access_token_expire_time
        if current > expire:
            flash(message="请重新登陆", category="error")
            return redirect(url_for('god_login'))
        return func(*args, **kwargs)
    return whether_login

