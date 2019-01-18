"""
Project     : bugaboo
Filename    : views.py
Author      : zhancongc
Description : 路由处理
"""

import time
import json
import datetime
import requests
import hashlib
import random
import html
import qrcode
import configparser
from PIL import Image
from config import configs
from functools import wraps
from app import app, db
from sqlalchemy import desc
from flask_login import login_required, login_user, logout_user
from flask import jsonify, request, render_template, redirect, url_for, flash
from .package import wxlogin, get_sha1
from .models import User, UserInfo, Composition, AwardRecord, Award, Store, God, Follow
from .forms import GodLoginForm


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
    if random.randint(1, 100) < 85:
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
        current = datetime.datetime.utcnow()
        expire = user.session_id_expire_time
        if current > expire:
            res.update({
                'state': 0,
                'msg': 'session_id expired'
            })
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


@app.route('/test')
def test():
    """
    :function: 测试页面
    :return: 测试页面
    """
    return render_template('test.html')


@app.route('/user/login', methods=['POST'])
def user_login():
    """
    :function: 微信小程序登陆
    :return: 返回state, msg, session_id. state 1表示成功，0表示异常，msg是错误信息，如果登陆成功，还会返回session_id
    """
    res = dict()
    # 微信登陆
    code = request.values.get('code')
    if code is None:
        res.update({
            'state': 0,
            'msg': 'None code'
        })
        logging(json.dumps(res))
        return jsonify(res)
    try:
        wx = wxlogin(code)
    except Exception as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'weixin login error'
        })
        logging(json.dumps(res))
        return jsonify(res)
    open_id = wx.get('openid')
    session_key = wx.get('session_key')
    if open_id is None or session_key is None:
        res.update({
            'state': 0,
            'msg': 'open_id, session_key non existed'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 计算session_id
    session_id = get_sha1(session_key)
    current_time = datetime.datetime.utcnow()
    login_time = current_time.strftime(configs['development'].STRFTIME_FORMAT)
    session_id_expire_time = (current_time + datetime.timedelta(hours=6)).strftime(
        configs['development'].STRFTIME_FORMAT)
    # 更新session信息，如果找不到这个用户，那么创建一个新的用户再更新信息
    temp_user = User.query.filter_by(open_id=open_id).first()
    try:
        if temp_user:
            temp_user.login_time = login_time
            temp_user.session_id_expire_time = session_id_expire_time
            temp_user.session_key = session_key
            temp_user.session_id = session_id
            db.session.add(temp_user)
        else:
            temp_user = User(open_id=open_id, session_key=session_key,
                        session_id=session_id, session_id_expire_time=session_id_expire_time)
            db.session.add(temp_user)
        db.session.commit()
    except Exception as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'write to database error'
        })
        logging(json.dumps(res))
        return jsonify(res)
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    activity_on = conf.getboolean('app', 'activity_on')
    data = {
        'user_id': temp_user.user_id,
        'session_id': session_id,
        'activity_on': activity_on,
        'raffle_times': temp_user.raffle_times,
        'avatarUrl': temp_user.avatarUrl,
        'nickName': temp_user.nickName
    }
    if temp_user:
        composition = Composition.query.filter_by(user_id=temp_user.user_id).first()
        if composition:
            data.update({
                'composition_id': composition.composition_id
            })
    else:
        res.update({
            'state': 2,
            'msg': 'new user',
            'data': data
        })
        logging(json.dumps(res))
        return jsonify(res)
    res.update({
        'state': 1,
        'msg': 'success',
        'data': data
    })
    logging(json.dumps(res))
    return jsonify(res)


@app.route('/user/info/upload', methods=['POST'])
@login_required1
def user_info_upload(temp_user):
    """
    :function: 上传用户信息，最关键的是 nickName, avatarUrl 排行榜会用到
        avatarUrl, city, country, gender, language, nickName, province
    :return:
    """
    res = dict()
    avatar_url = request.values.get('avatarUrl')
    city = request.values.get('city')
    country = request.values.get('country')
    gender = request.values.get('gender')
    language = request.values.get('language')
    nick_name = request.values.get('nickName')
    province = request.values.get('province')
    if avatar_url is None or city is None or country is None or gender is None or language is None \
            or nick_name is None or province is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 类型转换
    try:
        gender = int(gender)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error: gender'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 将用户信息写入数据库
    user_info_list = UserInfo.query.filter_by(user_id=temp_user.user_id).all()
    try:
        if len(user_info_list) == 0:
            user_info = UserInfo(user_id=temp_user.user_id, city=city, country=country,
                                 gender=gender, language=language, province=province)
            temp_user.avatarUrl = avatar_url
            temp_user.nickName = nick_name
        elif len(user_info_list) == 1:
            user_info = user_info_list[0]
            user_info.city = city
            user_info.country = country
            user_info.gender = gender
            user_info.language = language
            user_info.province = province
            temp_user.avatarUrl = avatar_url
            temp_user.nickName = nick_name
        else:
            res.update({
                'state': 0,
                'msg': 'cannot upload user info'
            })
            return jsonify(res)
        db.session.add(user_info)
        db.session.add(temp_user)
        db.session.commit()
    except Exception as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'save data to database error'
        })
        return jsonify(res)
    res.update({
        'state': 1,
        'msg': 'success'
    })
    return jsonify(res)


@app.route('/user/composition/info', methods=['GET'])
@login_required1
def user_composition_info(temp_user):
    """
    :function: 自己的作品
    :return:
    """
    res = dict()
    # 获取作品信息
    composition = Composition.query.filter_by(user_id=temp_user.user_id).first()
    owner = User.query.filter_by(user_id=composition.user_id).first()
    if composition is None:
        res.update({
            'state': 0,
            'msg': 'none composition id'
        })
        return jsonify(res)
    data = dict()
    data.update({
        'user_id': temp_user.user_id,
        'nickName': temp_user.nickName,
        'avatarUrl': temp_user.avatarUrl,
        'composition_id': composition.composition_id,
        'composition_type': composition.composition_type,
        'composition_msg': composition.composition_msg,
        'composition_url': composition.composition_url,
        'timestamp': composition.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
    })
    res.update({
        'state': 1,
        'msg': 'my composition',
        'data': data
    })
    return jsonify(res)


@app.route('/user/composition/upload', methods=['POST'])
@login_required1
def user_composition_upload(temp_user):
    """
    :function: 上传作品 composition_type(1是bugaboo用户，0是非bugaboo用户), composition
    :return:
    """
    res = dict()
    # 检查用户是否有作品，有作品直接免谈
    temp_composition = Composition.query.filter_by(user_id=temp_user.user_id).first()
    if temp_composition:
        res.update({
            'state': 2,
            'msg': 'you have uploaded composition'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 检查作品类型
    composition_type = request.values.get('composition_type')
    composition_angle = request.values.get('composition_angle')
    composition_msg = request.values.get('composition_msg')
    if composition_type is None or composition_angle is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 类型转换
    try:
        composition_type = int(composition_type)
        composition_angle = int(composition_angle)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error: composition angle or type'
        })
        logging(json.dumps(res))
        return jsonify(res)
    if composition_angle not in [0, 90, 180, 270]:
        res.update({
            'state': 0,
            'msg': 'value error: composition angle'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 验证上传的图片
    img = request.files.get('composition')
    if img is None:
        res.update({
            'state': 0,
            'msg': 'None file'
        })
        return jsonify(res)
    if not allowed_file(img.filename):
        res.update({
            'state': 0,
            'msg': 'Wrong file format'
        })
        return jsonify(res)
    if img.filename == '':
        res.update({
            'state': 0,
            'msg': 'No selected file'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 保存图片到本地
    filename = str(int(time.mktime(time.gmtime()))) + '_' + img.filename
    file_path = configs['development'].UPLOAD_FOLDER + filename
    try:
        img.save(file_path)
    except Exception as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'Error occurred while saving file'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 如果图片需要旋转
    if composition_angle in [90, 180, 270]:
        im = Image.open(file_path)
        if composition_angle == 90:
            out = im.transpose(Image.ROTATE_270)
            out.save(file_path)
        elif composition_angle == 180:
            out = im.transpose(Image.ROTATE_180)
            out.save(file_path)
        else:
            out = im.transpose(Image.ROTATE_90)
            out.save(file_path)
    # 图片压缩
    im = Image.open(file_path)
    im_a, im_b = im.size
    if im_a > im_b:
        im_long, im_short = im_a, im_b
        if im_short > 600:
            coef = 600 / im_short
            im_long_modify = int(im_long * coef)
            im_short_modify = 600
            im.resize((im_long_modify, im_short_modify))
        if im_long > 1200:
            coef = 1200 / im_long
            im_short_modify = int(im_short * coef)
            im_long_modify = 1200
            im.resize((im_long_modify, im_short_modify))
    else:
        im_long, im_short = im_b, im_a
        if im_short > 600:
            coef = 600/im_short
            im_long_modify = int(im_long*coef)
            im_short_modify = 600
            im.resize((im_short_modify, im_long_modify))
        if im_long > 1200:
            coef = 1200/im_long
            im_short_modify = int(im_short*coef)
            im_long_modify = 1200
            im.resize((im_short_modify, im_long_modify))
    im.save(file_path)
    # 图片处理完成，生成图片的URI
    composition_url = configs['development'].COMPOSITION_PREFIX + filename
    # 保存到数据库
    try:
        composition = Composition(user_id=temp_user.user_id, composition_type=composition_type,
                                  composition_msg=composition_msg, composition_url=composition_url)
        db.session.add(composition)
        composition.sync_user_type()
        db.session.commit()
        composition_id = composition.composition_id
    except Exception as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'write to database error'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 返回图片信息
    image = dict()
    composition = Composition.query.filter_by(composition_id=composition_id).first()
    image.update({
        'composition_id': composition.composition_id,
        'composition_msg': composition.composition_msg,
        'composition_url': composition.composition_url,
        'composition_type': composition.composition_type,
        'timestamp': composition.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    })
    res.update({
        'state': 1,
        'msg': 'success',
        'data': image
    })
    logging(json.dumps(res))
    return jsonify(res)


@app.route('/user/composition', methods=['POST'])
@login_required1
def user_composition(temp_user):
    """
    :function: 根据composition_id查找作品信息 composition_id
    :return:
    """
    res = dict()
    composition_id = request.values.get('composition_id')
    if composition_id is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 类型转换
    try:
        composition_id = int(composition_id)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error: composition id'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 获取作品信息
    composition = Composition.query.filter_by(composition_id=composition_id).first()
    owner = User.query.filter_by(user_id=composition.user_id).first()
    if composition is None:
        res.update({
            'state': 0,
            'msg': 'none composition id'
        })
        return jsonify(res)

    data = dict()
    data.update({
        'user_id': composition.user_id,
        'nickName': owner.nickName,
        'avatarUrl': owner.avatarUrl,
        'composition_id': composition.composition_id,
        'composition_type': composition.composition_type,
        'composition_msg': composition.composition_msg,
        'composition_url': composition.composition_url,
        'timestamp': composition.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'followers': [],
        'follow_times': owner.follow_times
    })
    # 找到关注者
    who = owner.followers.all()
    followers = []
    temp = who[:8]
    if temp:
        for foll in temp:
            temp_foll = User.query.filter_by(user_id=foll.follower_id).first()
            followers.append({'avatarUrl': temp_foll.avatarUrl})
        data.update({
            'followers': followers
        })
    # 判断是否可以祝福
    can_follow = True
    if composition.user_id == temp_user.user_id:
        can_follow = False
        data.update({
            'can_follow': can_follow
        })
        res.update({
            'state': 1,
            'msg': 'my composition',
            'data': data
        })
    else:
        for w in who:
            if w.follower_id == temp_user.user_id:
                can_follow = False
        data.update({
            'can_follow': can_follow
        })
        res.update({
            'state': 2,
            'msg': 'others composition',
            'data': data
        })
    return jsonify(res)


@app.route('/rankinglist', methods=['GET', 'POST'])
@login_required1
def rankinglist(temp_user):
    """
    :function: 获取排行榜，分为婴儿车用户榜和非婴儿车用户榜, ranking_list_type
    :return: 根据用户类型，返回不同的排行榜，该榜单是即时生成的
    """
    print(temp_user)
    res = dict()
    ranking_list_type = request.values.get('ranking_list_type')
    if ranking_list_type is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 类型转换
    try:
        ranking_list_type = int(ranking_list_type)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error: ranking list type'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 获取排行榜用户信息
    if ranking_list_type in [0, 1]:
        user_list = User.query.filter_by(user_type=ranking_list_type).order_by(desc(User.follow_times)).limit(50).all()
        if user_list:
            data = []
            for index in range(len(user_list)):
                temp = {
                    'number': index+1,
                    'nickName': user_list[index].nickName,
                    'avatarUrl': user_list[index].avatarUrl,
                    'follow_times': user_list[index].follow_times
                }
                data.append(temp)
        else:
            res.update({
                'state': 0,
                'msg': 'no data'
            })
            return jsonify(res)
    else:
        res.update({
            'state': 0,
            'msg': 'invalid ranking list type'
        })
        return jsonify(res)
    res.update({
        'state': 1,
        'msg': 'success',
        'ranking_list_type': ranking_list_type,
        'data': data
    })
    return jsonify(res)


@app.route('/user/followers', methods=['GET'])
@login_required1
def user_followers(temp_user):
    """
    :function: 祝福我的人
    :return:
    """
    res = dict()
    # 获取关注我的人
    if temp_user.followers is None:
        res.update({
            'state': 0,
            'msg': 'no one follows me',
            'ranking_list_type': temp_user.user_type
        })
        return jsonify(res)
    user_list = list()
    for foll in temp_user.followers:
        temp_foll = User.query.filter_by(user_id=foll.follower_id).first()
        temp1 = {'avatarUrl': temp_foll.avatarUrl, 'nickName': temp_foll.nickName}
        user_list.append(temp1)
    res.update({
        'state': 1,
        'msg': 'success',
        'ranking_list_type': temp_user.user_type,
        'data': user_list
    })
    return jsonify(res)


@app.route('/user/follow', methods=['POST'])
@login_required1
def user_follow(temp_user):
    """
    :function: 帮人助力，composition_id
    :return: 助力成功
    """
    res = dict()
    # 助力
    composition_id = request.values.get('composition_id')
    if composition_id is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 类型转换
    try:
        composition_id = int(composition_id)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error: ranking list type'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 找到作品对应的用户
    composition = Composition.query.filter_by(composition_id=composition_id).first()
    if composition is None:
        res.update({
            'state': 0,
            'msg': 'invalid composition_id'
        })
        logging(json.dumps(res))
        return jsonify(res)
    author_id = composition.user_id
    # 助力的用户必须存在
    user = User.query.filter_by(user_id=author_id).first()
    if user is None:
        res.update({
            'state': 0,
            'msg': 'cannot find owner'
        })
        return jsonify(res)
    if temp_user.user_id == user.user_id:
        res.update({
            'state': 2,
            'msg': 'not myself'
        })
        return jsonify(res)
    # 尝试助力，把数据写入数据库
    try:
        temp_user.follow(user)
        db.session.commit()
    except Exception as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'write to db error'
        })
        return jsonify(res)
    data = {
        'followed_id': temp_user.user_id,
        'follower_id': user.user_id
    }
    res.update({
        'state': 1,
        'msg': 'success',
        'data': data
    })
    return jsonify(res)


@app.route('/user/follow/info', methods=['GET'])
@login_required1
def user_follow_info(temp_user):
    """
    :function: 判断是否有作品
    :return: None
    """
    res = dict()
    # 找关注者，获取他们的头像和昵称
    if temp_user.followers is None:
        res.update({
            'state': 0,
            'msg': 'none follower'
        })
        return jsonify(res)
    follower_info = list()
    for user in temp_user.followers:
        follower_info.append({
            'avatarUrl': user.avatarUrl,
            'nickName': user.nickName
        })
    res.update({
        'state': 1,
        'msg': 'get follower info',
        'data': follower_info
    })
    return jsonify(res)


@app.route('/raffle', methods=['GET'])
@login_required1
def raffle(temp_user):
    """
    :function: 抽奖接口
    :return: 抽奖信息
    """
    res = dict()
    if temp_user.raffle_times <= 0:
        res.update({
            'state': 0,
            'msg': 'not have enough raffle times',
        })
        return jsonify(res)
    temp_user.raffle()
    # 抽奖逻辑
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    temp_award_id = int(raffle_award())
    if temp_award_id == 1:
        award_id = temp_award_id
    elif temp_award_id == 7:
        award_id = 3
    elif temp_award_id == 13:
        award_id = 5
    elif temp_award_id in [2, 3, 4, 5, 6]:
        award_id = 2
    elif temp_award_id in [8, 9, 10, 11, 12]:
        award_id = 4
    else:
        award_id = 0
    if award_id != 0:
        award = Award.query.filter_by(award_id=award_id).first()
        if award.award_number <= 0:
            award_id = 0
    if award_id == 0:
        res.update({
            'state': 1,
            'msg': 'Thanks for participate',
            'data': {
                'award_id': 0
            }
        })
        return jsonify(res)
    data = dict()
    data.update({
        'award_id': award.award_id,
        'award_name': award.award_name,
        'award_image': award.award_image,
        'award_type': award.award_type,
        'award_description': award.award_description
    })
    app_secret = conf.get('app', 'app_secret')
    sh = hashlib.sha1()
    sh.update(str(temp_user.user_id).encode())
    sh.update(str(award_id).encode())
    sh.update(app_secret.encode())
    awardrecord_token = sh.hexdigest()
    qrcode_url = configs['development'].DOMAIN + configs['development'].QRCODE_URL_PREFIX + awardrecord_token
    # 保存图片到本地
    qrcode_name = str(int(time.mktime(time.gmtime()))) + '_' + awardrecord_token + '.png'
    qrcode_image_path = configs['development'].QRCODE_FOLDER
    image = qrcode.make(data=qrcode_url)
    image.save(qrcode_image_path + qrcode_name)
    qrcode_image_url = configs['development'].DOMAIN + '/static/qrcode/' + qrcode_name
    try:
        # 发奖
        awardrecord = AwardRecord(award_id=award_id, user_id=temp_user.user_id, awardrecord_type=award.award_type,
                                  awardrecord_token=awardrecord_token, qrcode_image_url=qrcode_image_url)
        if award_id in [2, 4]:
            awardrecord.informed = True
        award.award_number -= 1
        temp_user.raffle_times -= 1
        me = User.query.filter_by(user_id=temp_user.user_id).first()
        me.raffle_times -= 1
        # 抽奖次数减一
        db.session.add(me)
        db.session.add(awardrecord)
        db.session.add(award)
        db.session.commit()
    except Exception as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'write to database error'
        })
        return jsonify(res)
    res.update({
        'state': 1,
        'msg': 'success',
        'data': data
    })
    return jsonify(res)


@app.route('/raffle/times', methods=['GET'])
@login_required1
def raffle_times(temp_user):
    data = dict()
    res = dict()
    data.update({
        'raffle_times': temp_user.raffle_times,
        'nickName': temp_user.nickName,
        'avatarUrl': temp_user.avatarUrl
    })
    res.update({
        'state': 1,
        'msg': 'get follower info',
        'data': data
    })
    return jsonify(res)


@app.route('/user/award/list', methods=['GET'])
@login_required1
def user_award_list(temp_user):
    """
    :function: 获取我的奖品列表
    :return: 返回所有奖品
    """
    res = dict()
    # 获取所有奖励
    temp_award_record_list = AwardRecord.query.filter_by(user_id=temp_user.user_id).all()
    if temp_award_record_list is None:
        res.update({
            'state': 2,
            'msg': 'none award'
        })
        return jsonify(res)
    # 把所有奖励写入数组
    data = list()
    for temp in temp_award_record_list:
        awardrecord = dict()
        awardrecord.update({
            'awardrecord_id': temp.awardrecord_id,
            'award_time': temp.award_time.strftime('%Y-%m-%d %H:%M'),  # 中奖时间， 需要转成北京时间
            'awardrecord_token': temp.awardrecord_token,
            'informed': temp.informed,
            'checked': temp.checked,
            'check_time': temp.check_time.strftime('%Y-%m-%d %H:%M'),  # 兑换奖品时间，需要转成北京时间
            'awardrecord_type': temp.awardrecord_type,
            'award_id': temp.award_id,
        })
        award = Award.query.filter_by(award_id=temp.award_id).first()
        awardrecord.update({
            'award_name': award.award_name,
            'award_image': award.award_image
        })
        data.append(awardrecord)
    res.update({
        'state': 1,
        'msg': 'success',
        'data': data
    })
    return jsonify(res)


@app.route('/user/award', methods=['POST'])
@login_required1
def user_award(temp_user):
    """
    :function: 获取奖品以及收货信息 awardrecord_id
    :return:
    """
    res = dict()
    # 获取特定奖励
    awardrecord_id = request.values.get('awardrecord_id')
    if awardrecord_id is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 类型转换
    try:
        awardrecord_id = int(awardrecord_id)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error: award record id'
        })
        logging(json.dumps(res))
        return jsonify(res)
    # 查找这条奖品记录
    awardrecord = AwardRecord.query.filter_by(awardrecord_id=awardrecord_id).first()
    if awardrecord is None:
        res.update({
            'state': 0,
            'msg': 'none award'
        })
        return jsonify(res)
    if awardrecord.user_id != temp_user.user_id:
        res.update({
            'state': 0,
            'msg': 'this is not your award'
        })
        return jsonify(res)
    # 把所有奖励写入数组
    data = dict()
    data.update({
        'awardrecord_id': awardrecord.awardrecord_id,
        'award_id': awardrecord.award_id,
        'award_time': awardrecord.award_time,
        'user_id': awardrecord.user_id,
        'receiver': awardrecord.receiver,
        'phone': awardrecord.phone,
        'checked': awardrecord.checked,
        'check_time': awardrecord.check_time.strftime('%Y-%m-%d %H:%M:%S'),
        'store_id': awardrecord.store_id,
        'awardrecord_type': awardrecord.awardrecord_type,
        'awardrecord_token': awardrecord.awardrecord_token,
        'qrcode_image_url': awardrecord.qrcode_image_url
    })
    award = Award.query.filter_by(award_id=awardrecord.award_id).first()
    data.update({
        'award_type': award.award_type,
        'award_name': award.award_name,
        'award_image': award.award_image,
        'award_description': award.award_description
    })
    if awardrecord.awardrecord_id == 2:
        store = Store.query.filter_by(store_id=awardrecord.store_id).first()
        if store:
            data.update({
                'store_id': store.store_id,
                'store_name': store.store_name,
                'store_city': store.store_city,
                'store_address': store.store_address,
                'store_phone': store.store_phone
            })
    res.update({
        'state': 1,
        'msg': 'success',
        'data': data
    })
    return jsonify(res)


@app.route('/user/award/inform', methods=['POST'])
@login_required1
def user_award_store(temp_user):
    """
    :function: 上传门店信息 awardrecord_id, receiver, phone, store_id
    :return:
    """
    res = dict()
    awardrecord_id = request.values.get('awardrecord_id')
    receiver = request.values.get('receiver')
    phone = request.values.get('phone')
    address = request.values.get('address')
    store_id = request.values.get('store_id')
    # 检查空值
    if awardrecord_id is None or receiver is None or phone is None:
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 类型转换
    try:
        awardrecord_id = int(awardrecord_id)
    except ValueError as e:
        print(e)
        res.update({
            'state': 0,
            'msg': 'type error'
        })
        logging(json.dumps(res))
        return jsonify(res)
    awardrecord = AwardRecord.query.filter_by(awardrecord_id=awardrecord_id).first()
    if (awardrecord.awardrecord_type == 1 and address is None) or (awardrecord.awardrecord_type in [3, 4] and store_id is None):
        res.update({
            'state': 0,
            'msg': 'incomplete data'
        })
        return jsonify(res)
    # 检查奖品和用户是否对应
    if awardrecord.user_id != temp_user.user_id:
        res.update({
            'state': 0,
            'msg': 'award and user does not match'
        })
        return jsonify(res)
    if awardrecord.awardrecord_type in [3, 4]:
        # 检查门店是否存在
        store_id = Store.query.filter_by(store_id=store_id).first()
        if store_id is None:
            res.update({
                'state': 0,
                'msg': 'invalid store'
            })
            return jsonify(res)
        # 添加收货记录
        try:
            awardrecord.set_address(store_id, receiver, phone)
            db.session.add(awardrecord)
            db.session.commit()
        except Exception as e:
            print(e)
            res.update({
                'state': 0,
                'msg': 'write to database error'
            })
            return jsonify(res)
    elif awardrecord.awardrecord_type == 1:
        # 添加收货记录
        try:
            awardrecord.set_address(address, receiver, phone)
            db.session.add(awardrecord)
            db.session.commit()
        except Exception as e:
            print(e)
            res.update({
                'state': 0,
                'msg': 'write to database error'
            })
            return jsonify(res)
    res.update({
        'state': 1,
        'msg': 'success'
    })
    return jsonify(res)


@app.route('/receive/award/<string:awardrecord_token>', methods=['GET'])
def receive_award(awardrecord_token):
    """
    :function: 领奖专用链接 session_id, awardrecord_token解密为用户的user_id, award_id和application_secret
    :return: 返回领奖成功的页面
    """
    awardrecord_token = html.escape(awardrecord_token)
    awardrecord = AwardRecord.query.filter_by(awardrecord_token=awardrecord_token).first()
    if awardrecord is None:
        return render_template('receive_award.html')
    award = Award.query.filter_by(award_id=awardrecord.award_id).first()
    if award:
        return render_template('receive_award.html',
                               award_name=award.award_name, award_description=award.award_description,
                               checked=awardrecord.checked, awardrecord_token=awardrecord.awardrecord_token)
    return render_template('none_award.html')


@app.route('/acquire/award', methods=['POST'])
def acquire_award():
    """
    :functino: 兑奖
    :return:
    """
    awardrecord_token = request.values.get('awardrecord_token')
    exchange_token = request.values.get('exchange_token')
    if awardrecord_token and exchange_token:
        awardrecord = AwardRecord.query.filter_by(awardrecord_token=awardrecord_token).first()
        awardrecord.check()
        db.session.add(awardrecord)
        db.session.commit()
        return render_template('exchange_result.html', is_exchange=True)
    return render_template('exchange_result.html', is_exchange=False)


@app.route('/online/service', methods=['GET', 'POST'])
def online_service():
    signature = request.values.get("signature")
    timestamp = request.values.get("timestamp")
    nonce = request.values.get("nonce")
    print('signature, timestamp, nonce', signature, timestamp, nonce)
    if signature is None or timestamp is None or nonce is None:
        return 'bad guys'
    conf = configparser.ConfigParser()
    conf.read('config.ini')
    token = conf.get('app', 'online_service_token')
    params = list()
    params.append(token)
    params.append(timestamp)
    params.append(nonce)
    params.sort()
    out = ''
    for i in params:
        out += i
    sign = hashlib.sha1(out.encode()).hexdigest()
    if sign != signature:
        return 'bad guys'
    if request.method == 'GET':
        echostr = request.values.get("echostr")
        if echostr:
            return echostr
        else:
            return 'bad guys'
    if request.method == 'POST':
        message = json.loads(request.get_data(as_text=True))
        print("客服message: ", message)
        open_id = message.get('FromUserName')
        response_data = dict()
        if message['MsgType'] == 'event' and message['Event'] == 'user_enter_tempsession':
            response_data.update({
                "touser": open_id,
                "msgtype": "text",
                "text": {
                    "content": "回复1，关注bugaboo官方公众号之后，可以到小程序【bugaboo用心说爱你】中抽奖"
                }
            })
        elif message['MsgType'] == 'text' and message['Content'] == '1':

            media_id = conf.get('weixin', 'media_id')
            response_data.update({
                "touser": open_id,
                "msgtype": "image",
                "image": {"media_id": media_id}
            })
        else:
            open_id = message['FromUserName']
            response_data.update({
                "touser": open_id,
                "msgtype": "text",
                "text": {
                    "content": "回复1，关注bugaboo官方公众号之后，可以到小程序【bugaboo用心说爱你】中抽奖"
                }
            })
        print('打印返回消息')
        print(response_data)
        access_token = get_access_token()
        if access_token:
            response_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + access_token
            res = requests.post(url=response_url, data=json.dumps(response_data, ensure_ascii=False).encode())
            print(res.text)
            return ''
        else:
            return ''


@app.route('/god/login', methods=['GET', 'POST'])
def god_login():
    """
    :function: 管理员登陆
    :return:
    """
    form = GodLoginForm()
    if form.validate_on_submit():
        conf = configparser.ConfigParser()
        conf.read('config.ini')
        if conf.get('weixin', 'god_name') == form.username.data and \
                        conf.get('weixin', 'god_password') == form.password.data:
            ip_addr = request.remote_addr
            value = random.random()
            value = hash(value)
            value = str(value)
            access_token = get_sha1(value)
            current_time = datetime.datetime.utcnow()
            login_time = current_time.strftime(configs['development'].STRFTIME_FORMAT)
            access_token_expire_time = (current_time + datetime.timedelta(minutes=30)).strftime(
                configs['development'].STRFTIME_FORMAT)
            god = God(access_token=access_token, login_time=login_time, ip_addr=ip_addr,
                      access_token_expire_time=access_token_expire_time)
            db.session.add(god)
            db.session.commit()
            login_user(god)
            return redirect(url_for('god_index'))
        else:
            flash(message='用户名或者密码错误', category='warning')
    return render_template("god_login.html", form=form)


@app.route('/logout')
@login_required
def god_logout():
    logout_user()
    flash(message='您已注销')
    return redirect(url_for('god_login'))


@app.route('/god/index', methods=['GET'])
@login_required
def god_index():
    """
    :function: 后台首页， 搜索用户信息， 查看排行榜， 活动开启和关闭
    :return:
    """
    return render_template("god_index.html")


#  pages/authorize/authorize?share_data={"parameter_name":"a","parameter_value":1,"next_page":"/pages/raffle/raffle"}
